# Limitations and unresolved questions

1. **Development sample.** All fresh inference used new-model validation images. The old model had historical training/validation/test exposure to 99/23/38 of those images. Comparison is descriptive, not a fair independent clinical evaluation.
2. **Image groups are not patients.** The augmented/upsampled Kaggle derivative lacks patient identity evidence. Neither hash-group separation nor apparently perfect clean accuracy demonstrates patient-disjoint generalization.
3. **Artificial occlusion.** Erasure creates out-of-distribution inputs. Matched areas and two fill values improve the diagnostic, but cannot rule out all shortcuts or distinguish every failure cause.
4. **Corners are not necessarily blank.** A nonblack display proxy occurred in corner masks for 23/160 images and border masks for 88/160. It includes bright padding and is not brain segmentation.
5. **Coarse explanations.** Native 7×7 receptive fields overlap. Upsampling adds display detail, not evidence. Normalized score mass is not an anatomical probability, biological causation, or a statistical hypothesis test.
6. **No universal improvement.** Central erasure hurt candidate 3 more than the old model. This audit does not establish the newer model as stronger for every perturbation.
7. **Limited reproduction payload.** Raw images, per-case records, archived native arrays and weights are intentionally absent. Package checks verify aggregate consistency and integrity; full recomputation requires authorized source inputs.
8. **No newly completed marker experiment.** The Learn article's hypothetical added corner marker is a separate proposed experiment. This Build is the completed corner/border erasure and retain-only audit.
9. **No clinical claim.** Results are not evidence of diagnostic readiness, patient outcomes or clinical utility.
10. **Archived attribution replay differences.** The preceding attribution audit reproduced all 200 original100 class predictions, but 43 probability vectors exceeded its fixed 0.0001 absolute tolerance (38 old / 5 candidate 3). Maximum differences were 0.001191 and 0.001996. The tolerance was not widened and the cause was not established. Those historical maps were reused by the corner audit; no fresh replay or resolution is claimed here. The attribution source also recorded two failed/flat randomized maps and mixed masking-control outcomes, so faithful anatomical localization was not established.

The audit did not justify cropping the field of view, forcing Grad-CAM toward the center, or aggressively removing corners. Further work should use a separately documented protocol and retain clean validation performance as a guard, without using reused test outcomes for model selection.
