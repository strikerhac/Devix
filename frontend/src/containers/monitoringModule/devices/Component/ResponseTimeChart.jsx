import React, { useEffect } from "react";
import * as echarts from "echarts";
const GaugeChart = ({ id, value, color, title }) => {
  useEffect(() => {
    var responseTimeChart = document.getElementById("responseTime");
    var responseTimeChartInstance = echarts.init(responseTimeChart);
    var responseTimeOption = {
      series: [
        {
          type: "gauge",
          progress: {
            show: false,
          },
          splitLine: {
            show: false,
          },
          axisLine: {
            show: false,
          },
          axisTick: {
            show: false,
          },
          axisLabel: {
            show: false,
          },
          pointer: {
            show: false,
          },
          anchor: {
            show: false,
          },
          title: {
            show: true,
            fontSize: 24,
            offsetCenter: [0, "-35%"],
          },
          detail: {
            valueAnimation: true,
            offsetCenter: [0, "-60%"],
            formatter: `{value}ms `,
          },
          data: [
            {
              value: 8,
              name: "Response Time",
            },
          ],
        },
      ],
    };
    responseTimeOption &&
      responseTimeChartInstance.setOption(responseTimeOption);
    var chartDom = document.getElementById(id);
    var myChart = echarts.init(chartDom);
    var option = {
      series: [
        {
          startAngle: 180,
          endAngle: 0,
          type: "gauge",
          max: 100,
          radius: "100%",
          axisLine: {
            lineStyle: {
              color: [[1, color]],
              width: 25,
            },
          },
          splitLine: {
            show: "",
          },
          axisTick: {
            show: "",
          },
          axisLabel: {
            show: "",
          },
          anchor: {
            show: true,
            showAbove: true,
            icon: "circle",
            size: 15,
            itemStyle: {
              color: color,
            },
          },
          pointer: {
            length: "65%",
            icon: "path://M2090.36389,615.30999 L2090.36389,615.30999 C2091.48372,615.30999 2092.40383,616.194028 2092.44859,617.312956 L2096.90698,728.755929 C2097.05155,732.369577 2094.2393,735.416212 2090.62566,735.56078 C2090.53845,735.564269 2090.45117,735.566014 2090.36389,735.566014 L2090.36389,735.566014 C2086.74736,735.566014 2083.81557,732.63423 2083.81557,729.017692 C2083.81557,728.930412 2083.81732,728.84314 2083.82081,728.755929 L2088.2792,617.312956 C2088.32396,616.194028 2089.24407,615.30999 2090.36389,615.30999 Z",
            itemStyle: {
              color: color,
            },
          },
          detail: {
            valueAnimation: true,
            formatter: `{value}% `,
            offsetCenter: [10, "25%"],
          },
          title: {
            text: title,
            offsetCenter: [0, "60%"],
            textStyle: {
              fontSize: 16,
            },
          },
          data: [
            {
              value: value,
              name: title,
            },
          ],
        },
        {
          startAngle: 180,
          endAngle: 0,
          type: "gauge",
          radius: "70%",
          axisLine: {
            lineStyle: {
              color: [[1, color]],
              width: 5,
            },
          },
          splitLine: {
            show: "",
          },
          axisTick: {
            show: "",
          },
          axisLabel: {
            show: "",
          },
        },
      ],
    };
    option && myChart.setOption(option);
    return () => {
      myChart.dispose();
    };
  }, [id, value, color, title]);
  return (
    <>
      <div id={id} style={{ flex: "1", margin: "0px 20px", height: "350px" }}></div>
    </>
  );
};
const ResponseTimeChart = () => {
  return (
    <div style={{ display: "flex" }}>
     <GaugeChart
  id="Availability"
  value={100}
  color='#4CA749'
  title="Availability"
/>
      <GaugeChart id="PacketLoss" value={0} color="#DD0707" title="Packet Loss" />
      <GaugeChart
        id="responseTime"
        style={{ width: "50%", height: "300px", float: "left" }}
      ></GaugeChart>
      <GaugeChart
        id="CPUUtilisation"
        value={4}
        color="#FFCB47"
        title="CPU Utilisation"
      />
      <GaugeChart
        id="MemoryUtilisation"
        value={34.59}
        color="#0F4EEE"
        title="Memory Utilisation"
      />
    </div>
  );
};
export default ResponseTimeChart;