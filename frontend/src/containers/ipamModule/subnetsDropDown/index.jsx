import React from "react";
import { Outlet } from "react-router-dom";

export const DROPDOWN_NAME = "Subnets";
export const DROPDOWN_PATH = "subnets";

function Index(props) {
  return <Outlet />;
}

export default Index;
