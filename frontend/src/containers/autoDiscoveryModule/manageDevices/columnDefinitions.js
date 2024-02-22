import { indexColumnNameConstants } from "./constants";

export function useIndexTableColumnDefinitions({} = {}) {
  const columnDefinitions = [
    indexColumnNameConstants.IP_ADDRESS,
    indexColumnNameConstants.SUBNET,
    indexColumnNameConstants.OS_TYPE,
    indexColumnNameConstants.MAKE_MODEL,
    indexColumnNameConstants.FUNCTION,
    indexColumnNameConstants.VENDOR,
    indexColumnNameConstants.SNMP_STATUS,
    indexColumnNameConstants.SNMP_VERSION,
    indexColumnNameConstants.SSH_STATUS,
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
