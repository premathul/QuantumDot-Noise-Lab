import numpy as np

def white_psd(f_hz, level_hz2_per_hz):
    f=np.asarray(f_hz,float)
    if level_hz2_per_hz<0: raise ValueError("PSD level must be nonnegative")
    return np.full_like(f,level_hz2_per_hz,dtype=float)

def one_over_f_psd(f_hz, amplitude_hz2, alpha=1.0, f_ref_hz=1.0):
    f=np.asarray(f_hz,float)
    if np.any(f<=0): raise ValueError("frequencies must be positive")
    if amplitude_hz2<0 or alpha<=0 or f_ref_hz<=0: raise ValueError("invalid parameters")
    return amplitude_hz2*(f_ref_hz/f)**alpha

def random_telegraph_psd(f_hz, amplitude_hz, switching_rate_hz):
    f=np.asarray(f_hz,float)
    if amplitude_hz<0 or switching_rate_hz<=0: raise ValueError("invalid parameters")
    gamma=switching_rate_hz
    return 4*amplitude_hz**2*gamma/((2*np.pi*f)**2+(2*gamma)**2)
