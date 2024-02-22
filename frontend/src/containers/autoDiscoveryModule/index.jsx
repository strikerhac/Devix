import React from "react";
import { Outlet } from "react-router-dom";
import { getDefaultPagePath } from "../../utils/helpers";
import { useAuthorization } from "../../hooks/useAuth";
import Card from "../../components/cards";
import HorizontalMenu from "../../components/horizontalMenu/index";
import {
  PAGE_NAME as PAGE_NAME_DASHBOARD,
  PAGE_PATH as PAGE_PATH_DASHBOARD,
} from "./dashboard/constants";
import {
  PAGE_NAME as PAGE_NAME_MANAGE_NETWORKS,
  PAGE_PATH as PAGE_PATH_MANAGE_NETWORKS,
} from "./manageNetworks/constants";
import {
  PAGE_NAME as PAGE_NAME_DISCOVERY,
  PAGE_PATH as PAGE_PATH_DISCOVERY,
} from "./discovery/constants";
import {
  PAGE_NAME as PAGE_NAME_MANAGE_DEVICES,
  PAGE_PATH as PAGE_PATH_MANAGE_DEVICES,
} from "./manageDevices/constants";
import {
  DROPDOWN_NAME as DROPDOWN_NAME_MANAGE_CREDENTIALS,
  DROPDOWN_PATH as DROPDOWN_PATH_MANAGE_CREDENTIALS,
} from "./manageCredentialsDropDown";
import {
  PAGE_NAME as PAGE_NAME_LOGIN_CREDENTIALS,
  PAGE_PATH as PAGE_PATH_LOGIN_CREDENTIALS,
} from "./manageCredentialsDropDown/loginCredentials/constants";
import {
  DROPDOWN_NAME as DROPDOWN_NAME_SNMP_CREDENTIALS,
  DROPDOWN_PATH as DROPDOWN_PATH_SNMP_CREDENTIALS,
} from "./manageCredentialsDropDown/snmpDropDown";
import {
  PAGE_NAME as PAGE_NAME_V1_V2_CREDENTIALS,
  PAGE_PATH as PAGE_PATH_V1_V2_CREDENTIALS,
} from "./manageCredentialsDropDown/snmpDropDown/v1V2Credentials/constants";
import {
  PAGE_NAME as PAGE_NAME_V3_CREDENTIALS,
  PAGE_PATH as PAGE_PATH_V3_CREDENTIALS,
} from "./manageCredentialsDropDown/snmpDropDown/v3Credentials/constants";
import { MAIN_LAYOUT_PATH } from "../../layouts/mainLayout";

export const MODULE_NAME = "Auto Discovery";
export const MODULE_PATH = "auto_discovery_module";

function Index(props) {
  let menuItems = [
    {
      id: PAGE_PATH_DASHBOARD,
      name: PAGE_NAME_DASHBOARD,
      path: PAGE_PATH_DASHBOARD,
      icon: "ic:outline-dashboard",
    },
    {
      id: PAGE_PATH_MANAGE_NETWORKS,
      name: PAGE_NAME_MANAGE_NETWORKS,
      path: PAGE_PATH_MANAGE_NETWORKS,
      icon: "carbon:network-2",
    },
    {
      id: PAGE_PATH_DISCOVERY,
      name: PAGE_NAME_DISCOVERY,
      path: PAGE_PATH_DISCOVERY,
      icon: "iconamoon:discover-light",
    },
    {
      id: PAGE_PATH_MANAGE_DEVICES,
      name: PAGE_NAME_MANAGE_DEVICES,
      path: PAGE_PATH_MANAGE_DEVICES,
      icon: "tdesign:device",
    },
    {
      id: DROPDOWN_PATH_MANAGE_CREDENTIALS,
      name: DROPDOWN_NAME_MANAGE_CREDENTIALS,
      icon: "octicon:id-badge-16",
      children: [
        {
          id: PAGE_PATH_LOGIN_CREDENTIALS,
          name: PAGE_NAME_LOGIN_CREDENTIALS,
          path: `/${MAIN_LAYOUT_PATH}/${MODULE_PATH}/${DROPDOWN_PATH_MANAGE_CREDENTIALS}/${PAGE_PATH_LOGIN_CREDENTIALS}`,
          icon: "carbon:password",
        },
        {
          id: DROPDOWN_PATH_SNMP_CREDENTIALS,
          name: DROPDOWN_NAME_SNMP_CREDENTIALS,
          icon: "fluent:protocol-handler-16-regular",
          children: [
            {
              id: PAGE_PATH_V1_V2_CREDENTIALS,
              name: PAGE_NAME_V1_V2_CREDENTIALS,
              path: `/${MAIN_LAYOUT_PATH}/${MODULE_PATH}/${DROPDOWN_PATH_MANAGE_CREDENTIALS}/${DROPDOWN_PATH_SNMP_CREDENTIALS}/${PAGE_PATH_V1_V2_CREDENTIALS}`,
              icon: "solar:shield-network-broken",
            },
            {
              id: PAGE_PATH_V3_CREDENTIALS,
              name: PAGE_NAME_V3_CREDENTIALS,
              path: `/${MAIN_LAYOUT_PATH}/${MODULE_PATH}/${DROPDOWN_PATH_MANAGE_CREDENTIALS}/${DROPDOWN_PATH_SNMP_CREDENTIALS}/${PAGE_PATH_V3_CREDENTIALS}`,
              icon: "solar:shield-network-broken",
            },
          ],
        },
      ],
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
