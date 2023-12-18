from fastapi import FastAPI, HTTPException, Depends, Request, Query, Body
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import json
from backend.identification import Identification
from backend.constants import databaseV2
# import google.cloud.logging

# client = google.cloud.logging.Client()

class_id = Identification()

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
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
userState = ""
userCity = ""
userCounty = ""
userCountry = ""
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
    global buildingArea
    userCity = userInputData['city']
    userState = userInputData['state']
    userCounty = userInputData['county']
    userCountry = userInputData['country']
    buildingArea = float(userInputData["building_area"])
    return ({'status': 200})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)


    # # Location configuration using user zipcode
    # if 89999 < int(userInputData["zipcode"]) < 96162:
    #     userState = "CA"
    # else:
    #     userState = "NY"
    # dfZipcode = class_id.locationConfig(userState)
    # userZipcode = int(userInputData["zipcode"])
    # userCity = dfZipcode[dfZipcode["Zipcode"] == userZipcode]["City"].iloc[0]
    # userCounty = dfZipcode[dfZipcode["Zipcode"] == userZipcode]["County"].iloc[0]
    # userState = dfZipcode[dfZipcode["Zipcode"] == userZipcode]["State"].iloc[0]
    # userCountry = "USA" # Hardcoded for now

    # # Filtered incentives based on locality
    # rebateData = databaseV2.copy()
    # fiteredRebateData = rebateData[ (rebateData["State"] == userCountry) | \
    #                             ((rebateData["State"] == userState) & (rebateData["County"] == userState)) | \
    #                             (rebateData["County"] == userCounty)]
    # fiteredRebateData['Estimated Incentive Value'] = fiteredRebateData['Estimated Incentive Value'].astype(float)

    # # Group by aggregation
    # ## HL 1 Table 
    # resdf1 = fiteredRebateData.groupby(['Technology' , 'Sub-Technology'])['Estimated Incentive Value'].agg(['mean'])

    # ## HL 2 Table
    # resdf2 = fiteredRebateData.groupby(['Technology' , 'Sub-Technology','Incentive Name','Provider', 'Incentive Type'])[['Estimated Incentive Value']].agg(['mean'])

    # print(resdf1)
    # print(resdf2)
    # return {
    #         'status': 200,
    #         "User City" : userCity,
    #         "User County" : userCounty,
    #         "User State" : userState,
    #         "Zipcode" : userInputData["zipcode"]
    #     }