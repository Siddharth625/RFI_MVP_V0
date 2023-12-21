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
    "http://localhost",
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

@app.get('/')
def index():
    return {'Hello' : "World"}

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
    fiteredRebateData = rebateData[ (rebateData["State"] == userCountry) | \
                                ((rebateData["State"] == userState) & (rebateData["County"] == userState)) | \
                                (rebateData["County"] == userCounty)]
    # fiteredRebateData['Estimated Incentive Value'] = fiteredRebateData['Estimated Incentive Value'].astype(float)
    # rebates_data = fiteredRebateData[fiteredRebateData['Incentive Type'] == 'Discount']
    # tax_amount_data = fiteredRebateData[fiteredRebateData['Incentive Value'] != 'Discount']
    fiteredRebateData = assumptions.Caliberate_Assumptions(fiteredRebateData)
    resultDF = fiteredRebateData.copy()
    print(resultDF)
    return json.loads(resultDF.to_json(orient="records"))

@app.get('/high_level_view')
async def highLevelView():
    global resultDF
    dfHighLevel = resultDF.copy()
    dfHighLevel = dfHighLevel.groupby(['Technology' , 'Sub-Technology'])['Amt_Estimation'].agg(['median']).reset_index()
    result_dict = {}
    for (category, group_type), group in dfHighLevel.groupby(['Technology' , 'Sub-Technology']):
        group_json = group.to_json(orient='records')
        result_dict.setdefault(category, {}).setdefault(group_type, json.loads(group_json))
    result_json = json.dumps(result_dict, indent=2)
    print(result_json)
    return {"data" : result_json}

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
    print(result_json)
    return {"data" : result_json}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
