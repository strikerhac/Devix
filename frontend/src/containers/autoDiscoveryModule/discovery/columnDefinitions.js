import { indexColumnNameConstants } from "./constants";

export function useIndexTableColumnDefinitions({ handleEdit } = {}) {
  const columnDefinitions = [
    indexColumnNameConstants.IP_ADDRESS,
    indexColumnNameConstants.SUBNET,
    indexColumnNameConstants.MAKE_MODEL,
    indexColumnNameConstants.OS_TYPE,
    indexColumnNameConstants.VENDOR,
    indexColumnNameConstants.SNMP_STATUS,
    indexColumnNameConstants.SNMP_VERSION,
    indexColumnNameConstants.FUNCTION,
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
