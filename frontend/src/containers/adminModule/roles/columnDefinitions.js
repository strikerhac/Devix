import React from "react";
import { Icon } from "@iconify/react";
import { indexColumnNameConstants } from "./constants";

export function useIndexTableColumnDefinitions({
  pageEditable,
  handleEdit,
} = {}) {
  const columnDefinitions = [
    indexColumnNameConstants.ROLE,

    {
      data_key: indexColumnNameConstants.ACTIONS,
      search: false,
      fixed: "right",
      align: "center",
      width: 100,
      render: (text, record) => (
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
      ),
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
    columnDefinitions,
    dataKeys,
  };
}
