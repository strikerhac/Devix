import React from 'react';
import { Table, Progress } from 'antd';
import { useSelector } from "react-redux";


import {
selectTopTenSubnet,
// selectNcmChangeByVendor

} from "../../../../store/features/ipamModule/dashboard/selectors";


import {
useGetTopTenSubnetQuery,
// useGetNcmChangeByVendorQuery

} from "../../../../store/features/ipamModule/dashboard/apis";

const columns = [
  {
    title: 'Subnet',
    dataIndex: 'subnet',
    key: 'subnet',
    align: 'start',
    render: text => <a style={{ display: 'block', fontWeight: '600', color: 'green' }}>{text}</a>,
  },
  {
    title: 'Progress',
    dataIndex: 'value',
    key: 'value',
    align: 'start',
    render: (_, record) => (
      <Progress
        percent={record.value}  // Use the actual percentage value from your data
        status="active"
        strokeColor={record.value > 50 ? '#FF0000' : { from: '#108ee9', to: '#87d068' }}
      />
    ),
  },
];  

const data = [
  {
    key: '1',
    subnet: '10..66.211.141',
    value: "50"
  },
  {
    key: '2',
    subnet: '10..66.211.141',
    value: "10"
  },
  {
    key: '3',
    subnet: '1',
    value: "60"
  },
];

const TenSubnetTable = () => {
  const getRowClassName = (record, index) => {
    return index % 2 === 0 ? 'dark-row' : 'light-row';
  };


  const {
    data: topTenData,
    isSuccess: isTopTenSuccess,
    isLoading: isTopTenLoading,
    isError: isTopTenError,
    error: topTenError,
   
  } = useGetTopTenSubnetQuery();

  console.log("husnain",topTenData)


  return (
    <Table
    dataSource={topTenData || []}
    columns={columns}
    pagination={false}
    bordered={false}
    rowClassName={getRowClassName}
    style={{ border: 'none', overflow: "scroll", height: "400px",padding:"0 20px" }}
    headerStyle={{ background: 'black', color: 'white' }}
  />
  
  );
};

export default TenSubnetTable;
