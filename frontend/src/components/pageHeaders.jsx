import React from "react";
import { useTheme } from "@mui/material/styles";
import { Typography } from "@mui/material";
import useButtonGenerator from "../hooks/useButtonGenerator";

export default function DefaultPageHeader({ pageName, buttons }) {
  const theme = useTheme();
  const buttonGenerator = useButtonGenerator();

  return (
    <div style={{ padding: "10px" }}>
      <Typography
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <Typography sx={{ color: theme?.palette?.page_header?.primary_text }}>
          {pageName}
        </Typography>

        <Typography
          sx={{
            display: "flex",
            alignItems: "center",
            gap: "10px",
          }}
        >
          {buttons.map((button, index) => {
            return buttonGenerator(button, index);
          })}
        </Typography>
      </Typography>
    </div>
  );
}

export function CardHeader({ cardName }) {
  const theme = useTheme();

  return (
    <div style={{ padding: "10px" }}>
      <Typography sx={{ color: theme?.palette?.page_header?.primary_text }}>
        {cardName}
      </Typography>
    </div>
  );
}
