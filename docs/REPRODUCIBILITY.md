# Reproduction and validation

## 1. Verify this package without data or models

From the repository root:

```bash
python3 scripts/verify_package.py
```

Python 3.9+ is sufficient for this standard-library-only checker. It validates immutable payload hashes, parses Python source without importing it, checks aggregate confusion matrices/accuracy/F1/recall, compares the CSV projection, checks sample and scenario counts, verifies relative documentation links and enforces the bounded file inventory. It does not execute the model, download data or use cloud resources.

The current packaging check report is [provenance/package_validation.json](../provenance/package_validation.json). Historical inference verification is [provenance/historical/verification.json](../provenance/historical/verification.json). Their scopes are deliberately separate.

## 2. Full historical inference reproduction (not run while packaging)

The exact source snapshots preserve their original relative layout under `source_snapshot/`. They require PyTorch, torchvision, NumPy, Pillow, matplotlib and scikit-learn. The optional historical attribution path additionally uses SciPy. Package versions for the original corner run were not frozen in its protocol; [requirements-reproduction.txt](../requirements-reproduction.txt) lists observed dependencies without claiming a validated lockfile. Use a reviewed compatible environment and record its actual versions before a new run.

Acquire the authorized inputs in [the manifest](../provenance/omitted_inputs_manifest.json) and keep them outside the Git repository. The simplest faithful reproduction is in a separate authorized copy of the original research checkout with the preserved source paths and pinned inputs. Compare source and checkpoint hashes against the manifests before running. No training command is needed for the corner audit.

From that original-layout copy, choose a **new, nonexistent** output directory:

```bash
MPLCONFIGDIR=/tmp/tks-corner-mpl XDG_CACHE_HOME=/tmp/tks-corner-cache \
python docs/kevin_paper_20261011/round2_corner_audit/corner_audit.py \
  --device cpu --output /path/to/new-corner-audit-output
```

Use `--device mps` only with a compatible Mac/PyTorch environment. Do not overwrite the historical results. This command performs inference on the 160-image validation sample and recreates galleries from archived maps; it needs all relevant source images, not just the validation sample. Model checkpoints are hash-pinned. The historical loader uses PyTorch pickle checkpoint loading: only load the exact trusted source files after hash verification.

`verify_and_plot.py` expects results at its default sibling `results/` directory and requires original per-image outputs and input hashes. In a separate reproduction copy, place the new run there only when that path is absent; preserve historical evidence separately. Running the original verifier recomputes all 26 records from 4,160 rows and creates plots, including image-bearing figures that are intentionally not published here.

Do not invoke `run_attribution_audit.py` as a package check. It is included for method provenance and would perform historical-case inference; the completed corner audit reused those archived arrays instead.

## Checks not performed for this package

- No new model inference, training or checkpoint selection.
- No full recomputation from per-image probabilities, which are excluded.
- No recreation of images, native arrays or galleries.
- No independent patient-level or clinical validation.
- No claim that the dependencies form a tested clean-install inference environment.
- External reference URLs are recorded sources; only repository-local links are exhaustively checked by the package verifier.
