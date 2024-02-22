import React from "react";
import { DatePicker } from "antd";
import { useTheme, styled } from "@mui/material/styles";

export default function DefaultDate({ field, sx, children, ...rest }) {
  const theme = useTheme();

  return (
    <DatePicker
      {...field}
      style={{
        color: theme?.palette?.default_option?.primary_text,
        backgroundColor: theme?.palette?.default_option?.background,
        border: `2px solid ${theme?.palette?.default_option?.border}`,
        borderRadius: "5px",
        width: "100%",
        boxShadow: "none",
        ...sx,
      }}
      {...rest}
    />
  );
}
