import React, { useEffect, useState } from "react";
import { useTheme, styled } from "@mui/material/styles";
import MenuItem from "./menuItem";
import "./main.css";

const Navbar = ({ menuItems, defaultPagePath = [] }) => {
  const depthLevel = 0;
  const [menuPath, setMenuPath] = useState([]);
  const [selectedMenuPath, setSelectedMenuPath] = useState(defaultPagePath);

  const StyledNav = styled("nav")(({ theme, sx }) => ({}));

  const StyledUL = styled("ul")(({ theme, sx }) => ({
    display: "flex",
    alignItems: "center",
    flexWrap: "wrap",
    listStyle: "none",
  }));

  function handleAddMenuPath(menuItem) {
    setMenuPath((prev) => [...prev, menuItem]);
  }

  function handleRemoveMenuPath() {
    setMenuPath((prev) => prev.slice(0, -1));
  }

  return (
    <nav className="desktop-nav">
      <ul className="menus">
        {menuItems.map((menu, index) => {
          return (
            <MenuItem
              item={menu}
              key={index}
              depthLevel={depthLevel}
              menuPath={menuPath}
              handleAddMenuPath={handleAddMenuPath}
              handleRemoveMenuPath={handleRemoveMenuPath}
              selectedMenuPath={selectedMenuPath}
              setSelectedMenuPath={setSelectedMenuPath}
            />
          );
        })}
      </ul>
    </nav>
  );
};

export default Navbar;
