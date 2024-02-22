import React from "react";
import { Outlet } from "react-router-dom";

export const DROPDOWN_NAME = "Servers";
export const DROPDOWN_PATH = "servers";

function Index(props) {
  return <Outlet />;
}

export default Index;
