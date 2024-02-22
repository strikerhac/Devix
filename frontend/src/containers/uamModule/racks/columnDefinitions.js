import React from "react";
import { Icon } from "@iconify/react";
import { DEFAULT_RACK, indexColumnNameConstants } from "./constants";

export function useIndexTableColumnDefinitions({
  pageEditable,
  handleEdit,
} = {}) {
  const columnDefinitions = [
    indexColumnNameConstants.RACK_NAME,
    indexColumnNameConstants.SITE_NAME,
    indexColumnNameConstants.SERIAL_NUMBER,
    indexColumnNameConstants.MANUFACTURE_DATE,
    indexColumnNameConstants.UNIT_POSITION,
    indexColumnNameConstants.STATUS,
    indexColumnNameConstants.RU,
    indexColumnNameConstants.RFS_DATE,
    indexColumnNameConstants.HEIGHT,
    indexColumnNameConstants.WIDTH,
    indexColumnNameConstants.DEPTH,
    indexColumnNameConstants.FLOOR,
    indexColumnNameConstants.PN_CODE,
    indexColumnNameConstants.RACK_MODEL,
    {
      data_key: indexColumnNameConstants.ACTIONS,
      search: false,
      fixed: "right",
      align: "center",
      width: 100,
      render: (text, record) => {
        return record[indexColumnNameConstants.RACK_NAME] !== DEFAULT_RACK ? (
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
    indexColumnNameConstants.RACK_NAME,
    indexColumnNameConstants.SITE_NAME,
    indexColumnNameConstants.SERIAL_NUMBER,
    indexColumnNameConstants.MANUFACTURE_DATE,
    indexColumnNameConstants.UNIT_POSITION,
    indexColumnNameConstants.STATUS,
    indexColumnNameConstants.RU,
    indexColumnNameConstants.RFS_DATE,
    indexColumnNameConstants.HEIGHT,
    indexColumnNameConstants.WIDTH,
    indexColumnNameConstants.DEPTH,
    indexColumnNameConstants.FLOOR,
    indexColumnNameConstants.PN_CODE,
    indexColumnNameConstants.RACK_MODEL,
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
