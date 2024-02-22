import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

const CountPerFunction = ({ chartData }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    if (!chartData || !chartData.name || !chartData.value) {
      console.error('Invalid chart data:', chartData);
      return;
    }

    const option = {
      xAxis: {
        type: 'category',
        data: chartData.name,
        axisLabel: {
          interval: 0, // Adjust the label display interval if necessary
          rotate: 0, // Set to 0 to align labels straight
          fontSize: 10, // Adjust font size of the labels
        },
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          fontSize: 10, // Adjust font size of the labels
        },
      },
      series: [
        {
          data: chartData.value,
          type: 'bar',
          barMaxWidth: '50%', // Adjust the maximum width of bars if necessary
          showBackground: true,
          backgroundStyle: {
            color: '#F4F8F3',
            borderRadius: [20, 20, 0, 0],
          },
          itemStyle: {
            color: '#66B127',
            borderRadius: [20, 20, 0, 0],
          },
          emphasis: {
            itemStyle: {
              color: '#66B127',
              borderRadius: [20, 20, 0, 0],
            },
          },
        },
      ],
    };

    const myChart = echarts.init(chartRef.current);
    myChart.setOption(option);

    return () => {
      myChart.dispose();
    };
  }, [chartData]);

  return <div ref={chartRef} style={{ width: '100%', height: '400px' }} />;
};

export default CountPerFunction;
