# QuantumDot-Noise-Lab

A compact numerical laboratory for decoherence models in semiconductor spin qubits.

## Included models
- Gaussian quasistatic detuning/frequency noise
- white-noise exponential decay
- phenomenological 1/f-like stretched-exponential envelopes
- Ramsey and echo envelopes
- independent-noise combination rules

## Quick start
```bash
python -m pip install -e .
python examples/compare_envelopes.py
pytest
```

## Conventions
For Gaussian quasistatic frequency noise with standard deviation \\(\sigma_f\\):
\\[
W_R(t)=\exp[-2\pi^2\sigma_f^2 t^2].
\\]

The code keeps conventions explicit so that prefactors can be audited rather than hidden inside fitted time constants.

## Status
Research/teaching software. Models are intentionally transparent and should be replaced or extended when a device-specific noise spectrum is known.

## License
MIT.
