import numpy as np
from qd_noise_lab.core import ramsey_quasistatic, exponential_envelope

t=np.linspace(0,20e-6,5)
print("t [us]   quasistatic   exponential")
for ti,a,b in zip(t, ramsey_quasistatic(t,2e4), exponential_envelope(t,15e-6)):
    print(f"{ti*1e6:6.1f}   {a:10.6f}   {b:10.6f}")
