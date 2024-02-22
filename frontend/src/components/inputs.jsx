import React, { useState } from "react";
import { useTheme } from "@mui/material/styles";
import { Icon } from "@iconify/react";

export default function DefaultInput({
  field,
  type = "text",
  sx,
  children,
  ...rest
}) {
  const theme = useTheme();

  return (
    <>
      {rest?.icon ? (
        <>
          <input
            {...field}
            type={type}
            style={{
              borderStyle: "solid",
              color: theme?.palette?.default_input?.primary_text,
              backgroundColor: theme?.palette?.default_input?.background,
              borderColor: theme?.palette?.default_input?.border,
              borderRadius: "5px 0px 0px 5px",
              padding: "7px 10px",
              width: "100%",
              borderRight: "none",
              outline: "none",
              ...sx,
            }}
            {...rest}
          >
            {children}
          </input>
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              backgroundColor: theme?.palette?.default_input?.background,
              border: `2px solid ${theme?.palette?.default_input?.border}`,
              borderRadius: "0px 5px 5px 0px",
              borderLeft: "none",
              paddingRight: "5px",
              outline: "none",
            }}
          >
            <Icon
              fontSize={"18px"}
              icon={rest.icon}
              style={{ cursor: "pointer" }}
            />
          </div>
        </>
      ) : (
        <input
          {...field}
          type={type}
          style={{
            borderStyle: "solid",
            color: theme?.palette?.default_input?.primary_text,
            backgroundColor: rest.disabled
              ? "#F6F6F6"
              : theme?.palette?.default_input?.background,
            borderColor: theme?.palette?.default_input?.border,
            borderRadius: "5px",
            padding: "7px 10px",
            width: "100%",
            outline: "none",
            ...sx,
          }}
          {...rest}
        >
          {children}
        </input>
      )}
    </>
  );
}

export function PasswordInput({ field, type = "text", sx, children, ...rest }) {
  const theme = useTheme();
  const [showPassword, setShowPassword] = useState(false);

  function handleShowPassword() {
    setShowPassword((prev) => !prev);
  }

  return (
    <>
      <input
        {...field}
        type={showPassword ? "string" : type}
        style={{
          borderStyle: "solid",
          color: theme?.palette?.default_input?.primary_text,
          backgroundColor: theme?.palette?.default_input?.background,
          borderColor: theme?.palette?.default_input?.border,
          borderRadius: "5px 0px 0px 5px",
          padding: "7px 10px",
          width: "100%",
          borderRight: "none",
          outline: "none",
          ...sx,
        }}
        {...rest}
      >
        {children}
      </input>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          backgroundColor: theme?.palette?.default_input?.background,
          border: `2px solid ${theme?.palette?.default_input?.border}`,
          borderRadius: "0px 5px 5px 0px",
          borderLeft: "none",
          paddingRight: "5px",
          cursor: "pointer",
          outline: "none",
        }}
        onClick={handleShowPassword}
      >
        <Icon fontSize={"18px"} icon="ph:eye" style={{ cursor: "pointer" }} />
      </div>
    </>
  );
}
