import React, { useEffect } from "react";
import * as echarts from "echarts";

const SortBySeverity = ({ data }) => {
  useEffect(() => {
    const chartDom = document.getElementById("Severity");
    const myChart = echarts.init(chartDom);
    const createSeries = (name, value) => ({
      type: "bar",
      data: [value],
      coordinateSystem: "polar",
      name,
      color: "green",
      showBackground: true,
      emphasis: {
        focus: "series",
        label: {
          show: true,
          position: "inside",
          formatter: "{c}%",
          fontSize: 30,
          fontWeight: "bold",
          color: "black",
        },
      },
    });
    const option = {
      tooltip: { show: false },
      angleAxis: {
        max: 100,
        axisLabel: { show: false },
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { show: false },
      },
      radiusAxis: {
        type: "category",
        axisLabel: { show: false },
        axisLine: { show: false },
        axisTick: { show: false },
      },
      polar: { radius: [80, "70%"] },
      series: data.map(({ name, value }) =>
        createSeries(name, value)
      ),
      backgroundStyle: { color: "rgba(180, 180, 180, 0.2)" },
      itemStyle: { borderRadius: [20, 20, 20, 20] },
      legend: { show: true, icon: "circle", itemGap: 20, y: "bottom" },
    };
    myChart.setOption(option);
    return () => myChart.dispose();
  }, [data]);
  
  return <div id="Severity" style={{ width: "100%", height: "400px" }} />;
};

export default SortBySeverity;
