import React from "react";
import { Outlet } from "react-router-dom";

export const DROPDOWN_NAME = "AWS";
export const DROPDOWN_PATH = "aws";

function Index(props) {
  return <Outlet />;
}

export default Index;
