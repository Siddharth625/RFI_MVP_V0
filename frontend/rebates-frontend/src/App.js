import React, { useEffect, useState } from "react";
import "./App.css";
import { Alignment, Button, Header, LayoutBox } from "./styled";
import SelectComponent from "./component/SelectComponent";
import InputComponent from "./component/InputComponent";
import axios from "axios";

function App() {
  const [inputValue, setInputValue] = useState({
    zipcode: null,
    utility: "",
    building_area: null,
  });

  let rowData = [];
  const [highLevelView, setHighLevelView] = useState([]);
  const [toggle, setToggle] = useState(false);
  const [clickedIndex, setClickedIndex] = useState(null);
  const handleInputChange = (value, name) => {
    console.log("nane", name, value);
    setInputValue((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const [viewData, setViewData] = useState();
  const [source, setSource] = useState([]);

  const postUtilityData = async () => {
    const response = await axios.post("http://localhost:8000/get_user_info", {
      utility: inputValue?.utility,
      city: "NY",
      state: "NY",
      county: "NY",
      country: "USA",
      zipcode: inputValue?.zipcode,
      building_area: parseFloat(inputValue?.building_area),
    });

    if (response?.data) {
      let jurisdiction = 0;
      let stateSum = 0;
      let localSum = 0;
      const sourceRebate = response?.data?.map((data) => {
        console.log("dataFromSource", data);
        if (data?.Jurisdiction.toLowerCase() === "federal") {
          jurisdiction = jurisdiction + data?.Amt_Estimation;
        } else if (data?.Jurisdiction.toLowerCase() === "state") {
          stateSum = stateSum + data?.Amt_Estimation;
        } else if (data?.Jurisdiction.toLowerCase() === "utility") {
          localSum = localSum + data?.Amt_Estimation;
        }
        return;
      });
      let updatedJurisdiction = Math.round(jurisdiction * 100) / 100;
      let updatedStateSum = Math.round(stateSum * 100) / 100;
      let updatedLocalSum = Math.round(localSum * 100) / 100;
      setSource({
        updatedJurisdiction,
        updatedStateSum,
        updatedLocalSum,
      });
      const highLevelView = await axios.get(
        "http://localhost:8000/high_level_view"
      );
      console.log("highLevelView", highLevelView);

      Object.entries(highLevelView?.data?.data).map(([key, value], index) => {
        let subtechnologyArray = [];
        let sum = 0;
        Object.values(value)?.map((data) => {
          sum = sum + data?.[0]?.median;
        });
        Object.values(value)?.map((data, index) => {
          console.log("subet", data);
          subtechnologyArray?.push({
            technology: data?.[0]?.["Sub-Technology"],
            amount: Math.round(data?.[0]?.median * 100) / 100,
          });
        });
        console.log("keyss", key, value);
        console.log("subtech", subtechnologyArray);

        rowData?.push({
          technology: key,
          subtechnology: subtechnologyArray,
          amount: Math.round(sum * 100) / 100,
        });
        console.log("rowData", rowData);
      });
      setHighLevelView({
        headers: ["Technology", "Subtechnology", "Maximum Amount"],
        rowData,
      });
    }

    console.log("data", response);
  };

  const SUMMARY = [
    {
      name: "Upfront discounts",
      amount: "$ 14,000",
    },
    {
      name: "Tax Incentives",
      amount: "$ 56,000",
    },
    {
      name: "Breakdown by source",
      title: [
        {
          Federal: `$ ${source?.updatedJurisdiction}`,
        },
        {
          State: `$ ${source?.updatedStateSum}`,
        },
        {
          Local: `$ ${source?.updatedLocalSum}`,
        },
      ],
      // amount: "$ 56,000",
    },
  ];

  const updatedTechnology = {
    Controls: {
      "Building Controls": [
        {
          Technology: "Controls",
          "Sub-Technology": "Building Controls",
          median: 405,
        },
      ],
      Controls: [
        {
          Technology: "Controls",
          "Sub-Technology": "Controls",
          median: 10000,
        },
      ],
    },
    "Custom Program": {
      Lighting: [
        {
          Technology: "Custom Program",
          "Sub-Technology": "Lighting",
          median: 189,
        },
      ],
    },
    HVAC: {
      "Air Compressor": [
        {
          Technology: "HVAC",
          "Sub-Technology": "Air Compressor",
          median: 225,
        },
      ],
      "Air Conditioners": [
        {
          Technology: "HVAC",
          "Sub-Technology": "Air Conditioners",
          median: 211.3125,
        },
      ],
      HVAC: [
        {
          Technology: "HVAC",
          "Sub-Technology": "HVAC",
          median: 6410,
        },
      ],
      "HVAC Controls": [
        {
          Technology: "HVAC",
          "Sub-Technology": "HVAC Controls",
          median: 150,
        },
      ],
      "Heat Pump": [
        {
          Technology: "HVAC",
          "Sub-Technology": "Heat Pump",
          median: 1102.679325,
        },
      ],
      Heaters: [
        {
          Technology: "HVAC",
          "Sub-Technology": "Heaters",
          median: 57.0351375,
        },
      ],
      "Pumps & Motors": [
        {
          Technology: "HVAC",
          "Sub-Technology": "Pumps & Motors",
          median: 180,
        },
      ],
    },
    Insulation: {
      Envelope: [
        {
          Technology: "Insulation",
          "Sub-Technology": "Envelope",
          median: 734.4,
        },
      ],
      Insulation: [
        {
          Technology: "Insulation",
          "Sub-Technology": "Insulation",
          median: 6410,
        },
      ],
      Pipe: [
        {
          Technology: "Insulation",
          "Sub-Technology": "Pipe",
          median: 314.6721426447,
        },
      ],
    },
    "LED Lighting": {
      Downlights: [
        {
          Technology: "LED Lighting",
          "Sub-Technology": "Downlights",
          median: 500,
        },
      ],
      Exterior: [
        {
          Technology: "LED Lighting",
          "Sub-Technology": "Exterior",
          median: 306,
        },
      ],
      Interior: [
        {
          Technology: "LED Lighting",
          "Sub-Technology": "Interior",
          median: 400,
        },
      ],
      "LED Controls": [
        {
          Technology: "LED Lighting",
          "Sub-Technology": "LED Controls",
          median: 3.41796875,
        },
      ],
      "LED Lighting": [
        {
          Technology: "LED Lighting",
          "Sub-Technology": "LED Lighting",
          median: 6410,
        },
      ],
      Lamps: [
        {
          Technology: "LED Lighting",
          "Sub-Technology": "Lamps",
          median: 344.25,
        },
      ],
      Troffers: [
        {
          Technology: "LED Lighting",
          "Sub-Technology": "Troffers",
          median: 286.875,
        },
      ],
    },
    Solar: {
      Solar: [
        {
          Technology: "Solar",
          "Sub-Technology": "Solar",
          median: 10000,
        },
      ],
    },
  };

  return (
    <Alignment style={{ padding: "32px" }}>
      <Header>
        <LayoutBox
          justifyContent="center"
          alignItems="center"
          style={{ padding: "10px" }}
        >
          Rebates and Incentives
        </LayoutBox>
      </Header>
      <Alignment style={{ border: "1px solid black", padding: "32px" }}>
        <Alignment justifyContent="space-evenly" style={{ gap: "24px" }}>
          <Alignment margin="16px 0px">
            <InputComponent
              handleInputChange={handleInputChange}
              name="zipcode"
              label="Zipcode"
              // icon={<FiLayers />}
              value={inputValue?.zipcode}
              type="number"
            />
          </Alignment>
          <Alignment padding="0px 0px 24px">
            <InputComponent
              handleInputChange={handleInputChange}
              name="building_area"
              label="Building Area"
              // icon={<FiLayers />}
              // unit="sq.ft."
              value={inputValue?.building_area}
              type="number"
            />
          </Alignment>
        </Alignment>
        <Alignment
          justifyContent="center"
          alignItems="center"
          style={{ gap: "12px" }}
        >
          <Alignment padding="0px 0px 24px">
            <InputComponent
              handleInputChange={handleInputChange}
              name="utility"
              label="Utility"
              // icon={<FiLayers />}
              // unit="sq.ft."
              value={inputValue?.utility}
              type="text"
            />
          </Alignment>
          <Button
            onClick={() => {
              postUtilityData();
            }}
            style={{
              margin: "24px 0px 0px 0px",
              cursor: "pointer",
              width: "70px",
            }}
          >
            Calculate
          </Button>
        </Alignment>
      </Alignment>
      <Alignment>
        <Header>
          <LayoutBox
            justifyContent="center"
            alignItems="center"
            style={{ padding: "10px" }}
          >
            Summary
          </LayoutBox>
        </Header>
        <Alignment style={{ border: "1px solid black", padding: "24px" }}>
          <LayoutBox justifyContent="space-evenly" alignItems="center">
            {SUMMARY?.map((data, index) => {
              return (
                <>
                  <LayoutBox
                    style={{
                      gap: "24px",
                      marginTop: index === SUMMARY?.length - 1 ? "14px" : "0px",
                    }}
                  >
                    <Alignment
                      style={{
                        background: "#ffbf00",
                        height: "90px",
                        width: "10px",
                      }}
                    ></Alignment>
                    <Alignment>
                      {data.name}
                      <Alignment>{data.amount}</Alignment>
                      <Alignment style={{ margin: "20px 0px 0px" }}>
                        <LayoutBox style={{ gap: "24px" }}>
                          {data?.title?.map((item, index) => {
                            return (
                              <div>
                                <Alignment>{Object?.keys(item)?.[0]}</Alignment>
                                <Alignment>
                                  {Object?.values(item)?.[0]}
                                </Alignment>
                              </div>
                            );
                          })}
                        </LayoutBox>
                      </Alignment>
                    </Alignment>
                  </LayoutBox>
                </>
              );
            })}
          </LayoutBox>
        </Alignment>
        <Alignment style={{ border: "1px solid black", padding: "24px" }}>
          <Alignment padding="0px 32px">
            <table>
              <tr>
                {highLevelView?.headers?.map((headerData) => {
                  return (
                    <th style={{ width: "400px" }}>
                      <Alignment>
                        {!toggle && headerData !== "Subtechnology"
                          ? headerData
                          : toggle
                          ? headerData
                          : null}
                      </Alignment>
                    </th>
                  );
                })}
              </tr>

              {highLevelView?.rowData?.map((data, index) => {
                return (
                  <tr style={{ position: "relative", left: "155px" }}>
                    <td style={{ padding: "19px 0px" }}>
                      <LayoutBox style={{ gap: "24px" }}>
                        <Alignment style={{ position: "relative" }}>
                          <div
                            style={{
                              fontSize: "16px",
                              lineHeight: "20.85px",
                              margin: "0px 0px -14px",
                              fontWeight: "600",
                              display: "flex",
                              gap: "4px",
                              alignItems: "center",
                            }}
                          >
                            {data?.technology?.split(", ")?.[0]}
                          </div>
                          <br />
                          {/* <div style={{ fontWeight: "300" }}>
                            {data?.technology?.split(", ")?.[1]}
                          </div> */}
                        </Alignment>
                        {toggle && index === clickedIndex ? (
                          <Alignment
                            style={{ cursor: "pointer" }}
                            onClick={() => {
                              setToggle(!toggle);
                              setClickedIndex(index);
                            }}
                          >
                            &uarr;
                          </Alignment>
                        ) : (
                          <Alignment
                            style={{ cursor: "pointer" }}
                            onClick={() => {
                              setToggle(!toggle);
                              setClickedIndex(index);
                            }}
                          >
                            &darr;
                          </Alignment>
                        )}
                      </LayoutBox>
                    </td>
                    {toggle ? (
                      <td>
                        {/* <LayoutBox>{data?.subtechnology?.[0]}</LayoutBox> */}
                        {toggle && index === clickedIndex
                          ? data?.subtechnology?.map((data, index) => {
                              return (
                                <Alignment
                                  style={{
                                    marginBottom: "15px",
                                    position: "relative",
                                    right: "14px",
                                  }}
                                >
                                  {data?.technology + ": " + "$" + data?.amount}
                                </Alignment>
                              );
                            })
                          : null}
                      </td>
                    ) : (
                      <Alignment style={{ width: "100px" }}></Alignment>
                    )}
                    <td style={{ padding: "19px 0px" }}>
                      <LayoutBox style={{ gap: "24px" }}>
                        <Alignment
                          style={{ position: "relative", right: "20px" }}
                        >
                          <div
                            style={{
                              fontSize: "16px",
                              lineHeight: "20.85px",
                              margin: "0px 0px -14px",
                              fontWeight: "600",
                              display: "flex",
                              gap: "4px",
                              alignItems: "center",
                            }}
                          >
                            {"$" + data?.amount}
                          </div>
                          <br />
                        </Alignment>
                      </LayoutBox>
                    </td>
                  </tr>
                );
              })}
            </table>
          </Alignment>
        </Alignment>
      </Alignment>
    </Alignment>
  );
}

export default App;
