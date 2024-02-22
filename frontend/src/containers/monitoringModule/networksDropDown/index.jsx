import React from "react";
import { Outlet } from "react-router-dom";

export const DROPDOWN_NAME = "Networks";
export const DROPDOWN_PATH = "networks";

function Index(props) {
  return <Outlet />;
}

export default Index;
