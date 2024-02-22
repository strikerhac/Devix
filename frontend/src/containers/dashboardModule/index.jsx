import React from "react";
import { Outlet } from "react-router-dom";
import { getDefaultPagePath } from "../../utils/helpers";
import { useAuthorization } from "../../hooks/useAuth";
import Card from "../../components/cards";
import HorizontalMenu from "../../components/horizontalMenu/index";

export const MODULE_NAME = "Dashboard";
export const MODULE_PATH = "dashboard_module";

function Index(props) {
  let menuItems = [];

  // hooks
  const { getUserInfoFromAccessToken, filterPageMenus } = useAuthorization();

  // user information
  const userInfo = getUserInfoFromAccessToken();
  const roleConfigurations = userInfo?.configuration;

  menuItems = filterPageMenus(menuItems, roleConfigurations, MODULE_PATH);

  const defaultPagePath = getDefaultPagePath(MODULE_PATH, menuItems);

  return (
    <>
      {menuItems.length > 0 ? (
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
      ) : null}
      <Outlet />
    </>
  );
}

export default Index;
