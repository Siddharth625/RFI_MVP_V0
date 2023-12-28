import styled from "styled-components";

export const Alignment = styled.div``;
export const Header = styled.div`
  background: rgba(167, 167, 167, 1);
  height: 40px;
`;
export const InputWrapper = styled.div`
  position: relative;
`;

export const IconContainer = styled.div`
  position: absolute;
  top: 17px;
  left: 19px;
  img {
    width: 18px;
    height: 18px;
  }
`;

export const StyledInput = styled.input`
  padding: 16px;
  border-radius: 4px;
  border: 1px solid black;
  width: 323px;
  //   padding-left: 50px;
  font-size: 16px;
  font-weight: 500;
  height: 24px;
  font-family: "Plus Jakarta Sans", sans-serif;
  &:focus {
    border: 2px solid #1876d1;
    -webkit-transition: 0.5s;
    transition: 0.2s;
    outline: none;
  }

  &::-webkit-outer-spin-button,
  &::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }
`;

export const IconLabel = styled.div`
  font-size: 12px;
  font-family: "Plus Jakarta Sans", sans-serif;
  line-height: 15.64px;
`;

export const LayoutBox = styled.div(({ justifyContent, alignItems }) => ({
  display: "flex",
  justifyContent,
  alignItems,
}));

export const Button = styled.div`
  background: #ffbf00;
  padding: 12px 24px;
  border-radius: 4px;
`;
