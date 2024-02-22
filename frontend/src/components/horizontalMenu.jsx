import React, { useState } from "react";
import { Link } from "react-router-dom";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import { useTheme, styled } from "@mui/material/styles";

export default function HorizontalMenu({ menuItems, defaultPage }) {
  const theme = useTheme();

  const [openSubmenus, setOpenSubmenus] = useState({});
  const [selectedMenuItem, setSelectedMenuItem] = useState(defaultPage);

  const StyledMenuItem = styled(MenuItem)(({ theme, sx }) => ({
    height: "50px !important",
    color: sx.color,
    borderBottom: `3px solid ${
      sx.isClicked ? sx.color : "transparent"
    } !important`,
    "&:hover": {
      color: `${theme?.palette?.horizontal_menu?.secondary_text} !important`,
      borderBottom: `3px solid ${theme?.palette?.horizontal_menu?.secondary_text} !important`,
      backgroundColor: "transparent !important",
    },
  }));

  const handleMenuClick = (event, id, type = "page") => {
    setOpenSubmenus((prevOpenSubmenus) => ({
      ...prevOpenSubmenus,
      [id]: !prevOpenSubmenus[id],
    }));
    if (type === "page") setSelectedMenuItem(id);
  };

  const renderMenuItems = (
    items,
    parentId = null,
    position = { top: 125, left: 0 }
  ) => {
    return items?.map((item) => {
      const id = parentId ? `${parentId}-${item.id}` : item.id;
      const isClicked = id === selectedMenuItem;
      if (item.children) {
        return (
          <div key={id} style={{ position: "relative", height: "50px" }}>
            <StyledMenuItem
              key={id}
              id={id}
              onClick={(event) => handleMenuClick(event, id, "dropDown")}
              sx={{
                color: isClicked
                  ? theme?.palette?.horizontal_menu?.secondary_text
                  : theme?.palette?.horizontal_menu?.primary_text,
                isClicked: isClicked,
              }}
            >
              {item.name} DropDown
            </StyledMenuItem>
            <Menu
              anchorEl={document.getElementById(id)}
              open={openSubmenus[id]}
              onClose={(event) => handleMenuClick(event, id)}
              anchorReference="anchorPosition"
              anchorPosition={{
                top: position.top,
                left:
                  position.left +
                    document.getElementById(id)?.offsetWidth +
                    240 || 0,
              }} // Position the nested menu to the right side of the parent menu item
            >
              {renderMenuItems(item.children, id)}
            </Menu>
          </div>
        );
      } else {
        return (
          <StyledMenuItem
            id={id}
            key={id}
            component={Link}
            to={parentId ? `${parentId}/${item.path}` : item.path}
            // to={item.path}
            onClick={(event) => handleMenuClick(event, id)}
            sx={{
              color: isClicked
                ? theme?.palette?.horizontal_menu?.secondary_text
                : theme?.palette?.horizontal_menu?.primary_text,
              isClicked: isClicked,
            }}
          >
            {item.name}
          </StyledMenuItem>
        );
      }
    });
  };

  return <div style={{ display: "flex" }}>{renderMenuItems(menuItems)}</div>;
}
