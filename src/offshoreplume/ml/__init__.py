"""False-positive reduction.

A small CNN classifier (<5 M parameters) that operates on retrieved
ΔXCH4 enhancement patches to distinguish real plumes from common
artifacts: residual sun-glint, cloud shadow, ship wakes, internal waves,
oil sheens, biological surface films.

Modules (to be filled in Phase 3):
    dataset         Patch extraction, positive/negative label assembly,
                    class-imbalance handling.
    model           ResNet-style architecture (architecture choice in ADR-0005).
    train           Stratified k-fold training loop.
    infer           Apply trained model to Phase 4 candidate detections,
                    producing a per-detection confidence score.
"""
