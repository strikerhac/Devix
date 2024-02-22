import React, { useState, useEffect, useRef } from "react";
import { Button } from "@mui/material";
import { useTheme, styled } from "@mui/material/styles";
import { Icon } from "@iconify/react";
import { CheckBox } from "@mui/icons-material";
import { getTitle } from "../utils/helpers";

export default function DefaultBarChart({
  sx,
  handleClick,
  children,
  ...rest
}) {
  const theme = useTheme();
  return (
    <Button
      sx={{
        display: "flex",
        alignItems: "center",
        height: "30px",
        gap: "10px",
        padding: "5px 12px",
        "&:hover": {
          backgroundColor: sx?.backgroundColor,
          opacity: 0.8,
        },
        ...sx,
      }}
      onClick={handleClick}
      {...rest}
    >
      {children}
    </Button>
  );
}
