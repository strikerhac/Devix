import React from "react";
import { useTheme, styled } from "@mui/material/styles";

export default function DefaultSelect({ field, sx, children, ...rest }) {
  const theme = useTheme();

  return (
    <select
      {...field}
      style={{
        color: theme?.palette?.default_option?.primary_text,
        backgroundColor: theme?.palette?.default_option?.background,
        border: `2px solid ${theme?.palette?.default_option?.border}`,
        borderRadius: "5px",
        padding: "7px 10px",
        width: "100%",
        outline: "none",
        ...sx,
      }}
      {...rest}
    >
      {children}
    </select>
  );
}

export function AddableSelect({ field, sx, onAddClick, children, ...rest }) {
  const theme = useTheme();

  const StyledActionDiv = styled("div")(({ theme, sx }) => ({
    color: theme?.palette?.default_option?.primary_text,
    backgroundColor: theme?.palette?.default_option?.background,
    border: `2px solid ${theme?.palette?.default_option?.border}`,
    borderRadius: "0px 5px 5px 0px",
    width: "30px",
    textAlign: "center",
    cursor: "pointer",
    paddingTop: "2px",
    "&:hover": {
      color: `${theme?.palette?.horizontal_menu?.secondary_text} !important`,
      borderBottom: `3px solid ${theme?.palette?.horizontal_menu?.secondary_text} !important`,
      backgroundColor: `${theme?.palette?.default_option?.background} !important`,
    },
  }));

  return (
    <>
      <select
        {...field}
        style={{
          color: theme?.palette?.default_option?.primary_text,
          backgroundColor: theme?.palette?.default_option?.background,
          border: `2px solid ${theme?.palette?.default_option?.border}`,
          borderRadius: "5px 0px 0px 5px",
          borderRight: "none",
          padding: "7px 10px",
          width: "100%",
          ...sx,
        }}
        {...rest}
      >
        {children}
      </select>
      <StyledActionDiv onClick={onAddClick}>+</StyledActionDiv>
    </>
  );
}
