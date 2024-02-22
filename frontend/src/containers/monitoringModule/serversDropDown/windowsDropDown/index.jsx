import React from "react";
import { Outlet } from "react-router-dom";

export const DROPDOWN_NAME = "Windows";
export const DROPDOWN_PATH = "windows";

function Index(props) {
  return <Outlet />;
}

export default Index;
