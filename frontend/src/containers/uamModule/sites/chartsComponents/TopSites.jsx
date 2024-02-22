
import React, { useEffect } from "react";
import * as echarts from "echarts";
const TopSites = () => {
  useEffect(() => {
    const chartDom = document.getElementById("main");
    const myChart = echarts.init(chartDom);
    const option = {
    //   title: { text: "Device Type" },
      xAxis: {
        type: "category",
        data: [
          "CISCO 1900 IS Series",
          "Citrix NetScaler Virtual",
          "Palo Alto PAVM",
          "Fortinet fgt100",
          "Citrix NetScaler Virtual",
        ],
        axisLine: { show: false }, // Hide the x-axis line
        axisTick: { show: false }, // Hide the x-axis ticks
        axisLabel: {
          interval: 0,
          rotate: 0,
          formatter: (value) => value.split(" ").join("\n"),
        },
      },
      yAxis: { type: "value" },
      series: [
        {
          data: [120, 180, 150, 80, 70],
          type: "bar",
          showBackground: true,
          backgroundStyle: {
            color: "rgba(180, 180, 180, 0.2)",
            borderRadius: [20, 20, 0, 0],
          },
          itemStyle: { color: "#66B127", borderRadius: [20, 20, 0, 0] },
        },
      ],
    };
    myChart.setOption(option);
    return () => myChart.dispose();
  }, []);
  return <div id="main" style={{ width: "100%", height: "400px" }} />;
};
export default TopSites;