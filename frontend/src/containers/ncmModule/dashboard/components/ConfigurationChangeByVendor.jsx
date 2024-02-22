import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

const ConfigurationChangeByVendor = ({ deviceNames, time, values }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    const myChart = echarts.init(chartRef.current);

    // Concatenate time with device names
    const categories = deviceNames.map((device, index) => `${time[index]} - ${device}`);

    const option = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross',
          label: {
            backgroundColor: '#283b56',
          },
        },
      },
      toolbox: {
        show: true,
        feature: {
          // dataView: { readOnly: false },
          // restore: {},
          // saveAsImage: {},
        },
      },
      dataZoom: {
        show: false,
        start: 0,
        end: 100,
      },
      grid: {  
        left: 30,
        right: 30,
        bottom: 0,
        top: 30, 
        containLabel: true
      },
      xAxis: [
        {
          type: 'category',
          boundaryGap: true,
          data: categories,
        }
      ],
      yAxis: [
        {
          type: 'value',
          scale: true,
          name: '',
          max: 30,
          min: 0,
          boundaryGap: [0.2, 0.2],
        },
        {
          type: 'value',
          scale: true,
          name: '',
          max: 1200,
          min: 0,
          boundaryGap: [0.2, 0.2],
        },
      ],
      series: [
        {
          type: 'bar',
          yAxisIndex: 1,
          data: values,
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#31C7A4' },
              { offset: 1, color: '#FFFFFF' },
            ]),
            borderRadius: [15, 15, 15, 15],
          },
          barCategoryGap: '80%',
        },
        {
          type: 'line',
          yAxisIndex: 0,
          data: values,
          itemStyle: {
            color: '#31C7A4',
          },
        },
      ],
    };

    myChart.setOption(option);

    const intervalId = setInterval(() => {
      let axisData = new Date().toLocaleTimeString().replace(/^\D*/, '');
      values.shift();
      values.push(Math.round(Math.random() * 1000));

      myChart.setOption({
        xAxis: [
          {
            data: categories,
          }
        ],
        series: [
          {
            data: values,
          },
          {
            data: values,
          },
        ],
      });
    }, 2100);

    return () => {
      clearInterval(intervalId);
      myChart.dispose();
    };
  }, [deviceNames, time, values]);

  return <div ref={chartRef} className="chart-container" style={{ width: '100%', height: '400px' }} />;
};

export default ConfigurationChangeByVendor;
