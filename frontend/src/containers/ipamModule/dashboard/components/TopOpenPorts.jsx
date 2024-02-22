import React, { useEffect } from "react";
import * as echarts from "echarts";

const TopOpenPorts = ({ data }) => {
  useEffect(() => {
    const chartDom = document.getElementById("main");
    const myChart = echarts.init(chartDom);

    if (!data || data.length === 0 || !data[0].value) {
      // Handle the case when data is not available or the value property is missing
      return;
    }

    const option = {
      xAxis: {
        type: "category",
        data: data[0].name ? data[0].name.slice(1) : [], // Null check for the "name" property
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
          data: data[0].value ? data[0].value.slice(1) : [], // Null check for the "value" property
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

export default TopOpenPorts;
