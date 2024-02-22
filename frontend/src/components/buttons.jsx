import React, { useState, useEffect, useRef } from "react";
import { Button } from "@mui/material";
import { useTheme, styled } from "@mui/material/styles";
import { Icon } from "@iconify/react";
import { CheckBox } from "@mui/icons-material";
import { getTitle } from "../utils/helpers";

export default function DefaultButton({ sx, handleClick, children, ...rest }) {
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

export function DropDownButton({
  sx,
  handleClick,
  children,
  options,
  ...rest
}) {
  const theme = useTheme();
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const handleOutsideClick = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleOutsideClick);
    return () => {
      document.removeEventListener("mousedown", handleOutsideClick);
    };
  }, [dropdownRef]);

  const StyledDiv = styled("div")(({ theme, sx }) => ({
    display: "flex",
    alignItems: "center",
    gap: "10px",
    border: `1px solid ${theme?.palette?.drop_down_button?.border}`,
    color: sx?.color,
    cursor: "pointer",
    "&:hover": {
      backgroundColor: sx?.backgroundColor,
      opacity: 0.8,
    },
  }));

  const DropdownOptions = styled("div")(({ theme }) => ({
    position: "absolute",
    zIndex: "9999",
    top: "100%",
    right: 0,
    width: "100%",
    backgroundColor: theme?.palette?.drop_down_button?.options_background,
    border: `1px solid ${theme?.palette?.drop_down_button?.border}`,
    borderRadius: "0 0 4px 4px",
    zIndex: 3,
    display: isOpen ? "block" : "none",
    borderRadius: "5px",
    marginTop: "5px",
  }));

  const StyledOption = styled("div")(({ theme, sx }) => ({
    borderRadius: "4px",
    color: theme?.palette?.drop_down_button?.options_text,
    padding: "6px 12px",
    fontSize: "12px",
    cursor: "pointer",
    "&:hover": {
      backgroundColor:
        theme?.palette?.drop_down_button?.options_hover_background,
      color: theme?.palette?.drop_down_button?.options_hover_text,
    },
    ...sx,
  }));

  const handleButtonClick = () => {
    setIsOpen(!isOpen);
  };

  const handleOptionClick = (optionType) => {
    setIsOpen(false);
    handleClick(optionType);
  };

  return (
    <div
      ref={dropdownRef}
      style={{ position: "relative", display: "inline-block" }}
      onClick={handleButtonClick}
      {...rest}
    >
      <div style={{ display: "flex" }}>
        <StyledDiv
          sx={{
            borderTopLeftRadius: "4px",
            borderBottomLeftRadius: "4px",
            padding: "5px 12px 6px 12px",
            borderRight: "none",
            ...sx,
          }}
        >
          {children}
        </StyledDiv>
        <StyledDiv
          sx={{
            borderTopRightRadius: "4px",
            borderBottomRightRadius: "4px",
            padding: "5px 5px 6px 5px",
            ...sx,
          }}
        >
          <Icon fontSize="16px" icon="icon-park-outline:down" />
        </StyledDiv>
      </div>
      <DropdownOptions>
        {options.map((option) => (
          <StyledOption
            key={option.type}
            onClick={() => handleOptionClick(option.type)}
            sx={{ display: "flex" }}
          >
            {option.icon}
            &nbsp;&nbsp;
            <div style={{ marginTop: "-2px" }}>{getTitle(option.type)}</div>
          </StyledOption>
        ))}
      </DropdownOptions>
    </div>
  );
}

export function DropDownCheckboxButton({
  sx,
  handleClick,
  children,
  options,
  ...rest
}) {
  const initialSelectedOptions = options.reduce((acc, option) => {
    acc[option] = false;
    return acc;
  }, {});

  const theme = useTheme();
  const [isOpen, setIsOpen] = useState(false);
  const [selectedOptions, setSelectedOptions] = useState(
    initialSelectedOptions
  );
  const dropdownRef = useRef(null);

  useEffect(() => {
    const handleOutsideClick = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleOutsideClick);
    return () => {
      document.removeEventListener("mousedown", handleOutsideClick);
    };
  }, [dropdownRef]);

  const StyledDiv = styled("div")(({ theme, sx }) => ({
    display: "flex",
    alignItems: "center",
    gap: "10px",
    border: `1px solid ${theme?.palette?.drop_down_button?.border}`,
    color: sx?.color,
    cursor: "pointer",
    "&:hover": {
      backgroundColor: sx?.backgroundColor,
      opacity: 0.8,
    },
  }));

  const DropdownOptions = styled("div")(({ theme }) => ({
    position: "absolute",
    zIndex: "99999",
    top: "100%",
    right: 0,
    width: "100%",
    backgroundColor: theme?.palette?.drop_down_button?.options_background,
    border: `1px solid ${theme?.palette?.drop_down_button?.border}`,
    borderRadius: "0 0 4px 4px",
    zIndex: 3,
    display: isOpen ? "block" : "none",
    borderRadius: "5px",
    marginTop: "5px",
  }));

  const StyledOption = styled("div")(({ theme, sx }) => ({
    borderRadius: "4px",
    color: theme?.palette?.drop_down_button?.options_text,
    padding: "6px 12px",
    fontSize: "12px",
    ...sx,
  }));

  const handleCheckboxChange = (optionType) => {
    setSelectedOptions((prev) => ({
      ...prev,
      [optionType]: !prev[optionType],
    }));
  };

  const handleDownClick = () => {
    setIsOpen(!isOpen);
  };

  const handleButtonClick = () => {
    setIsOpen(false);
    handleClick(selectedOptions);
  };

  return (
    <div
      ref={dropdownRef}
      style={{ position: "relative", display: "inline-block" }}
      {...rest}
    >
      <div style={{ display: "flex" }}>
        <StyledDiv
          sx={{
            borderTopLeftRadius: "4px",
            borderBottomLeftRadius: "4px",
            padding: "5px 12px 6px 12px",
            borderRight: "none",
            ...sx,
          }}
          onClick={handleButtonClick}
        >
          {children}
        </StyledDiv>
        <StyledDiv
          sx={{
            borderTopRightRadius: "4px",
            borderBottomRightRadius: "4px",
            padding: "5px 5px 6px 5px",
            ...sx,
          }}
          onClick={handleDownClick}
        >
          <Icon fontSize="16px" icon="icon-park-outline:down" />
        </StyledDiv>
      </div>
      <DropdownOptions>
        {options.map((option) => (
          <StyledOption key={option} sx={{ display: "flex" }}>
            <input
              type="checkbox"
              id={option}
              name={option}
              value={option}
              checked={selectedOptions[option] || false}
              onChange={() => handleCheckboxChange(option)}
              style={{
                cursor: "pointer",
              }}
            />
            &nbsp;&nbsp;
            <div>{getTitle(option)}</div>
          </StyledOption>
        ))}
      </DropdownOptions>
    </div>
  );
}
