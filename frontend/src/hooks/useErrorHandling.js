import { useEffect } from "react";
import useSweetAlert from "./useSweetAlert";

export const TYPE_FETCH = "fetch";
export const TYPE_SINGLE = "single";
export const TYPE_BULK = "Operation Executed";
export const TYPE_BULK_ADD = "Added";
export const TYPE_BULK_ADD_UPDATE = "Added/Updated";
export const TYPE_BULK_DELETE = "Deleted";
export const TYPE_BULK_ONBOARD = "Onboarded";
export const TYPE_BULK_FETCH = "Fetched";
export const TYPE_BULK_SCAN = "Scanned";
export const TYPE_BULK_DISMANTLE = "Dismantled";
export const TYPE_BULK_SYNC = "Synced";
export const TYPE_BULK_RESTORE = "Restored";
export const TYPE_BULK_BACKUP = "Backup Completed";
export const TYPE_BULK_MONITORING = "Monitoring Completed";

export default function useErrorHandling({
  data,
  isSuccess,
  isError,
  error,
  type,
  showMessage = true,
  callback = () => {},
}) {
  const { handleErrorAlert, handleCallbackAlert } = useSweetAlert();

  useEffect(() => {
    if (type === TYPE_FETCH) {
      if (isSuccess) {
      } else if (isError) {
        if (error?.status === 400) {
          handleErrorAlert(error?.data);
        } else if (error?.status === 404) {
          handleErrorAlert(error?.data?.detail);
        } else if (error?.status === 422) {
          handleErrorAlert(
            error?.data?.detail
              .map(
                (item) =>
                  // `${item?.loc[2]} ${item?.msg} in ${item?.loc[0]} at index  ${item?.loc[1]}`
                  `${item?.msg}}`
              )
              .join("<br>")
          );
        } else if (error?.status === 500) {
          handleErrorAlert(error?.data);
        } else {
          console.log(error);
        }
      }
    } else if (type === TYPE_SINGLE) {
      if (showMessage) {
        if (isSuccess) {
          handleCallbackAlert(data?.message, callback, "success");
        } else if (isError) {
          if (error?.status === 400) {
            handleErrorAlert(error?.data);
          } else if (error?.status === 404) {
            handleErrorAlert(error?.data?.detail);
          } else if (error?.status === 422) {
            handleErrorAlert(
              error?.data?.detail
                .map(
                  (item) =>
                    // `${item?.loc[2]} ${item?.msg} in ${item?.loc[0]} at index  ${item?.loc[1]}`
                    `${item?.msg}}`
                )
                .join("<br>")
            );
          } else if (error?.status === 500) {
            handleErrorAlert(error?.data);
          } else {
            console.log(error);
          }
        }
      }
    } else if (
      type === TYPE_BULK ||
      type === TYPE_BULK_ADD ||
      type === TYPE_BULK_ADD_UPDATE ||
      type === TYPE_BULK_DELETE ||
      type === TYPE_BULK_ONBOARD ||
      type === TYPE_BULK_FETCH ||
      type === TYPE_BULK_SCAN ||
      type === TYPE_BULK_DISMANTLE ||
      type === TYPE_BULK_SYNC ||
      type === TYPE_BULK_RESTORE ||
      type === TYPE_BULK_BACKUP ||
      type === TYPE_BULK_MONITORING
    ) {
      if (isSuccess) {
        if (data?.error === 0) {
          handleCallbackAlert(`${type} Successfully.`, callback, "success");
        } else if (data?.success === 0) {
          handleCallbackAlert(
            data?.error_list?.join("<br>"),
            callback,
            "error"
          );
        } else {
          handleCallbackAlert(
            `${type} Successfully with the following Exceptions:<br>${data?.error_list?.join(
              "<br>"
            )}`,
            callback,
            "info"
          );
        }
      } else if (isError) {
        if (error?.status === 400) {
          handleCallbackAlert(error?.data, callback, "error");
        } else if (error?.status === 404) {
          handleCallbackAlert(error?.data?.detail, callback, "error");
        } else if (error?.status === 422) {
          handleCallbackAlert(
            error?.data?.detail
              .map(
                (item) =>
                  // `${item?.loc[2]} ${item?.msg} in ${item?.loc[0]} at index  ${item?.loc[1]}`
                  `${item?.msg}`
              )
              .join("<br>"),
            callback,
            "error"
          );
        } else if (error?.status === 500) {
          handleCallbackAlert(error?.data, callback, "error");
        } else {
          console.log(error);
        }
      }
    }
  }, [isSuccess, isError]);
}
