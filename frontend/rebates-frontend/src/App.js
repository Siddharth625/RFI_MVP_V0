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

  const [source, setSource] = useState([]);
  const [programView, setProgramView] = useState([]);

  const PROGRAM_ESTIMATION= {
    "('Amt_Estimation', 'median')" : 'amount_estimation',
    "('Incentive Name', '')" : 'incentive_name',
    "('Provider', '')" : 'provider',
    "('Technology', '')" : 'technology',
    "('Website Link', '')" : 'link',
  };

  const postUtilityData = async () => {
    const response = await axios.post("http://localhost:8080/get_user_info", {
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
      let discount = 0;
      let nonDiscount = 0;
      const sourceRebate = response?.data?.map((data) => {
        if (data?.Jurisdiction.toLowerCase() === "federal") {
          jurisdiction = jurisdiction + data?.Amt_Estimation;
        } else if (data?.Jurisdiction.toLowerCase() === "state") {
          stateSum = stateSum + data?.Amt_Estimation;
        } else if (data?.Jurisdiction.toLowerCase() === "utility") {
          localSum = localSum + data?.Amt_Estimation;
        }
        if (data?.["Incentive Type"].toLowerCase() === "discount") {
          discount = discount + data?.Amt_Estimation;
        } else {
          nonDiscount = nonDiscount + data?.Amt_Estimation;
        }
        return;
      });
      let updatedJurisdiction = Math.round(jurisdiction * 100) / 100;
      let updatedStateSum = Math.round(stateSum * 100) / 100;
      let updatedLocalSum = Math.round(localSum * 100) / 100;
      let updatedDiscount = Math.round(discount * 100) / 100;
      let updatedNonDiscount = Math.round(nonDiscount * 100) / 100;

      setSource({
        updatedJurisdiction,
        updatedStateSum,
        updatedLocalSum,
        updatedDiscount,
        updatedNonDiscount,
      });

      const highLevelView = await axios.get(
        "http://localhost:8080/high_level_view"
      );
      const lowlevelview = await axios.get(
        "http://localhost:8080/low_level_view"
      );

      let programStructure = {};
        let programDetailsArray = [];
        console.log("low level", lowlevelview?.data, highLevelView?.data);
      Object.entries(lowlevelview?.data?.data)?.map(([key, value], _) => {
       
        Object.entries(value)?.map(([program, provider])=>{
        let programs = [];
        let programDetails = {};
          Object?.entries(Object.values(provider)?.[0]?.Link?.[0])?.map(([key, value])=>{
            programDetails = {...programDetails, [PROGRAM_ESTIMATION?.[key]]:value}
          })
          Object.keys(value)?.map((childKey, _) => {
            programs?.push({program: childKey, programDetails});
          });

          programDetailsArray?.push(programDetails);
            programStructure = { ...programStructure, [key]: programs };
        })
        
      });

      console.log("programDetails22", programDetailsArray, programStructure);
      Object.entries(highLevelView?.data?.data).map(([key, value], index) => {
        let subtechnologyArray = [];
        let sum = 0;
        Object.values(value)?.map((data) => {
          sum = sum + data?.[0]?.median;
        });
        Object.values(value)?.map((data, index) => {
          subtechnologyArray?.push({
            technology: data?.[0]?.["Sub-Technology"],
            amount: Math.round(data?.[0]?.median * 100) / 100,
          });
        });

        rowData?.push({
          technology: key,
          subtechnology: subtechnologyArray,
          amount: Math.round(sum * 100) / 100,
          program: programStructure?.[key],
        });
      });

      setHighLevelView({
        headers: ["Technology", "Subtechnology", "Maximum Amount"],
        rowData,
      });
    }
  };

  console.log("high level view", highLevelView)
  const SUMMARY = [
    {
      name: "Upfront discounts",
      amount: `$ ${source?.updatedDiscount}`,
    },
    {
      name: "Tax Incentives",
      amount: `$ ${source?.updatedNonDiscount}`,
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

  const program = {
    Controls: {
      "Central Air Conditioner program": {
        "Central Hudson": {
          Link: [
            {
              "('Technology', '')": "Controls",
              "('Incentive Name', '')": "Central Air Conditioner program",
              "('Provider', '')": "Central Hudson",
              "('Website Link', '')": "Link",
              "('Estimated Incentive Value', 'median')": 200.0,
            },
          ],
        },
      },
      "Commercial and Industrial Energy Efficiency Program": {
        ConEd: {
          Link: [
            {
              "('Technology', '')": "Controls",
              "('Incentive Name', '')":
                "Commercial and Industrial Energy Efficiency Program",
              "('Provider', '')": "ConEd",
              "('Website Link', '')": "Link",
              "('Estimated Incentive Value', 'median')": 607.5,
            },
          ],
        },
      },
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

      <Alignment
        style={{
          border: "1px solid black",
          padding: "32px",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          flexDirection: "column",
        }}
      >
        <Alignment
          style={{
            gap: "24px",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
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
                      <strong>{data.name}</strong>

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
                          : programView
                          ? "SubProgram"
                          : null}
                      </Alignment>
                    </th>
                  );
                })}
              </tr>

              {highLevelView?.rowData?.map((data, index) => {
                console.log("data121",data);
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
                        <Alignment>
                          <button
                            onClick={() => {
                              setProgramView(!programView);
                              setClickedIndex(index);
                              if (programView) {
                                setToggle(false);
                              }
                            }}
                          >
                            Program
                          </button>
                        </Alignment>
                      </LayoutBox>
                    </td>
                    {toggle || program ? (
                      <td>
                        {/* <LayoutBox>{data?.subtechnology?.[0]}</LayoutBox> */}
                        {toggle && index === clickedIndex
                          ? data?.subtechnology?.map((item, index) => {
                              return (
                                <Alignment
                                  style={{
                                    marginBottom: "15px",
                                    position: "relative",
                                    right: "14px",
                                  }}
                                >
                                  {item?.technology + ": " + "$" + item?.amount}
                                </Alignment>
                              );
                            })
                          : programView && index === clickedIndex
                          ? data?.program?.map((programData, index) => {
                                          console.log("pro121", programData);
                              return (
                                <Alignment
                                  style={{
                                    marginBottom: "15px",
                                    position: "relative",
                                    right: "14px",
                                  }}
                                >
                                  {programData?.program + " | " + programData?.programDetails?.provider + " | " + programData?.programDetails?.amount_estimation + " | " }
                                  <a href={programData?.programDetails?.link}>Apply</a>
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
                          <div></div>
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
