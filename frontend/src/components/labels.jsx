import React from "react";
import { useTheme } from "@mui/material/styles";

export default function DefaultLabel({ required, sx, children, ...rest }) {
  const theme = useTheme();

  return (
    <label
      {...rest}
      style={{
        color: theme?.palette?.default_label?.primary_text,
        fontSize: theme.typography.textSize.small,
        ...sx,
      }}
    >
      {children}{" "}
      {required ? (
        <span style={{ color: theme?.palette?.default_label?.required_star }}>
          *
        </span>
      ) : null}
    </label>
  );
}
