import React, { useState } from "react";
import "./App.css";
import { Alignment, Button, Header, LayoutBox } from "./styled";
import SelectComponent from "./component/SelectComponent";
import InputComponent from "./component/InputComponent";
import axios from "axios";

function App() {
  const [inputValue, setInputValue] = useState({
    zipcode: "",
    utility: "",
    building_area: "",
  });

  const handleInputChange = (value, name) => {
    console.log("nane", name, value);
    setInputValue((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const postUtilityData = async () => {
    const response = await axios.post("/get_user_info", {
      utility: inputValue?.utility,
      zipcode: inputValue?.zipcode,
      building_area: inputValue?.building_area,
    });
    console.log("data", response);
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
        <LayoutBox justifyContent="space-evenly" style={{ gap: "24px" }}>
          <Alignment margin="16px 0px">
            {/* <InputComponent
              handleInputChange={handleInputChange}
              name="householdIncome"
              label="Household Income"
              // icon={<FiLayers />}
              value={inputValue?.householdIncome}
              type="number"
            /> */}
            {/* <SelectComponent
              Options={[
                { name: "City", value: "City" },
                { name: "Area", value: "Area" },
                { name: "Building", value: "Building" },
              ]}
              label="Rent or Own"
              // icon={<GrLocation />}
              name="ownership"
              handleInputChange={handleInputChange}
              value={inputValue?.ownership}
            /> */}
          </Alignment>
          <Alignment margin="16px 0px">
            {/* <SelectComponent
              Options={[
                { name: "City", value: "City" },
                { name: "Area", value: "Area" },
                { name: "Building", value: "Building" },
              ]}
              label="Tax Filing"
              // icon={<GrLocation />}
              name="taxFiling"
              handleInputChange={handleInputChange}
              value={inputValue?.taxFiling}
            /> */}
          </Alignment>
        </LayoutBox>
        <LayoutBox justifyContent="space-evenly" style={{ gap: "24px" }}>
          <Alignment margin="16px 0px">
            {/* <SelectComponent
              Options={[
                { name: "City", value: "City" },
                { name: "Area", value: "Area" },
                { name: "Building", value: "Building" },
              ]}
              label="Household Size"
              // icon={<GrLocation />}
              name="householdSize"
              handleInputChange={handleInputChange}
              value={inputValue?.householdSize}
            /> */}
          </Alignment>
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
        </LayoutBox>
        <LayoutBox
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
            style={{ margin: "24px 0px 0px 0px", cursor: "pointer" }}
          >
            Calculate
          </Button>
        </LayoutBox>
      </Alignment>
    </Alignment>
  );
}

export default App;
