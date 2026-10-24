# Separate follow-up: Round 2 robustness fine-tuning

This completed follow-up is context for the Build. It is **separate from the original corner/border audit** and does not change that audit's conclusion: the fixed controls did not support dominant input-corner reliance.

## What was done

Three stage-only MobileNetV3-Large fine-tuning runs used supervised, class-labelled cross-entropy with 0.05 label smoothing, inverse hash-group/class-group weighting and full-network AdamW. The full 224×224 field of view was retained. Label-independent constant or low-frequency background texture was restricted to heuristic safe-background pixels; flips, intensity changes, noise and blur were also used. Intensity/noise/blur could affect foreground. The protected support was **not** an anatomical segmentation, and bright corner text could remain protected.

Training used 19,023 images; clean validation used 2,705. Fixed stress validation used 256 images per scenario, 64 per class, with hash-distinct groups. Checkpoint selection combined clean NLL and an equally weighted mean of four stress-family NLLs at equal weight. Clean accuracy and balanced accuracy could fall at most 0.002 from same-device initialization; clean NLL had to remain at most 1.2×initial NLL + 0.002. All selected checkpoints passed those guards. The runs stopped at validation plateau, after at least 20 epochs and 15 consecutive epochs without an eligible selection-score improvement.

## Verified saved results

NLL is negative log-likelihood; lower is better. Initial values are epoch 0 of each run. Selected values are the validation-selected checkpoint, **not the final epoch**.

| Seed | Completed epochs | Selected epoch | Initial stress-family mean NLL | Selected stress-family mean NLL | Selected clean validation accuracy |
| --- | ---: | ---: | ---: | ---: | ---: |
| 20261011 | 21 | 6 | 0.066446 | 0.037534 | 99.9261% |
| 20261012 | 33 | 18 | 0.056495 | 0.038284 | 99.9630% |
| 20261013 | 35 | 20 | 0.054412 | 0.037701 | 100.0000% |

All three saved statuses are `complete`, with reason `validation_plateau` and `smoke_only: false`. The aggregate [machine-readable summary](../results/robustness_followup_summary.json) records exact values and SHA256 hashes for every source read. Packaging cross-checked the per-run history, selection, run status and suite selection freeze. It did not rerun training or inference.

## Interpretation and limits

The stress-validation losses improved relative to each run's initialization. Because those same development stress cases contributed to checkpoint selection, this is development evidence. It is not a patient-disjoint or source-disjoint generalization result and does not establish that shortcuts were eliminated. Prior test results were already known; the source protocol labels this retrospective reused-benchmark development. No clinical-readiness or causal anatomical claim follows. The original corner audit and these later robustness runs answer different questions.

The historical implementation-check record reports nine passing unit tests and two smoke runs. Those are historical checks, not fresh packaging-test results. No per-case data, images or weights are included in this follow-up note.

## Source locations in the original research repository

- `docs/kevin_paper_20261011/round2_training/round2.py`
- `docs/kevin_paper_20261011/round2_training/README.md`
- `docs/kevin_paper_20261011/round2_training/prepared/protocol.json`
- `docs/kevin_paper_20261011/round2_training/verification/implementation_checks.json`
- `training_logs/experiments/kevin_20261011/round2_blackwell_20261011/suite_status.json`
- `training_logs/experiments/kevin_20261011/round2_blackwell_20261011/validation_selection_before_any_round2_test.json`
- For seeds 20261011, 20261012 and 20261013: `training_logs/experiments/kevin_20261011/round2_blackwell_20261011/stage_only_seed<seed>/{history.json,selection.json,run_status.json}`.
