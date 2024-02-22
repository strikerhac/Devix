import React from "react";
import MenuItem from "./menuItem";
import "./main.css";
import { useTheme, styled } from "@mui/material/styles";

const Dropdown = ({
  submenus,
  dropdown,
  depthLevel,
  menuPath,
  handleAddMenuPath,
  handleRemoveMenuPath,
  selectedMenuPath,
  setSelectedMenuPath,
}) => {
  depthLevel = depthLevel + 1;
  const dropdownClass = depthLevel > 1 ? "dropdown-submenu" : "";

  const StyledUL = styled("ul")(({ theme, sx }) => ({
    position: "absolute",
    left: 0,
    left: "auto",
    boxShadow:
      "0 10px 15px -3px rgba(46, 41, 51, 0.08), 0 4px 6px -2px rgba(71, 63, 79, 0.16)",
    fontSize: "0.875rem",
    zIndex: "9999",
    minWidth: "10rem",
    padding: "0.5rem 0",
    listStyle: "none",
    backgroundColor: "#fff",
    borderRadius: "0.5rem",
    display: "none",
  }));

  return (
    <ul className={`dropdown ${dropdownClass} ${dropdown ? "show" : ""}`}>
      {submenus.map((submenu, index) => (
        <MenuItem
          item={submenu}
          key={index}
          depthLevel={depthLevel}
          menuPath={menuPath}
          handleAddMenuPath={handleAddMenuPath}
          handleRemoveMenuPath={handleRemoveMenuPath}
          selectedMenuPath={selectedMenuPath}
          setSelectedMenuPath={setSelectedMenuPath}
        />
      ))}
    </ul>
  );
};

export default Dropdown;
