import React from "react";
import { Outlet } from "react-router-dom";

export const DROPDOWN_NAME = "Switches";
export const DROPDOWN_PATH = "switches";

function Index(props) {
  return <Outlet />;
}

export default Index;
