import React from "react";
import { SmallText } from "../styled";
import {
  IconContainer,
  IconLabel,
  InputWrapper,
  StyledInput,
  UnitContainer,
} from "../styled";
// import { CiCircleInfo } from "react-icons/ci";

const InputComponent = ({
  handleInputChange,
  name,
  label,
  icon,
  unit,
  value,
  type,
}) => {
  return (
    <>
      <div style={{ display: "flex", gap: "10px", marginBottom: "8px" }}>
        <IconLabel style={{ color: "#343541", opacity: "0.6" }}>
          {label}
        </IconLabel>
        {/* <>
          <CiCircleInfo style={{ position: "relative", bottom: "1px" }} />
        </> */}
      </div>
      <InputWrapper>
        <IconContainer>{icon}</IconContainer>
        <StyledInput
          type={type ?? "text"}
          onChange={(e) => {
            handleInputChange(e.target.value, name);
          }}
          value={value}
        />
      </InputWrapper>
    </>
  );
};

export default InputComponent;
