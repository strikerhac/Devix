import React from "react";
import { Outlet } from "react-router-dom";

export const DROPDOWN_NAME = "Wireless";
export const DROPDOWN_PATH = "wireless";

function Index(props) {
  return <Outlet />;
}

export default Index;
