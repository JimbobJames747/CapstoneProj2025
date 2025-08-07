from EuCrystalAFC import EuCrystalAFC

def main():
    print("\n--- Valid Eu:YSO AFC (Short Storage) ---")
    try: 
        eu_short = EuCrystalAFC(
            name="EuAFC_Short",
            in_wavelength=580e-9,
            in_storage_time=10e-6,  # less than 12e-6
            in_fidelity=0.85,
            long_storage=False,
            verbose=True
        )
        eu_short.summary
        print(f"Retrieved Fidelity: {eu_short.retrieved_fidelity()}")
        print(f"Retrieved Efficiency: {eu_short.retrieved_efficiency()}")
    except Exception as e:
        print("Error:", e)

    print("\n--- Valid Eu:YSO AFC (Long Storage) ---")
    try:
        eu_long = EuCrystalAFC(
            name="EuAFC_Long",
            in_wavelength=570e-9,
            in_storage_time=3000,  # less than 3600s
            in_fidelity=0.95,
            long_storage=True,
            verbose=True
        )
        eu_long.summary
        print(f"Retrieved Fidelity: {eu_long.retrieved_fidelity()}")
        print(f"Retrieved Efficiency: {eu_long.retrieved_efficiency()}")
    except Exception as e:
        print("Error:", e)

    print("\n--- Invalid: Negative Wavelength ---")
    try:
        EuCrystalAFC(
            name="InvalidWavelength",
            in_wavelength=-580e-9,
            in_storage_time=1e-6,
            in_fidelity=0.9,
            long_storage=False
        )
    except Exception as e:
        print(e)

    print("\n--- Invalid: Fidelity > 1 ---")
    try:
        EuCrystalAFC(
            name="InvalidFidelity",
            in_wavelength=580e-9,
            in_storage_time=1e-6,
            in_fidelity=1.2,
            long_storage=False
        )
    except Exception as e:
        print(e)

    print("\n--- Warning: Storage Time Exceeds Limit ---")
    try:
        eu_warn = EuCrystalAFC(
            name="TooLongStorage",
            in_wavelength=580e-9,
            in_storage_time=4000,  # exceeds long limit of 3600s
            in_fidelity=0.9,
            long_storage=True
        )
        eu_warn.summary
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
