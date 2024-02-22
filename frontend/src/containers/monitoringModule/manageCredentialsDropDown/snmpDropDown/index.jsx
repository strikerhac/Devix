import React from "react";
import { Outlet } from "react-router-dom";

export const DROPDOWN_NAME = "SNMP";
export const DROPDOWN_PATH = "snmp";

function Index(props) {
  return <Outlet />;
}

export default Index;
