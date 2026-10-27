"""Objective extensions for the explicitly synthetic wearable teaching example.

Called from notebook 09 after its original fit. No personal response is supplied.
"""
import hashlib
import json
from pathlib import Path
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch


def array_sha256(*arrays):
    digest = hashlib.sha256()
    for array in arrays:
        array = np.ascontiguousarray(array)
        digest.update(str(array.dtype).encode())
        digest.update(json.dumps(list(array.shape)).encode())
        digest.update(array.tobytes())
    return digest.hexdigest()


def state_sha256(state):
    digest = hashlib.sha256()
    for key in sorted(state):
        digest.update(key.encode())
        digest.update(array_sha256(state[key].detach().cpu().numpy()).encode())
    return digest.hexdigest()


def prediction_table(probabilities, encoded_truth, expected_labels, sample_ids, subjects, vocabulary):
    probabilities = probabilities.detach().cpu().numpy()
    encoded_truth = encoded_truth.detach().cpu().numpy().reshape(-1)
    vocabulary = np.asarray([int(value) for value in vocabulary])
    if len(np.unique(vocabulary)) != len(vocabulary):
        raise ValueError("Class vocabulary contains duplicate labels")
    if not (len(probabilities) == len(encoded_truth) == len(expected_labels) == len(sample_ids)):
        raise ValueError("Prediction/sample alignment length mismatch")
    if probabilities.ndim != 2 or probabilities.shape[1] != len(vocabulary):
        raise ValueError("Probability/vocabulary shape mismatch")
    if not np.isfinite(probabilities).all():
        raise ValueError("Nonfinite probabilities")
    if not np.allclose(probabilities.sum(axis=1), 1, atol=1e-5):
        raise ValueError("Class probabilities do not sum to one")
    decoded_truth = vocabulary[encoded_truth.astype(np.int64)]
    if not np.array_equal(decoded_truth, np.asarray(expected_labels).reshape(-1)):
        raise ValueError("Vocabulary or prediction order does not match source labels")
    predicted = vocabulary[probabilities.argmax(axis=1)]
    table = pd.DataFrame({"sample_id": sample_ids, "synthetic_subject_id": subjects[sample_ids],
                          "true_class": decoded_truth, "predicted_class": predicted,
                          "confidence": probabilities.max(axis=1), "wrong": decoded_truth != predicted})
    for column, label in enumerate(vocabulary):
        table[f"probability_class_{label}"] = probabilities[:, column]
    return table


def run_wearable_objective_extensions(*, baseline_learner, frame, x, y, subjects,
                                     train, valid, test, probabilities, truth, results,
                                     quick_run=False):
    from fastai.tabular.all import (TabularPandas, FillMissing, Normalize, CategoryBlock,
                                   tabular_learner, accuracy, set_seed, Callback)
    from sklearn.metrics import f1_score, balanced_accuracy_score, confusion_matrix

    results = Path(results)
    results.mkdir(parents=True, exist_ok=True)
    models = Path("models")
    models.mkdir(parents=True, exist_ok=True)
    # These invariants describe this supplied synthetic exercise only.
    if x.shape != (288, 64, 3) or tuple(map(len, (train, valid, test))) != (216, 36, 36):
        raise ValueError("The full original synthetic teaching dataset/split changed")
    source_sha = array_sha256(x, y, subjects)
    split_sha = array_sha256(train, valid, test)
    baseline_table = prediction_table(probabilities, truth, y[test], test, subjects, baseline_learner.dls.vocab)
    baseline_table.to_csv(results / "wearable_baseline_test_predictions.csv", index=False)
    wrong = baseline_table[baseline_table.wrong].sort_values(["confidence", "sample_id"], ascending=[False, True])
    case = {"dataset": "synthetic", "selection_rule": "highest-confidence baseline test error; sample ID breaks ties",
            "wrong_predictions": int(len(wrong)), "test_rows": 36, "input_sha256": source_sha,
            "split_sha256": split_sha, "observed_real_participant_harm": False,
            "learner_personal_inspection_claimed": False,
            "hypothetical_use_risk": "An erroneous emotion label could mislead a research summary or an inappropriate downstream decision. This generated teaching sample cannot establish real participant harm or deployment validity."}
    if len(wrong):
        selected = wrong.iloc[0]
        sample_id = int(selected.sample_id)
        case.update({"status": "actual_saved_model_misclassification", "sample": selected.to_dict(),
                     "nonfinite_sensor_values": int((~np.isfinite(x[sample_id])).sum()),
                     "aggregate_features": frame.drop(columns="label").iloc[sample_id].to_dict()})
        pd.DataFrame(x[sample_id], columns=["synthetic_channel_0", "synthetic_channel_1", "synthetic_channel_2"]).to_csv(
            results / "wearable_failed_case_signal.csv", index_label="time_index")
        fig, axes = plt.subplots(3, 1, figsize=(10, 7), sharex=True)
        for channel, axis in enumerate(axes):
            axis.plot(x[sample_id, :, channel])
            axis.set_ylabel(f"Synthetic {channel}")
        axes[-1].set_xlabel("Generated time index")
        fig.suptitle(f"Actual synthetic test error: sample {sample_id}; true={int(selected.true_class)}, predicted={int(selected.predicted_class)}, confidence={selected.confidence:.3f}")
        fig.tight_layout()
        fig.savefig(results / "wearable_failed_case_signal.png", dpi=140)
        plt.show()
    else:
        case["status"] = "no_baseline_test_error_observed"
        case["note"] = "No failed case is invented. This small synthetic test set does not establish real-world reliability."
    (results / "wearable_failed_prediction_case.json").write_text(json.dumps(case, indent=2), encoding="utf-8")

    class BatchEvidence(Callback):
        order = 100

        def before_fit(self):
            self.epoch_hashes = {}
            self.batch_counts = {}
            self.row_counts = {}

        def before_batch(self):
            if not self.learn.training:
                return
            epoch = int(self.epoch)
            digest = self.epoch_hashes.setdefault(epoch, hashlib.sha256())
            for value in (*self.xb, *self.yb):
                digest.update(array_sha256(value.detach().cpu().numpy()).encode())
            self.batch_counts[epoch] = self.batch_counts.get(epoch, 0) + 1
            self.row_counts[epoch] = self.row_counts.get(epoch, 0) + len(self.yb[0])

        def evidence(self):
            return [{"epoch": epoch, "training_batches": self.batch_counts[epoch],
                     "training_rows_seen": self.row_counts[epoch],
                     "actual_ordered_batch_sha256": self.epoch_hashes[epoch].hexdigest()}
                    for epoch in sorted(self.epoch_hashes)]

    seed = 2026

    def make_dls():
        set_seed(seed, reproducible=True)
        table = TabularPandas(frame.copy(deep=True), procs=[FillMissing, Normalize],
                              cont_names=list(frame.columns.drop("label")), y_names="label",
                              y_block=CategoryBlock(), splits=(list(train), list(valid)))
        return table.dataloaders(bs=32, num_workers=0, drop_last=False)

    initial_dls = make_dls()
    initial_learner = tabular_learner(initial_dls, path=Path.cwd(), model_dir="models", layers=[32, 16], metrics=accuracy)
    initial_state = {key: value.detach().cpu().clone() for key, value in initial_learner.model.state_dict().items()}
    initial_sha = state_sha256(initial_state)
    torch.save({"state_dict": initial_state, "layers": [32, 16], "initial_sha256": initial_sha},
               models / "wearable_controlled_initial_state.pt")
    del initial_learner, initial_dls
    runs = []
    final_models = {}
    for lr in (0.01, 0.003):
        tag = f"lr_{str(lr).replace('.', 'p')}"
        controlled_dls = make_dls()
        controlled = tabular_learner(controlled_dls, path=Path.cwd(), model_dir="models", layers=[32, 16], metrics=accuracy)
        controlled.model.load_state_dict(initial_state, strict=True)
        loaded_sha = state_sha256(controlled.model.state_dict())
        if loaded_sha != initial_sha:
            raise ValueError("Initial weights/buffers differ")
        preprocessing_sha = array_sha256(controlled_dls.train.dataset.conts.to_numpy(), controlled_dls.valid.dataset.conts.to_numpy())
        callback = BatchEvidence()
        set_seed(seed, reproducible=True)
        started = time.perf_counter()
        with controlled.no_bar(), controlled.no_logging():
            controlled.fit_one_cycle(8, lr_max=lr, cbs=callback)
        duration = time.perf_counter() - started
        validation_dl = controlled.dls.test_dl(frame.iloc[valid].copy(), with_labels=True, shuffle=False, drop_last=False)
        validation_p, validation_truth = controlled.get_preds(dl=validation_dl)
        validation = prediction_table(validation_p, validation_truth, y[valid], valid, subjects, controlled.dls.vocab)
        validation.to_csv(results / f"wearable_{tag}_validation_predictions.csv", index=False)
        pd.DataFrame(confusion_matrix(validation.true_class, validation.predicted_class, labels=[0, 1, 2])).to_csv(
            results / f"wearable_{tag}_validation_confusion.csv", index=False)
        pd.DataFrame(controlled.recorder.values, columns=controlled.recorder.metric_names[1:-1]).to_csv(
            results / f"wearable_{tag}_history.csv", index=False)
        row = {"run": tag, "lr_max": lr, "epochs": 8, "seed": seed, "layers": [32, 16], "batch_size": 32,
               "training_rows": 216, "validation_rows": 36, "test_rows": 36, "dataset": "synthetic",
               "initial_state_sha256": loaded_sha, "input_sha256": source_sha, "split_sha256": split_sha,
               "preprocessed_train_validation_sha256": preprocessing_sha,
               "validation_macro_f1": float(f1_score(validation.true_class, validation.predicted_class, average="macro", labels=[0, 1, 2], zero_division=0)),
               "validation_balanced_accuracy": float(balanced_accuracy_score(validation.true_class, validation.predicted_class)),
               "training_seconds": duration, "actual_batch_order": callback.evidence(), "quick_run": bool(quick_run)}
        controlled.save(f"wearable_controlled_{tag}", with_opt=True)
        runs.append(row)
        final_models[tag] = controlled
        (results / f"wearable_{tag}_configuration.json").write_text(json.dumps(row, indent=2), encoding="utf-8")
    controls = {"initial_state_equal": runs[0]["initial_state_sha256"] == runs[1]["initial_state_sha256"],
                "preprocessing_equal": runs[0]["preprocessed_train_validation_sha256"] == runs[1]["preprocessed_train_validation_sha256"],
                "actual_batch_order_equal": runs[0]["actual_batch_order"] == runs[1]["actual_batch_order"],
                "same_source_and_split": all(r["input_sha256"] == source_sha and r["split_sha256"] == split_sha for r in runs)}
    if not all(controls.values()) or any(len(r["actual_batch_order"]) != 8 or
            any(epoch["training_rows_seen"] != 216 for epoch in r["actual_batch_order"]) for r in runs):
        (results / "wearable_controlled_comparison_incomplete.json").write_text(json.dumps({"runs": runs, "controls": controls}, indent=2), encoding="utf-8")
        raise ValueError("The controlled comparison failed an actual control check; inspect saved run evidence")
    # Fixed rule: use validation macro F1, then balanced accuracy, then smaller LR.
    selected = sorted(runs, key=lambda r: (-r["validation_macro_f1"], -r["validation_balanced_accuracy"], r["lr_max"]))[0]
    selected_learner = final_models[selected["run"]]
    selected_test_dl = selected_learner.dls.test_dl(frame.iloc[test].copy(), with_labels=True, shuffle=False, drop_last=False)
    selected_p, selected_truth = selected_learner.get_preds(dl=selected_test_dl)
    selected_test = prediction_table(selected_p, selected_truth, y[test], test, subjects, selected_learner.dls.vocab)
    selected_test.to_csv(results / "wearable_validation_selected_test_predictions.csv", index=False)
    concise = pd.DataFrame([{k: v for k, v in row.items() if k != "actual_batch_order"} for row in runs])
    concise.to_csv(results / "wearable_controlled_validation_comparison.csv", index=False)
    fig, axis = plt.subplots(figsize=(7, 4))
    locations = np.arange(len(concise))
    axis.bar(locations - .18, concise.validation_macro_f1, .36, label="Validation macro F1")
    axis.bar(locations + .18, concise.validation_balanced_accuracy, .36, label="Validation balanced accuracy")
    axis.set_xticks(locations, concise.run)
    axis.set_ylim(0, 1)
    axis.legend()
    axis.set_title("Actual same-initialization/same-split synthetic comparison")
    fig.tight_layout()
    fig.savefig(results / "wearable_controlled_validation_comparison.png", dpi=140)
    plt.show()
    evidence = {"dataset": "synthetic", "runs": runs, "verified_controls": controls,
                "selection_rule": "validation macro F1, balanced accuracy, then smaller LR; no test tuning",
                "selected_run": selected["run"],
                "observed_validation_macro_f1_lr_0p003_minus_0p01": runs[1]["validation_macro_f1"] - runs[0]["validation_macro_f1"],
                "selected_test_macro_f1": float(f1_score(selected_test.true_class, selected_test.predicted_class, average="macro", labels=[0, 1, 2], zero_division=0)),
                "selected_test_balanced_accuracy": float(balanced_accuracy_score(selected_test.true_class, selected_test.predicted_class)),
                "objective_computations_observed": True, "learner_personal_setting_change_claimed": False,
                "learner_personal_reflection_completed": False, "real_dataset_or_clinical_validity_claimed": False,
                "provider_course_completion_claimed": False, "quick_run": bool(quick_run),
                "limitations": "Two learning rates, one synthetic split and initialization; no independent evidence about real participant emotion, real-world harm or general superiority."}
    (results / "wearable_controlled_comparison_evidence.json").write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    project = {"document_status": "Documented proposal/plan; intended facts, not proof of implementation",
               "planned": {"student": "Learner", "supervisor_from_learning_plan": "the supervisor",
                           "project": "Benchmark replication and robust improvement of wearable physiological emotion recognition",
                           "primary_dataset": "Emognition", "secondary_dataset": "WESAD",
                           "responsibility": "Student-led research with planned supervisor review/feedback",
                           "evaluation": "Subject-held-out/LOSO, training-subject validation and training-only normalization",
                           "safeguards": "Verify dataset terms; no new recruitment/video; secure secondary wearable/self-report data; confirm applicable ethics review/exemption with supervisor"},
               "unknown_actual_facts": ["Original data access and terms reviewed/accepted", "Final labels/windows/use and included subjects", "Actual ethics decision/storage safeguards", "Real team involvement and perspectives consulted or missing"],
               "performed_in_this_synthetic_notebook": {"dataset": "generated synthetic teaching data", "split_subjects": {"train": list(range(6)), "validation": [6], "test": [7]}, "objective_failure_record": case["status"], "controlled_validation_comparison": controls},
               "candidate_analysis": "Use the intended research question of predicting specified annotations across unseen participants, with leakage/error audits and uncertainty. For the intended student-led project, supervisor/domain/affected-user consultation could uncover missing collection conditions or harmful interpretations; actual consultation must be supplied by the learner.",
               "sources": {"learning_plan": "unpublished learning plan, pages 1–5", "proposal": "unpublished research proposal, dataset/method/ethics/responsibility sections"},
               "learner_personal_opinion_or_consultation_fabricated": False}
    (results / "wearable_project_analysis_planned_unknown_performed.json").write_text(json.dumps(project, indent=2), encoding="utf-8")
    print(concise[["run", "validation_macro_f1", "validation_balanced_accuracy", "training_seconds"]].to_string(index=False))
    print("Verified comparison controls:", controls)
    print("Failed-case status:", case["status"], "; selected by validation:", selected["run"])
    return {"case": case, "comparison": evidence, "project_analysis": project}
