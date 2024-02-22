import React from "react";
import Swal from "sweetalert2";
import { useTheme } from "@mui/material/styles";

export default function useSweetAlert() {
  const theme = useTheme();

  const sweetAlertWrapper = {
    success: (title, text) =>
      Swal.fire({
        icon: "success",
        title,
        html: text,
        background: theme?.palette?.sweet_alert?.background,
        color: theme?.palette?.sweet_alert?.primary_text,
        confirmButtonColor:
          theme?.palette?.default_button?.success_alert_background,
      }),
    error: (title, text) =>
      Swal.fire({
        icon: "error",
        title,
        html: text,
        background: theme?.palette?.sweet_alert?.background,
        color: theme?.palette?.sweet_alert?.primary_text,
        confirmButtonColor:
          theme?.palette?.default_button?.error_alert_background,
      }),
    warning: (title, text) =>
      Swal.fire({
        icon: "warning",
        title,
        html: text,
        background: theme?.palette?.sweet_alert?.background,
        color: theme?.palette?.sweet_alert?.primary_text,
        confirmButtonText: "Ok",
        confirmButtonColor:
          theme?.palette?.default_button?.warning_alert_background,
      }),
    info: (title, text) =>
      Swal.fire({
        icon: "info",
        title,
        html: text,
        background: theme?.palette?.sweet_alert?.background,
        color: theme?.palette?.sweet_alert?.primary_text,
        confirmButtonColor:
          theme?.palette?.default_button?.info_alert_background,
      }),
    custom: (options) => Swal.fire(options),
    callback: (type, title, text, callback) => {
      const confirmButtonColor =
        type === "success"
          ? theme?.palette?.default_button?.success_alert_background
          : type === "error"
          ? theme?.palette?.default_button?.error_alert_background
          : theme?.palette?.default_button?.info_alert_background;
      Swal.fire({
        icon: type,
        title,
        html: text,
        background: theme?.palette?.sweet_alert?.background,
        color: theme?.palette?.sweet_alert?.primary_text,
        confirmButtonText: "Ok",
        confirmButtonColor,
      }).then((result) => {
        if (result.isConfirmed && callback) {
          callback();
        }
      });
    },

    decision_callback: (type, title, text, callback) =>
      Swal.fire({
        icon: type,
        title,
        html: text,
        background: theme?.palette?.sweet_alert?.background,
        color: theme?.palette?.sweet_alert?.primary_text,
        showCancelButton: true,
        cancelButtonText: "No",
        cancelButtonColor: theme?.palette?.default_button?.cancel_background,
        confirmButtonText: "Yes",
        confirmButtonColor:
          theme?.palette?.default_button?.success_alert_background,
      }).then((result) => {
        if (result.isConfirmed && callback) {
          callback(true);
        } else if (callback) {
          callback(false);
        }
      }),
  };

  const handleSuccessAlert = (message) => {
    sweetAlertWrapper.success("Success!", message);
  };

  const handleErrorAlert = (message) => {
    sweetAlertWrapper.error("Error!", message);
  };

  const handleWarningAlert = (message) => {
    sweetAlertWrapper.warning("Warning!", message);
  };

  const handleInfoAlert = (message) => {
    sweetAlertWrapper.info("Info!", message);
  };

  const handleCustomAlert = (icon, title, text) => {
    sweetAlertWrapper.custom({
      icon,
      title,
      text,
    });
  };

  const handleCallbackAlert = (
    message,
    callback,
    type = "warning",
    title = null
  ) => {
    if (type === "success") {
      sweetAlertWrapper.callback(type, title ?? "Success!", message, callback);
    } else if (type === "error") {
      sweetAlertWrapper.callback(type, title ?? "Error!", message, callback);
    } else if (type === "warning") {
      sweetAlertWrapper.decision_callback(
        type,
        title ?? "Warning!",
        message,
        callback
      );
    } else if (type === "info") {
      sweetAlertWrapper.callback(type, title ?? "Info!", message, callback);
    }
  };
  return {
    sweetAlertWrapper,
    handleSuccessAlert,
    handleInfoAlert,
    handleErrorAlert,
    handleWarningAlert,
    handleCustomAlert,
    handleCallbackAlert,
  };
}
