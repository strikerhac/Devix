import React, { useEffect } from "react";
import * as echarts from "echarts";

const TopSubnet = ({ data }) => {
  useEffect(() => {
    if (!data || !Array.isArray(data)) return;

    const chartDom = document.getElementById("subnet");
    const myChart = echarts.init(chartDom);

    const discoveredAddedEntry = data.find(entry => entry.name === "discovered_added");
    const manuallyAddedEntry = data.find(entry => entry.name === "manually_added");

    const discoveredAddedValue = discoveredAddedEntry ? discoveredAddedEntry.value : 0;
    const manuallyAddedValue = manuallyAddedEntry ? manuallyAddedEntry.value : 0;

    const option = {
      angleAxis: {
        max: 6,
        axisLabel: {
          show: false,
        },
        axisLine: {
          show: false,
        },
        axisTick: {
          show: false,
        },
        splitLine: {
          show: false,
        },
      },
      radiusAxis: {
        type: "category",
        axisLabel: {
          show: false,
        },
        axisLine: {
          show: false,
        },
        axisTick: {
          show: false,
        },
      },
      polar: {
        radius: [80, "80%"],
        center: ["50%", "40%","50%", "50%"], // Adjusted center to be in the middle horizontally and at the top vertically
      },
      series: [
        {
          type: "bar",
          data: [discoveredAddedValue],
          coordinateSystem: "polar",
          name: "Discovered from Devices",
          color: "orange",
          showBackground: true,
          backgroundStyle: {
            color: "rgba(180, 180, 180, 0.2)",
          },
          itemStyle: {
            borderRadius: [20, 20, 20, 20],
          },
          emphasis: {
            focus: "series",
          },
        },
        {
          type: "bar",
          data: [manuallyAddedValue],
          coordinateSystem: "polar",
          name: "Manual Added",
          showBackground: true,
          backgroundStyle: {
            color: "rgba(180, 180, 180, 0.2)",
          },
          itemStyle: {
            borderRadius: [20, 20, 20, 20],
          },
          emphasis: {
            focus: "series",
          },
        },
      ],
      graphic: [
        {
          type: "text",
          left: "center",
          top: "center",
          style: {
            text: "Alarms",
            fill: "black",
            fontSize: 18,
          },
        },
      ],
      legend: {
        show: true,
        data: ["Manual Added", "Discovered from Devices"],
        icon: "circle",
        itemGap: 20,
        bottom:20
      },
    };

    myChart.setOption(option);

    return () => {
      myChart.dispose();
    };
  }, [data]);

  return <div id="subnet" style={{ width: "100%", height: "400px" }} />;
};

export default TopSubnet;
