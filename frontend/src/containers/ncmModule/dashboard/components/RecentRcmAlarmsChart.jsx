import React from 'react';
import RcmAlarmsChart from '../../../../components/charts/RcmAlarms';
import RcmAlarmDeviceTable from '../components/RcmAlarmDeviceTable';
import {
  selectRecentRcmAlarms,
  selectRecentRcmAlarmsCount
} from "../../../../store/features/ncmModule/dashboard/selectors";
import {
  useGetRecentRcmAlarmsQuery,
  useGetRecentRcmAlarmsCountQuery,
} from "../../../../store/features/ncmModule/dashboard/apis";
import { useSelector } from "react-redux";

function RecentRcmAlarmsChart() {
  const {
    data: rcmData,
    isSuccess: isRcmSuccess,
    isLoading: isRcmLoading,
    isError: isRcmError,
    error: recentRcmAlarmsError,
  } = useGetRecentRcmAlarmsQuery();

  const {
    data: rcmAlarmsCountData,
    isSuccess: isRcmAlarmsCountSuccess,
    isLoading: isRcmAlarmsCountLoading,
    isError: isRcmAlarmsCountError,
    error: recentRcmAlarmsCountError,
  } = useGetRecentRcmAlarmsCountQuery();

  const recentRcmAlarms = useSelector(selectRecentRcmAlarms);
  const recentRcmAlarmsCount = useSelector(selectRecentRcmAlarmsCount);

  // console.log("recentRcmAlarms", recentRcmAlarms);
  // console.log("recentRcmAlarmsCount", recentRcmAlarmsCount);

  return (
    <div style={{ display: "flex", justifyContent: "space-between" }}>
      <div style={{ padding: "5px 10px 0px 0px", display: "flex", justifyContent: "center", flexBasis: "50%" }}>
        <RcmAlarmsChart data={recentRcmAlarmsCount} />
      </div>

      <div style={{ padding: "5px 10px 0px 0px", display: "flex", justifyContent: "center", flexBasis: "30%" }}>
        <RcmAlarmDeviceTable data={recentRcmAlarms} />
      </div>
    </div>
  );
}

export default RecentRcmAlarmsChart;
