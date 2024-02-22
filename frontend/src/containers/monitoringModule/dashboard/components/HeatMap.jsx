import React from 'react';

function HeatMap({ data }) {
  const rows = Math.ceil(data.length / 7);

  const createRows = () => {
    const rowsArray = [];
    for (let i = 0; i < rows; i++) {
      const rowData = data.slice(i * 7, (i + 1) * 7);
      rowsArray.push(
        <div key={i} style={{ display: "flex", justifyContent: "start", margin: "20px 0 20px 50px" }}>
          {rowData.map((item, index) => (
            <div key={index} style={{ width: "63px", height: "60px", backgroundColor: item.fill, borderRadius: "2px", marginRight: "20px", borderRadius:"7px" }}></div>
          ))}
        </div>
      );
    }
    return rowsArray;
  };

  return (
    <div>
      {createRows()}
    </div>
  );
}

export default HeatMap;
