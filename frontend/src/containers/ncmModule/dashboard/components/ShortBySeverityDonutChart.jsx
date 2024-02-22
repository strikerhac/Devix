import React, { useEffect } from 'react';
import * as echarts from 'echarts';

const ShortBySeverityDonutChart = () => {
  useEffect(() => {
    const chartDom = document.getElementById('main');
    const myChart = echarts.init(chartDom);

    const option = {
      angleAxis: {
        max: 2,
        startAngle: 30,
        splitLine: {
          show: false
        }
      },
      radiusAxis: {
        type: 'category',
        data: ['v', 'w', 'x', 'y', 'z'],
        z: 10
      },
      polar: {},
      series: [
        {
          type: 'bar',
          data: [4, 3, 2, 1, 0],
          coordinateSystem: 'polar',
          name: 'Without Round Cap',
          itemStyle: {
            borderColor: 'red',
            opacity: 0.8,
            borderWidth: 1
          }
        },
        {
          type: 'bar',
          data: [4, 3, 2, 1, 0],
          coordinateSystem: 'polar',
          name: 'With Round Cap',
          roundCap: true,
          itemStyle: {
            borderColor: 'green',
            opacity: 0.8,
            borderWidth: 1
          }
        }
      ],
      legend: {
        show: true,
        data: ['Without Round Cap', 'With Round Cap']
      }
    };

    option && myChart.setOption(option);

    // Clean up the chart on component unmount
    return () => {
      myChart.dispose();
    };
  }, []); // Empty dependency array ensures that the effect runs only once on component mount

  return <div id="main" style={{ width: '100%', height: '400px' }}></div>;
};

export default ShortBySeverityDonutChart;
