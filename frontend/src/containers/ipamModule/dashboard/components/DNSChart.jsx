import React, { useEffect } from "react";
import * as echarts from "echarts";

const DNSChart = ({ data }) => {
  useEffect(() => {
    if (!data || !Array.isArray(data)) return;

    const notResolvedEntry = data.find(entry => entry.name === "not_resolved_ip");
    const resolvedEntry = data.find(entry => entry.name === "resolved_ip");

    const notResolvedValue = notResolvedEntry ? notResolvedEntry.value : 0;
    const resolvedValue = resolvedEntry ? resolvedEntry.value : 0;

    const notResolvedChartDom = document.getElementById("notresolved");
    const notResolvedChart = echarts.init(notResolvedChartDom);

    const notResolvedOption = {
      angleAxis: {
        max: 100,
        startAngle: 0,
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
        radius: [50, "100%"],
      },
      series: [
        {
          type: "bar",
          data: [notResolvedValue],
          coordinateSystem: "polar",
          name: "Not Resolved",
          color: "red",
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
            text: `${notResolvedValue}%`,
            fill: "black",
            fontSize: 24,
            fontWeight: "bold",
          },
        },
      ],
      legend: {
        show: true,
        data: ["Not Resolved"],
        icon: "none",
        bottom:10,
        align: "center",
        textStyle: {
          fontWeight: "bold",
        },
      },
    };

    notResolvedChart.setOption(notResolvedOption);

    const resolvedChartDom = document.getElementById("resolved");
    const resolvedChart = echarts.init(resolvedChartDom);

    const resolvedOption = {
      angleAxis: {
        max: 100,
        startAngle: 0,
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
        radius: [50, "100%"],
      },
      series: [
        {
          type: "bar",
          data: [resolvedValue],
          coordinateSystem: "polar",
          name: "Resolved",
          color: "green", // Choose your desired color
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
            text: `${resolvedValue}%`,
            fill: "black",
            fontSize: 24,
            fontWeight: "bold",
          },
        },
      ],
      legend: {
        show: true,
        data: ["Resolved"],
        icon: "none",
        bottom:10,
        align: "center",
        textStyle: {
          fontWeight: "bold",
        },
      },
    };

    resolvedChart.setOption(resolvedOption);

    return () => {
      notResolvedChart.dispose();
      resolvedChart.dispose();
    };
  }, [data]);

  return (
    <>
      <div id="notresolved" style={{ width: "50%", height: "350px" }} />
      <div id="resolved" style={{ width: "50%", height: "350px" }} />
    </>
  );
};

export default DNSChart;
