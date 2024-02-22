import React from "react";
import { Outlet } from "react-router-dom";
import { useAuthorization } from "../../hooks/useAuth";
import Card from "../../components/cards";
import HorizontalMenu from "../../components/horizontalMenu/index";
import { getDefaultPagePath } from "../../utils/helpers";
import {
  PAGE_NAME as PAGE_NAME_DASHBOARD,
  PAGE_PATH as PAGE_PATH_DASHBOARD,
} from "./dashboard/constants";
import {
  PAGE_NAME as PAGE_NAME_MANAGE_CONFIGURATIONS,
  PAGE_PATH as PAGE_PATH_MANAGE_CONFIGURATIONS,
} from "./manageConfigurations/constants";

export const MODULE_NAME = "NCM";
export const MODULE_PATH = "ncm_module";

function Index(props) {
  let menuItems = [
    {
      id: PAGE_PATH_DASHBOARD,
      name: PAGE_NAME_DASHBOARD,
      path: PAGE_PATH_DASHBOARD,
      icon: "ic:outline-dashboard",
    },
    {
      id: PAGE_PATH_MANAGE_CONFIGURATIONS,
      name: PAGE_NAME_MANAGE_CONFIGURATIONS,
      path: PAGE_PATH_MANAGE_CONFIGURATIONS,
      icon: "icon-park-outline:setting-config",
    },
  ];

  // hooks
  const { getUserInfoFromAccessToken, filterPageMenus } = useAuthorization();

  // user information
  const userInfo = getUserInfoFromAccessToken();
  const roleConfigurations = userInfo?.configuration;

  menuItems = filterPageMenus(menuItems, roleConfigurations, MODULE_PATH);

  const defaultPagePath = getDefaultPagePath(MODULE_PATH, menuItems);

  return (
    <>
      <Card>
        <HorizontalMenu
          menuItems={menuItems}
          defaultPagePath={defaultPagePath}
        />
      </Card>
      <Outlet />
    </>
  );
}

export default Index;
