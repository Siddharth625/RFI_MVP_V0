/* eslint-disable no-undef */
import React from "react";

import { MenuItem, Select } from "@mui/material";
import { Alignment, IconLabel } from "../styled";
// import { CiCircleInfo } from "react-icons/ci";

const SelectComponent = ({
  Options,
  label,
  handleInputChange,
  icon,
  placeholder,
  name,
  value,
}) => {
  return (
    <>
      <div
        style={{
          display: "flex",
          gap: "6px",
          marginBottom: "8px",
          width: "249px",
        }}
      >
        <IconLabel style={{ color: "#343541", opacity: "0.6" }}>
          {label}
        </IconLabel>
      </div>
      <Alignment style={{ position: "relative" }}>
        <Alignment style={{ position: "absolute", top: "9px", left: "16px" }}>
          {icon}
        </Alignment>
        <Select
          value={value}
          onChange={(selected) => {
            handleInputChange(selected.target.value, name);
          }}
          displayEmpty
          sx={{
            borderRadius: "4px",
            // width: "298px",
            padding: "0px",
            height: "54px",
          }}
          fullWidth
          inputProps={{ "aria-label": "Without label" }}
          renderValue={(selected) => {
            if (selected?.length === 0) {
              return <div style={{ opacity: 0.8 }}>{placeholder}</div>;
            }
            return selected;
          }}
        >
          {Options?.map((option, index) => {
            return <MenuItem value={option?.value}>{option?.name}</MenuItem>;
          })}
        </Select>
      </Alignment>
    </>
  );
};

export default SelectComponent;
