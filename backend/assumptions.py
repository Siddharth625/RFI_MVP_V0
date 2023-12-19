import os
import math
import pandas as pd
import numpy as np
from backend.constants import *

# Energy Breakup for a small office
HVAC_SO_EUI = 4.95
LED_SO_EUI = 1.8
INSULATION_SO_EUI = 0.9
CONTROLS_SO_EUI = 1.35
TOTAL_SO_EUI = 9



# HVAC Type 1
ASMP_BTUH_SCALING_FACTOR = 5 # Needs Revision

# HVAC Type 2
KWH_TO_BTU = 3414
HVAC_Breakup = {
    "Air Conditioners" : 0.6,
    "Air Compressors" : 0.6,
    "Heat Pumps" : 0.6,
    "Heaters" : 0.6,
    "Pumps and Motors" : 0.3,

}

# Insulation Type 1
THERM_FACTOR = 0.0341296

class Assumptions:
    def __init__(self) -> None:
        pass

    def HVAC_TYPE_1(self, resdf):
        """_summary_

        Args:
            resdf (_type_): _description_
        """
        resdf["Amt_Estimation"] = np.where(resdf["Assumption Type"] == "HVAC Type 1", \
                                  resdf["Incentive Value"] * ASMP_BTUH_SCALING_FACTOR, \
                                  resdf["Incentive Value"])
        return resdf
        
    
    def HVAC_TYPE_2(self, resdf):
        """_summary_

        Args:
            resdf (_type_): _description_
        """
        resdf["Amt_Estimation"] = np.where(resdf["Assumption Type"] == "HVAC Type 2", \
                                  (HVAC_Breakup[resdf["Sub-Technology"]] * buildingArea * resdf["Incentive Value"] * KWH_TO_BTU * HVAC_SO_EUI)/1000000, \
                                  resdf["Incentive Value"])
        return resdf

    def Insulation_Type_1(self, resdf):
        """_summary_

        Args:
            resdf (_type_): _description_
        """
        resdf["Amt_Estimation"] = np.where(
                    resdf["Assumption Type"] == "Insulation Type 1",
                    np.where(
                        resdf["Unit"] == "kWh", 
                        resdf["Sub-Technology"].map(INSULATION_BREAKUP) * INSULATION_SO_EUI * resdf["Incentive Value"] * buildingArea,
                        np.where(
                            resdf["Unit"] == "Therm",
                            resdf["Sub-Technology"].map(INSULATION_BREAKUP) * INSULATION_SO_EUI * resdf["Incentive Value"] * buildingArea * THERM_FACTOR,
                            0
                        )
                    ),
                    resdf["Incentive Value"]
                )
        return resdf

        def Insulation_Type_2(self, resdf):
        """_summary_

        Args:
            resdf (_type_): _description_
        """
        resdf["Amt_Estimation"] = np.where(
                    resdf["Assumption Type"] == "Insulation Type 2",
                    buildingArea * resdf["Incentive Value"],
                    resdf["Incentive Value"]
                )
        return resdf


        def Insulation_Type_3(self, resdf):
        """_summary_

        Args:
            resdf (_type_): _description_
        """
        resdf["Amt_Estimation"] = np.where(
                    resdf["Assumption Type"] == "Insulation Type 3",
                    resdf["Incentive Value"] * (math.sqrt(buildingArea) + math.sqrt(math.sqrt(buildingArea))),
                    resdf["Incentive Value"]
                )
        return resdf


        def Controls_Type_1(self, resdf):
        """_summary_

        Args:
            resdf (_type_): _description_
        """
        resdf["Amt_Estimation"] = np.where(
                    resdf["Assumption Type"] == "Controls Type 1",
                    buildingArea * resdf["Incentive Value"] * CONTROLS_SO_EUI,
                    resdf["Incentive Value"]
                )
        return resdf


        def Controls_Type_2(self, resdf):
        """_summary_

        Args:
            resdf (_type_): _description_
        """
        resdf["Amt_Estimation"] = np.where(
                    resdf["Assumption Type"] == "Controls Type 2",
                    resdf["Incentive Value"],
                    resdf["Incentive Value"]
                )
        return resdf

        # Custom Project Type 1 function yet to be standardized

        def Custom_Project_Type_2(self, resdf):
        """For LED Lighting

        Args:
            resdf (_type_): _description_
        """
        resdf["Amt_Estimation"] = np.where(
                    resdf["Assumption Type"] == "Custom Project Type 2",
                    resdf["Incentive Value"] * buildingArea * LED_SO_EUI,
                    resdf["Incentive Value"]
                )
        return resdf