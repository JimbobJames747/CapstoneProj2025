from RbVapourEIT import RbVapourEIT
from RbVapourRaman import RbVapourRaman  
from PrGEM import PrGEM
from EuCrystalAFC import EuCrystalAFC
from ErCrystalAFC import ErCrystalAFC
from parameters import *


def main():
    # Rb EIT (qfcd enabled)
    rb_eit = RbVapourEIT(
        name="RbEIT",
        in_wavelength=VAPOUR_EIT_MEMORY_WAVELENGTH,
        in_storage_time=VAPOUR_EIT_MEMORY_STORAGE_TIME,  # match spec
        in_fidelity=0.95,
        qfcd=True,
        verbose=True,
    )
    rb_eit.summary  # prints

    # Rb Raman (qfcd enabled)
    rb_raman = RbVapourRaman(
        name="RbRaman",
        in_wavelength=VAPOUR_RAMAN_MEMORY_WAVELENGTH,
        in_storage_time=VAPOUR_RAMAN_MEMORY_STORAGE_TIME / 2,  # safely <= spec
        in_fidelity=0.96,
        qfcd=True,
        verbose=True,
    )
    rb_raman.summary  # prints

    # Pr GEM (qfcd enabled)
    pr_gem = PrGEM(
        name="PrGEM",
        in_wavelength=PR_GEM_MEMORY_WAVELENGTH,
        in_storage_time=PR_GEM_MEMORY_STORAGE_TIME / 2,
        in_fidelity=0.97,
        qfcd=True,
        verbose=True,
    )
    pr_gem.summary  # prints

    # Eu:YSO AFC (short-storage variant, qfcd enabled)
    eu_afc = EuCrystalAFC(
        name="EuAFC",
        in_wavelength=EU_AFC_MEMORY_WAVELENGTH,
        in_storage_time=min(10e-6, EU_SHORT_AFC_MEMORY_STORAGE_TIME),
        in_fidelity=0.90,
        long_storage=False,
        qfcd=True,
        verbose=True,
    )
    eu_afc.summary  # prints

    # Er:YSO AFC
    er_afc = ErCrystalAFC(
        name="ErAFC",
        in_wavelength=ER_AFC_MEMORY_WAVELENGTH,
        in_storage_time=ER_AFC_MEMORY_STORAGE_TIME / 2,
        in_fidelity=0.92,
        verbose=True,
    )
    er_afc.summary  # prints


if __name__ == "__main__":
    main()