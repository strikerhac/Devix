import React from "react";
import { Outlet } from "react-router-dom";

export const DROPDOWN_NAME = "Routers";
export const DROPDOWN_PATH = "routers";

function Index(props) {
  return <Outlet />;
}

export default Index;
