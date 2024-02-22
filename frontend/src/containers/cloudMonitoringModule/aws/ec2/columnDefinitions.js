import React from "react";
import { indexColumnNameConstants } from "./constants";
import { Switch } from "antd";

export function useIndexTableColumnDefinitions({
  handleMonitoringSwitchChange,
} = {}) {
  const columnDefinitions = [
    indexColumnNameConstants.INSTANCE_ID,
    indexColumnNameConstants.INSTANCE_NAME,
    indexColumnNameConstants.ACCOUNT_LABEL,
    indexColumnNameConstants.ACCESS_KEY,
    indexColumnNameConstants.REGION_ID,
    {
      data_key: indexColumnNameConstants.MONITORING_STATUS,
      search: false,
      title: "Monitoring",
      fixed: "right",
      align: "center",
      width: 120,
      render: (text, record) => (
        <Switch
          style={{ backgroundColor: "green" }}
          onChange={(checked) => handleMonitoringSwitchChange(checked, record)}
        />
      ),
    },
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
