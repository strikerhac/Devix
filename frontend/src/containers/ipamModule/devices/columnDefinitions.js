import { indexColumnNameConstants } from "./constants";

export function useIndexTableColumnDefinitions({} = {}) {
  const columnDefinitions = [
    indexColumnNameConstants.IP_ADDRESS,
    indexColumnNameConstants.DEVICE_NAME,
    indexColumnNameConstants.SUBNET_ADDRESS,
    indexColumnNameConstants.SUBNET_MASK,
    indexColumnNameConstants.SUBNET_NAME,
    indexColumnNameConstants.INTERFACE,
    indexColumnNameConstants.INTERFACE_IP,
    indexColumnNameConstants.INTERFACE_LOCATION,
    indexColumnNameConstants.INTERFACE_DESCRIPTION,
    indexColumnNameConstants.INTERFACE_STATUS,
    indexColumnNameConstants.VIRTUAL_IP,
    indexColumnNameConstants.VLAN,
    indexColumnNameConstants.VLAN_NUMBER,
    indexColumnNameConstants.FETCH_DATE,
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
