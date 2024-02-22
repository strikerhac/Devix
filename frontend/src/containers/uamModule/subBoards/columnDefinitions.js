import { indexColumnNameConstants } from "./constants";

export function useIndexTableColumnDefinitions({} = {}) {
  const columnDefinitions = [
    indexColumnNameConstants.SUB_BOARD_NAME,
    indexColumnNameConstants.DEVICE_NAME,
    indexColumnNameConstants.SERIAL_NUMBER,
    indexColumnNameConstants.STATUS,
    indexColumnNameConstants.PN_CODE,
    indexColumnNameConstants.SUB_BOARD_TYPE,
    indexColumnNameConstants.SUB_RACK_ID,
    indexColumnNameConstants.SLOT_NUMBER,
    indexColumnNameConstants.SUB_SLOT_NUMBER,
    indexColumnNameConstants.DEVICE_SLOT_ID,
    indexColumnNameConstants.SOFTWARE_VERSION,
    indexColumnNameConstants.HARDWARE_VERSION,
    indexColumnNameConstants.MANUFACTURE_DATE,
    indexColumnNameConstants.EOS_DATE,
    indexColumnNameConstants.EOL_DATE,
  ];

  const plainColumnDefinitions = [
    indexColumnNameConstants.SUB_BOARD_NAME,
    indexColumnNameConstants.DEVICE_NAME,
    indexColumnNameConstants.SERIAL_NUMBER,
    indexColumnNameConstants.STATUS,
    indexColumnNameConstants.PN_CODE,
    indexColumnNameConstants.SUB_BOARD_TYPE,
    indexColumnNameConstants.SUB_RACK_ID,
    indexColumnNameConstants.SLOT_NUMBER,
    indexColumnNameConstants.SUB_SLOT_NUMBER,
    indexColumnNameConstants.DEVICE_SLOT_ID,
    indexColumnNameConstants.SOFTWARE_VERSION,
    indexColumnNameConstants.HARDWARE_VERSION,
    indexColumnNameConstants.MANUFACTURE_DATE,
    indexColumnNameConstants.EOS_DATE,
    indexColumnNameConstants.EOL_DATE,
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
