import React, { useEffect } from "react";
import * as echarts from "echarts";

const CredentialSummary = ({ data }) => {
  useEffect(() => {
    if (!data || !data.name || !data.value || data.name.length !== data.value.length) {
      console.error("Invalid data:", data);
      return;
    }

    var chartDom = document.getElementById("CredentialSummary");
    var myChart = echarts.init(chartDom);
    var option = {
      tooltip: {
        trigger: "axis",
        axisPointer: {
          lineStyle: {
            type: "line",
            color: "orange",
          },
        },
        label: {
          show: false,
        },
      },
      xAxis: {
        type: "category",
        boundaryGap: false,
        axisLine: {
          show: false,
        },
        axisTick: {
          show: false,
        },
        splitLine: {
          show: true,
        },
        axisLabel: {
          show: false,
        },
        data: data.name,
      },
      yAxis: {
        type: "value",
      },
      legend: {
        y: "bottom",
        icon: "circle",
        data: data.name,
      },
      series: data.name.map((name, index) => ({
        name: name,
        data: [data.value[index]], // Corrected this line
        type: "line",
        smooth: true,
        itemStyle: {
          color: index === 0 ? "green" : index === 1 ? "blue" : "grey",
        },
        emphasis: {
          focus: "series",
        },
      })),
    };
    option && myChart.setOption(option);
    return () => {
      myChart.dispose();
    };
  }, [data]);

  return (
    <div id="CredentialSummary" style={{ width: "100%", height: "400px" }}></div>
  );
};

export default CredentialSummary;
