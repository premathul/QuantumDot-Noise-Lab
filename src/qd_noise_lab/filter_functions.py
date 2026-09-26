import numpy as np

def ramsey_filter_sq(f_hz, t_s):
    f=np.asarray(f_hz,float)
    x=np.pi*f*t_s
    out=np.empty_like(x)
    mask=np.abs(x)>1e-14
    out[mask]=(np.sin(x[mask])/(np.pi*f[mask]))**2
    out[~mask]=t_s**2
    return out

def echo_filter_sq(f_hz, t_s):
    f=np.asarray(f_hz,float)
    x=np.pi*f*t_s/2
    out=np.empty_like(x)
    mask=np.abs(f)>1e-14
    out[mask]=(4*np.sin(x[mask])**4/(np.pi*f[mask])**2)
    out[~mask]=0.0
    return out

def gaussian_phase_coherence(f_hz, psd_hz2_per_hz, filter_sq):
    f=np.asarray(f_hz,float)
    s=np.asarray(psd_hz2_per_hz,float)
    ff=np.asarray(filter_sq,float)
    if f.shape!=s.shape or f.shape!=ff.shape: raise ValueError("shape mismatch")
    chi=2*np.pi**2*np.trapezoid(s*ff,f)
    return float(np.exp(-chi)),float(chi)
