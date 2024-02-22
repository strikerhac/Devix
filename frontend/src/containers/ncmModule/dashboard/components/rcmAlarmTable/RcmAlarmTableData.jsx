import { Descriptions } from 'antd';
import React from 'react';
import calendar from "../../../../../resources/svgs/calendar.svg"

function RcmAlarmTableData(props) {
  const { Title, Description, label,date } = props;

  return (
    <div style={{ width: "554px", backgroundColor: "#FFFFFF", borderRadius: "8px", padding:"0px 0px 20px 0px " }}>
        <div style={{display:"flex",justifyContent:"space-between", alignItems:"center", padding:"0px 5px"}}>
      <h3 style={{ padding: "5px 10px", margin: "0px" }}>{Title}</h3>
      <div style={{display:"flex", alignItems:"center"}}>
        <img src={calendar}/>
      <p style={{ padding: "5px 10px", margin: "0px" }}>{date}</p>
      </div>
      </div>
      <p style={{ padding: "5px 15px", margin: "0px" }}>{Description}</p>
      <div style={{paddingTop:"10px"}}>
      <label style={{ padding: "5px 15px", margin: "0px", backgroundColor:"#EEEEEE", borderRadius:"115px" ,margin:"10px"}}>{label}</label>
      </div>
    </div>
  );
}

export default RcmAlarmTableData;
