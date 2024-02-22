import { indexColumnNameConstants } from "./constants";

export function useIndexTableColumnDefinitions({} = {}) {
  const columnDefinitions = [
    indexColumnNameConstants.FILE_NAME,
    indexColumnNameConstants.DATE,
  ];

  const restoreColumnDefinitions = [
    indexColumnNameConstants.FILE_NAME,
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
    restoreColumnDefinitions,
    dataKeys,
  };
}
