#!/usr/bin/env python3
"""Verify the bounded aggregate package. Never imports ML code or runs inference."""
import ast
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
MUTABLE = {'provenance/package_validation.json'}
MANIFEST = 'provenance/package_sha256.json'


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(name):
    return json.loads((ROOT/name).read_text())


def close(a, b, what):
    require(math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-12), what)


def main():
    manifest = read(MANIFEST)
    files = {str(p.relative_to(ROOT)): p for p in ROOT.rglob('*')
             if p.is_file() and '.git' not in p.relative_to(ROOT).parts
             and '__pycache__' not in p.parts and p.suffix != '.pyc'}
    require(set(files) == set(manifest) | MUTABLE | {MANIFEST}, 'Unexpected or missing package file')
    require(not any(p.is_symlink() for p in ROOT.rglob('*') if '.git' not in p.parts), 'Symlink in package')
    for name, expected in manifest.items():
        require(digest(files[name]) == expected, 'Hash mismatch: '+name)
    source = read('provenance/source_manifest.json')
    for item in source['copied_files']:
        require(digest(ROOT/item['package_path']) == item['sha256'], 'Source copy changed')

    protocol = read('results/protocol_before_inference.json')
    require(protocol['n'] == 160 and protocol['per_class'] == 40 and protocol['unique_hash_groups'] == 160, 'Sample mismatch')
    require(protocol['evaluation_only'] is True, 'Audit unexpectedly trains')
    require(len(protocol['scenarios']) == 13 and len(protocol['models']) == 2, 'Design mismatch')
    scenarios = {r['name']: r for r in protocol['scenarios']}
    close(scenarios['corners32_erase_black']['masked_fraction'], 4096/50176, 'Corner area')
    close(scenarios['border16_erase_black']['masked_fraction'], 13312/50176, 'Border area')
    for region in ('corners32', 'border16'):
        for fill in ('black', 'imagenet_mean'):
            close(scenarios[region+'_erase_'+fill]['masked_fraction'], scenarios[region+'_matched_center_erase_'+fill]['masked_fraction'], 'Matched center area')

    metrics = read('results/validation_metrics.json')
    require(len(metrics) == 26, 'Metric record count')
    lookup = {(r['model'], r['scenario']): r for r in metrics}
    require(len(lookup) == 26 and set(lookup) == {(m,s) for m in protocol['models'] for s in scenarios}, 'Condition coverage')
    for record in metrics:
        cm = record['confusion_matrix']
        require(len(cm) == 4 and all(len(row) == 4 for row in cm), 'Confusion shape')
        require(all(isinstance(x, int) and x >= 0 for row in cm for x in row), 'Invalid confusion counts')
        require([sum(row) for row in cm] == [40]*4 and record['n'] == 160, 'Class/sample count')
        accuracy = sum(cm[k][k] for k in range(4))/160
        close(record['accuracy'], accuracy, 'Accuracy inconsistency')
        recall = [cm[k][k]/40 for k in range(4)]
        close(record['balanced_accuracy'], sum(recall)/4, 'Balanced accuracy inconsistency')
        f1 = []
        for k, label in enumerate(protocol['class_order']):
            close(record['recall_'+label], recall[k], 'Recall inconsistency')
            denominator = sum(cm[k])+sum(row[k] for row in cm)
            f1.append(2*cm[k][k]/denominator if denominator else 0)
        close(record['macro_f1'], sum(f1)/4, 'F1 inconsistency')
        close(record['label_flip_fraction'], record['label_flip_count']/160, 'Flip count inconsistency')
    for model in protocol['models']:
        require(lookup[(model,'clean')]['accuracy'] == 1, 'Clean result differs')
        require(all(lookup[(model,'corners32_erase_'+f)]['accuracy'] == 1 for f in ('black','imagenet_mean')), 'Corner-erasure claim differs')
    require(all(lookup[('candidate_3','corners32_only_'+f)]['accuracy'] == .25 for f in ('black','imagenet_mean')), 'Candidate3 corners-only claim differs')
    with (ROOT/'results/control_results.csv').open(newline='') as f:
        rows = list(csv.DictReader(f))
    require(len(rows) == 26, 'CSV count')
    for row in rows:
        record = lookup[(row['model'],row['scenario'])]
        for key,value in row.items():
            if key not in ('model','scenario'):
                close(float(value), record[key], 'CSV differs: '+key)
    summary = read('results/aggregate_summary.json')
    require(summary['metrics'] == metrics and 'input_sha256' not in summary, 'Derived summary mismatch')
    require(summary['training'] is False and summary['heldout_inference'] is False, 'Scope mismatch')
    require(summary['old_baseline_exposure_counts'] == {'test':38, 'train':99, 'val':23}, 'Old exposure mismatch')
    with (ROOT/'results/native_map_summary.csv').open(newline='') as f:
        native = list(csv.DictReader(f))
    require(len(native) == 6 and sum(int(row['n']) for row in native) == 230, 'Native map summary count')
    require(all(float(row['peak_in_corner']) == 0 for row in native), 'Peak claim mismatch')
    historical = read('provenance/historical/verification.json')
    require(historical['predictions_recomputed_and_verified'] == 4160 and historical['metric_records_verified'] == 26, 'Historical check counts')

    py_count = 0
    links = 0
    secret = re.compile(r'(?:ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{24,}|AKIA[A-Z0-9]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)')
    forbidden = {'.pt','.pth','.ckpt','.npy','.npz','.dcm','.dicom','.nii','.zip','.xlsx','.parquet'}
    for name,path in files.items():
        require(path.suffix not in forbidden and not name.endswith('.nii.gz'), 'Excluded artifact present: '+name)
        if path.suffix in {'.png','.pdf'}:
            require(name in {'figures/'+stem+'.'+ext for stem in ('native_location_mass','validation_masking_controls') for ext in ('png','pdf')}, 'Unexpected binary figure')
            continue
        text = path.read_text()
        require(not secret.search(text), 'Potential credential literal: '+name)
        if path.suffix == '.py':
            ast.parse(text, filename=name)
            py_count += 1
        if path.suffix == '.md':
            for target in re.findall(r'\]\(([^)]+)\)', text):
                if '://' in target or target.startswith(('mailto:','#')):
                    continue
                target = unquote(target.split('#')[0])
                require((path.parent/target).resolve().exists(), 'Broken local link: '+name+' -> '+target)
                links += 1
    report = dict(status='passed', scope='Package integrity, aggregate arithmetic, source syntax, bounded inventory and local documentation links only; no model inference or per-image metric regeneration.',
                  immutable_payload_files=len(manifest), source_python_files_parsed=py_count,
                  aggregate_metric_records_checked=26, original_probability_rows_not_recomputed=4160,
                  local_links_checked=links, raw_images_or_weights_included=False,
                  training_or_inference_performed=False,
                  checks_not_run=['Full original probability recomputation', 'Model inference or training', 'Clean-install ML environment reproduction', 'External URL availability', 'Clinical or patient-independent validation'])
    (ROOT/'provenance/package_validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
