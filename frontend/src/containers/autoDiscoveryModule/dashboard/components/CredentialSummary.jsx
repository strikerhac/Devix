import React, { useEffect } from 'react';
import * as echarts from 'echarts';

const CredentialSummary = ({ data }) => {
  useEffect(() => {
    const chartDom = document.getElementById('credentialSummaryChart');
    const myChart = echarts.init(chartDom);

    const option = {
      tooltip: {
        trigger: 'axis'
      },
      legend: {
        data: data?.name
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      toolbox: {
        feature: {
          saveAsImage: {}
        }
      },
      xAxis: {
        type: 'category',
        data: data?.name
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          name: data?.name,
          type: 'line',
          data: data?.value
        }
      ]
    };

    option && myChart.setOption(option);

    return () => {
      myChart.dispose();
    };
  }, [data]);

  return (
    <div id="credentialSummaryChart" style={{ width: '100%', height: '400px' }}>
      {/* ECharts will be rendered inside this div */}
    </div>
  );
};

export default CredentialSummary;
