"""Restricted evaluator for the pinned original deterministic convolution sheet.

No arbitrary Python eval, workbook mutation, Excel UI automation, or training.
"""
import csv
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import xml.etree.ElementTree as ET
import zipfile

import numpy as np

SOURCE_SHA256 = "28d885e8e07e3fb8fbeea49288c17e25edd0f168f0dbdaabd403017e83c15f0b"
SOURCE_URL = "https://github.com/fastai/course22p2/blob/df9323235bc395b5c2f58a3d08b83761947b9b93/xl/conv-example.xlsx"
NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main", "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
CELL = re.compile(r"(\$?)([A-Z]{1,3})(\$?)([0-9]+)")
TOKEN = re.compile(r"\s*(\$?[A-Z]{1,3}\$?[0-9]+|[A-Z]+|(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][+-]?\d+)?|[()+*/,:-])")


def column_number(label):
    value = 0
    for character in label:
        value = value * 26 + ord(character) - 64
    return value


def column_label(number):
    if number < 1:
        raise ValueError("Invalid shifted column")
    value = ""
    while number:
        number, remainder = divmod(number - 1, 26)
        value = chr(65 + remainder) + value
    return value


def coordinates(address):
    match = CELL.fullmatch(address)
    if not match:
        raise ValueError(f"Invalid cell address: {address}")
    return column_number(match[2]), int(match[4])


def addresses(start, end):
    c1, r1 = coordinates(start)
    c2, r2 = coordinates(end)
    if c2 < c1 or r2 < r1:
        raise ValueError("Reversed range")
    return [[f"{column_label(column)}{row}" for column in range(c1, c2 + 1)] for row in range(r1, r2 + 1)]


def shift_formula(formula, source, target):
    source_c, source_r = coordinates(source)
    target_c, target_r = coordinates(target)
    def shift(match):
        abs_c, column, abs_r, row = match.groups()
        new_c = column_number(column) + (0 if abs_c else target_c - source_c)
        new_r = int(row) + (0 if abs_r else target_r - source_r)
        if new_r < 1:
            raise ValueError("Invalid shifted row")
        return f"{abs_c}{column_label(new_c)}{abs_r}{new_r}"
    return CELL.sub(shift, formula)


class ConvolutionSheet:
    def __init__(self, path, verify_hash=True):
        path = Path(path)
        self.source_sha256 = hashlib.sha256(path.read_bytes()).hexdigest()
        if verify_hash and self.source_sha256 != SOURCE_SHA256:
            raise ValueError("Original workbook fingerprint differs")
        self.formulas, self.cached, self.values = {}, {}, {}
        self.sheet_name = "conv-example"
        with zipfile.ZipFile(path) as archive:
            workbook = ET.fromstring(archive.read("xl/workbook.xml"))
            sheets = {sheet.get("name"): sheet.get("{" + NS["r"] + "}id") for sheet in workbook.findall("s:sheets/s:sheet", NS)}
            relationships = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
            targets = {item.get("Id"): item.get("Target") for item in relationships}
            target = targets[sheets[self.sheet_name]]
            member = str(PurePosixPath("xl") / target) if not target.startswith("/") else target.lstrip("/")
            shared_strings = []
            if "xl/sharedStrings.xml" in archive.namelist():
                shared_strings = ["".join(item.itertext()) for item in ET.fromstring(archive.read("xl/sharedStrings.xml"))]
            sheet = ET.fromstring(archive.read(member))
            shared, pending = {}, []
            for cell in sheet.findall(".//s:c", NS):
                address = cell.get("r")
                formula = cell.find("s:f", NS)
                stored = cell.find("s:v", NS)
                text = stored.text if stored is not None else None
                if cell.get("t") == "s" and text is not None:
                    value = shared_strings[int(text)]
                elif cell.get("t") == "inlineStr":
                    value = "".join(cell.find("s:is", NS).itertext())
                else:
                    value = float(text) if text is not None else 0.0
                self.values[address] = value
                if formula is not None:
                    if formula.get("t") == "array" and formula.get("ref", address) != address:
                        raise ValueError("Unexpected multi-cell array formula; explicit handling needed")
                    if formula.text:
                        self.formulas[address] = formula.text.lstrip("=")
                        if formula.get("t") == "shared":
                            shared[formula.get("si")] = (address, formula.text)
                    else:
                        pending.append((address, formula.get("si")))
                    self.cached[address] = value
            for address, index in pending:
                base_address, base_formula = shared[index]
                self.formulas[address] = shift_formula(base_formula, base_address, address)
        self.reset()

    def reset(self, overrides=None):
        self.overrides = overrides or {}
        self.memo, self.dependencies, self.active = {}, {}, set()

    def value(self, address):
        address = address.replace("$", "")
        if address in self.memo:
            return self.memo[address]
        if address in self.active:
            raise ValueError("Formula dependency cycle")
        self.active.add(address)
        try:
            if address in self.overrides:
                result = float(self.overrides[address])
            elif address not in self.formulas:
                result = self.values.get(address, 0.0)
                if isinstance(result, str):
                    raise ValueError(f"Numeric formula references text at {address}")
            else:
                parser = FormulaParser(self, address, self.formulas[address])
                result = parser.parse()
                self.dependencies[address] = sorted(parser.precedents)
            result = float(result)
            if not np.isfinite(result):
                raise ValueError(f"Nonfinite formula result: {address}")
            self.memo[address] = result
            return result
        finally:
            self.active.remove(address)

    def trace(self, target):
        self.value(target)
        found, edges = set(), set()
        def visit(address):
            if address in found:
                return
            found.add(address)
            for predecessor in self.dependencies.get(address, []):
                edges.add((address, predecessor))
                visit(predecessor)
        visit(target)
        return [{"cell": address, "formula": self.formulas.get(address), "value": self.value(address)} for address in sorted(found)], sorted(edges)


class FormulaParser:
    def __init__(self, sheet, address, formula):
        self.sheet, self.address, self.precedents = sheet, address, set()
        self.tokens = []
        position = 0
        while position < len(formula):
            match = TOKEN.match(formula, position)
            if not match:
                raise ValueError(f"Unsupported token in {address}: {formula[position:]}")
            self.tokens.append(match[1])
            position = match.end()
        self.index = 0

    def take(self, expected=None):
        if self.index >= len(self.tokens):
            raise ValueError("Unexpected end of formula")
        token = self.tokens[self.index]
        if expected is not None and token != expected:
            raise ValueError(f"Expected {expected}, found {token}")
        self.index += 1
        return token

    def peek(self):
        return self.tokens[self.index] if self.index < len(self.tokens) else None

    def parse(self):
        value = self.expression()
        if self.peek() is not None or np.ndim(value):
            raise ValueError("Unconsumed tokens or nonscalar cell output")
        return float(value)

    def expression(self):
        value = self.product()
        while self.peek() in ("+", "-"):
            operator = self.take()
            right = self.product()
            value = value + right if operator == "+" else value - right
        return value

    def product(self):
        value = self.atom()
        while self.peek() in ("*", "/"):
            operator = self.take()
            right = self.atom()
            if np.ndim(value) and np.ndim(right) and np.shape(value) != np.shape(right):
                raise ValueError("Range product shapes differ")
            value = value * right if operator == "*" else value / right
        return value

    def reference(self, address):
        address = address.replace("$", "")
        self.precedents.add(address)
        return self.sheet.value(address)

    def atom(self):
        token = self.take()
        if token in ("+", "-"):
            value = self.atom()
            return value if token == "+" else -value
        if token == "(":
            value = self.expression()
            self.take(")")
            return value
        if CELL.fullmatch(token):
            if self.peek() == ":":
                self.take(":")
                end = self.take()
                return np.asarray([[self.reference(address) for address in row] for row in addresses(token, end)], dtype=float)
            return self.reference(token)
        if token in ("MAX", "SUM", "SUMPRODUCT"):
            self.take("(")
            arguments = [self.expression()]
            while self.peek() == ",":
                self.take(",")
                arguments.append(self.expression())
            self.take(")")
            if token == "SUM":
                return sum(float(np.sum(argument)) for argument in arguments)
            if token == "MAX":
                return max(float(np.max(argument)) for argument in arguments)
            if len(arguments) != 2 or np.shape(arguments[0]) != np.shape(arguments[1]):
                raise ValueError("SUMPRODUCT requires two equally shaped arrays")
            return float(np.sum(arguments[0] * arguments[1]))
        try:
            return float(token)
        except ValueError as error:
            raise ValueError(f"Unsupported formula token: {token}") from error


def save_csv(path, rows, fields):
    with Path(path).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def run_workbook_exercise(workbook, results):
    import matplotlib.pyplot as plt
    results = Path(results)
    results.mkdir(parents=True, exist_ok=True)
    sheet = ConvolutionSheet(workbook)
    checked = []
    for address in sorted(sheet.formulas):
        computed, cached = sheet.value(address), float(sheet.cached[address])
        checked.append({"cell": address, "formula": "=" + sheet.formulas[address], "recomputed": computed,
                        "cached": cached, "absolute_error": abs(computed - cached)})
    save_csv(results / "convolution_workbook_formula_checks.csv", checked, list(checked[0]))
    if any(not np.isclose(row["recomputed"], row["cached"], rtol=1e-9, atol=1e-9) for row in checked):
        raise ValueError("Pinned workbook cached/formula values differ; inspect saved checks")
    nodes, edges = sheet.trace("BM4")
    save_csv(results / "convolution_workbook_dependency_nodes.csv", nodes, ["cell", "formula", "value"])
    save_csv(results / "convolution_workbook_dependency_edges.csv", [{"dependent": a, "precedent": b} for a, b in edges], ["dependent", "precedent"])
    dot = ["digraph ConvolutionPrecedents {", "rankdir=LR;"]
    for node in nodes:
        dot.append(f'"{node["cell"]}" [label="{node["cell"]}"];')
    for dependent, predecessor in edges:
        dot.append(f'"{predecessor}" -> "{dependent}";')
    dot.append("}")
    (results / "convolution_workbook_dependencies.dot").write_text("\n".join(dot), encoding="utf-8")
    targets = ["AH3", "BM4", "CM4", "EN4"]
    baseline = {target: sheet.value(target) for target in targets}
    patch_addresses = addresses("A2", "C4")
    kernel_addresses = addresses("AD11", "AF13")
    patch = np.asarray([[sheet.value(address) for address in row] for row in patch_addresses])
    kernel = np.asarray([[sheet.value(address) for address in row] for row in kernel_addresses])
    python_first_output = max(0.0, float(np.sum(patch * kernel)))
    if not np.isclose(python_first_output, baseline["AH3"]):
        raise ValueError("Python patch/kernel operation differs from the workbook")
    old_pixel = sheet.value("B3")
    new_pixel = float(np.clip(old_pixel + 255, 0, 255))
    if new_pixel == old_pixel:
        raise ValueError("Predeclared pixel perturbation made no change")
    sheet.reset({"B3": new_pixel})
    changed = {target: sheet.value(target) for target in targets}
    changed_patch = patch.copy()
    changed_patch[1, 1] = new_pixel
    python_changed = max(0.0, float(np.sum(changed_patch * kernel)))
    if not np.isclose(python_changed, changed["AH3"]):
        raise ValueError("Changed Python patch operation differs from the workbook")
    comparison = [{"cell": target, "baseline": baseline[target], "pixel_changed": changed[target],
                   "difference": changed[target] - baseline[target]} for target in targets]
    save_csv(results / "convolution_workbook_pixel_perturbation.csv", comparison, list(comparison[0]))
    fig, axes = plt.subplots(1, 3, figsize=(11, 4))
    for axis, matrix, title in zip(axes, (patch, kernel, changed_patch), ("Original A2:C4", "Kernel AD11:AF13", "B3 changed in memory")):
        axis.imshow(matrix, cmap="coolwarm")
        for (row, column), value in np.ndenumerate(matrix):
            axis.text(column, row, f"{value:.3g}", ha="center", va="center")
        axis.set_title(title)
        axis.set_xticks([])
        axis.set_yticks([])
    fig.suptitle(f"AH3 = ReLU(sum(patch * kernel)): {baseline['AH3']:.6g} → {changed['AH3']:.6g}")
    fig.tight_layout()
    fig.savefig(results / "convolution_workbook_patch_kernel_comparison.png", dpi=150)
    plt.show()
    # Draw a representative branch with actual references; full DAG is in CSV/DOT.
    fig, axis = plt.subplots(figsize=(11, 6))
    labels = ["Original pixels\nA2:C4", "Original weights\nAD11:AF13", "AH3: weighted sum\n+ ReLU", "BM4: channel sums\n+ ReLU", "CM4: max pool", "EN4: output sum"]
    xy = [(0, 1), (0, -1), (2, 0), (4, 0), (6, 0), (8, 0)]
    for label, (cx, cy) in zip(labels, xy):
        axis.text(cx, cy, label, ha="center", va="center", bbox={"boxstyle": "round", "facecolor": "#e7f1fa", "edgecolor": "#315b7f"})
    for left, right in ((0, 2), (1, 2), (2, 3), (3, 4), (4, 5)):
        axis.annotate("", xy=(xy[right][0] - .7, xy[right][1]), xytext=(xy[left][0] + .7, xy[left][1]), arrowprops={"arrowstyle": "->"})
    axis.set(xlim=(-1.2, 9.3), ylim=(-2, 2))
    axis.axis("off")
    axis.set_title("Representative actual dependency branch; other channels/weights are in the full saved DAG")
    fig.tight_layout()
    fig.savefig(results / "convolution_workbook_dependency_branch.png", dpi=150)
    plt.show()
    evidence = {"source_url": SOURCE_URL, "source_sha256": sheet.source_sha256, "sheet": sheet.sheet_name,
                "formulas_checked": len(checked), "maximum_absolute_cached_error": max(row["absolute_error"] for row in checked),
                "shared_formula_translation_checked": True, "array_formula_cells_checked": True,
                "trace_target": "BM4", "trace_nodes": len(nodes), "trace_edges": len(edges),
                "direct_precedents": [b for a, b in edges if a == "BM4"],
                "python_first_output": python_first_output, "python_changed_output": python_changed,
                "perturbation": {"cell": "B3", "old": old_pixel, "new": new_pixel, "source_workbook_modified": False},
                "observed_target_changes": comparison, "objective_formula_dependency_exercise_executed": True,
                "adaptation": "CPU Colab formula/dependency exercise using the original deterministic workbook sheet",
                "excel_trace_precedents_ui_performed": False, "learner_independent_practice_claimed": False,
                "provider_equivalence_or_completion_claimed": False,
                "limits": "Original deterministic sheet only; historical RAND/dropout masks are not recalculated. The authored representative branch omits other recorded parents; CSV/DOT contain the full BM4 graph."}
    (results / "convolution_workbook_colab_evidence.json").write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    print(json.dumps(evidence, indent=2))
    return evidence
