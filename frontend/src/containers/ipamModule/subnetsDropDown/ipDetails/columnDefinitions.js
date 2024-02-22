import React from "react";
import DefaultAnchor from "../../../../components/anchor";
import { indexColumnNameConstants } from "./constants";

export function useIndexTableColumnDefinitions({ handleIpAddressClick } = {}) {
  const columnDefinitions = [
    {
      data_key: indexColumnNameConstants.IP_ADDRESS,
      render: (text, record) => (
        <DefaultAnchor onClick={() => handleIpAddressClick(record)}>
          {text}
        </DefaultAnchor>
      ),
    },
    indexColumnNameConstants.SUBNET_ADDRESS,
    indexColumnNameConstants.MAC_ADDRESS,
    indexColumnNameConstants.STATUS,
    indexColumnNameConstants.VIP,
    indexColumnNameConstants.ASSET_TAG,
    indexColumnNameConstants.CONFIGURATION_SWITCH,
    indexColumnNameConstants.CONFIGURATION_INTERFACE,
    indexColumnNameConstants.OPEN_PORTS,
    indexColumnNameConstants.IP_DNS,
    indexColumnNameConstants.DNS_IP,
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
