import numpy as np

def ramsey_quasistatic(t_s, sigma_f_hz):
    t=np.asarray(t_s,float)
    return np.exp(-2*np.pi**2*sigma_f_hz**2*t**2)

def exponential_envelope(t_s, T_s):
    if T_s <= 0: raise ValueError("T_s must be positive")
    return np.exp(-np.asarray(t_s,float)/T_s)

def stretched_exponential(t_s, T_s, beta):
    if T_s <= 0 or beta <= 0: raise ValueError("T_s and beta must be positive")
    return np.exp(-(np.asarray(t_s,float)/T_s)**beta)

def combine_independent(*envelopes):
    if not envelopes: raise ValueError("provide at least one envelope")
    out=np.ones_like(np.asarray(envelopes[0],float))
    for e in envelopes: out=out*np.asarray(e,float)
    return out
