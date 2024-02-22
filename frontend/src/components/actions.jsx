import React from "react";
import IconButton from "@mui/material/IconButton";
import DeleteIcon from "@mui/icons-material/Delete";
import EditIcon from "@mui/icons-material/Edit";
import { Typography } from "@mui/material";

export default function Actions() {
  // Create an array with 13 elements to represent the 13 rows
  const rows = new Array(13).fill(null);

  return (
    <Typography
      component="div"
      sx={{
        boxShadow: "0px 2px 8px rgba(0, 0, 0, 0.32)",
        background: "white",
        width: "100%",
      }}
    >
      <Typography sx={{ textAlign: "center" }}>Actions</Typography>
      {rows?.map((row, rowIndex) => (
        <div
          key={rowIndex}
          style={{
            display: "flex",
            alignItems: "center",
          }}
        >
          <IconButton
            onClick={() => {
              // Handle edit button click for this row
              // console.log("Edit button clicked for row", rowIndex);
            }}
          >
            <EditIcon />
          </IconButton>
          <IconButton
            onClick={() => {
              // Handle delete button click for this row
              // console.log("Delete button clicked for row", rowIndex);
            }}
          >
            <DeleteIcon />
          </IconButton>
        </div>
      ))}
    </Typography>
  );
}
