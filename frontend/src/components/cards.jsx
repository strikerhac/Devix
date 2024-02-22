import React from "react";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import { useTheme } from "@mui/material/styles";

export default function DefaultCard({ sx, children }) {
  const theme = useTheme();

  return (
    <div
      style={{
        // position: "relative",
        // boxShadow:
        //   "0 10px 10px -3px rgba(46, 41, 51, 0.08), 0 4px 6px -2px rgba(71, 63, 79, 0.16)",
        boxShadow: "rgba(99, 99, 99, 0.2) 0px 2px 2px 0px",
        backgroundColor: theme?.palette?.default_card?.background,
        borderRadius: "7px",
        ...sx,
      }}
    >
      <CardContent style={{ padding: "0px" }}>{children}</CardContent>
    </div>
  );
}
