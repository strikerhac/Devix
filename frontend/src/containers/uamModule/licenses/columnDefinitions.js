import { indexColumnNameConstants } from "./constants";

export function useIndexTableColumnDefinitions({} = {}) {
  const columnDefinitions = [
    indexColumnNameConstants.DEVICE_NAME,
    indexColumnNameConstants.LICENSE_NAME,
    indexColumnNameConstants.STATUS,
    indexColumnNameConstants.LICENSE_DESCRIPTION,
    indexColumnNameConstants.RFS_DATE,
    indexColumnNameConstants.ACTIVATION_DATE,
    indexColumnNameConstants.EXPIRY_DATE,
    indexColumnNameConstants.GRACE_PERIOD,
    indexColumnNameConstants.SERIAL_NUMBER,
    indexColumnNameConstants.CAPACITY,
    indexColumnNameConstants.USAGE,
    indexColumnNameConstants.PN_CODE,
  ];

  const plainColumnDefinitions = [
    indexColumnNameConstants.DEVICE_NAME,
    indexColumnNameConstants.LICENSE_NAME,
    indexColumnNameConstants.STATUS,
    indexColumnNameConstants.LICENSE_DESCRIPTION,
    indexColumnNameConstants.RFS_DATE,
    indexColumnNameConstants.ACTIVATION_DATE,
    indexColumnNameConstants.EXPIRY_DATE,
    indexColumnNameConstants.GRACE_PERIOD,
    indexColumnNameConstants.SERIAL_NUMBER,
    indexColumnNameConstants.CAPACITY,
    indexColumnNameConstants.USAGE,
    indexColumnNameConstants.PN_CODE,
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
