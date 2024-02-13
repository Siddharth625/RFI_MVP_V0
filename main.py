from fastapi import FastAPI, HTTPException, Depends, Request, Query, Body
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import json
from backend.identification import Identification
from backend.constants import *
from backend.rebate_fn import rebateFunctionsClass
from backend.discounts import discountFunctionsClass
# import google.cloud.logging
# client = google.cloud.logging.Client()

identification_class = Identification()
rebateFunctions = rebateFunctionsClass()
discountFunctions = discountFunctionsClass()

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
DiscountresultDF = pd.DataFrame()


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

@app.post('/tax_incentives')
async def CalculateTaxIncentives():
    global taxTable
    TaxrebateData = Nexus_DB_Path_Tax_db.copy()
    TaxresultDF = TaxrebateData[(TaxrebateData["State"] == userCountry) | \
                                (TaxrebateData["State"] == userState)]
    print(TaxresultDF)
    TaxresultDF["Amount Estimation"] = None
    taxCalcRes = []
    for taxRebate in TaxresultDF["Incentive_ID"].tolist():
        if taxRebate in ["USA_FED_0001","USA_FED_0002","USA_FED_0003"]:
            if taxRebate == "USA_FED_0001":
                IRA_179D_res = rebateFunctions.IRA_179D(buildingArea)
                TaxresultDF.loc[TaxresultDF['Incentive_ID'] == taxRebate, 'Amount Estimation'] = \
                                                            "$" + \
                                                            str(IRA_179D_res[0]["Base Deduction"]) + \
                                                            " - " + \
                                                            "$" + \
                                                            str(IRA_179D_res[0]["Bonus Deduction"])
                taxCalcRes.append({"Incentive ID" : taxRebate,"Result" : IRA_179D_res})
            elif taxRebate == "USA_FED_0002":
                IRA_ITC_res = rebateFunctions.IRA_ITC(buildingArea)
                print(IRA_ITC_res)
                TaxresultDF.loc[TaxresultDF['Incentive_ID'] == taxRebate, 'Amount Estimation'] = \
                                                            "$" + str(IRA_ITC_res[1]["Amount"])
                taxCalcRes.append({"Incentive ID" : taxRebate,"Result" : IRA_ITC_res})
            elif taxRebate == "USA_FED_0003":
                IRA_PTC_res = rebateFunctions.IRA_PTC(buildingArea)
                TaxresultDF.loc[TaxresultDF['Incentive_ID'] == taxRebate, 'Amount Estimation'] = \
                                                            "$" + str(IRA_PTC_res[1]["Amount"])
                taxCalcRes.append({"Incentive ID" : taxRebate,"Result" : IRA_PTC_res})
        else:
            TaxresultDF.loc[TaxresultDF['Incentive_ID'] == taxRebate, 'Amount Estimation'] = "Variable Amount"

    result_dict = {
        "status" : 200,
        "Tax_DF" : json.loads(TaxresultDF.to_json(orient="records")),
        "Tax_Rebate_Calc_List" : taxCalcRes,
    }
    return result_dict

@app.get('/discounts')
async def getDiscount(userIncID: str):
    global discountTable
    discountData = Nexus_DB_Path_Discount_db.copy()
    # For SGIP -> Jurisdiction - State, and State -> CA
    discountTable = discountData[((discountData["Jurisdiction"] == "State") & (discountData["State"] == userState))]
    utilityData  = discountData[(discountData["Incentive_ID"] == userIncID)]
    discountUTPResult = discountFunctions.getDiscountResult(utilityData, buildingArea)
    return json.loads(discountUTPResult.to_json(orient="records"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
