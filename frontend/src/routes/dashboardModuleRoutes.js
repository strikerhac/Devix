import React from "react";
import DashboardModule from "../containers/dashboardModule";
import Dashboard from "../containers/dashboardModule/dashboard";
import { PAGE_PATH as PAGE_PATH_DASHBOARD } from "../containers/dashboardModule/dashboard/constants";
import { MODULE_PATH } from "../containers/dashboardModule";
import { MAIN_LAYOUT_PATH } from "../layouts/mainLayout";

export default function moduleRoutes(roleConfigurations, authorizePageRoutes) {
  const routes = [
    {
      path: PAGE_PATH_DASHBOARD,
      element: <Dashboard />,
    },
  ];

  // Authorize module page routes
  const authorizedPageRoutes = authorizePageRoutes({
    module: MODULE_PATH,
    pageRoutes: routes,
    roleConfigurations,
    defaultPagePath: `/${MAIN_LAYOUT_PATH}/${MODULE_PATH}`,
  });

  return {
    path: MODULE_PATH,
    element: <DashboardModule />,
    children: authorizedPageRoutes,
  };
}
