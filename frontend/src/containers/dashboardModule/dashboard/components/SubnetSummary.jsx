import React, { useEffect } from "react";
import * as echarts from "echarts";
const SubnetSummary = () => {
  useEffect(() => {
    var chartDom = document.getElementById("Subnet Summary");
    var myChart = echarts.init(chartDom);
    var option;
    option = {
    //   title: {
    //     text: "Subnet Summary",
    //   },
      tooltip: {
        trigger: "axis",
      },
      xAxis: {
        type: "category",
        data: ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul"],
        boundaryGap: false,
        axisLine: {
          show: "",
        },
        axisTick: {
          show: "",
        },
        splitLine: {
          show: true,
        },
      },
      yAxis: {
        type: "value",
        axisLine: {
          show: "",
        },
      },
      legend: {
        y: "bottom",
        icon: "circle",
      },
      series: [
        {
          name: "Mannual Added",
          type: "line",
          data: [20, 32, 10, 34, 10, 25, 10],
          symbol: "circle",
          symbolSize: 8,
          itemStyle: {
            color: "purple",
          },
          emphasis: {
            focus: "series",
          },
        },
        {
          name: "DHCP",
          type: "line",
          symbol: "circle",
          symbolSize: 8,
          data: [-10, 42, 20, 44, 19, 10, 41],
          itemStyle: {
            color: "blue",
          },
          emphasis: {
            focus: "series",
          },
        },
        {
          name: "Discovered from Devices",
          type: "line",
          symbol: "circle",
          symbolSize: 8,
          data: [15, 12, 40, 14, 30, -10, 20],
          itemStyle: {
            color: "green",
          },
          emphasis: {
            focus: "series",
          },
        },
      ],
    };
    option && myChart.setOption(option);
    return () => {
      myChart.dispose();
    };
  }, []);
  return <div id="Subnet Summary" style={{ width: "100%", height: "400px" }}></div>;
};
export default SubnetSummary;