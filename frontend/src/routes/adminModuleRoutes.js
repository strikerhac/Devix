import React from "react";
import { Navigate } from "react-router-dom";

import { MAIN_LAYOUT_PATH } from "../layouts/mainLayout";

import AdminModule from "../containers/adminModule";
import { MODULE_PATH } from "../containers/adminModule";

import Members from "../containers/adminModule/members";
import { PAGE_PATH as PAGE_PATH_MEMBERS } from "../containers/adminModule/members/constants";

import Roles from "../containers/adminModule/roles";
import { PAGE_PATH as PAGE_PATH_ROLES } from "../containers/adminModule/roles/constants";

import FailedDevicesLanding from "../containers/adminModule/failedDevicesLanding";
import { LANDING_PAGE_PATH as LANDING_PAGE_PATH_FAILED_DEVICES } from "../containers/adminModule/failedDevicesLanding";

import AutoDiscovery from "../containers/adminModule/failedDevicesLanding/autoDiscovery";
import { PAGE_PATH as PAGE_PATH_AUTO_DISCOVERY } from "../containers/adminModule/failedDevicesLanding/autoDiscovery/constants";

import IPAM from "../containers/adminModule/failedDevicesLanding/ipam";
import { PAGE_PATH as PAGE_PATH_IPAM } from "../containers/adminModule/failedDevicesLanding/ipam/constants";

import Monitoring from "../containers/adminModule/failedDevicesLanding/monitoring";
import { PAGE_PATH as PAGE_PATH_MONITORING } from "../containers/adminModule/failedDevicesLanding/monitoring/constants";

import NCM from "../containers/adminModule/failedDevicesLanding/ncm";
import { PAGE_PATH as PAGE_PATH_NCM } from "../containers/adminModule/failedDevicesLanding/ncm/constants";

import UAM from "../containers/adminModule/failedDevicesLanding/uam";
import { PAGE_PATH as PAGE_PATH_UAM } from "../containers/adminModule/failedDevicesLanding/uam/constants";

export default function moduleRoutes(roleConfigurations, authorizePageRoutes) {
  const routes = [
    {
      path: PAGE_PATH_MEMBERS,
      element: <Members />,
    },
    {
      path: PAGE_PATH_ROLES,
      element: <Roles />,
    },
    {
      path: LANDING_PAGE_PATH_FAILED_DEVICES,
      element: <FailedDevicesLanding />,
      children: [
        {
          path: `/${MAIN_LAYOUT_PATH}/${MODULE_PATH}/${LANDING_PAGE_PATH_FAILED_DEVICES}`,
          element: <Navigate to={PAGE_PATH_AUTO_DISCOVERY} replace />,
        },
        {
          path: PAGE_PATH_AUTO_DISCOVERY,
          element: <AutoDiscovery />,
        },
        {
          path: PAGE_PATH_IPAM,
          element: <IPAM />,
        },
        {
          path: PAGE_PATH_MONITORING,
          element: <Monitoring />,
        },
        {
          path: PAGE_PATH_NCM,
          element: <NCM />,
        },
        {
          path: PAGE_PATH_UAM,
          element: <UAM />,
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
    element: <AdminModule />,
    children: authorizedPageRoutes,
  };
}
