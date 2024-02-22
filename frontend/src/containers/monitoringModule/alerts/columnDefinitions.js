import React from "react";
import { indexColumnNameConstants } from "./constants";
import DefaultAnchor from "../../../components/anchor";

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
    indexColumnNameConstants.DESCRIPTION,
    indexColumnNameConstants.ALERT_TYPE,
    indexColumnNameConstants.ALERT_STATUS,
    indexColumnNameConstants.CATEGORY,
    indexColumnNameConstants.DATE,
  ];

  const alertHistoryColumnDefinitions = [
    indexColumnNameConstants.IP_ADDRESS,
    indexColumnNameConstants.DESCRIPTION,
    indexColumnNameConstants.ALERT_TYPE,
    indexColumnNameConstants.DATE,
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
    alertHistoryColumnDefinitions,
    dataKeys,
  };
}
