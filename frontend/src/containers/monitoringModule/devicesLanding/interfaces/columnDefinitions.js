import React from "react";
import { indexColumnNameConstants } from "./constants";
import DefaultAnchor from "../../../../components/anchor";

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
    indexColumnNameConstants.DEVICE_NAME,
    indexColumnNameConstants.INTERFACE_NAME,
    indexColumnNameConstants.INTERFACE_STATUS,
    indexColumnNameConstants.UPLOAD_SPEED,
    indexColumnNameConstants.DOWNLOAD_SPEED,
    indexColumnNameConstants.INTERFACE_DESCRIPTION,
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
