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
amountAggregation = {
    'Tax_Total' : 0,
    'Discount_Total' : 0,
    'Solar_Total' : 0,
    'HVAC_Total' : 0,
    'Insulation_Total' : 0,
    'Control_Total' : 0,
    'Lighting_Total' : 0, 
}


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
    global amountAggregation
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
                amountAggregation["Tax_Total"] = amountAggregation["Tax_Total"] + IRA_179D_res[0]["Bonus Deduction"]
                amountAggregation["HVAC_Total"] = amountAggregation["HVAC_Total"] + (IRA_179D_res[0]["Bonus Deduction"])/3
                amountAggregation["Insulation_Total"] = amountAggregation["Insulation_Total"] + (IRA_179D_res[0]["Bonus Deduction"])/3
                amountAggregation["Lighting_Total"] = amountAggregation["Lighting_Total"] + (IRA_179D_res[0]["Bonus Deduction"])/3
                TaxresultDF.loc[TaxresultDF['Incentive_ID'] == taxRebate, 'Amount Estimation'] = \
                                                            "$" + \
                                                            str(IRA_179D_res[0]["Base Deduction"]) + \
                                                            " - " + \
                                                            "$" + \
                                                            str(IRA_179D_res[0]["Bonus Deduction"])
                taxCalcRes.append({"Incentive ID" : taxRebate,"Result" : IRA_179D_res})
            elif taxRebate == "USA_FED_0002":
                IRA_ITC_res = rebateFunctions.IRA_ITC(buildingArea)
                amountAggregation["Tax_Total"] = amountAggregation["Tax_Total"] + IRA_ITC_res[1]["Amount"]
                amountAggregation["Solar_Total"] = amountAggregation["Solar_Total"] + IRA_ITC_res[1]["Amount"]
                print(IRA_ITC_res)
                TaxresultDF.loc[TaxresultDF['Incentive_ID'] == taxRebate, 'Amount Estimation'] = \
                                                            "$" + str(IRA_ITC_res[1]["Amount"])
                taxCalcRes.append({"Incentive ID" : taxRebate,"Result" : IRA_ITC_res})
            elif taxRebate == "USA_FED_0003":
                IRA_PTC_res = rebateFunctions.IRA_PTC(buildingArea)
                amountAggregation["Tax_Total"] = amountAggregation["Tax_Total"] + IRA_PTC_res[1]["Amount"]
                amountAggregation["Solar_Total"] = amountAggregation["Solar_Total"] + IRA_PTC_res[1]["Amount"]
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
    print(amountAggregation)
    return result_dict

@app.get('/discounts')
async def getDiscount(userIncID: str):
    global discountTable
    global amountAggregation
    discountData = Nexus_DB_Path_Discount_db.copy()
    # For SGIP -> Jurisdiction - State, and State -> CA
    discountTable = discountData[((discountData["Jurisdiction"] == "State") & (discountData["State"] == userState))]
    utilityData  = discountData[(discountData["Incentive_ID"] == userIncID)]
    discountUTPResult = discountFunctions.getDiscountResult(utilityData, buildingArea)
    tech_list = discountUTPResult["Technology"].unique()
    tech_subtech_list = {}
    for tech in tech_list:
        tech_subtech_list[tech] = list(discountUTPResult[discountUTPResult["Technology"] == tech]["Sub-Technology"].unique())
    print(tech_subtech_list)
    techTotalGrpByAVG = discountUTPResult.groupby(['Technology','Sub-Technology'])

    tech_subtech_agg = {}
    for tech, subtech_list in tech_subtech_list.items():
        for subtech in subtech_list:
            tech_subtech_agg[tech + "," +subtech] = techTotalGrpByAVG.get_group((tech,subtech)).agg({'Amt_Estimation':'mean'})
    print(tech_subtech_agg)
    discount_agg = {
        "HVAC" : 0,
        "Control" : 0,
        "Lighting" : 0,
        "Insulation" : 0
    }
    for key, value in tech_subtech_agg.items():
        if 'HVAC' in key:
            discount_agg["HVAC"] += value['Amt_Estimation']
        if 'CONTROL' in key:
            discount_agg["Control"] += value['Amt_Estimation']
    print(discount_agg)
    amountAggregation["HVAC_Total"] += discount_agg["HVAC"]
    amountAggregation["Control_Total"] += discount_agg["Control"]
    amountAggregation["Lighting_Total"] += discount_agg["Lighting"]
    amountAggregation["Insulation_Total"] += discount_agg["Insulation"]
    amountAggregation["Discount_Total"] += discount_agg["HVAC"] + \
                                           discount_agg["Control"] + \
                                           discount_agg["Lighting"]+ \
                                           discount_agg["Insulation"]
    amountAggregation["Total Amount"] = amountAggregation["Tax_Total"] + amountAggregation["Discount_Total"]
    print(amountAggregation)
    return {
        "DiscountUTPtable" : json.loads(discountUTPResult.to_json(orient="records"))
    }

@app.get('/totalamt')
async def getTotalSavings():
    global amountAggregation
    return amountAggregation


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
