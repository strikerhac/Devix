import React from "react";
import NcmModule from "../containers/ncmModule";
import Dashboard from "../containers/ncmModule/dashboard";
import ConfigData from "../containers/ncmModule/manageConfigurations";
import ManageConfigurationsLanding from "../containers/ncmModule/manageConfigurationsLanding";
import ConfigurationBackups from "../containers/ncmModule/manageConfigurationsLanding/configurationBackups";
import RemoteCommandSender from "../containers/ncmModule/manageConfigurationsLanding/remoteCommandSender";
import { Navigate } from "react-router-dom";
import { PAGE_PATH as PAGE_PATH_DASHBOARD } from "../containers/ncmModule/dashboard/constants";
import { PAGE_PATH as PAGE_PATH_CONFIG_DATA } from "../containers/ncmModule/manageConfigurations/constants";
import { LANDING_PAGE_PATH as LANDING_PAGE_PATH_MANAGE_CONFIGURATIONS } from "../containers/ncmModule/manageConfigurationsLanding";
import { PAGE_PATH as PAGE_PATH_CONFIGURATION_BACKUPS } from "../containers/ncmModule/manageConfigurationsLanding/configurationBackups/constants";
import { PAGE_PATH as PAGE_PATH_REMOTE_COMMAND_SENDER } from "../containers/ncmModule/manageConfigurationsLanding/remoteCommandSender/constants";
import { MODULE_PATH } from "../containers/ncmModule";
import { MAIN_LAYOUT_PATH } from "../layouts/mainLayout";

export default function moduleRoutes(roleConfigurations, authorizePageRoutes) {
  const routes = [
    {
      path: PAGE_PATH_DASHBOARD,
      element: <Dashboard />,
    },
    {
      path: PAGE_PATH_CONFIG_DATA,
      element: <ConfigData />,
    },
    {
      path: LANDING_PAGE_PATH_MANAGE_CONFIGURATIONS,
      element: <ManageConfigurationsLanding />,
      children: [
        {
          path: PAGE_PATH_CONFIGURATION_BACKUPS,
          element: <ConfigurationBackups />,
        },
        {
          path: PAGE_PATH_REMOTE_COMMAND_SENDER,
          element: <RemoteCommandSender />,
        },
      ],
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
    element: <NcmModule />,
    children: authorizedPageRoutes,
  };
}
