import numba.core.registry
import numba.np.ufunc.gufunc

def _resample_loop(x, t_out, interp_win, interp_delta, num_table, scale, y): ...

_resample_loop_p: numba.core.registry.CPUDispatcher
_resample_loop_s: numba.core.registry.CPUDispatcher
resample_f_p: numba.np.ufunc.gufunc.GUFunc
resample_f_s: numba.np.ufunc.gufunc.GUFunc
