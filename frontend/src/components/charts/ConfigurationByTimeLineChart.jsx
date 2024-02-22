
import React, { useEffect } from "react";
import * as echarts from "echarts";

const ConfigurationByTimeLineChart = ({ data }) => {
  useEffect(() => {
    const chartDom = document.getElementById("main");
    const myChart = echarts.init(chartDom);
    
    const option = {
    //   title: { text: "Device Type" },
      xAxis: {
        type: "category",
        data: data.map(item => item.name),
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
          data: data.map(item => item.value),
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
  }, [data]);

  return <div id="main" style={{ width: "100%", height: "400px" }} />;
};

export default ConfigurationByTimeLineChart;

