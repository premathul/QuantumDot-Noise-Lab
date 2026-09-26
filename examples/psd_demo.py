import numpy as np
from qd_noise_lab.spectra import one_over_f_psd
from qd_noise_lab.filter_functions import ramsey_filter_sq, echo_filter_sq, gaussian_phase_coherence

f=np.logspace(0,7,4000)
s=one_over_f_psd(f,1e10,alpha=1)
for t in (1e-6,10e-6,100e-6):
    wr,_=gaussian_phase_coherence(f,s,ramsey_filter_sq(f,t))
    we,_=gaussian_phase_coherence(f,s,echo_filter_sq(f,t))
    print(f"t={t*1e6:7.1f} us  Ramsey={wr:.6f} Echo={we:.6f}")
