import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

const SnmpStatus = ({ responseData }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    if (!responseData || responseData.length === 0) {
      // Handle empty data
      return;
    }

    if (chartRef.current) {
      const myChart = echarts.init(chartRef.current);

      const option = {
        legend: {
          data: responseData.map(item => item.name)
        },
        radar: {
          indicator: responseData.map(item => ({ name: item.name, max: item.value }))
        },
        series: [
          {
            name: 'SNMP Status',
            type: 'radar',
            areaStyle: {
              color: 'rgba(67, 160, 71, 0.3)', // Green color with opacity
            },
            lineStyle: {
              color: '#43A047' // Adjust radar line color
            },
            data: [
              {
                value: responseData.map(item => item.value),
                name: 'SNMP Status'
              }
            ]
          }
        ]
      };

      myChart.setOption(option);
    }
  }, [responseData]);

  return (
    <div ref={chartRef} id="snmpStatusChart" style={{ width: '100%', height: '400px' }} />
  );
};

export default SnmpStatus;
