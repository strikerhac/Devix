import { indexColumnNameConstants } from "./constants";

export function useIndexTableColumnDefinitions({} = {}) {
  const columnDefinitions = [
    indexColumnNameConstants.DEVICE_NAME,
    indexColumnNameConstants.STATUS,
    indexColumnNameConstants.SERIAL_NUMBER,
    indexColumnNameConstants.MEDIA_TYPE,
    indexColumnNameConstants.PORT_NAME,
    indexColumnNameConstants.PORT_TYPE,
    indexColumnNameConstants.CONNECTOR,
    indexColumnNameConstants.MODE,
    indexColumnNameConstants.SPEED,
    indexColumnNameConstants.WAVE_LENGTH,
    indexColumnNameConstants.OPTICAL_DIRECTION_TYPE,
    indexColumnNameConstants.PN_CODE,
    indexColumnNameConstants.EOS_DATE,
    indexColumnNameConstants.EOL_DATE,
    indexColumnNameConstants.RFS_DATE,
  ];

  const plainColumnDefinitions = [
    indexColumnNameConstants.DEVICE_NAME,
    indexColumnNameConstants.STATUS,
    indexColumnNameConstants.SERIAL_NUMBER,
    indexColumnNameConstants.MEDIA_TYPE,
    indexColumnNameConstants.PORT_NAME,
    indexColumnNameConstants.PORT_TYPE,
    indexColumnNameConstants.CONNECTOR,
    indexColumnNameConstants.MODE,
    indexColumnNameConstants.SPEED,
    indexColumnNameConstants.WAVE_LENGTH,
    indexColumnNameConstants.OPTICAL_DIRECTION_TYPE,
    indexColumnNameConstants.PN_CODE,
    indexColumnNameConstants.EOS_DATE,
    indexColumnNameConstants.EOL_DATE,
    indexColumnNameConstants.RFS_DATE,
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
