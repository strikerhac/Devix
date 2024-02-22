import React from "react";
import { Outlet } from "react-router-dom";

export const DROPDOWN_NAME = "Clouds";
export const DROPDOWN_PATH = "clouds";

function Index(props) {
  return <Outlet />;
}

export default Index;
