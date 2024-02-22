import React from "react";
import { Table } from "antd";
import { selectNcmDeviceSummaryTable } from "../../../../store/features/ncmModule/dashboard/selectors";
import { useGetNcmDeviceSummaryTableQuery } from "../../../../store/features/ncmModule/dashboard/apis";
import { useSelector } from "react-redux";

function NcmDeviceSummaryTable() {
  const {
    data: ncmTableData,
    isSuccess: isNcmTableSuccess,
    isLoading: isNcmTableLoading,
    isError: isNcmTableError,
    error: recentNcmTableError,
  } = useGetNcmDeviceSummaryTableQuery();

  const ncmTable = useSelector(selectNcmDeviceSummaryTable);

  // console.log('ncmTable', ncmTable);

  const dataSource = ncmTableData || []; // Use API response data or provide a default empty array

  const columns = [
    { title: "Device Type", dataIndex: "device_type", key: "device_type" },
    { title: "Vendor ", dataIndex: "vendor", key: "vendor" },
    { title: "OS Type", dataIndex: "function", key: "function" },
    { title: "Devices", dataIndex: "device_count", key: "device_count" },
  ];

  return (
    <div style={{ padding: "0px 15px" }}>
      <Table dataSource={dataSource} columns={columns}  />
    </div>
  );
}

export default NcmDeviceSummaryTable;
