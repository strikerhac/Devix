import React from "react";
import { Outlet } from "react-router-dom";

export const DROPDOWN_NAME = "Manage Credentials";
export const DROPDOWN_PATH = "manage_credentials";

function Index(props) {
  return <Outlet />;
}

export default Index;
