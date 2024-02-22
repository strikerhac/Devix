
import React, { useEffect } from "react";
import * as echarts from "echarts";

const DataCenterStatusChart = () => {
  useEffect(() => {
    const chartDom = document.getElementById("status");
    const myChart = echarts.init(chartDom);
    const option = {
      legend: {
        bottom: 10,
        icon: "circle",
      },
      series: [
        {
          type: "pie",
          radius: [80, 150],
          center: ["50%", "50%"],
          roseType: "area",
          startAngle: 30,
          label: {
            show: true,
            position: "inside",
            formatter: ({ value }) => value,
            textStyle: {
              color: "white",
            },
          },
          data: [
            { value: 40, name: "Type A", itemStyle: { color: "#009900" } }, // Adjusted data values
            { value: 30, name: "Type B", itemStyle: { color: "#32CD32" } }, // Adjusted data values
            { value: 20, name: "Type C", itemStyle: { color: "#8FBC8F" } }, // Adjusted data values
          ],
        },
      ],
    };
    myChart.setOption(option);
    return () => {
      myChart.dispose();
    };
  }, []);

  return <div id="status" style={{ width: "100%", height: "400px" }}></div>;
};

export default DataCenterStatusChart;
