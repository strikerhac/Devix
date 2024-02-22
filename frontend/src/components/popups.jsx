import React, { useState } from "react";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import { useTheme } from "@mui/material/styles";
import MenuItem from "@mui/material/MenuItem";
import MenuList from "@mui/material/MenuList";
import Button from "@mui/material/Button";
import Popper from "@mui/material/Popper";
import Grow from "@mui/material/Grow";
import Paper from "@mui/material/Paper";
import ClickAwayListener from "@mui/material/ClickAwayListener";
import { Icon } from "@iconify/react";

export function ProfilePicturePopup({ handleLogout, sx, children }) {
  const theme = useTheme();
  const [open, setOpen] = useState(false);
  const anchorRef = React.useRef(null);

  const handleToggle = () => {
    setOpen((prevOpen) => !prevOpen);
  };

  const handleClose = (event) => {
    if (anchorRef.current && anchorRef.current.contains(event.target)) {
      return;
    }

    setOpen(false);
  };

  return (
    <>
      <div
        ref={anchorRef}
        onClick={handleToggle}
        style={{
          borderRadius: "100px",
          width: "35px",
          height: "35px",
          backgroundColor:
            theme?.palette?.main_layout?.profile_picture_background,
          cursor: "pointer",
          marginBottom: "10px", // Adjust the margin bottom to add space
          display: "flex",
          justifyContent: "center",
        }}
      >
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
          }}
        >
          <Icon fontSize={"20px"} icon="ph:user" style={{ color: "white" }} />
        </div>
      </div>
      <Popper
        open={open}
        anchorEl={anchorRef.current}
        role={undefined}
        transition
        disablePortal
        style={{ zIndex: 99999 }}
      >
        {({ TransitionProps, placement }) => (
          <Grow
            {...TransitionProps}
            style={{
              transformOrigin:
                placement === "bottom" ? "center top" : "center bottom",
            }}
          >
            <div
              style={{
                backgroundColor: "#F7F7F7",
                boxShadow: "rgba(99, 99, 99, 0.2) 0px 2px 2px 0px",
                borderRadius: "7px",
                marginTop: "12px", // Adjust the margin top to add space
                position: "relative",
              }}
            >
              <div
                style={{
                  position: "absolute",
                  top: "-10px",
                  left: "50%",
                  transform: "translateX(-50%)",
                  width: "0",
                  height: "0",
                  borderLeft: "10px solid transparent",
                  borderRight: "10px solid transparent",
                  borderBottom: "10px solid #F7F7F7",
                }}
              ></div>
              <ClickAwayListener onClickAway={handleClose}>
                <MenuList autoFocusItem={false} id="menu-list-grow">
                  <MenuItem onClick={handleLogout} style={{ color: "grey" }}>
                    Logout
                  </MenuItem>
                </MenuList>
              </ClickAwayListener>
            </div>
          </Grow>
        )}
      </Popper>
    </>
  );
}
