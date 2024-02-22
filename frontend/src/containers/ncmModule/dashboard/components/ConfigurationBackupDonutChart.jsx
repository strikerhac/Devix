// import React from 'react';
// import ReactECharts from 'echarts-for-react';

// const ConfigurationBackupDonutChart = ({ chartData }) => {
//   const option = {
//     title: {
//       text: 'Configuration Backup Summary',
//       left: 'center',
//     },
//     tooltip: {
//       trigger: 'item',
//     },
//     legend: {
//       orient: 'vertical',
//       left: 'left',
//     },
//     series: [
//       {
//         name: 'Backup Status',
//         type: 'pie',
//         radius: ['50%', '70%'],
//         avoidLabelOverlap: false,
//         label: {
//           show: false,
//           position: 'center',
//         },
//         emphasis: {
//           label: {
//             show: true,
//             fontSize: '40',
//             fontWeight: 'bold',
//           },
//         },
//         labelLine: {
//           show: false,
//         },
//         data: chartData.map((item) => ({
//           value: item.value,
//           name: item.name,
//           itemStyle: {
//             color: item.color,
//           },
//         })),
//       },
//     ],
//   };

//   return <ReactECharts option={option} />;
// };

// export default ConfigurationBackupDonutChart;


import React from 'react'

function ConfigurationBackupDonutChart() {
  return (
    <div>ConfigurationBackupDonutChart</div>
  )
}

export default ConfigurationBackupDonutChart
