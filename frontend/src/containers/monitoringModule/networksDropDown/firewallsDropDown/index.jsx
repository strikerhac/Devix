import React from "react";
import { Outlet } from "react-router-dom";

export const DROPDOWN_NAME = "Firewalls";
export const DROPDOWN_PATH = "firewalls";

function Index(props) {
  return <Outlet />;
}

export default Index;
