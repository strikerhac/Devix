import React from "react";
import { Outlet } from "react-router-dom";
import { getDefaultPagePath } from "../../utils/helpers";
import { useAuthorization } from "../../hooks/useAuth";
import Card from "../../components/cards";
import HorizontalMenu from "../../components/horizontalMenu/index";
import {
  PAGE_NAME as PAGE_NAME_ATOMS,
  PAGE_PATH as PAGE_PATH_ATOMS,
} from "./atoms/constants";
import {
  PAGE_NAME as PAGE_NAME_PASSWORD_GROUPS,
  PAGE_PATH as PAGE_PATH_PASSWORD_GROUPS,
} from "./passwordGroups/constants";

export const MODULE_NAME = "Atom";
export const MODULE_PATH = "atom_module";

function Index(props) {
  let menuItems = [
    {
      id: PAGE_PATH_ATOMS,
      name: PAGE_NAME_ATOMS,
      path: PAGE_PATH_ATOMS,
      icon: "solar:atom-outline",
    },
    {
      id: PAGE_PATH_PASSWORD_GROUPS,
      name: PAGE_NAME_PASSWORD_GROUPS,
      path: PAGE_PATH_PASSWORD_GROUPS,
      icon: "solar:passport-linear",
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
      <Card
        sx={{
          marginBottom: "10px",
          height: "50px",
        }}
      >
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
