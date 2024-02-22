import React, { useEffect, useRef, useState } from 'react';
import * as echarts from 'echarts';

const IpAvailable = ({ data }) => {
  const chartRef = useRef(null);
  const [chartData, setChartData] = useState({ total: 0, used: 0, available: 0 });

  useEffect(() => {
    setChartData({ total: data.total_ip, used: data.used_ip, available: data.available_ip });
  }, [data.total_ip, data.used_ip, data.available_ip]);

  useEffect(() => {
    const myChart = echarts.init(chartRef.current);

    const option = {
      tooltip: {
        trigger: 'item',
      },
      legend: {
        top: '80%',
        left: 'center',
      },
      series: [
        {
          name: 'Access From',
          type: 'pie',
          radius: ['40%', '70%'],
          center: ['50%',"40%","50%", '50%'],
          avoidLabelOverlap: false,
          label: {
            show: false,
            position: 'center',
          },
          emphasis: {
            label: {
              show: true,
              fontSize: 40,
              fontWeight: 'bold',
            },
          },
          labelLine: {
            show: false,
          },
          data: [
            { value: chartData.total, name: 'Total IPs', itemStyle: { color: '#74ABFF' } },
            { value: chartData.available, name: 'Free IPs', itemStyle: { color: '#66B127' } },
            { value: chartData.used, name: 'Used IPs', itemStyle: { color: '#8F37FF' } },
          ],
        },
      ],
    };

    myChart.setOption(option);

    // Cleanup function to detach chart when component unmounts
    return () => myChart.dispose();
  }, [chartData]);

  return <div ref={chartRef} style={{ maxWidth: '100%', height: '400px' }} />;
};

export default IpAvailable;
