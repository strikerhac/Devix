import React, { useEffect } from 'react';
import * as echarts from 'echarts';

const Compliance = () => {
  useEffect(() => {
    const ROOT_PATH = 'https://echarts.apache.org/examples';

    const weatherIcons = {
      Sunny: ROOT_PATH + '/data/asset/img/weather/sunny_128.png',
      Cloudy: ROOT_PATH + '/data/asset/img/weather/cloudy_128.png',
      Showers: ROOT_PATH + '/data/asset/img/weather/showers_128.png'
    };

    const chartDom = document.getElementById('complianceChart');
    const myChart = echarts.init(chartDom);

    const option = {
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b} : {c} ({d}%)'
      },
      legend: {
        bottom: 25,
        left: 'center',
        data: ['Complaint', 'Voilation', 'Data Not Availble']
      },
      series: [
        {
          type: 'pie',
          radius: '65%',
          center: ['50%',"40%","50%", '50%'],
          selectedMode: 'single',
          data: [
            { value: 735, name: 'Complaint' },
            { value: 510, name: 'Voilation' },
            { value: 434, name: 'Data Not Availble' },
          ],
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    };

    myChart.setOption(option);

    return () => {
      myChart.dispose();
    };
  }, []);

  return <div id="complianceChart" style={{ width: '100%', height: '400px', paddingTop: '0px' }}></div>;
};

export default Compliance;
