import React from "react";
import { Outlet } from "react-router-dom";

export const DROPDOWN_NAME = "All Devices";
export const DROPDOWN_PATH = "all_devices";

function Index(props) {
  return <Outlet />;
}

export default Index;
