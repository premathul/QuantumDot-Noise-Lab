import numpy as np
from qd_noise_lab.spectra import one_over_f_psd, random_telegraph_psd
from qd_noise_lab.filter_functions import ramsey_filter_sq, echo_filter_sq, gaussian_phase_coherence

def test_one_over_f_scaling():
    s=one_over_f_psd(np.array([1.,10.]),100.,alpha=1)
    assert np.isclose(s[0]/s[1],10)

def test_rtn_positive():
    assert np.all(random_telegraph_psd([1,10],100,1e3)>0)

def test_echo_dc_zero():
    assert np.isclose(echo_filter_sq(np.array([0.0]),1e-6)[0],0)

def test_zero_psd_coherence_one():
    f=np.logspace(0,6,1000)
    w,chi=gaussian_phase_coherence(f,np.zeros_like(f),ramsey_filter_sq(f,1e-6))
    assert np.isclose(w,1) and np.isclose(chi,0)
