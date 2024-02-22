import React from "react";
import DefaultAnchor from "../../../components/anchor";
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
    indexColumnNameConstants.STATUS,
    indexColumnNameConstants.DEVICE_NAME,
    indexColumnNameConstants.DEVICE_TYPE,
    indexColumnNameConstants.SITE_NAME,
    indexColumnNameConstants.RACK_NAME,
    indexColumnNameConstants.SOFTWARE_TYPE,
    indexColumnNameConstants.SOFTWARE_VERSION,
    indexColumnNameConstants.PATCH_VERSION,
    indexColumnNameConstants.MANUFACTURER,
    indexColumnNameConstants.HW_EOS_DATE,
    indexColumnNameConstants.HW_EOL_DATE,
    indexColumnNameConstants.SW_EOS_DATE,
    indexColumnNameConstants.SW_EOL_DATE,
    indexColumnNameConstants.RFS_DATE,
    indexColumnNameConstants.CONTRACT_EXPIRY,
    indexColumnNameConstants.UP_TIME,
    indexColumnNameConstants.MANUFACTURE_DATE,
    indexColumnNameConstants.AUTHENTICATION,
    indexColumnNameConstants.SERIAL_NUMBER,
    indexColumnNameConstants.PN_CODE,
    indexColumnNameConstants.SUB_RACK_ID_NUMBER,
    indexColumnNameConstants.HARDWARE_VERSION,
    indexColumnNameConstants.MAX_POWER,
    indexColumnNameConstants.SITE_TYPE,
    indexColumnNameConstants.SOURCE,
    indexColumnNameConstants.STACK,
    indexColumnNameConstants.CONTRACT_NUMBER,
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
