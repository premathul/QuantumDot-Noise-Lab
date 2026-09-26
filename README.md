# QuantumDot-Noise-Lab

QuantumDot-Noise-Lab is a research-oriented Python framework for studying noise and decoherence in semiconductor quantum dots and spin qubits. The project is designed around a physically important separation: the environmental noise spectrum, the pulse sequence applied to the qubit, and the measured coherence envelope should be treated as distinct parts of the problem. Keeping these elements separate makes it possible to compare different noise mechanisms, investigate different experimental control sequences, and understand exactly which assumptions produce a reported coherence time.

In semiconductor qubits, decoherence rarely originates from one perfectly defined process. Charge fluctuations, magnetic noise, random telegraph fluctuators, (1/f) noise, control-amplitude errors, and slow calibration drift can all contribute over different frequency ranges. A Ramsey experiment and a Hahn-echo experiment can therefore report very different coherence times even for the same physical device. This does not imply that the device itself has changed; it reflects the fact that each pulse sequence filters environmental noise differently. The purpose of this repository is to make that filtering explicit.

The current code supports Gaussian quasistatic dephasing, exponential and stretched-exponential phenomenological envelopes, white noise, (1/f^alpha) spectra, random-telegraph spectra, Ramsey and Hahn-echo filter functions, numerical Gaussian phase-noise integration, independent-envelope combination, and synthesis of Gaussian time-domain noise traces from a target power spectral density.

For Gaussian quasistatic frequency noise with standard deviation (sigma_f), the Ramsey envelope used in this project is

[
W_R(t)=
expleft[-2pi^2sigma_f^2t^2ight].
]

The associated (1/e) dephasing time is

[
T_2^*=
rac{1}{sqrt{2}pisigma_f}.
]

This convention is written explicitly because many disagreements in the literature and in simulation code arise from hidden factors of (2pi), different angular-frequency versus ordinary-frequency conventions, or different definitions of spectral density.

A simple exponential decay is written as

[
W(t)=e^{-t/T},
]

while a stretched exponential is

[
W(t)=
expleft[-(t/T)^etaight].
]

These phenomenological models are useful for fitting data, but they should not automatically be interpreted as proof of a unique microscopic noise mechanism. The value of (eta) can summarize the shape of an envelope, yet different underlying stochastic processes can produce similar fitted behavior over a limited time window.

The repository includes several frequency-domain noise models. White noise is represented by a constant power spectral density,

[
S(f)=S_0,
]

while a power-law spectrum is represented as

[
S(f)=
A
left(
rac{f_{mathrm{ref}}}{f}
ight)^alpha.
]

The common (1/f) case corresponds to (alpha=1). Random telegraph noise is represented by a Lorentzian form associated with a two-state fluctuator with characteristic switching rate (gamma). These models are not intended to imply that all experimental noise can be reduced to one analytic expression. Instead, they provide controlled components that can be combined, compared, and benchmarked.

The central filter-function picture is expressed schematically through

[
W(t)=e^{-chi(t)},
]

with

[
chi(t)
propto
int_0^infty
S(f)
|F(f,t)|^2,df.
]

Here (S(f)) is the relevant noise power spectral density and (F(f,t)) describes the frequency response of the chosen pulse sequence. The precise normalization depends on the convention used for (S(f)) and for the Fourier transform. This repository therefore exposes the implementation instead of burying the convention inside a fitted time constant.

Ramsey evolution is strongly sensitive to low-frequency noise because there is no refocusing pulse. A Hahn-echo sequence suppresses slowly varying fluctuations by reversing the accumulated phase in the second half of the sequence. The repository currently implements both filter functions so that the same noise spectrum can be passed through two different experimental protocols. This makes it possible to see directly why echo can significantly extend coherence when the dominant noise is concentrated at low frequency.

A particularly important issue for (1/f) noise is bandwidth. An idealized (1/f) spectrum cannot extend unchanged from exactly zero frequency to infinite frequency. Every realistic calculation must therefore specify lower and upper cutoffs,

[
f_{min}le fle f_{max}.
]

The lower cutoff can be related to the total observation time, recalibration interval, or experimental acquisition protocol. The upper cutoff may be set by device physics, instrumentation bandwidth, or the frequency scale at which the assumed noise mechanism changes. Because the calculated coherence can depend strongly on these cutoffs, a quoted (T_2^*) is incomplete unless the assumed bandwidth is documented.

The code also supports time-domain synthesis of Gaussian noise traces from a target power spectral density. This functionality is useful when one wants to compare analytical filter-function predictions against Monte Carlo pulse simulations, generate controlled synthetic data, or examine how finite sampling and finite measurement duration affect estimated coherence. The present synthesis routine is intentionally simple and should be checked for convergence with respect to record length, number of samples, frequency interpolation, and random seed.

The repository is organized as a compact package. The `core.py` module contains the fundamental coherence envelopes. The `spectra.py` module defines analytic power spectral densities. The `filter_functions.py` module contains Ramsey and echo filter functions together with numerical coherence integration. The `synthesis.py` module provides time-domain noise generation. The `examples` directory contains runnable demonstrations, and the automated test suite checks basic physical and numerical properties such as correct low-frequency behavior, PSD scaling, and unity coherence in the zero-noise limit.

Installation can be performed with

```bash
git clone https://github.com/premathul/QuantumDot-Noise-Lab.git
cd QuantumDot-Noise-Lab
python -m pip install -e .
```

Development dependencies and tests can be installed with

```bash
python -m pip install -e .[dev]
pytest -q
```

A simple calculation comparing two phenomenological envelopes can be written as

```python
import numpy as np
from qd_noise_lab.core import ramsey_quasistatic, exponential_envelope

t = np.linspace(0, 20e-6, 100)

W_qs = ramsey_quasistatic(t, sigma_f_hz=2e4)
W_exp = exponential_envelope(t, T_s=15e-6)
```

A frequency-domain calculation using a (1/f) spectrum can be written as

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

The exact numbers produced by a calculation like this depend on the adopted PSD normalization and integration limits. The repository is intended to make those assumptions inspectable.

The current independent-noise helper multiplies separate coherence envelopes,

[
W_{mathrm{total}}(t)=prod_iW_i(t),
]

which is appropriate only when the underlying assumptions justify independent factorization. Correlated environmental channels require a more general treatment. Future versions will introduce cross-spectral-density matrices (S_{ij}(f)), allowing multiple gate voltages or multiple control channels to be treated together.

One of the primary applications of this repository is charge-noise dephasing in Ge/SiGe hole-spin qubits. If a device model provides a gate susceptibility

[
rac{partial f_Z}{partial V},
]

and the voltage-noise spectrum is (S_V(f)), then the first-order frequency-noise spectrum is approximately

[
S_f(f)=
left(
rac{partial f_Z}{partial V}
ight)^2
S_V(f).
]

For multiple gates, this becomes a matrix problem involving cross-correlations between channels. This connection is the bridge between device electrostatics and measurable spin coherence.

The planned development of QuantumDot-Noise-Lab includes CPMG filters, driven Rabi decay, arbitrary pulse-sequence filter functions, exact random-telegraph trajectories, multi-axis noise, finite pulse-width effects, and cross-spectral-density matrices. A more advanced long-term goal is to support direct inference of a noise model from experimental coherence data, while preserving a clear distinction between measured observables and model-dependent interpretation.

A reproducible coherence calculation should document the PSD convention, frequency units, low- and high-frequency cutoffs, sampling grid, pulse sequence, sensitivity conversion, numerical integration method, and exact software version. If stochastic synthesis is used, the random seed and sampling duration should also be reported. These details can materially change the numerical result and therefore belong to the scientific record rather than to implementation trivia.

The current project is suitable for theoretical studies, teaching, benchmarking, experimental post-processing, and development of noise-analysis methods. It should not be treated as a complete open-system solver. Bloch-Redfield theory, Lindblad dynamics, non-Gaussian stochastic processes, and microscopic phonon calculations are outside the present scope, although some may be added later.

## Contact

**Athul Prem**

For questions, collaboration, scientific discussion, or suggestions related to this repository, please contact Athul Prem through the GitHub account associated with the project.
