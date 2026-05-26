"""Methane retrieval algorithms.

Implements MBMP and SBMP from Varon et al. 2021 (Atmos. Meas. Tech., DOI
10.5194/amt-14-2771-2021). All algorithm steps are commented inline with
the equation numbers from that paper. See ADR-0001 for why we chose this
family of retrievals over full radiative-transfer inversion.

Modules (to be filled in Phase 1):
    sbmp            Single-band multi-pass on Band 12 alone.
    mbmp            Multi-band multi-pass with Band 11 normalization.
    reference       Reference-scene selection (see ADR-0003 when written).
"""
