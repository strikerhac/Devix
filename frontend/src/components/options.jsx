import React from "react";
import { useTheme } from "@mui/material/styles";

export default function DefaultOption({ value, sx, children, ...rest }) {
  const theme = useTheme();

  return (
    <option
      style={{
        color: theme?.palette?.default_option?.primary_text,
        backgroundColor: theme?.palette?.default_option?.background,
        borderColor: theme?.palette?.default_option?.border,
        ...sx,
      }}
      {...rest}
      value={value}
    >
      {children}
    </option>
  );
}
