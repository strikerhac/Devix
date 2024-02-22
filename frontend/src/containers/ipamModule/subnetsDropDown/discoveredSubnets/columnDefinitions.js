import { indexColumnNameConstants } from "./constants";

export function useIndexTableColumnDefinitions({} = {}) {
  const columnDefinitions = [
    indexColumnNameConstants.SUBNET_ADDRESS,
    indexColumnNameConstants.SUBNET_NAME,
    indexColumnNameConstants.SUBNET_MASK,
    indexColumnNameConstants.SUBNET_SIZE,
    indexColumnNameConstants.SUBNET_USAGE,
    indexColumnNameConstants.SUBNET_LOCATION,
    indexColumnNameConstants.SUBNET_STATUS,
    indexColumnNameConstants.DISCOVERED_FROM,
    indexColumnNameConstants.SCAN_DATE,
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
