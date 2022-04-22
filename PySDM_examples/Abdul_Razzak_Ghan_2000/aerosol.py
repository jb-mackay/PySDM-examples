from chempy import Substance
from PySDM.initialisation import spectra
from PySDM.physics import si
from pystrict import strict

from PySDM_examples.utils import BasicAerosol


@strict
class AerosolARG(BasicAerosol):
    def __init__(
        self,
        M2_sol: float = 0,
        M2_N: float = 100 / si.cm**3,
        M2_rad: float = 50 * si.nm,
    ):
        mode1 = {
            "(NH4)2SO4": 1.0,
            "insoluble": 0,
        }
        mode2 = {
            "(NH4)2SO4": M2_sol,
            "insoluble": (1 - M2_sol),
        }
        super().__init__(
            ionic_dissociation_phi={"(NH4)2SO4": 3, "insoluble": 0},
            molar_masses={
                "(NH4)2SO4": Substance.from_formula("(NH4)2SO4").mass
                * si.gram
                / si.mole,
                "insoluble": 44 * si.g / si.mole,
            },
            aerosol_modes=(
                {
                    "kappa": super().kappa(mode1),
                    "spectrum": spectra.Lognormal(
                        norm_factor=100.0 / si.cm**3, m_mode=50.0 * si.nm, s_geom=2.0
                    ),
                },
                {
                    "kappa": super().kappa(mode2),
                    "spectrum": spectra.Lognormal(
                        norm_factor=M2_N, m_mode=M2_rad, s_geom=2.0
                    ),
                },
            ),
            densities={
                "(NH4)2SO4": 1.77 * si.g / si.cm**3,
                "insoluble": 1.77 * si.g / si.cm**3,
            },
            compounds=("(NH4)2SO4", "insoluble"),
            is_soluble={"(NH4)2SO4": True, "insoluble": False},
        )


@strict
class AerosolWhitby(BasicAerosol):
    def __init__(self):
        nuclei = {
            "(NH4)2SO4": 1.0,
        }
        accum = {"(NH4)2SO4": 1.0}
        coarse = {"(NH4)2SO4": 1.0}

        super().__init__(
            ionic_dissociation_phi={"(NH4)2SO4": 3},
            molar_masses={
                "(NH4)2SO4": Substance.from_formula("(NH4)2SO4").mass
                * si.gram
                / si.mole
            },
            aerosol_modes=(
                {
                    "kappa": super().kappa(nuclei),
                    "spectrum": spectra.Lognormal(
                        norm_factor=1000.0 / si.cm**3,
                        m_mode=0.008 * si.um,
                        s_geom=1.6,
                    ),
                },
                {
                    "kappa": super().kappa(accum),
                    "spectrum": spectra.Lognormal(
                        norm_factor=800 / si.cm**3, m_mode=0.034 * si.um, s_geom=2.1
                    ),
                },
                {
                    "kappa": super().kappa(coarse),
                    "spectrum": spectra.Lognormal(
                        norm_factor=0.72 / si.cm**3, m_mode=0.46 * si.um, s_geom=2.2
                    ),
                },
            ),
            densities={"(NH4)2SO4": 1.77 * si.g / si.cm**3},
            compounds="(NH4)2SO4",
            is_soluble={"(NH4)2SO4": True},
        )
