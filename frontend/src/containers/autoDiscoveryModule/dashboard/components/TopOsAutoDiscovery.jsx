import React, { useEffect } from "react";
import * as echarts from "echarts";

function TopOsAutoDiscovery({ data }) {
  // Extracting names and values from data
  const names = data.map(item => item.name);
  const values = data.map(item => item.value);

  useEffect(() => {
    const chartDom = document.getElementById("topOsChart");
    const myChart = echarts.init(chartDom);
    const option = {
      tooltip: {
        trigger: "axis",
      },
      legend: {
        data: names,
        y: "bottom",
      },
      xAxis: {
        type: "category",
        boundaryGap: false,
        axisLine: {
          show: "",
        },
        axisTick: {
          show: "",
        },
        data: names,
      },
      yAxis: {
        type: "value",
      },
      series: [
        {
          name: "Value",
          type: "line",
          data: values,
        },
      ],
    };
    myChart.setOption(option);
    return () => {
      myChart.dispose();
    };
  }, [data, names, values]);

  return (
    <div id="topOsChart" style={{ width: "100%", height: "400px" }}></div>
  );
}

export default TopOsAutoDiscovery;
