import { indexColumnNameConstants } from "./constants";

export function useIndexTableColumnDefinitions({} = {}) {
  const columnDefinitions = [
    indexColumnNameConstants.IP_ADDRESS,
    indexColumnNameConstants.DEVICE_NAME,
    indexColumnNameConstants.INTERNAL_IP,
    indexColumnNameConstants.VIP,
    indexColumnNameConstants.SOURCE_PORT,
    indexColumnNameConstants.DESTINATION_PORT,
    indexColumnNameConstants.EXTERNAL_INTERFACE,
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
