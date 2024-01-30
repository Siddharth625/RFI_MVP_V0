from fastapi import FastAPI, HTTPException, Depends, Request, Query, Body
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import json
from backend.identification import Identification
from backend.constants import databaseV2
from backend.assumptions import Assumptions
# import google.cloud.logging
# client = google.cloud.logging.Client()

identification_class = Identification()
assumptions = Assumptions()

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


userInputData = {
    "building_area" : "",
    "zipcode": ""
}
userUtility = ""
userState = ""
userCity = ""
userCounty = ""
userCountry = ""
userZipcode = 0
buildingArea = 0
resultDF = pd.DataFrame()
TaxresultDF = pd.DataFrame()


@app.post('/getUserData')
async def getUserData(userInputData: dict):
    global userCity
    global userCounty
    global userState
    global userCountry
    global userZipcode
    global buildingArea
    global userUtility
    global resultDF

    # Data from the user - Zipcode & Building Area
    userZipcode = int(userInputData['zipcode'])
    buildingArea = float(userInputData["building_area"])

    # Configuring City, State, County and Country manually
    # For future versions we require a service which gives us the city, state, country details with just a zipcode
    if 89999 < userZipcode < 96162:
        userState = "CA"
    else:
        userState = "NY"
    dfZipcode = identification_class.locationConfig(userState, "USA")
    
    # Location configuration using user zipcode
    userCity = dfZipcode[dfZipcode["Zipcode"] == userZipcode]["City"].iloc[0]
    userCounty = dfZipcode[dfZipcode["Zipcode"] == userZipcode]["County"].iloc[0]
    userState = dfZipcode[dfZipcode["Zipcode"] == userZipcode]["State"].iloc[0]
    userCountry = dfZipcode[dfZipcode["Zipcode"] == userZipcode]["Country"].iloc[0]
    return {
            "status" : 200,
            "zipcode" : userZipcode,
            "city": userCity,
            "state" : userState,
            "county" : userCounty,
            "country" : userCountry,
            "building area" : buildingArea
            }

#------------------------------------- Above Code Working Fine ---------------------------------------------

@app.post('/tax_incentives')
async def CalculateTaxIncentives(userSelectedTech : list):
    global TaxresultDF
    TaxrebateData = databaseV2.copy()
    TaxresultDF = TaxrebateData[(TaxrebateData["Jurisdiction"] == "Federal")]


    return json.loads(TaxresultDF.to_json(orient="records"))



    # tax_table = resultDF.copy()
    # tax_table = tax_table[tax_table["Jurisdiction"] == "Federal"]
    # userSelectedTech = ["HVAC", "LED","Insulation","Controls"]
    # # userSelectedTech = ["All"]
    # Section179D_params = {
    # 'Base_Deduction_High' : 1.00,
    # 'Base_Deduction_Low' : 0.50,
    # 'Base_Deduction_Inc' : 0.02,
    # 'Bonus_Deduction_High' : 5.00,
    # 'Bonus_Deduction_Low' : 2.50,
    # 'Bonus_Deduction_Inc' : 0.10,
    # 'Energy_Efficiency_Low' : 0.25,
    # 'Energy_Efficiency_High' : 0.50,
    # 'Prevailing_Wages_Law' : 1,
    # 'Apprenticeship_Hours_Met' : 1,
    # }
    # energy_eff_lst = [0.25, 0.5]
    # buildingArea = 20000
    # return IRA_179D(energy_eff_lst, buildingArea, Section179D_params)






if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)


@app.post('/get_user_info')
async def getUserInfo(userInputData: dict):
    global userCity
    global userCounty
    global userState
    global userCountry
    global userZipcode
    global buildingArea
    global userUtility
    global resultDF
    userUtility = userInputData['utility']
    userCity = userInputData['city']
    userState = userInputData['state']
    userCounty = userInputData['county']
    userCountry = userInputData['country']
    userZipcode = int(userInputData['zipcode'])
    buildingArea = float(userInputData["building_area"])
    # # Checking for which State does the user belong to and then initializing that state's zipcode csv
    # # Need to know if I can get the state from only the zipcode from the frontend - Rishabh
    # if 89999 < userZipcode < 96162:
    #     userState = "CA"
    # else:
    #     userState = "NY"
    # dfZipcode = identification_class.locationConfig(userState, userCountry)
    
    # # # Location configuration using user zipcode
    # # userCity = dfZipcode[dfZipcode["Zipcode"] == userZipcode]["City"].iloc[0]
    # # userCounty = dfZipcode[dfZipcode["Zipcode"] == userZipcode]["County"].iloc[0]
    # # userState = dfZipcode[dfZipcode["Zipcode"] == userZipcode]["State"].iloc[0]

    # Filtered incentives based on locality
    rebateData = databaseV2.copy()
    fiteredRebateData = rebateData[(rebateData["State"] == userCountry) | \
                                ((rebateData["State"] == userState) & (rebateData["County"] == userState)) | \
                                (rebateData["County"] == userCounty)]
    # fiteredRebateData['Estimated Incentive Value'] = fiteredRebateData['Estimated Incentive Value'].astype(float)
    # rebates_data = fiteredRebateData[fiteredRebateData['Incentive Type'] == 'Discount']
    # tax_amount_data = fiteredRebateData[fiteredRebateData['Incentive Value'] != 'Discount']
    resultDF = fiteredRebateData.copy()
    print(resultDF)
    resultDF = assumptions.Caliberate_Assumptions(resultDF, buildingArea)
    # resultDF.to_csv("RESDF.csv", index = False)
    return json.loads(resultDF.to_json(orient="records"))

@app.get('/statstodisplay')
async def statstodisplay():
    global resultDF
    dfStats = resultDF.copy()
    # Federal Stats
    federalStat = len(dfStats[dfStats["Jurisdiction"] == "Federal"])
    stateStat = len(dfStats[dfStats["Jurisdiction"] == "State"])
    utilityStat = len(dfStats[dfStats["Jurisdiction"] == "Utility"])
    return {"federalStat" : federalStat,
            "stateStat" : stateStat,
            "utilityStat" : utilityStat}

@app.get('/high_level_view')
async def highLevelView():
    global resultDF
    dfHighLevel = resultDF.copy()
    print(dfHighLevel.head())
    dfHighLevel = dfHighLevel.groupby(['Technology' , 'Sub-Technology'])['Amt_Estimation'].agg(['median']).reset_index()
    result_dict = {}
    for (category, group_type), group in dfHighLevel.groupby(['Technology' , 'Sub-Technology']):
        group_json = group.to_json(orient='records')
        result_dict.setdefault(category, {}).setdefault(group_type, json.loads(group_json))
    result_json = json.dumps(result_dict, indent=2)
    print(result_json)
    return {"data" : json.loads(result_json)}

@app.get('/low_level_view')
async def lowLevelView():
    global resultDF
    dfLowLevel = resultDF.copy()
    dfLowLevel = dfLowLevel.groupby(['Technology' ,'Incentive Name','Provider','Website Link'])[['Amt_Estimation']].agg(['median']).reset_index()
    result_dict = {}
    for (category, group_type, size, location), group in dfLowLevel.groupby(['Technology' ,'Incentive Name','Provider','Website Link']):
        group_json = group.to_json(orient='records')
        result_dict \
            .setdefault(category, {}) \
            .setdefault(group_type, {}) \
            .setdefault(size, {}) \
            .setdefault(location, json.loads(group_json))
    result_json = json.dumps(result_dict, indent=2)
    return {"data" : json.loads(result_json)}


    
