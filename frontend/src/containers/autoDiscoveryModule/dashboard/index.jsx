import React, { useEffect } from "react";
import { Row, Col } from "antd";

import ConfigurationChangeByVendor from "../../../components/charts/ConfigurationChangeByVendor";
// import { selectTableData } from "../../../store/features/ncmModule/dashboard/selectors";
import { useSelector } from "react-redux";
import {
  selectSnmpStatus,
  selectCredentialsSummary,
  selectTopVendorForDiscovery,
  selectTopOs,
  selectCountPerFunction
} from "../../../store/features/autoDiscoveryModule/dashboard/selectors";
import {
  useGetSnmpStatusQuery,
  useGetCredentialsSummaryQuery,
  useGetTopVendorForDiscoveryQuery,
  useGetTopOsQuery,
  useGetCountPerFunctionQuery,
  
} from "../../../store/features/autoDiscoveryModule/dashboard/apis";
import "./index.css";
import TopOpenPorts from "../../ipamModule/dashboard/components/TopOpenPorts";
import CredentialSummary from "./components/CredentialSummary";
import SnmpStatus from "./components/SnmpStatus";
import TopOsAutoDiscovery from "./components/TopOsAutoDiscovery";
import TopVendorForDiscovery from "./components/TopVendorForDiscovery";
import CountPerFuntion from "./components/CountPerFuntion";
import { useGetEolQuery } from "../../../store/features/dashboardModule/dashboard/apis";

function Index() {
  

  const {
    data: snmpStatusData,
    isSuccess: isSnmpStatusSuccess,
    isLoading: isSnmpStatusLoading,
    isError: isSnmpStatusError,
    error: SnmpStatusError,
  } = useGetSnmpStatusQuery();
  const {
    data: credentialsSummaryData,
    isSuccess: isCredentialsSummarySuccess,
    isLoading: isCredentialsSummaryLoading,
    isError: isCredentialsSummaryError,
    error: credentialsSummaryError,
  } = useGetCredentialsSummaryQuery();
  const {
    data: topVendorData,
    isSuccess: isTopVendorSuccess,
    isLoading: isTopVendorLoading,
    isError: isTopVendorError,
    error: topVendorError,
  } = useGetTopVendorForDiscoveryQuery();
  const {
    data: topOsData,
    isSuccess: isTopOsSuccess,
    isLoading: isTopOsLoading,
    isError: isTopOsError,
    error: topOsError,
  } = useGetTopOsQuery();


  const {
    data: countPerFunctionData,
    isSuccess: isCountPerFunctionSuccess,
    isLoading: isCountPerFunctionLoading,
    isError: isCountPerFunctionError,
    error: countPerFunctionError,
  } = useGetCountPerFunctionQuery();
  console.log("snmpStatusDataHUnsain",snmpStatusData)
  console.log("credentialsSummaryData",credentialsSummaryData)
  console.log("topVendorData",topVendorData)
  console.log("topOsData",topOsData)
  console.log("countPerFunctionData",countPerFunctionData)

  

  const companyData = {
    Cisco: 50,
    Fortinet: 10,
    PaloAlto: 5,
    Huawai: 3,
    Linux: 50,
    Citrix: 10,
    Hp: 20,
    Juniper: 10,
  };


  const apiResponse = [
    {
      name: "Sales",
      value: 4200
    },
    {
      name: "Admin",
      value: 3000
    },
    {
      name: "Inform",
      value: 20000
    },
    {
      name : "Customer",
      value: 35000
    },
   
  ];
  const data=[
    { name: "Windows_1", value: 4200 },
    { name: "Linux_1", value: 8200 },
    { name: "IOS_1", value: 3200 },
 
  ];


  const chartData = {
    ports: ['Port 1', 'Port 2', 'Port 3', 'Port 4'],
    counts: [10, 20, 15, 30],
  };

  const sampleData = {
    name: ['SNMP V1/V2', 'SNMP V3', 'SSH Login'],
    value: [3, 0, 23]
  };
 
  
 const count= [
    {
        "name": "Router",
        "value": 29
    },
    {
        "name": "General purpose",
        "value": 20
    },
    {
        "name": "Specialized",
        "value": 2
    },
    {
        "name": "Firewall",
        "value": 1
    },
    {
        "name": "Remote management",
        "value": 1
    }
] ;
 return (
    <>
      <Row gutter={[32, 32]} justify="space-between">
        <Col span={7}>
          <div className="container">
            <h6 className="heading">SNMP Status </h6>
            <SnmpStatus
             responseData={snmpStatusData !== undefined? snmpStatusData:[]} 
            // responseData={apiResponse}
             /> 
                      </div>
        </Col>

        <Col span={10}>
          <div className="container">
            <h6 className="heading">Credentials Summary </h6>
            <CredentialSummary 
    data={credentialsSummaryData !== undefined ? credentialsSummaryData : []} 

/>
          </div>
        </Col>
        <Col span={7}>
          <div className="container">
            <h6 className="heading">Top Vendors For Discovery</h6>
            <TopVendorForDiscovery data={topVendorData !== undefined? topVendorData:[]} />
          </div>
        </Col>
      </Row>

      <Row gutter={[24, 24]} justify="space-between" className="page_row">
        <Col span={16} xs={24} sm={24} md={16} lg={16} xl={16}>
          <div className="container">
            <h6 className="heading">Top OS in Auto Discovery</h6>
            <TopOsAutoDiscovery data={data !== undefined? data:[]}
 
/>

          </div>
        </Col>

        <Col span={8} xs={24} sm={24} md={16} lg={8} xl={8}>
          <div className="container">
            <h6 className="heading">Count Per Function</h6>
           
            

            <CountPerFuntion chartData={countPerFunctionData} />
          </div>
        </Col>
      </Row>
    </>
  );
}

export default Index;
