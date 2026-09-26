# QuantumDot-Noise-Lab

QuantumDot-Noise-Lab is a modular Python project for studying **noise, decoherence, and coherence envelopes in semiconductor quantum dots and spin qubits**.

The repository is built around a simple idea:

> Separate the physical noise spectrum from the pulse sequence and from the final coherence observable.

That separation makes it easier to compare noise mechanisms, test assumptions, and extend the model without rewriting the entire calculation.

---

## 1. Scientific motivation

Spin-qubit coherence is affected by multiple noise mechanisms, including:

- quasistatic charge noise,
- (1/f^alpha) noise,
- white noise,
- random telegraph noise,
- nuclear-spin fluctuations,
- magnetic-field noise,
- control-amplitude noise,
- pulse errors,
- correlated gate noise.

Different experiments probe different frequency bands of that noise.

Ramsey, Hahn echo, Rabi, CPMG, and more general dynamical-decoupling sequences do not respond identically to the same spectrum.

A useful computational framework should therefore distinguish:

[
S(f)
]

from

[
F(f,t)
]

and from

[
W(t).
]

---

## 2. Current capabilities

The current implementation contains:

- Gaussian quasistatic Ramsey decay,
- exponential decay,
- stretched-exponential decay,
- white-noise PSD,
- (1/f^alpha) PSD,
- random-telegraph PSD,
- Ramsey filter function,
- Hahn-echo filter function,
- Gaussian phase-noise coherence integration,
- independent-envelope multiplication,
- synthetic Gaussian noise-trace generation from a target PSD.

---

## 3. Core conventions

### 3.1 Gaussian quasistatic frequency noise

For frequency fluctuations with standard deviation (sigma_f),

[
W_R(t)
=
expleft(
-2pi^2sigma_f^2t^2
ight).
]

The corresponding (1/e) time is

[
T_2^*
=
rac{1}{sqrt{2}pisigma_f}.
]

This convention is made explicit because factors of (2), (2pi), and one-sided versus two-sided PSD definitions commonly cause discrepancies between codes.

### 3.2 Exponential envelope

[
W(t)=e^{-t/T}.
]

### 3.3 Stretched exponential

[
W(t)
=
expleft[-(t/T)^etaight].
]

This is a phenomenological model that can represent a broad range of observed decays.

---

## 4. Noise spectra

### White noise

[
S(f)=S_0.
]

### Power-law noise

[
S(f)
=
A
left(
rac{f_{mathrm{ref}}}{f}
ight)^alpha.
]

The special case (alpha=1) is conventional (1/f) noise.

### Random telegraph noise

The repository includes a Lorentzian PSD model associated with two-state switching.

Qualitatively,

[
S_{m RTN}(f)
propto
rac{gamma}
{(2pi f)^2+(2gamma)^2}.
]

Here (gamma) is the switching rate.

---

## 5. Filter-function framework

For Gaussian frequency noise, coherence can be written schematically as

[
W(t)=e^{-chi(t)},
]

where

[
chi(t)
propto
int_0^infty
S(f)
|F(f,t)|^2
,df.
]

The exact prefactor depends on the PSD and filter-function conventions.

This repository keeps those definitions in code rather than silently absorbing them into fitted time constants.

### Ramsey

The Ramsey filter emphasizes low-frequency noise strongly.

### Hahn echo

A refocusing pulse suppresses low-frequency contributions relative to Ramsey.

The project currently implements both filter functions.

---

## 6. Repository structure

```text
QuantumDot-Noise-Lab/
├── README.md
├── pyproject.toml
├── examples/
│   ├── example.py
│   └── psd_demo.py
├── src/
│   └── qd_noise_lab/
│       ├── __init__.py
│       ├── core.py
│       ├── spectra.py
│       ├── filter_functions.py
│       └── synthesis.py
├── tests/
│   ├── test_core.py
│   └── test_spectra.py
└── .github/
    └── workflows/
        └── tests.yml
```

---

## 7. Installation

```bash
git clone https://github.com/premathul/QuantumDot-Noise-Lab.git
cd QuantumDot-Noise-Lab
python -m pip install -e .
```

For tests:

```bash
python -m pip install -e .[dev]
pytest -q
```

---

## 8. Example: compare phenomenological envelopes

```python
import numpy as np
from qd_noise_lab.core import (
    ramsey_quasistatic,
    exponential_envelope,
)

t = np.linspace(0, 20e-6, 100)

W_qs = ramsey_quasistatic(t, sigma_f_hz=2e4)
W_exp = exponential_envelope(t, T_s=15e-6)
```

---

## 9. Example: integrate a (1/f) spectrum

```python
import numpy as np
from qd_noise_lab.spectra import one_over_f_psd
from qd_noise_lab.filter_functions import (
    ramsey_filter_sq,
    echo_filter_sq,
    gaussian_phase_coherence,
)

f = np.logspace(0, 7, 4000)
S = one_over_f_psd(f, amplitude_hz2=1e10, alpha=1)

t = 10e-6

Wr, chi_r = gaussian_phase_coherence(
    f,
    S,
    ramsey_filter_sq(f, t),
)

We, chi_e = gaussian_phase_coherence(
    f,
    S,
    echo_filter_sq(f, t),
)
```

The frequency integration limits are physically important. For (1/f) noise, the result depends on low- and high-frequency cutoffs.

---

## 10. Why cutoffs matter

An idealized (1/f) spectrum cannot extend unchanged from zero to infinite frequency.

Practical calculations require finite bandwidth,

[
f_{min}
le f le
f_{max}.
]

The inferred coherence therefore depends on:

- experiment duration,
- calibration interval,
- sampling bandwidth,
- pulse sequence,
- detector bandwidth,
- microscopic noise rolloff.

A numerical (T_2^*) is incomplete unless these assumptions are stated.

---

## 11. Synthetic noise generation

The `synthesis.py` module can construct a Gaussian time-domain noise trace from a target frequency-domain PSD.

This is useful for:

- validating analytical coherence predictions,
- simulating pulse sequences,
- generating synthetic training or test data,
- studying nonstationary analysis pipelines.

The current implementation is intentionally simple and should be convergence-tested against sample count and duration.

---

## 12. Independent versus correlated noise

If independent noise mechanisms produce coherence envelopes (W_i(t)), then

[
W_{mathrm{total}}(t)
=
prod_i W_i(t)
]

under the appropriate independence assumptions.

Correlated noise does not generally reduce to a simple product.

Future versions will include covariance-aware multichannel noise generation.

---

## 13. Numerical validation

Automated tests currently check:

- Ramsey coherence starts at unity,
- independent envelopes multiply correctly,
- (1/f) scaling,
- positivity of random-telegraph PSD,
- zero-frequency suppression of the echo filter,
- zero-noise coherence remains exactly one.

---

## 14. Numerical integration

The current code uses numerical quadrature over explicitly supplied frequency grids.

Users should perform convergence checks with respect to:

- number of frequency samples,
- logarithmic versus linear sampling,
- lower frequency cutoff,
- upper frequency cutoff.

A smooth plot is not evidence of convergence.

---

## 15. Current limitations

The package does not yet include:

- CPMG filter functions,
- arbitrary pulse sequences,
- non-Gaussian RTN coherence,
- exact stochastic-Liouville solutions,
- Bloch-Redfield dynamics,
- Lindblad master equations,
- driven Rabi filter functions,
- multi-axis noise,
- correlated gate-noise PSD matrices,
- Bayesian PSD inference.

---

## 16. Planned development

### Near-term

- CPMG-(N) filters,
- Rabi decay,
- noise-bandwidth utilities,
- automatic (T_2) extraction,
- plotting functions,
- PSD normalization checks.

### Intermediate

- multichannel cross-spectral-density matrices,
- Monte Carlo Ramsey experiments,
- explicit random telegraph trajectories,
- finite pulse-width effects,
- pulse-sequence parser,
- dynamical-decoupling comparison.

### Long-term

A general workflow:

[
	ext{measured or modeled noise}
ightarrow
S_{ij}(f)
ightarrow
	ext{pulse sequence}
ightarrow
F_{ij}(f,t)
ightarrow
chi(t)
ightarrow
W(t)
ightarrow
T_2.
]

---

## 17. Connection to Ge hole-spin qubits

Although the code is intentionally general, one target application is charge-noise-induced decoherence in Ge/SiGe hole-spin qubits.

If a qubit has gate-frequency susceptibility

[
rac{partial f_Z}{partial V},
]

and voltage-noise PSD (S_V(f)), then frequency-noise PSD is approximately

[
S_f(f)
=
left(
rac{partial f_Z}{partial V}
ight)^2
S_V(f)
]

for a single linear noise channel.

This provides a direct bridge between device electrostatics and coherence.

---

## 18. Reproducibility checklist

A coherence calculation should report:

- PSD definition,
- one-sided or two-sided convention,
- frequency units,
- low-frequency cutoff,
- high-frequency cutoff,
- frequency sampling,
- pulse sequence,
- filter-function definition,
- sensitivity conversion,
- numerical integration method,
- code commit.

---

## 19. Contributing

Contributions are welcome in:

- new PSD models,
- analytical benchmarks,
- filter functions,
- numerical validation,
- experimental data interfaces,
- plotting,
- documentation,
- stochastic simulation.

Please include a physical definition and test for every new model.

---

## 20. License

MIT License.

---

## 21. Project status

**Status:** active development.

The repository already provides a useful foundation for comparing noise spectra and coherence models. The long-term objective is a general, convention-explicit coherence engine for semiconductor spin-qubit experiments.
