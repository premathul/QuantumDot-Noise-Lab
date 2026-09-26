import numpy as np

def synthesize_gaussian_noise_from_psd(f_hz, psd_hz2_per_hz, duration_s, n_samples, rng=None):
    """Generate a real Gaussian frequency-noise trace using target one-sided PSD samples."""
    if duration_s<=0 or n_samples<4: raise ValueError("invalid duration or sample count")
    gen=np.random.default_rng(rng)
    dt=duration_s/n_samples
    freqs=np.fft.rfftfreq(n_samples,dt)
    target=np.interp(freqs,np.asarray(f_hz,float),np.asarray(psd_hz2_per_hz,float),left=0,right=0)
    df=1/duration_s
    amp=np.sqrt(np.maximum(target,0)*df/2)
    z=gen.normal(size=freqs.size)+1j*gen.normal(size=freqs.size)
    z*=amp
    z[0]=0
    if n_samples%2==0: z[-1]=z[-1].real
    return np.fft.irfft(z,n_samples)*n_samples
