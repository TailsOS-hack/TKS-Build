# Data and model access

This repository redistributes aggregate results and code only. It does not contain raw images, individual prediction records, native arrays or model checkpoints.

The source project identifies the image dataset as Aryan Singhal's augmented/upsampled [Alzheimer's Disease Multiclass Images Dataset](https://www.kaggle.com/datasets/aryansinghal10/alzheimers-multiclass-dataset-equal-and-augmented), with an upstream chain through [UraninJo](https://www.kaggle.com/datasets/uraninjo/augmented-alzheimer-mri-dataset-v2) and [Tourist55](https://www.kaggle.com/datasets/tourist55/alzheimers-dataset-4-class-of-images). These are source-project provenance statements, not a fresh license certification. Obtain data through the provider's authorized access flow and review current terms and attribution requirements; do not assume all derivative licenses are interchangeable.

Exact reproduction also requires the original prepared manifest, selection record, two pinned checkpoints and archived native maps. Re-downloading a current dataset version does not guarantee the same manifest or pixels. Consult [omitted_inputs_manifest.json](../provenance/omitted_inputs_manifest.json) and the original research project. Check hashes before inference; never replace a mismatching file merely to make the experiment run.

Patient identifiers were unavailable in the source data. No patient-disjoint claim is made. The package excludes per-image paths and records even when the source project described its images as public/de-identified. Do not add private/restricted source inputs to Git.
