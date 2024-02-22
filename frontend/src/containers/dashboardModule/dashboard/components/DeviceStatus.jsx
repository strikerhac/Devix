import React, { useEffect } from "react";
import * as echarts from "echarts";

const Graphs = (name, value, color) => ({
  title: { 
    text: name, 
    bottom: 10, 
    left: 'center', // Align title to the center
    textStyle: { // Style for the title text
      fontWeight: 'bold',
      fontSize: 16,
      color: '#333', // Adjust color as needed
    }
  }, 
  series: [
    {
      type: "gauge",
      progress: { show: true, width: 20, itemStyle: { color } },
      axisLine: { lineStyle: { width: 20 } },
      axisTick: { show: true },
      splitLine: { length: 15 },
      axisLabel: { distance: 30, fontSize: 10 },
      anchor: {
        show: true,
        showAbove: true,
        size: 15,
        itemStyle: { borderWidth: 5, borderColor: color },
      },
      pointer: {
        icon: "path://M2.9,0.7L2.9,0.7c1.4,0,2.6,1.2,2.6,2.6v115c0,1.4-1.2,2.6-2.6,2.6l0,0c-1.4,0-2.6-1.2-2.6-2.6V3.3C0.3,1.9,1.4,0.7,2.9,0.7z",
        width: 5,
        length: "40%",
        itemStyle: { color },
      },
      detail: {
        valueAnimation: true,
        formatter: `{value}% Usage`,
        fontSize: 12,
        offsetCenter: [0, "100%"],
      },
      data: [{ value }],
    },
  ],
});

const DeviceStatus = ({ categories }) => {
  useEffect(() => {
    const myCharts = categories.map((category) =>
      echarts.init(document.getElementById(`Graph${category.name}`))
    );
    categories.forEach((category, index) =>
      myCharts[index].setOption(
        Graphs(category.name, category.value, getColor(index))
      )
    );
    return () => myCharts.forEach((chart) => chart.dispose());
  }, [categories]);

  const getColor = (index) => {
    switch (index) {
      case 0:
        return "#E34444"; // Red
      case 1:
        return "#F1B92A"; // Yellow
      case 2:
        return "#66B127"; // Green
      case 3:
        return "#7066FF"; // Purple
      default:
        return "#E34444"; // Default to red
    }
  };

  return (
    <div>
      {categories.map((category, index) => (
        <div
          key={index}
          id={`Graph${category.name}`}
          style={{ width: "25%", height: "400px", display: "inline-block" }}
        ></div>
      ))}
    </div>
  );
};

export default DeviceStatus;
