import React from "react";
import { Row, Col } from "antd";
import TypeSummaryChart from "./components/TypeSummaryChart";
import TopSubnet from "./components/TopSubnet";
import IpAvailble from "./components/IpAvailble";
import DNSChart from "./components/DNSChart";
import TenSubnetTable from "./components/TenSubnetTable";
import TopOpenPorts from "./components/TopOpenPorts";
import { useSelector } from "react-redux";

import {
  selectTopTenSubnet,
  selectNcmChangeByVendor,
  selectIpAvailbility,
  selectTypeSummary,
  selectSubnetSummary,
  selectTopTenOpenPorts,
  selectDns,
} from "../../../store/features/ipamModule/dashboard/selectors";

import {
  useGetTopTenSubnetQuery,
  // useGetNcmChangeByVendorQuery,
  useGetIpAvailibilityQuery,
  useGetTypeSummaryQuery,
  useGetSubnetSummaryQuery,
  useGetTopTenOpenPortsQuery,
  useGetDnsQuery,
} from "../../../store/features/ipamModule/dashboard/apis";

function Index() {
  const {
    data: ipAvailibilityData,
    isSuccess: isIpAvailibilitySuccess,
    isLoading: isIpAvailibilityLoading,
    isError: isIpAvailibilityError,
    error: ipAvailibilityError,
  } = useGetIpAvailibilityQuery();
  const {
    data: typeSummaryData,
    isSuccess: isTypeSummarySuccess,
    isLoading: isTypeSummaryLoading,
    isError: isTypeSummaryError,
    error: typeSummaryError,
  } = useGetTypeSummaryQuery();
  const {
    data: subnetSummaryData,
    isSuccess: isSubnetSummarySuccess,
    isLoading: isSubnetSummaryLoading,
    isError: isSubnetSummaryError,
    error: subnetSummaryError,
  } = useGetSubnetSummaryQuery();
  const {
    data: topTenOpenPortsData,
    isSuccess: isTopTenOpenPortsSuccess,
    isLoading: isTopTenOpenPortsLoading,
    isError: isTopTenOpenPortsError,
    error: topTenOpenPortsError,
  } = useGetTopTenOpenPortsQuery();
  console.log("topTenOpenPortsData1",topTenOpenPortsData)
  const {
    data: dnsData,
    isSuccess: isDnsSuccess,
    isLoading: isDnsLoading,
    isError: isDnsError,
    error: dnsError,
  } = useGetDnsQuery();
  console.log("dnsData",dnsData)
  const apiResponse = {
    total_ip: 1048,
    used_ip: 580,
    available_ip: 735,
  };
  const data = [
    { vender: "A", counts: 50 },
    { vender: "B", counts: 80 },
    { vender: "C", counts: 90 },
    { vender: "D", counts: 50 },
    { vender: "E", counts: 80 },
    { vender: "F", counts: 90 },
  ];
 
  const chartData = {
    ports: ["Port 1", "Port 2", "Port 3", "Port 4", "Port 5", "Port 6"],
    values: [10, 20, 15, 10, 20, 15],
  };

  const dns=[
      { name: "not_resolved_ip", value: 30 },
      { name: "resolved_ip", value: 70 }
    ];
    const deviceType=[
      {name: 'cisco_ios_xe', value: 1},
    {name: 'cisco_ftd', value: 1},
    {name: 'cisco_ios', value: 4},
    {name: 'huawei', value: 1}]

    const data1=[{"name":[null,"22","23","26","29","34","110"],"value":[0,6,6,13,13,27,27]}]

  return (
    <div
      style={{
        backgroundColor: "#f0f2f5", // Grey background
        margin: "0px", // Equal margin around content
        minHeight: "100vh", // Ensure the background covers the entire viewport height
      }}
    >
      <Row gutter={[16, 16]} justify="space-between" style={{ marginBottom: "20px" }}>
        <Col span={8}>
          <div
            style={{
              backgroundColor: "#FFFFFF",
              borderRadius: "8px",
              height: "100%",
            }}
          >
            <h5 style={{ padding: "10px", margin: "0px", fontSize: "16px" }}>
              Type Summary
            </h5>
            <TypeSummaryChart
              data={typeSummaryData !== undefined ? typeSummaryData : []}
            />
          </div>
        </Col>

        <Col span={8}>
          <div
            style={{
              backgroundColor: "#FFFFFF",
              borderRadius: "8px",
              height: "100%",
            }}
          >
            <h5 style={{ padding: "10px", margin: "0px", fontSize: "16px" }}>
              Top 10 Subnets by % IP Address Used{" "}
            </h5>
            <TenSubnetTable />
          </div>
        </Col>
        <Col span={8}>
          <div
            style={{
              backgroundColor: "#FFFFFF",
              borderRadius: "8px",
              height: "100%",
            }}
          >
            <h5 style={{ padding: "10px", margin: "0px", fontSize: "16px" }}>
              Subnet Summary
            </h5>
            <TopSubnet
              data={subnetSummaryData !== undefined ? subnetSummaryData : []}
            />
          </div>
        </Col>
      </Row>
      <Row gutter={[16, 16]} justify="space-between" style={{ marginBottom: "20px", height:"100%" }}>
        <Col span={7}>
          <div
            style={{
              backgroundColor: "#FFFFFF",
              borderRadius: "8px",
              height: "400px",
            }}
          >
            <h5 style={{ padding: "10px", margin: "0px", fontSize: "16px" }}>
              IP Availability Summary{" "}
            </h5>

            <IpAvailble
              data={ipAvailibilityData !== undefined ? ipAvailibilityData : []}
            />
          </div>
        </Col>

        <Col span={10}>
          <div
            style={{
              backgroundColor: "#FFFFFF",
              borderRadius: "8px",
              height: "400px",
            }}
          >
            <h5 style={{ padding: "10px", margin: "0px", fontSize: "16px" }}>
              Top 10 Open Ports
            </h5>
            <TopOpenPorts
              data={
                topTenOpenPortsData !== undefined ? topTenOpenPortsData : []
              }
            
            />{" "}
          </div>
        </Col>
        <Col span={7}>
          <div
            style={{
              backgroundColor: "#FFFFFF",
              borderRadius: "8px",
              height: "400px",
            }}
          >
            <h5 style={{ padding: "10px", margin: "0px", fontSize: "16px" }}>
              DNS{" "}
            </h5>
            <div style={{ display: "flex" }}>
              <DNSChart
                data={dnsData !== undefined ? dnsData : []}
              />
            </div>
          </div>
        </Col>
      </Row>
    </div>
  );
}

export default Index;


