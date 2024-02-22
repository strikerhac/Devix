import React, { useEffect } from "react";
import { Row, Col } from "antd";
import ConfigurationBackupSummary from "./components/ConfigurationBackupSummary";
// import ConfigurationByTimeLineChart from './ConfigurationByTimeLineChart';
import Compliance from "./components/Compliance";
import ChangeByTimeChart from "./components/ChangeByTimeChart";
import RecentRcmAlarmsChart from "./components/RecentRcmAlarmsChart";
import RcmAlarms from "../../../components/charts/RcmAlarms";

import NcmDeviceSummaryTable from "./components/NcmDeviceSummaryTable";
import ConfigurationChangeByVendor from "./components/ConfigurationChangeByVendor";
import {
  selectConfigurationBackupSummary,
  selectConfigurationChangeByDevice,
  selectNcmChangeByVendor,
} from "../../../store/features/ncmModule/dashboard/selectors";
import { useSelector } from "react-redux";

import {
  useGetConfigurationChangeByDeviceQuery,
  useGetConfigurationBackupSummaryQuery,
  useGetNcmChangeByVendorQuery,
} from "../../../store/features/ncmModule/dashboard/apis";
import "./index.css";
import ConfigurationByTimeLineChart from "../../../components/charts/ConfigurationByTimeLineChart";
import RcmAlarmDeviceTable from "./components/RcmAlarmDeviceTable";

function Index() {
  const {
    data: fetchRecordsData,
    isSuccess: isFetchRecordsSuccess,
    isLoading: isFetchRecordsLoading,
    isError: isFetchRecordsError,
    error: fetchRecordsError,
  } = useGetConfigurationChangeByDeviceQuery();

  const {
    data: backupSummaryData,
    isSuccess: isBackupSummarySuccess,
    isLoading: isBackupSummaryLoading,
    isError: isBackupSummaryError,
    error: backupSummaryError,
  } = useGetConfigurationBackupSummaryQuery();
  console.log("backupSummaryData",backupSummaryData)
  const {
    data: vendorData,
    isSuccess: isVendorSuccess,
    isLoading: isVendorLoading,
    isError: isVendorError,
    error: vendorError,
  } = useGetConfigurationBackupSummaryQuery();
  const {
    data: ncmData,
    isSuccess: isNcmSuccess,
    isLoading: isNcmLoading,
    isError: isNcmError,
    error: ncmError,
  } = useGetNcmChangeByVendorQuery();

  console.log("vendor data ", vendorData);

  const backupSummary = useSelector(selectConfigurationBackupSummary);
  const timeLineChart = useSelector(selectConfigurationChangeByDevice);
  const graph = useSelector(selectNcmChangeByVendor);

  console.log("backupSummaryhusnain", backupSummaryData);
  // console.log("timeLineChart", timeLineChart);

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
  const backsummary = {
    backupSuccess: 4.2,
    backupFailure: 2,
    notBackup: 1,
  };

  const deviceType=[
  {name: 'cisco_ios_xe', value: 1},
{name: 'cisco_ftd', value: 1},
{name: 'cisco_ios', value: 4},
{name: 'huawei', value: 1}]
  return (
    <>
      <Row gutter={[32, 32]} justify="space-between">
        <Col span={8}>
          <div className="container">
            <h6 className="heading">Configuration Backup Summary</h6>
            <ConfigurationBackupSummary data={backupSummaryData !==undefined? backupSummaryData:[]} />
          </div>
        </Col>

        <Col span={8}>
          <div className="container">
            <h6 className="heading">Configuration Change by Device</h6>
            <ConfigurationByTimeLineChart  data={deviceType}/>
          </div>
        </Col>
        <Col span={8}>
          <div className="container">
            <h6 className="heading">Compliance</h6>
            <Compliance />
          </div>
        </Col>
      </Row>

      <Row gutter={[24, 24]} justify="space-between" className="page_row">
        <Col span={14}>
          <div className="container">
            <h6 className="heading">Recent RCM Alarms</h6>

            <RecentRcmAlarmsChart />
          </div>
        </Col>
        <Col span={10}>
          <div className="container">
            <h6 className="heading">NCM Device Summary</h6>
            <NcmDeviceSummaryTable />
          </div>
        </Col>
      
      </Row>

      <Row gutter={[24, 24]} justify="space-between" className="page_row">
        <Col span={24}>
          <div className="container">
            <h6 className="heading">Configuration Change by Vendor</h6>
            <ConfigurationChangeByVendor
              deviceNames={[
                "Cisco",
                "Fortinet",
                "Citrix",
                "PaloAlto",
                "NetScaler",
              ]}
              time={["11:00", "11:30", "12:00", "12:30", "01:00"]}
              values={[5, 10, 6]}
            />
          </div>
        </Col>

       
      </Row>
    </>
  );
}

export default Index;
