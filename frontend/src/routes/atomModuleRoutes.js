import React from "react";
import AtomModule from "../containers/atomModule";
import Atoms from "../containers/atomModule/atoms";
import PasswordGroups from "../containers/atomModule/passwordGroups";
import { PAGE_PATH as PAGE_PATH_ATOMS } from "../containers/atomModule/atoms/constants";
import { PAGE_PATH as PAGE_PATH_PASSWORD_GROUPS } from "../containers/atomModule/passwordGroups/constants";
import { MODULE_PATH } from "../containers/atomModule";
import { MAIN_LAYOUT_PATH } from "../layouts/mainLayout";

export default function moduleRoutes(roleConfigurations, authorizePageRoutes) {
  const routes = [
    {
      path: PAGE_PATH_ATOMS,
      element: <Atoms />,
    },
    {
      path: PAGE_PATH_PASSWORD_GROUPS,
      element: <PasswordGroups />,
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
    element: <AtomModule />,
    children: authorizedPageRoutes,
  };
}
