import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

const CountPerVendors = ({ data }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    const myChart = echarts.init(chartRef.current);

    const colors = ['#3E72E7', '#74ABFF', '#30C9C9', '#8F37FF', '#409F47', '#F03F41']; // Define colors here

    const option = {
      dataset: {
        source: [
          ['product', 'score', 'amount', 'color'],
          ...data.map((device, index) => [device.vender, device.counts, index, colors[index]])
        ],
      },
      yAxis: { type: 'category' },
      xAxis: { type: 'value' },
      series: [
        {
          type: 'bar',
          encode: {
            x: 'amount',
            y: 'product',
          },
          itemStyle: {
            color: function (params) {
              return params.data[3]; // Set color based on the 'color' column
            },
            barBorderRadius: [0, 20, 20, 0], // Set bar radius [top-left, top-right, bottom-right, bottom-left]
          },
          barWidth: 15, // Adjust the width of the bars
          barHeight: 10, // Adjust the height of the bars
        },
      ],
    };

    myChart.setOption(option);

    // Cleanup function to destroy the chart when the component unmounts
    return () => myChart.dispose();
  }, [data]);

  return <div ref={chartRef} style={{ width: '100%', height: '400px' }} />;
};

export default CountPerVendors;
