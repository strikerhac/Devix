// import React, { useEffect } from 'react';
// import * as echarts from 'echarts';
// import $ from 'jquery';

// const ChangeByTimeLineChart = () => {
//   useEffect(() => {
//     const ROOT_PATH = 'https://echarts.apache.org/examples';

//     const fetchData = async () => {
//       try {
//         const rawData = await $.get(`${ROOT_PATH}/data/asset/data/life-expectancy-table.json`);
//         run(rawData);
//       } catch (error) {
//         console.error('Error fetching data:', error);
//       }
//     };

//     fetchData();

//     return () => {
//       // Clean up any resources or event listeners here if needed
//     };
//   }, []); // Empty dependency array ensures that the effect runs only once on component mount

//   const run = (_rawData) => {
//     const chartDom = document.getElementById('main');

//     // Clear the content of the chart container
//     chartDom.innerHTML = '';

//     const myChart = echarts.init(chartDom);

//     const option = {
//       // ... (rest of your option object remains unchanged)
//     };

//     option && myChart.setOption(option);

//     // Clean up the chart on component unmount
//     return () => {
//       myChart.dispose();
//     };
//   };

//   return <div id="main" style={{ width: '100%', height: '400px' }}></div>;
// };

// export default ChangeByTimeLineChart;

import React from 'react'

function ChangeByTimeLineChart() {
  return (
    <div>ChangeByTimeLineChart</div>
  )
}

export default ChangeByTimeLineChart