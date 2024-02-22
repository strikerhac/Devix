import React from "react";
import { Outlet } from "react-router-dom";

export const DROPDOWN_NAME = "VIP";
export const DROPDOWN_PATH = "vip";

function Index(props) {
  return <Outlet />;
}

export default Index;
