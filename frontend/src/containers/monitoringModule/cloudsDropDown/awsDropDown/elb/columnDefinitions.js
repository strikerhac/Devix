import React from "react";
import { indexColumnNameConstants } from "./constants";
import { Switch } from "antd";

export function useIndexTableColumnDefinitions({
  handleMonitoringSwitchChange,
} = {}) {
  const columnDefinitions = [
    indexColumnNameConstants.LOAD_BALANCER_NAME,
    indexColumnNameConstants.LOAD_BALANCER_TYPE,
    indexColumnNameConstants.LOAD_BALANCER_SCHEME,
    indexColumnNameConstants.LOAD_BALANCER_ARN,
    indexColumnNameConstants.ACCESS_KEY,
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
