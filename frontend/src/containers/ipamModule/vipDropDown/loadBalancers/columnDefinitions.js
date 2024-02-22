import { indexColumnNameConstants } from "./constants";

export function useIndexTableColumnDefinitions({} = {}) {
  const columnDefinitions = [
    indexColumnNameConstants.IP_ADDRESS,
    indexColumnNameConstants.DEVICE_NAME,
    indexColumnNameConstants.V_SERVER_NAME,
    indexColumnNameConstants.VIP,
    indexColumnNameConstants.POOL_NAME,
    indexColumnNameConstants.NODE,
    indexColumnNameConstants.SERVICE_PORT,
    indexColumnNameConstants.POOL_MEMBER,
    indexColumnNameConstants.MONITOR_VALUE,
    indexColumnNameConstants.MONITOR_STATUS,
    indexColumnNameConstants.LB_METHOD,
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
