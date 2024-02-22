import { indexColumnNameConstants } from "./constants";

export function useIndexTableColumnDefinitions({} = {}) {
  const columnDefinitions = [
    indexColumnNameConstants.AP_IP,
    indexColumnNameConstants.AP_NAME,
    indexColumnNameConstants.SERIAL_NUMBER,
    indexColumnNameConstants.AP_MODEL,
    indexColumnNameConstants.HARDWARE_VERSION,
    indexColumnNameConstants.SOFTWARE_VERSION,
    indexColumnNameConstants.DESCRIPTION,
  ];

  const plainColumnDefinitions = [
    indexColumnNameConstants.AP_IP,
    indexColumnNameConstants.AP_NAME,
    indexColumnNameConstants.SERIAL_NUMBER,
    indexColumnNameConstants.AP_MODEL,
    indexColumnNameConstants.HARDWARE_VERSION,
    indexColumnNameConstants.SOFTWARE_VERSION,
    indexColumnNameConstants.DESCRIPTION,
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
    plainColumnDefinitions,
    columnDefinitions,
    dataKeys,
  };
}
