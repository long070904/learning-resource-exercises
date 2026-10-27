"""Read saved MIT Colab evidence without importing ML packages or executing cells.

Use in the parent Colab after the batch, with Drive already mounted:
    python audit_mit_hosted.py --output /content/mit_hosted_audit.json

This only summarizes observed files and recorded claims. It never authenticates,
reruns coursework, loads checkpoints, or certifies a provider course completion.
The default output is stdout; --output writes only the explicitly named report.
"""
from __future__ import annotations

import argparse
import array
import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
import wave


DEFAULT_RESULTS = "/content/drive/MyDrive/HaiLong_Colab_Results/02_mit_6s191/results"
DEFAULT_MODELS = "/content/drive/MyDrive/HaiLong_Colab_Results/02_mit_6s191/models"
DEFAULT_EXECUTED = "/content/drive/MyDrive/HaiLong_Course_Progress/2026-10-03/notebooks/02_mit_6s191"
DEFAULT_RECORDS = "/content/drive/MyDrive/HaiLong_Course_Progress/2026-10-03/records/02_mit_6s191"


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except (OSError, ValueError) as exc:
        return None, f"{type(exc).__name__}: {exc}"


def file_info(path):
    result = {"path": str(path), "exists": path.is_file()}
    if result["exists"]:
        result["bytes"] = path.stat().st_size
        result["nonempty"] = result["bytes"] > 0
    return result


def csv_info(path):
    result = file_info(path)
    if not result["exists"]:
        return result
    try:
        with path.open(encoding="utf-8", newline="") as stream:
            rows = csv.reader(stream)
            result["columns"] = next(rows, [])
            result["data_rows"] = sum(1 for row in rows if row)
    except (OSError, ValueError, csv.Error) as exc:
        result["read_error"] = str(exc)
    return result


def wav_info(path):
    result = file_info(path)
    if not result["exists"]:
        return result
    try:
        with wave.open(str(path), "rb") as stream:
            result.update(channels=stream.getnchannels(), sample_width=stream.getsampwidth(),
                          sample_rate=stream.getframerate(), frames=stream.getnframes(),
                          duration_seconds=stream.getnframes() / stream.getframerate())
            # A bounded sample check is evidence of nonzero audio, not proof of
            # musical quality or complete-file integrity.
            sample = stream.readframes(min(stream.getnframes(), 8192))
            width = stream.getsampwidth()
            if width == 1:
                nonzero = any(value != 128 for value in sample)
            elif width == 2:
                values = array.array("h")
                values.frombytes(sample)
                nonzero = any(values)
            else:
                nonzero = any(sample)
            result["bounded_sample_nonzero"] = nonzero
            result["readable_wave_header_with_frames"] = result["frames"] > 0
    except (OSError, ValueError, EOFError, wave.Error, ZeroDivisionError) as exc:
        result["read_error"] = str(exc)
    return result


def notebook_info(path):
    result = file_info(path)
    if not result["exists"]:
        return result
    notebook, error = read_json(path)
    if error:
        result["read_error"] = error
        return result
    code = [(index, cell) for index, cell in enumerate(notebook.get("cells", []))
            if cell.get("cell_type") == "code" and "".join(cell.get("source", [])).strip()]
    executed = [(index, cell) for index, cell in code if cell.get("execution_count") is not None]
    errors = [{"cell_index_zero_based": index, "ename": output.get("ename"),
               "evalue": output.get("evalue")}
              for index, cell in code for output in cell.get("outputs", [])
              if output.get("output_type") == "error"]
    result.update(nonempty_code_cells=len(code), executed_code_cells=len(executed),
                  error_outputs=errors,
                  all_nonempty_code_cells_executed_without_saved_errors=(bool(code) and len(code) == len(executed) and not errors))
    return result


def map_recorded_path(value, results_root, models_root):
    """Map notebook-relative results/models references to persistent roots."""
    if not isinstance(value, str):
        return None
    parts = Path(value.replace("\\", "/")).parts
    for marker, root in (("results", results_root), ("models", models_root)):
        if marker in parts:
            candidate = root.joinpath(*parts[parts.index(marker) + 1:]).resolve()
            if candidate.is_relative_to(root.resolve()):
                return candidate
    return None


def recorded_files(value, results_root, models_root):
    found = {}
    def visit(item):
        if isinstance(item, dict):
            for child in item.values():
                visit(child)
        elif isinstance(item, list):
            for child in item:
                visit(child)
        elif isinstance(item, str):
            mapped = map_recorded_path(item, results_root, models_root)
            if mapped is not None:
                found[str(mapped)] = file_info(mapped) if not mapped.is_dir() else {
                    "path": str(mapped), "exists": True, "directory": True,
                    "files": [file_info(p) for p in sorted(mapped.rglob("*")) if p.is_file()]}
    visit(value)
    return list(found.values())


def recorded_domain_checks(filename, evidence, run_dir, audio_files):
    """Compare saved task fields with independent file counts, without ML work."""
    checks = {}
    def csv_rows(name):
        return csv_info(run_dir / name).get("data_rows")
    if filename.startswith("02_"):
        training = evidence.get("training_and_checkpoint", {})
        checks["full_3000_steps_and_history"] = (training.get("steps") == 3000
            and training.get("full_iterations") == 3000 and csv_rows("training.csv") == 3000)
        checks["checkpoint_round_trip_recorded"] = training.get("checkpoint_round_trip") is True
        checks["four_sampling_experiment_rows"] = csv_rows("sampling_experiments.csv") == 4
        checks["real_generated_audio_recorded"] = evidence.get("generated_audio", {}).get("generated_not_training_music") is True
        checks["readable_nonzero_generated_audio_observed"] = bool(audio_files) and any(
            item.get("duration_seconds", 0) > 0 and item.get("bounded_sample_nonzero") is True
            for item in audio_files)
    elif filename.startswith("05_"):
        data = evidence.get("real_mnist_data", {})
        checks["real_full_mnist_counts_recorded"] = (data.get("train_examples") == 60000
            and data.get("test_examples") == 10000 and data.get("synthetic") is False)
        for model in ("fc", "cnn"):
            training = evidence.get(model + "_full_training_and_test", {})
            checks[model + "_full_epoch_history_matches_record"] = (
                training.get("train_examples") == 60000 and training.get("test_examples") == 10000
                and training.get("epochs", 0) > 0 and csv_rows(model + "_full_training.csv") == training.get("epochs"))
        checks["all_test_predictions_recorded"] = evidence.get("cnn_predictions", {}).get("examples") == 10000
        checks["checkpoint_round_trip_recorded"] = evidence.get("checkpoint_round_trip", {}).get("passed") is True
    elif filename.startswith("06_"):
        data = evidence.get("real_face_data", {})
        checks["real_streamed_face_data_recorded"] = (data.get("synthetic") is False
            and data.get("streamed_hdf5") is True and data.get("examples", 0) > 0)
        for name in ("standard_cnn_training", "dbvae_training"):
            training = evidence.get(name, {})
            checks[name + "_history_matches_record"] = (
                training.get("steps", 0) > 0 and csv_rows(name + ".csv") == training.get("steps"))
        checks["adaptive_all_face_sampling_recorded"] = evidence.get("adaptive_resampling", {}).get("all_positive_faces_considered") is True
        checks["checkpoint_round_trip_recorded"] = evidence.get("checkpoint_round_trip", {}).get("passed") is True
    elif filename.startswith("07_"):
        for style in ("leprechaun", "yoda"):
            training = evidence.get(style + "_training", {})
            checks[style + "_full_200_updates_and_history"] = (training.get("updates") == 200
                and training.get("real_course_data") is True and csv_rows(style + "_training.csv") == 200)
        for name, count in (("heldout_generations.csv", 20), ("paired_controls.csv", 20),
                            ("judge_prompt_experiments.csv", 9), ("yoda_training_duration_experiments.csv", 12)):
            checks[name + "_expected_rows"] = csv_rows(name) == count
        checks["adapter_round_trip_recorded"] = evidence.get("adapter_checkpoint_round_trip", {}).get("passed") is True
        test = evidence.get("official_yoda_test_nll", {})
        nll = test.get("mean_negative_log_likelihood")
        checks["unchanged_official_test_nll_recorded"] = (test.get("original_text_unchanged") is True
            and isinstance(nll, (float, int)) and math.isfinite(nll))
    return checks


def summarize_mit(results_root=DEFAULT_RESULTS, models_root=DEFAULT_MODELS,
                  executed_root=DEFAULT_EXECUTED, records_root=DEFAULT_RECORDS,
                  scope_path=None):
    results_root, models_root = Path(results_root), Path(models_root)
    executed_root, records_root = Path(executed_root), Path(records_root)
    scope_path = Path(scope_path or Path(__file__).with_name("service_scope_audit.json"))
    scope, error = read_json(scope_path)
    if error:
        raise ValueError(f"Cannot read source criteria {scope_path}: {error}")
    report = {"audited_utc": datetime.now(timezone.utc).isoformat(),
              "audit_mode": "read_only_saved_artifacts_no_notebook_execution",
              "provider_course_completion_claimed": False,
              "roots": {"results": str(results_root), "models": str(models_root),
                        "executed_notebooks": str(executed_root), "runner_records": str(records_root)},
              "roots_exist": {"results": results_root.is_dir(), "models": models_root.is_dir(),
                              "executed_notebooks": executed_root.is_dir(), "runner_records": records_root.is_dir()},
              "limitations": ["Recorded task values are claims from notebook execution, not independent model recomputation.",
                              "Checkpoint files are inventoried without loading or executing them.",
                              "Hosted Opik server/UI delivery cannot be verified from local JSON or boolean switches alone.",
                              "No missing evidence is inferred as successful; no historical run is silently combined with a later run."],
              "notebooks": []}
    for requirement in scope["notebook_requirements"]:
        filename = requirement["filename"]
        stem = Path(filename).stem
        entry = {"filename": filename, "original_course_notebook": requirement["original_course_notebook"],
                 "saved_executed_notebook": notebook_info(executed_root / filename), "runs": []}
        runner_record, runner_error = read_json(records_root / (stem + ".json"))
        entry["runner_record"] = runner_record if not runner_error else {"read_error": runner_error}
        required = requirement.get("required_evidence_keys", [])
        for task_path in sorted((results_root / stem).glob("*/task_evidence.json")):
            evidence, evidence_error = read_json(task_path)
            run_id = task_path.parent.name
            run_dir = task_path.parent
            model_dir = models_root / stem / run_id
            run = {"run_id": run_id, "task_evidence_path": str(task_path),
                   "task_evidence_sha256": hashlib.sha256(task_path.read_bytes()).hexdigest()}
            if evidence_error or not isinstance(evidence, dict):
                run["read_error"] = evidence_error or "Task evidence is not an object."
                entry["runs"].append(run)
                continue
            run.update(recorded_task_evidence=evidence, required_keys=required,
                       missing_required_keys=[key for key in required if key not in evidence],
                       recorded_path_checks=recorded_files(evidence, results_root, models_root),
                       expected_results=[csv_info(run_dir / name) if name.endswith(".csv") else file_info(run_dir / name)
                                         for name in requirement.get("expected_result_files", [])],
                       expected_models=[file_info(model_dir / name) for name in requirement.get("expected_model_files", [])],
                       model_artifact_files=[file_info(p) for p in sorted(model_dir.rglob("*")) if p.is_file()],
                       audio_files=[wav_info(p) for p in sorted(run_dir.glob("*.wav"))])
            run["recorded_domain_checks"] = recorded_domain_checks(filename, evidence, run_dir, run["audio_files"])
            # Match final records by their artifact folder/run_id, never by the
            # newest filename alone. This preserves interrupted/partial runs.
            finals = []
            for candidate in sorted(results_root.glob(stem + "-*.json")):
                final, final_error = read_json(candidate)
                if not final_error and isinstance(final, dict) and (
                        final.get("execution_environment", {}).get("run_id") == run_id or
                        Path(final.get("artifact_folder", "")).name == run_id):
                    finals.append({"path": str(candidate), "record": final})
            run["matching_final_records"] = finals
            run["all_required_task_keys_present"] = bool(required) and not run["missing_required_keys"]
            run["expected_files_present_nonempty"] = all(item.get("nonempty", False)
                for item in run["expected_results"] + run["expected_models"])
            if filename.startswith("07_"):
                run["lab3_service_evidence"] = {
                    "judge_mode": evidence.get("judge_setup", {}).get("mode"),
                    "judge_model": evidence.get("judge_setup", {}).get("model"),
                    "monitoring_mode": evidence.get("inference_monitoring", {}).get("mode"),
                    "recorded_official_service_flags": [item["record"].get("official_service_exercises_completed") for item in finals],
                    "opik_ui_delivery_verified_by_this_helper": False,
                    "verification_limit": "Inspect an actual Opik UI trace/export with input, output and feedback score to confirm remote delivery."}
                continuations = []
                for path in sorted(run_dir.glob("official_services_*/service_completion.json")):
                    saved, saved_error = read_json(path)
                    item = {"path": str(path), "record": saved, "read_error": saved_error,
                            "opik_ui_independently_verified_by_helper": False}
                    monitor, monitor_error = read_json(path.parent / "monitored_inference.json")
                    item["saved_monitored_inference"] = monitor if not monitor_error else {"read_error": monitor_error}
                    item["saved_server_trace_exports"] = [file_info(p) for p in sorted(path.parent.glob("opik_server_trace_*.json"))]
                    continuations.append(item)
                run["lab3_service_continuations"] = continuations
            entry["runs"].append(run)
        entry["task_evidence_runs_found"] = len(entry["runs"])
        entry["no_task_evidence_observed"] = not entry["runs"] and bool(required)
        report["notebooks"].append(entry)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-root", default=DEFAULT_RESULTS)
    parser.add_argument("--models-root", default=DEFAULT_MODELS)
    parser.add_argument("--executed-root", default=DEFAULT_EXECUTED)
    parser.add_argument("--records-root", default=DEFAULT_RECORDS)
    parser.add_argument("--scope", default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    report = summarize_mit(args.results_root, args.models_root, args.executed_root,
                           args.records_root, args.scope)
    output = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        destination = Path(args.output)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(output + "\n", encoding="utf-8")
        print(destination)
    else:
        print(output)


if __name__ == "__main__":
    main()
