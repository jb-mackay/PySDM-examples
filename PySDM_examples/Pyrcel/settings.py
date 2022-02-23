import numpy as np
from pystrict import strict
from PySDM import Formulae
from PySDM.initialisation.sampling import spectral_sampling as spec_sampling
from PySDM.physics import si
from PySDM_examples.Lowe_et_al_2019.aerosol import Aerosol


@strict
class Settings:
    def __init__(self,
                 dz: float,
                 n_sd_per_mode: tuple,
                 aerosol: Aerosol,
                 spectral_sampling: type(spec_sampling.SpectralSampling),
                 ):
        self.n_sd_per_mode = n_sd_per_mode
        self.formulae = Formulae()
        const = self.formulae.constants
        self.aerosol = aerosol
        self.spectral_sampling = spectral_sampling

        max_altitude = 250 * si.m
        self.w = 1.0 * si.m / si.s
        self.t_max = max_altitude / self.w
        self.dt = dz / self.w
        self.output_interval = 1 * self.dt

        self.g = 9.81 * si.m / si.s**2

        self.p0 = 775 * si.mbar
        self.T0 = 274 * si.K
        pv0 = .98 * self.formulae.saturation_vapour_pressure.pvs_Celsius(self.T0 - const.T0)
        self.q0 = const.eps * pv0 / (self.p0 - pv0)

        self.cloud_radius_range = (
                .5 * si.micrometre,
                np.inf
        )

        self.mass_of_dry_air = 44

        self.wet_radius_bins_edges = np.logspace(
            np.log10(4 * si.um),
            np.log10(12 * si.um),
            128+1,
            endpoint=True
        )

        self.dry_radius_bins_edges = np.logspace(
            np.log10(1e-3 * si.um),
            np.log10(5e0 * si.um),
            128+1,
            endpoint=False
        )


    @property
    def rho0(self):
        const = self.formulae.constants
        rhod0 = self.formulae.trivia.p_d(self.p0, self.q0) / self.T0 / const.Rd
        return rhod0 * (1 + self.q0)

    @property
    def nt(self) -> int:
        nt = self.t_max / self.dt
        nt_int = round(nt)
        np.testing.assert_almost_equal(nt, nt_int)
        return nt_int

    @property
    def steps_per_output_interval(self) -> int:
        return int(self.output_interval / self.dt)

    @property
    def output_steps(self) -> np.ndarray:
        return np.arange(0, self.nt + 1, self.steps_per_output_interval)
