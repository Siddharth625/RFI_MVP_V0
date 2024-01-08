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

    if (response?.data.length > 0) {
      const highLevelView = await axios.get(
        "http://localhost:8000/high_level_view"
      );
      console.log("highLevelView", highLevelView);
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
          Federal: "$56,000",
        },
        {
          State: "$56,000",
        },
        {
          Local: "$56,000",
        },
      ],
      // amount: "$ 56,000",
    },
  ];

  const HIGH_LEVEL_VIEW = {
    headers: [
      "Technology",
      "Subtechnology",
      "Maximum Amount",
      "Upfront Cost",
      "Details",
      "Payback Period",
    ],
    rowData: [
      {
        technology: "HVAC",
        subtechnology: ["Sub Tech1", "Sub Tech2"],
        amount: "$ 14,000",
      },
      {
        technology: "Solar Panel",
        subtechnology: ["Sub Tech1", "Sub Tech2"],
        amount: "$ 56,000",
      },
      {
        technology: "Controls",
        subtechnology: ["Sub Tech1", "Sub Tech2"],
        title: [
          {
            Federal: "$56,000",
          },
          {
            State: "$56,000",
          },
          {
            Local: "$56,000",
          },
        ],
        // amount: "$ 56,000",
      },
    ],
  };

  const fetchHighLevelView = async () => {
    // const response = await axios?.get("/highlevelview");
    // setViewData(response?.data);
  };

  useEffect(() => {
    fetchHighLevelView();
  }, []);

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
                {HIGH_LEVEL_VIEW?.headers?.map((headerData) => {
                  return (
                    <th style={{ width: "300px" }}>
                      <Alignment>{headerData}</Alignment>
                    </th>
                  );
                })}
              </tr>

              {HIGH_LEVEL_VIEW?.rowData?.map((data, index) => {
                return (
                  <tr style={{ position: "relative", left: "70px" }}>
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
                          <div style={{ fontWeight: "300" }}>
                            {data?.technology?.split(", ")?.[1]}
                          </div>
                        </Alignment>
                      </LayoutBox>
                    </td>
                    <td>
                      <LayoutBox>
                        {data?.subtechnology?.[0]}
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
                      {toggle && index === clickedIndex
                        ? data?.subtechnology?.map((data, index) => {
                            return <Alignment>{data}</Alignment>;
                          })
                        : null}
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
