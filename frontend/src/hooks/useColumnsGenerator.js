import React from "react";
import { getTitle } from "../utils/helpers";
import useColumnSearchProps from "./useColumnSearchProps";

export default function useColumnsGenerator({ columnDefinitions }) {
  const getColumnSearchProps = useColumnSearchProps();
  return columnDefinitions?.map((item) => {
    if (typeof item === "object") {
      const { data_key, search = true, ...rest } = item;
      if (search) {
        return {
          title: getTitle(data_key),
          dataIndex: data_key,
          key: data_key,
          ellipsis: true,
          ...getColumnSearchProps(data_key),
          ...rest,
        };
      } else {
        return {
          title: getTitle(data_key),
          dataIndex: data_key,
          key: data_key,
          ellipsis: true,
          ...rest,
        };
      }
    } else {
      return {
        title: getTitle(item),
        dataIndex: item,
        key: item,
        ellipsis: true,
        ...getColumnSearchProps(item),
      };
    }
  });
}
