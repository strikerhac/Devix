import React from "react";
import { Outlet } from "react-router-dom";

export const DROPDOWN_NAME = "Linux";
export const DROPDOWN_PATH = "linux";

function Index(props) {
  return <Outlet />;
}

export default Index;
