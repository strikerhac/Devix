import React from "react";
import UamModule from "../containers/uamModule";
import Sites from "../containers/uamModule/sites";
import Racks from "../containers/uamModule/racks";
import Devices from "../containers/uamModule/devices";
import Boards from "../containers/uamModule/boards";
import SubBoards from "../containers/uamModule/subBoards";
import Sfps from "../containers/uamModule/sfps";
import Licenses from "../containers/uamModule/licenses";
import Aps from "../containers/uamModule/aps";
import Hwlifecycles from "../containers/uamModule/hwLifeCycles";
import { Navigate } from "react-router-dom";
import { PAGE_PATH as PAGE_PATH_SITES } from "../containers/uamModule/sites/constants";
import { PAGE_PATH as PAGE_PATH_RACKS } from "../containers/uamModule/racks/constants";
import { PAGE_PATH as PAGE_PATH_DEVICES } from "../containers/uamModule/devices/constants";
import { PAGE_PATH as PAGE_PATH_BOARDS } from "../containers/uamModule/boards/constants";
import { PAGE_PATH as PAGE_PATH_SUB_BOARDS } from "../containers/uamModule/subBoards/constants";
import { PAGE_PATH as PAGE_PATH_SFPS } from "../containers/uamModule/sfps/constants";
import { PAGE_PATH as PAGE_PATH_LICENSES } from "../containers/uamModule/licenses/constants";
import { PAGE_PATH as PAGE_PATH_APS } from "../containers/uamModule/aps/constants";
import { PAGE_PATH as PAGE_PATH_HW_LIFE_CYCLES } from "../containers/uamModule/hwLifeCycles/constants";
import { MODULE_PATH } from "../containers/uamModule";
import { MAIN_LAYOUT_PATH } from "../layouts/mainLayout";

export default function moduleRoutes(roleConfigurations, authorizePageRoutes) {
  const routes = [
    {
      path: PAGE_PATH_DEVICES,
      element: <Devices />,
    },
    {
      path: PAGE_PATH_SITES,
      element: <Sites />,
    },
    {
      path: PAGE_PATH_RACKS,
      element: <Racks />,
    },
    {
      path: PAGE_PATH_BOARDS,
      element: <Boards />,
    },
    {
      path: PAGE_PATH_SUB_BOARDS,
      element: <SubBoards />,
    },
    {
      path: PAGE_PATH_SFPS,
      element: <Sfps />,
    },
    {
      path: PAGE_PATH_LICENSES,
      element: <Licenses />,
    },
    {
      path: PAGE_PATH_APS,
      element: <Aps />,
    },
    {
      path: PAGE_PATH_HW_LIFE_CYCLES,
      element: <Hwlifecycles />,
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
    element: <UamModule />,
    children: authorizedPageRoutes,
  };
}
