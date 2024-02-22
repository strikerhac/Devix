import { indexColumnNameConstants } from "./constants";

export function useIndexTableColumnDefinitions({} = {}) {
  const columnDefinitions = [
    indexColumnNameConstants.IP_ADDRESS,
    indexColumnNameConstants.DEVICE_NAME,
    indexColumnNameConstants.INTERFACE_NAME,
    indexColumnNameConstants.INTERFACE_STATUS,
    indexColumnNameConstants.UPLOAD_SPEED,
    indexColumnNameConstants.DOWNLOAD_SPEED,
    indexColumnNameConstants.INTERFACE_DESCRIPTION,
  ];

  const dataKeys = columnDefinitions
    .map((item) => {
      if (typeof item === "object") {
        return item.data_key;
      } else {
        return item;
      }
    })
    .filter((item) => true);

  return {
    columnDefinitions,
    dataKeys,
  };
}
