import React from "react";
import { useTheme } from "@mui/material/styles";

export default function DefaultAnchor({ sx, children, ...rest }) {
  const theme = useTheme();

  return (
    <a
      {...rest}
      style={{
        color: "green",
        // fontWeight: "bold",
        textDecoration: "underline",
        ...sx,
      }}
    >
      {children}
    </a>
  );
}
