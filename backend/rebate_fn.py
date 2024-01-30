import os
import math
import pandas as pd
import numpy as np
from backend.constants import *

class rebateFunctions:
    def __init__(self) -> None:
        pass

    def IRA_179D (energy_eff_lst, bld_sq_footage, Section179D_params):
        base_deduction = 0
        bonus_deduction = 0
        # Base Deduction
        IRA_179D_df = []
        # result_df = result_df.append({
        #         'Energy_Efficiency': efficiency,
        #         'Simulation_Result': simulation_result
        #     }, ignore_index=True)
        for energy_eff in energy_eff_lst:
            if energy_eff >= Section179D_params['Energy_Efficiency_High']:
                base_deduction = Section179D_params['Base_Deduction_High'] * bld_sq_footage
            elif energy_eff > Section179D_params['Energy_Efficiency_Low'] \
                and energy_eff < Section179D_params['Energy_Efficiency_High']:
                additional_percent = energy_eff - Section179D_params['Energy_Efficiency_Low']
                base_deduction = Section179D_params['Base_Deduction_Low'] * bld_sq_footage
                base_deduction = base_deduction + \
                                (Section179D_params['Base_Deduction_Inc'] * additional_percent * bld_sq_footage)
            else:
                base_deduction = Section179D_params['Base_Deduction_Low'] * bld_sq_footage
            
            # Bonus Deduction
            if (Section179D_params['Prevailing_Wages_Law'] == 1 and Section179D_params['Apprenticeship_Hours_Met'] == 1):
                if energy_eff >= Section179D_params['Energy_Efficiency_High']:
                    bonus_deduction = Section179D_params['Bonus_Deduction_High'] * bld_sq_footage
                elif energy_eff > Section179D_params['Energy_Efficiency_Low'] \
                    and energy_eff < Section179D_params['Energy_Efficiency_High']:
                    additional_percent = energy_eff - Section179D_params['Energy_Efficiency_Low']
                    bonus_deduction = Section179D_params['Bonus_Deduction_Low'] * bld_sq_footage
                    bonus_deduction = bonus_deduction + \
                                    (Section179D_params['Bonus_Deduction_Inc'] * additional_percent * bld_sq_footage)
                else:
                    bonus_deduction = Section179D_params['Bonus_Deduction_Low'] * bld_sq_footage
            IRA_179D_df.append({
                "Program Name" : "IRA Section 179D",
                "Energy Efficiency" : energy_eff,
                "Prevailing Wage & Apprenticeship Rule" : "TRUE",
                "Base Deduction" : base_deduction,
                "Bonus Deduction" : bonus_deduction
            })
            result_df = pd.DataFrame(IRA_179D_df)
        return result_df
