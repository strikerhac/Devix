import React from "react";
import { useTheme } from "@mui/material/styles";
import useButtonGenerator from "../hooks/useButtonGenerator";
import useButtonsConfiguration from "../hooks/useButtonsConfiguration";

export default function DefaultDialogFooter({ handleClose, sx, ...rest }) {
  const theme = useTheme();
  const { buttonsConfigurationList } = useButtonsConfiguration({
    default_cancel: { handleClick: handleClose },
    default_submit: null,
  });
  const buttonGenerator = useButtonGenerator();

  return (
    <div
      style={{ display: "flex", justifyContent: "center", gap: "10px", ...sx }}
      {...rest}
    >
      {buttonsConfigurationList.map((item) => buttonGenerator(item))}
    </div>
  );
}

export function TableConfigurationDialogFooter({
  handleClose,
  handleReset,
  handleSave,
  sx,
  ...rest
}) {
  const theme = useTheme();
  const { buttonsConfigurationList } = useButtonsConfiguration({
    default_cancel: { handleClick: handleClose },
    default_reset: { handleClick: handleReset },
    default_save: { handleClick: handleSave },
  });
  const buttonGenerator = useButtonGenerator();

  return (
    <div
      style={{ display: "flex", justifyContent: "center", gap: "10px", ...sx }}
      {...rest}
    >
      {buttonsConfigurationList.map((item) => buttonGenerator(item))}
    </div>
  );
}

export function DeviceDetailsDialogFooter({ handleClose, sx, ...rest }) {
  const theme = useTheme();
  const { buttonsConfigurationObject } = useButtonsConfiguration({
    default_ok: { handleClick: handleClose },
  });
  const buttonGenerator = useButtonGenerator();

  return (
    <div
      style={{ display: "flex", justifyContent: "center", gap: "10px", ...sx }}
      {...rest}
    >
      {buttonGenerator(buttonsConfigurationObject.default_ok)}
    </div>
  );
}

export function CancelDialogFooter({ handleClose, sx, ...rest }) {
  const theme = useTheme();
  const { buttonsConfigurationList } = useButtonsConfiguration({
    default_cancel: { handleClick: handleClose },
  });
  const buttonGenerator = useButtonGenerator();

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        padding: "20px",
        ...sx,
      }}
      {...rest}
    >
      {buttonsConfigurationList.map((item) => buttonGenerator(item))}
    </div>
  );
}

export function LoginDialogFooter({ handleClose, sx, ...rest }) {
  const theme = useTheme();
  const { buttonsConfigurationList } = useButtonsConfiguration({
    default_login: {
      handleClick: handleClose,
      sx: { width: "150px", backgroundColor: "#66B127" },
    },
  });
  const buttonGenerator = useButtonGenerator();

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        padding: "20px 0",
        ...sx,
      }}
      {...rest}
    >
      {buttonsConfigurationList.map((item) => buttonGenerator(item))}
    </div>
  );
}

export function RegisterDialogFooter({ handleRegister, sx, ...rest }) {
  const theme = useTheme();
  const { buttonsConfigurationList } = useButtonsConfiguration({
    default_register: {
      handleClick: handleRegister,
      sx: { width: "150px", backgroundColor: "#66B127" },
    },
  });
  const buttonGenerator = useButtonGenerator();

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        padding: "20px 0",
        ...sx,
      }}
      {...rest}
    >
      {buttonsConfigurationList.map((item) => buttonGenerator(item))}
    </div>
  );
}

export function CompareDialogFooter({ handleClose, sx, ...rest }) {
  const theme = useTheme();
  const { buttonsConfigurationList } = useButtonsConfiguration({
    default_cancel: { handleClick: handleClose },
    default_compare_submit: null,
  });
  const buttonGenerator = useButtonGenerator();

  return (
    <div
      style={{ display: "flex", justifyContent: "center", gap: "10px", ...sx }}
      {...rest}
    >
      {buttonsConfigurationList.map((item) => buttonGenerator(item))}
    </div>
  );
}

export function UpdateDialogFooter({
  handleCancel,
  handleUpdate,
  sx,
  ...rest
}) {
  const theme = useTheme();
  const { buttonsConfigurationList } = useButtonsConfiguration({
    default_cancel: { handleClick: handleCancel },
    default_update: { handleClick: handleUpdate },
  });
  const buttonGenerator = useButtonGenerator();

  return (
    <div
      style={{ display: "flex", justifyContent: "center", gap: "10px", ...sx }}
      {...rest}
    >
      {buttonsConfigurationList.map((item) => buttonGenerator(item))}
    </div>
  );
}

export function UpdateSubmitDialogFooter({
  handleCancel,
  handleUpdate,
  sx,
  ...rest
}) {
  const theme = useTheme();
  const { buttonsConfigurationList } = useButtonsConfiguration({
    default_cancel: { handleClick: handleCancel },
    default_submit_update: null,
  });
  const buttonGenerator = useButtonGenerator();

  return (
    <div
      style={{ display: "flex", justifyContent: "center", gap: "10px", ...sx }}
      {...rest}
    >
      {buttonsConfigurationList.map((item) => buttonGenerator(item))}
    </div>
  );
}

export function AddSubmitDialogFooter({
  handleCancel,
  handleUpdate,
  sx,
  ...rest
}) {
  const theme = useTheme();
  const { buttonsConfigurationList } = useButtonsConfiguration({
    default_cancel: { handleClick: handleCancel },
    default_submit_add: null,
  });
  const buttonGenerator = useButtonGenerator();

  return (
    <div
      style={{ display: "flex", justifyContent: "center", gap: "10px", ...sx }}
      {...rest}
    >
      {buttonsConfigurationList.map((item) => buttonGenerator(item))}
    </div>
  );
}

export function CompanyDialogFooter({ handleBack, sx, ...rest }) {
  const theme = useTheme();
  const { buttonsConfigurationList } = useButtonsConfiguration({
    default_back: {
      handleClick: handleBack,
      sx: { width: "100%", backgroundColor: "#66B127" },
    },
    default_next: {
      sx: { width: "100%", backgroundColor: "#66B127" },
    },
  });
  const buttonGenerator = useButtonGenerator();

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "right",
        padding: "20px 0",
        ...sx,
      }}
      {...rest}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          gap: "10px",
          ...sx,
        }}
        {...rest}
      >
        {buttonsConfigurationList.map((item) => buttonGenerator(item))}
      </div>
    </div>
  );
}

export function UserDialogFooter({ handleBack, sx, ...rest }) {
  const theme = useTheme();
  const { buttonsConfigurationList } = useButtonsConfiguration({
    default_back: {
      handleClick: handleBack,
      sx: { backgroundColor: "#66B127" },
    },
    default_register: {
      sx: { backgroundColor: "#66B127" },
    },
  });
  const buttonGenerator = useButtonGenerator();

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "right",
        padding: "20px 0",
        ...sx,
      }}
      {...rest}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          gap: "10px",
          ...sx,
        }}
        {...rest}
      >
        {buttonsConfigurationList.map((item) => buttonGenerator(item))}
      </div>
    </div>
  );
}
