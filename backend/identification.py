import os
import pandas as pd
from backend.constants import *

class Identification:
    def __init__(self) -> None:
        pass

    def locationConfig(self, userInputState):
        """This function configures the loaction

        Args:
            country (_type_): _description_
            state (_type_): _description_
        """
        zipcode_config = {
            "USA" : {
                "CA" : pd.read_csv(CA_Zipcode_Path),
                "NY" : pd.read_csv(NY_Zipcode_Path),
            },

        }
        return zipcode_config["USA"][userInputState]