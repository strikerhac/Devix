import React from "react";
import DefaultCard from "./cards";
import DefaultPageHeader from "./pageHeaders";
import DefaultTable from "./tables";
import useWindowDimensions from "../hooks/useWindowDimensions";

export default function DefaultPageTableSection({
  PAGE_NAME,
  TABLE_DATA_UNIQUE_ID,
  buttonsConfigurationList,
  displayColumns,
  dataSource,
  selectedRowKeys = null,
  setSelectedRowKeys = null,
  selectedRows = null,
  setSelectedRows = null,
  getCheckboxProps = null,
  rowClickable = false,
  selectedRowKey = null,
  setSelectedRowKey = null,
  selectedRow = null,
  setSelectedRow = null,
  dynamicWidth = true,
  scroll = true,
  defaultPageSize = 10,
}) {
  const { height, width } = useWindowDimensions();
  const sx = dynamicWidth ? { width: `${width - 105}px` } : {};

  return (
    <DefaultCard sx={sx}>
      <DefaultPageHeader
        pageName={PAGE_NAME}
        buttons={buttonsConfigurationList}
      />
      <DefaultTable
        rowKey={TABLE_DATA_UNIQUE_ID}
        dataSource={dataSource}
        displayColumns={displayColumns}
        getCheckboxProps={getCheckboxProps}
        selectedRowKeys={selectedRowKeys}
        setSelectedRowKeys={setSelectedRowKeys}
        selectedRows={selectedRows}
        setSelectedRows={setSelectedRows}
        rowClickable={rowClickable}
        selectedRowKey={selectedRowKey}
        setSelectedRowKey={setSelectedRowKey}
        selectedRow={selectedRow}
        setSelectedRow={setSelectedRow}
        dynamicWidth={dynamicWidth}
        scroll={scroll}
        defaultPageSize={defaultPageSize}
      />
    </DefaultCard>
  );
}

export function PageTableSectionWithCustomPageHeader({
  TABLE_DATA_UNIQUE_ID,
  displayColumns,
  dataSource,
  selectedRowKeys = null,
  setSelectedRowKeys = null,
  selectedRows = null,
  setSelectedRows = null,
  getCheckboxProps = null,
  rowClickable = false,
  selectedRowKey = null,
  setSelectedRowKey = null,
  selectedRow = null,
  setSelectedRow = null,
  dynamicWidth = true,
  scroll = true,
  defaultPageSize = 10,
  customPageHeader = null,
}) {
  const { height, width } = useWindowDimensions();
  const sx = dynamicWidth ? { width: `${width - 105}px` } : {};

  return (
    <DefaultCard sx={sx}>
      {customPageHeader}
      <DefaultTable
        rowKey={TABLE_DATA_UNIQUE_ID}
        dataSource={dataSource}
        displayColumns={displayColumns}
        getCheckboxProps={getCheckboxProps}
        selectedRowKeys={selectedRowKeys}
        setSelectedRowKeys={setSelectedRowKeys}
        selectedRows={selectedRows}
        setSelectedRows={setSelectedRows}
        rowClickable={rowClickable}
        selectedRowKey={selectedRowKey}
        setSelectedRowKey={setSelectedRowKey}
        selectedRow={selectedRow}
        setSelectedRow={setSelectedRow}
        dynamicWidth={dynamicWidth}
        scroll={scroll}
        defaultPageSize={defaultPageSize}
      />
    </DefaultCard>
  );
}
