from cavity_model_resonance import LambdaCavityModel  
import numpy as np

# Constants
T_vals = np.linspace(1, 100, 100)  # x-axis: TCγ, 100 steps
C_values = [1, 10, 100, 1000]  # cooperativity values
Delta_vals = [1, 10, 100]  # detuning values

def run_lambda_cavity_plot():
    # wavelength = 1500, wavelength_eg defaults to 0
    model = LambdaCavityModel(
        name='memory 1',
        wavelength=1500,
        storage_time=10,
        fidelity=0.9,
        period=20,
        cooperativity=10,
        storage_decay=0.0,
        verbose=True
    )
    
    model.plot_efficiency_sweep(
        title='Total Efficiency against Period for Varying Cooperativity (C = 10)',
        save_filename='cavity_model_sweep_figure_1.png',
    )

    # model.plot_efficiency(
    #     title='Total Efficiency against Period (Δ = 0)',
    #     save_filename='cavity_model_figure_2.png',
    # )

    # model.plot_fidelity(
    #     title='Retrieval Fidelity against Period (Δ = 0)',
    #     save_filename='cavity_model_fidelity_figure_1.png',
    # )

    # model.plot_efficiency_sweep_Delta(
    #     title='Total Efficiency against Period for Varying Delta (C = 10)',
    #     save_filename='cavity_model_sweep_figure_3.png',
    # )

    # model.assumptions


if __name__ == "__main__":
    run_lambda_cavity_plot() 