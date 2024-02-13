import os
import math
import pandas as pd
import numpy as np
import json
from backend.constants import *
from backend.technology_calc import Technology

techClass = Technology()

class discountFunctionsClass(Technology):
    def __init__(self) -> None:
        pass

    def getDiscountResult(self, discountDF, buildingArea):
        if "USA_UTP_CA_0001" in discountDF["Incentive_ID"].unique().tolist():
            return discountFunctionsClass.PGE_Business_Rebate(self, discountDF, buildingArea)

    def PGE_Business_Rebate(self, discountDF, buildingArea):
        df_master = pd.DataFrame()
        df_master = self.Standard_Type(discountDF, buildingArea)
        df_master = techClass.HVAC_Motors(df_master, discountDF,buildingArea)
        df_master = techClass.HVAC_PACKAGED(df_master,discountDF,buildingArea)
        return df_master
    