import os
import pandas as pd

cwd = os.getcwd()
CA_Zipcode_Path = os.path.join(cwd, "backend", "database", "Zipcodes","USA","CA", "USA_CA_ZIPCODE.csv")
NY_Zipcode_Path = os.path.join(cwd, "backend", "database", "Zipcodes","USA","NY", "USA_NY_ZIPCODE.csv")

DB_Path = os.path.join(cwd, "backend",  "database", "MVP_DB_V2_NY_CA.csv")
databaseV2 = pd.read_csv(DB_Path)
