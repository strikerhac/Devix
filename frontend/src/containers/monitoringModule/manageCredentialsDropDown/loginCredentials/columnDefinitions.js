import React from "react";
import { indexColumnNameConstants } from "./constants";
import { DefaultTextWithSwitch } from "../../../../components/textWithSwitch";

export function useIndexTableColumnDefinitions({} = {}) {
  const columnDefinitions = [
    indexColumnNameConstants.USER_NAME,
    indexColumnNameConstants.PROFILE_NAME,
    {
      data_key: indexColumnNameConstants.PASSWORD,
      render: (text, record) => <DefaultTextWithSwitch text={text} />,
    },
    indexColumnNameConstants.CATEGORY,
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
