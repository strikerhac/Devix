import React from "react";
import { Outlet } from "react-router-dom";

export const DROPDOWN_NAME = "DNS Servers";
export const DROPDOWN_PATH = "dns_servers";

function Index(props) {
  return <Outlet />;
}

export default Index;
