# Methods

## Question and completed design

The audit tested whether two fixed image classifiers showed dominant dependence on input corners or borders. A Grad-CAM display had motivated this question. Native-map location was measured descriptively; causal sensitivity was probed using controlled input masking.

The models were MobileNetV3-Large: the historical old dementia classifier and validation-selected stage-only candidate 3, seed 20261012. Their training was supervised: image rows supplied class labels, and the trainer used cross-entropy loss. This audit did not train them. The exact checkpoint hashes are in the [protocol](../results/protocol_before_inference.json). Inference resized RGB images to 224×224 and normalized with ImageNet mean `[0.485, 0.456, 0.406]` and standard deviation `[0.229, 0.224, 0.225]`.

The source prepared manifest supplied 160 new-model validation images, 40 from each of MildDemented, ModerateDemented, NonDemented and VeryMildDemented. A deterministic SHA256 ordering of `seed|path` selected one image per prepared hash group. The protocol and selected sample were written before this audit's inference. These groups do not establish patient separation.

## Fixed controls

- Four 32×32 input corner squares cover 4,096 pixels, or 8.1633% of the input.
- The outer 16-pixel border covers 13,312 pixels, or 26.5306%.
- Erase and retain-only conditions were tested with black and ImageNet-mean fills.
- Central controls removed exactly the same number of pixels, selected in increasing radial distance from the image center. These masks are approximately disk-shaped; they are not crops.
- Each model had one clean condition plus twelve edited conditions, yielding 26 metric records and 4,160 image-condition-model probability rows in the original evidence.

The original verifier checked complete case alignment, source/checkpoint/native-array hashes and mask areas, and recomputed metrics from all probability rows. Saved checks report unchanged model state, no gradients and no training. That historical report is preserved at [provenance/historical/verification.json](../provenance/historical/verification.json); package validation is a separate, narrower check.

## Native-map analysis

The audit reused 230 archived native 7×7 Grad-CAM arrays for 115 cases: original100, eight historical class-balanced cases and seven historically selected gallery cases, for each model. It did not rerun original100 or test inference. Four native corner cells and the outer 24-cell ring were summarized after per-map score normalization. Input-corner masks and native corner cells are different objects; receptive fields overlap and are broad.

## Interpretation

Corner removal preserved 100% accuracy for both models with both fills. Candidate 3 corners-only accuracy was 25%, while equal-area central removal was substantially more harmful. This supports the narrow conclusion that these controls did not show dominant input-corner reliance. It does not prove the absence of shortcuts, clinical validity or superiority under every perturbation. Read the [limitations](LIMITATIONS.md) before using any number.
