import numpy as np
from qd_noise_lab.core import ramsey_quasistatic, combine_independent

def test_ramsey_starts_one():
    assert np.isclose(ramsey_quasistatic(0.0,1e5),1.0)

def test_independent_product():
    assert np.allclose(combine_independent([.5,.2],[.5,.5]),[.25,.1])
