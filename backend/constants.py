import os
import pandas as pd

cwd = os.getcwd()
CA_Zipcode_Path = os.path.join(cwd, "backend", "database", "Zipcodes","USA","CA", "USA_CA_ZIPCODE.csv")
NY_Zipcode_Path = os.path.join(cwd, "backend", "database", "Zipcodes","USA","NY", "USA_NY_ZIPCODE.csv")

DB_Path = os.path.join(cwd, "backend",  "database", "MVP_DB_V2_NY_CA.csv")
databaseV2 = pd.read_csv(DB_Path)

Nexus_DB_Path_Tax = os.path.join(cwd, "backend",  "database","Nexus_DB", "Tax_Incentive_DB.csv")
Nexus_DB_Path_Tax_db = pd.read_csv(Nexus_DB_Path_Tax)

Nexus_DB_Path_Discount = os.path.join(cwd, "backend",  "database","Nexus_DB", "Discount_Incentives.csv")
Nexus_DB_Path_Discount_db = pd.read_csv(Nexus_DB_Path_Discount)

RETRO_MOTOR_FAN_HP = 999
RETRO_HVAC_PACKAGED_W = 999

Section179D_params = {
    'Base_Deduction_High' : 1.00,
    'Base_Deduction_Low' : 0.50,
    'Base_Deduction_Inc' : 0.02,
    'Bonus_Deduction_High' : 5.00,
    'Bonus_Deduction_Low' : 2.50,
    'Bonus_Deduction_Inc' : 0.10,
    'Energy_Efficiency_Low' : 0.25,
    'Energy_Efficiency_High' : 0.50,
    'Prevailing_Wages_Law' : 1,
    'Apprenticeship_Hours_Met' : 1,
}

ITC_PTC_Params = {
    "project_rate" : 8,
    "project_kWh" : 100,
    "domestic_content" : True,
    "energy_community" : True
}
