import React from "react";
import { Icon } from "@iconify/react";
import { DEFAULT_SITE, indexColumnNameConstants } from "./constants";

export function useIndexTableColumnDefinitions({
  pageEditable,
  handleEdit,
} = {}) {
  const columnDefinitions = [
    indexColumnNameConstants.SITE_NAME,
    indexColumnNameConstants.STATUS,
    indexColumnNameConstants.REGION_NAME,
    indexColumnNameConstants.LATITUDE,
    indexColumnNameConstants.LONGITUDE,
    indexColumnNameConstants.CITY,
    {
      data_key: indexColumnNameConstants.ACTIONS,
      search: false,
      fixed: "right",
      align: "center",
      width: 100,
      render: (text, record) => {
        return record[indexColumnNameConstants.SITE_NAME] !== DEFAULT_SITE ? (
          <div
            style={{
              display: "flex",
              gap: "10px",
              justifyContent: "center",
            }}
          >
            <Icon
              fontSize={"15px"}
              onClick={() => handleEdit(record)}
              icon="bx:edit"
              style={{ cursor: "pointer" }}
            />
          </div>
        ) : null;
      },
    },
  ].filter((item) => {
    if (typeof item === "object") {
      if (pageEditable) {
        return true;
      } else {
        return item.data_key !== indexColumnNameConstants.ACTIONS;
      }
    } else {
      return true;
    }
  });

  const plainColumnDefinitions = [
    indexColumnNameConstants.SITE_NAME,
    indexColumnNameConstants.STATUS,
    indexColumnNameConstants.REGION_NAME,
    indexColumnNameConstants.LATITUDE,
    indexColumnNameConstants.LONGITUDE,
    indexColumnNameConstants.CITY,
  ];

  const dataKeys = columnDefinitions
    .map((item) => {
      if (typeof item === "object") {
        return item.data_key;
      } else {
        return item;
      }
    })
    .filter((item) => item !== indexColumnNameConstants.ACTIONS);

  return {
    plainColumnDefinitions,
    columnDefinitions,
    dataKeys,
  };
}
