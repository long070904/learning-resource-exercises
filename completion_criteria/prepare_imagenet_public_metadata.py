"""Prepare only public ImageNet class metadata; never fetch images or credentials."""
from __future__ import annotations

import ast
import hashlib
import html.parser
import json
from datetime import datetime, timezone
from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
REPORT_ROOT = Path(__file__).resolve().parent / "imagenet_public_metadata"
DEST = ROOT / "HaiLong_Colab_Exercises/04_fastai_part2/data/ILSVRC"
REVISION = "930a6f98f7debcc32ca7afbca4a176dbf9211e03"
BASE = f"https://raw.githubusercontent.com/tensorflow/models/{REVISION}/"
SOURCES = {
    "imagenet_lsvrc_2015_synsets.txt": "research/slim/datasets/imagenet_lsvrc_2015_synsets.txt",
    "imagenet_metadata.txt": "research/slim/datasets/imagenet_metadata.txt",
    "LICENSE": "LICENSE",
    "imagenet.py": "research/slim/datasets/imagenet.py",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def get_public(url: str) -> bytes:
    # Deliberately unauthenticated and confined to small, public metadata sources.
    req = urllib.request.Request(url, headers={"User-Agent": "HaiLong-public-metadata-provenance/1.0"})
    with urllib.request.urlopen(req, timeout=45) as response:
        data = response.read(2_000_001)
    if len(data) > 2_000_000:
        raise ValueError("Refusing a source larger than 2 MB; this task is metadata only")
    return data


def source_text(cell: dict) -> str:
    value = cell.get("source", "")
    return "".join(value) if isinstance(value, list) else value


class Tables(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.tables = []
        self.table = None
        self.row = None
        self.cell = None

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.depth += 1
            if self.depth == 1:
                self.table = []
        elif self.depth == 1 and tag == "tr":
            self.row = []
        elif self.depth == 1 and tag in {"td", "th"}:
            self.cell = []

    def handle_data(self, value):
        if self.cell is not None:
            self.cell.append(value)

    def handle_endtag(self, tag):
        if self.depth == 1 and tag in {"td", "th"} and self.cell is not None:
            self.row.append("".join(self.cell).strip())
            self.cell = None
        elif self.depth == 1 and tag == "tr" and self.row is not None:
            self.table.append(self.row)
            self.row = None
        elif tag == "table":
            if self.depth == 1:
                self.tables.append(self.table)
                self.table = None
            self.depth -= 1


def main():
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    raw = {name: get_public(BASE + path) for name, path in SOURCES.items()}
    ids = raw["imagenet_lsvrc_2015_synsets.txt"].decode("utf-8").splitlines()
    assert len(ids) == len(set(ids)) == 1000
    assert all(re.fullmatch(r"n\d{8}", wnid) for wnid in ids)
    assert ids == sorted(ids), "Original synset order must be retained, never reconstructed"
    pairs = [line.split("\t") for line in raw["imagenet_metadata.txt"].decode("utf-8").splitlines()]
    assert all(len(pair) == 2 and re.fullmatch(r"n\d{8}", pair[0]) and pair[1].strip() for pair in pairs)
    words = dict(pairs)
    assert len(words) == len(pairs), "Duplicate metadata WNIDs"
    assert set(ids).issubset(words), "Missing original ImageNet class description"
    assert all(words[wnid].strip() for wnid in ids)
    description_to_wnids = {}
    for wnid in ids:
        description_to_wnids.setdefault(words[wnid], []).append(wnid)
    duplicate_descriptions = {name: wnids for name, wnids in description_to_wnids.items() if len(wnids) > 1}
    assert "Apache License" in raw["LICENSE"].decode("utf-8")

    original_path = ROOT / "colab_migration_work/course22p2-df9323235bc395b5c2f58a3d08b83761947b9b93/nbs/31_imgnet_latents-widish.ipynb"
    prepared_path = ROOT / "HaiLong_Colab_Exercises/04_fastai_part2/31_imgnet_latents-widish.ipynb"
    original = json.loads(original_path.read_text(encoding="utf-8"))
    prepared = json.loads(prepared_path.read_text(encoding="utf-8"))
    order_cells = [(index + 1, source_text(cell)) for index, cell in enumerate(original["cells"])
                   if "id2str = (path_data/'imagenet_lsvrc_2015_synsets.txt')" in source_text(cell)]
    word_cells = [(index + 1, source_text(cell)) for index, cell in enumerate(original["cells"])
                  if "all_synsets =" in source_text(cell)]
    assert len(order_cells) == len(word_cells) == 1
    assert order_cells[0][1] in [source_text(cell) for cell in prepared["cells"]]
    assert word_cells[0][1] in [source_text(cell) for cell in prepared["cells"]]

    hf = {"url": "https://huggingface.co/datasets/ILSVRC/imagenet-1k",
          "authenticated": False, "dataset_files_accessed": False,
          "approved_access_verified": False, "live_revision_features_verified": False}
    try:
        card = get_public(hf["url"])
        parser = Tables()
        parser.feed(card.decode("utf-8"))
        candidates = [table for table in parser.tables if len(table) == 1001 and table[0] == ["id", "Class"]]
        if len(candidates) != 1:
            raise ValueError(f"Expected one public 1000-class table, observed {len(candidates)}")
        mapping = [(int(row[0]), row[1]) for row in candidates[0][1:]]
        assert [i for i, _ in mapping] == list(range(1000))
        expected = [words[wnid] for wnid in ids]
        discrepancies = [{"index": i, "wnid": ids[i], "tensorflow": expected[i], "public_card": name}
                         for i, name in mapping if name != expected[i]]
        hf.update({"page_sha256": sha(card), "public_card_rows": 1000,
                   "exact_display_name_matches_in_synset_order": 1000 - len(discrepancies),
                   "display_name_discrepancies": discrepancies,
                   "public_card_order_statement": "Labels are indexed based on a sorted list of synset IDs.",
                   "limitation": "Public display-name table/order is a cross-check only. It cannot certify authenticated immutable-revision ClassLabel WNIDs required by notebook31."})
        (REPORT_ROOT / "hf_public_class_table.json").write_text(json.dumps(mapping, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        hf["public_card_check_error"] = f"{type(exc).__name__}: {exc}"

    # Execute only the prepared metadata validator definition, with no course imports,
    # models, gated sources, images, encoding, datasets, or training.
    validator_source = next(source_text(cell) for cell in prepared["cells"]
                            if "def imagenet_original_metadata(" in source_text(cell))
    tree = ast.parse(validator_source)
    validator_node = next(node for node in tree.body
                          if isinstance(node, ast.FunctionDef) and node.name == "imagenet_original_metadata")
    validation_folder = REPORT_ROOT / "validated_public_sources"
    validation_folder.mkdir(exist_ok=True)
    validation_folder.joinpath("imagenet_lsvrc_2015_synsets.txt").write_bytes(raw["imagenet_lsvrc_2015_synsets.txt"])
    validation_folder.joinpath("words.txt").write_bytes(raw["imagenet_metadata.txt"])
    namespace = {"Path": Path, "cache_sha_file": lambda p: sha(Path(p).read_bytes())}
    exec(compile(ast.Module(body=[validator_node], type_ignores=[]), "<notebook31_metadata_only>", "exec"), namespace)
    validated_ids, fingerprints = namespace["imagenet_original_metadata"](validation_folder)
    assert validated_ids == ids
    # Also apply the unchanged original display-name expression to all classes.
    original_names = {key: value.split(",", maxsplit=1)[0] for key, value in pairs if key in ids}
    assert len(original_names) == 1000 and all(original_names.values())

    DEST.mkdir(parents=True, exist_ok=True)
    outputs = {"imagenet_lsvrc_2015_synsets.txt": raw["imagenet_lsvrc_2015_synsets.txt"],
               "words.txt": raw["imagenet_metadata.txt"]}
    for name, data in outputs.items():
        target = DEST / name
        if target.exists() and target.read_bytes() != data:
            raise FileExistsError(f"Refusing to overwrite existing different user metadata: {target}")
        target.write_bytes(data)
    for name, data in raw.items():
        (REPORT_ROOT / ("tensorflow_" + name)).write_bytes(data)
    report = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "status": "public_metadata_prepared_and_validated",
        "scope": "Two class metadata files only; no image/model/gated-dataset download, credential access, or notebook/helper edits",
        "tensorflow_repository": "https://github.com/tensorflow/models",
        "revision": REVISION,
        "revision_resolution": "Public git ls-remote HEAD; subsequent sources use the immutable40-character commit URL",
        "sources": {name: {"url": BASE + path, "sha256": sha(raw[name]), "bytes": len(raw[name])}
                    for name, path in SOURCES.items()},
        "license": {"repository_license": "Apache-2.0", "url": BASE + "LICENSE",
                    "sha256": sha(raw["LICENSE"]), "preserved_text": "execution/2026-10-03/imagenet_public_metadata/tensorflow_LICENSE",
                    "dataset_access_unchanged": "This public metadata preparation grants no ImageNet image access and does not accept ImageNet Terms of Access."},
        "prepared_files": {name: {"relative_path": (DEST / name).relative_to(ROOT).as_posix(),
                                  "sha256": sha(data), "bytes": len(data),
                                  "transformation": "Byte-for-byte original" if name != "words.txt" else "Byte-for-byte imagenet_metadata.txt, renamed to words.txt expected by original course; no subset or label transformation"}
                           for name, data in outputs.items()},
        "validation": {"wnids": len(ids), "distinct_wnids": len(set(ids)),
                       "valid_n_plus8_digit_ids": True, "original_order_retained": True,
                       "order_is_lexicographic": True, "metadata_rows": len(pairs),
                       "mapped_required_classes": len(original_names), "all_required_class_descriptions_nonempty": True,
                       "distinct_full_descriptions": len(description_to_wnids),
                       "duplicate_human_descriptions_retained_from_original": duplicate_descriptions,
                       "first5_wnids": ids[:5], "last5_wnids": ids[-5:],
                       "upstream_course_revision": "df9323235bc395b5c2f58a3d08b83761947b9b93",
                       "upstream_order_cell_1based": order_cells[0][0],
                       "upstream_words_cell_1based": word_cells[0][0],
                       "original_course_cell_sources_unchanged_in_prepared": True,
                       "prepared_metadata_validator_passed": True,
                       "prepared_validator_fingerprints": fingerprints,
                       "original_display_name_expression_all1000_passed": True,
                       "class_index_rule": "Zero-based index of preserved source synset-file lines, per original enumerate(id2str); no numeric labels inferred from human names"},
        "huggingface_public_metadata_comparison": hf,
        "full_image_training_executed": False,
        "imagenet_approved_access_verified": False,
        "all_coursework_complete": False,
    }
    path = REPORT_ROOT / "public_metadata_provenance.json"
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"report": str(path), "prepared_files": report["prepared_files"],
                      "validation": report["validation"], "hf_comparison": hf}, indent=2))


if __name__ == "__main__":
    main()
