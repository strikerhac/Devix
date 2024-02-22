import React, { useEffect } from "react";
import * as echarts from "echarts";
const TopVendorForDiscovery = () => {
  useEffect(() => {
    const chartDom = document.getElementById("main");
    const myChart = echarts.init(chartDom);
    const option = {
      title: [
        {
          text: "Configuration Backup Summary",
        },
      ],
      tooltip: {
        label: {
          show: false,
        },
      },
      angleAxis: {
        type: "category",
        startAngle: 270,
        axisLine: {
          show: false,
        },
        axisLabel: {
          show: false,
        },
        axisTick: {
          show: false,
        },
      },
      radiusAxis: {
        max: 12,
        startAngle: 90,
        axisLine: {
          show: false,
        },
        axisLabel: {
          show: false,
        },
        axisTick: {
          show: false,
        },
      },
      polar: {
        radius: [2, "80%"],
      },
      series: [
        {
          type: "bar",
          data: [10],
          coordinateSystem: "polar",
          name: "Backup Successful",
          color: "green",
        },
        {
          type: "bar",
          data: [5],
          coordinateSystem: "polar",
          name: "Backup Failure",
          color: "red",
        },
        {
          type: "bar",
          data: [7],
          coordinateSystem: "polar",
          name: "Not Backup",
          color: "orange",
        },
      ],
      legend: {
        show: true,
        y: "bottom",
        icon: "circle",
      },
      emphasis: {
        focus: "series",
      },
      barGap: "3%",
    };
    option && myChart.setOption(option);
    return () => {
      myChart.dispose();
    };
  }, []);
  return <div id="main" style={{ width: "100%", height: "400px" }}></div>;
};
export default TopVendorForDiscovery;