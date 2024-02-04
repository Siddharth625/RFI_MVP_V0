import os
import math
import pandas as pd
import numpy as np
import json
from backend.constants import *

class rebateFunctionsClass:
    def __init__(self) -> None:
        pass

    def IRA_179D (self, bld_sq_footage):
        base_deduction = 0
        bonus_deduction = 0
        energy_eff_lst = [0.25, 0.50]

        # Base Deduction
        IRA_179D_df = []
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
        return json.loads(result_df.to_json(orient="records"))
    
    def IRA_ITC(self, buildingArea):
        IRA_ITC_lst = []
        # Solar kWh estimation needs to come from Aurora
        project_cost = buildingArea * ITC_PTC_Params["project_rate"]
        itc_tax_credit = project_cost * 0.30
        bonus_amt = project_cost * 0.10
        IRA_ITC_lst.append({
                "Program Name" : "IRA - Investment Tax Credit",
                "Domestic Content" : "TRUE",
                "Energy Community" : "TRUE",
                "Low-Income Community" : "TRUE",
                "Amount" : itc_tax_credit
            })
        IRA_ITC_lst.append({
                "Program Name" : "IRA - Investment Tax Credit",
                "Domestic Content" : itc_tax_credit + bonus_amt,
                "Energy Community" : itc_tax_credit + 2*bonus_amt,
                "Low-Income Community" : itc_tax_credit + 3*bonus_amt,
                "Amount" : itc_tax_credit + 3*bonus_amt
            })
        result_df = pd.DataFrame(IRA_ITC_lst)
        return json.loads(result_df.to_json(orient="records"))
    
    def IRA_PTC(self, buildingArea):
        IRA_PTC_lst = []
        # Solar kWh estimation needs to come from Aurora
        kWh_gen = buildingArea * ITC_PTC_Params["project_kWh"]
        ptc_tax_credit = kWh_gen * 0.0275
        bonus_amt = kWh_gen * 0.003
        IRA_PTC_lst.append({
                "Program Name" : "IRA - Investment Tax Credit",
                "Domestic Content" : "TRUE",
                "Energy Community" : "TRUE",
                "Low-Income Community" : "TRUE",
                "Amount" : ptc_tax_credit
            })
        IRA_PTC_lst.append({
                "Program Name" : "IRA - Investment Tax Credit",
                "Domestic Content" : ptc_tax_credit + bonus_amt,
                "Energy Community" : ptc_tax_credit + 2 * bonus_amt,
                "Low-Income Community" : ptc_tax_credit + 3*bonus_amt,
                "Amount" : ptc_tax_credit + 3*bonus_amt
            }
        )
        result_df = pd.DataFrame(IRA_PTC_lst)
        return json.loads(result_df.to_json(orient="records"))
