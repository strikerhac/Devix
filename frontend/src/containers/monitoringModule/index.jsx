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
  PAGE_NAME as PAGE_NAME_DEVICES,
  PAGE_PATH as PAGE_PATH_DEVICES,
} from "./devices/constants";
////////////////////////////////////////////////
import {
  DROPDOWN_NAME as DROPDOWN_NAME_NETWORKS,
  DROPDOWN_PATH as DROPDOWN_PATH_NETWORKS,
} from "./networksDropDown";

import {
  DROPDOWN_NAME as DROPDOWN_NAME_NETWORKS_ALL_DEVICES,
  DROPDOWN_PATH as DROPDOWN_PATH_NETWORKS_ALL_DEVICES,
} from "./networksDropDown/allDevicesDropDown";

import {
  PAGE_NAME as PAGE_NAME_NETWORKS_ALL_DEVICES_DEVICES,
  PAGE_PATH as PAGE_PATH_NETWORKS_ALL_DEVICES_DEVICES,
} from "./networksDropDown/allDevicesDropDown/devices/constants";

import {
  PAGE_NAME as PAGE_NAME_NETWORKS_ALL_DEVICES_INTERFACES,
  PAGE_PATH as PAGE_PATH_NETWORKS_ALL_DEVICES_INTERFACES,
} from "./networksDropDown/allDevicesDropDown/interfaces/constants";

import {
  DROPDOWN_NAME as DROPDOWN_NAME_ROUTERS,
  DROPDOWN_PATH as DROPDOWN_PATH_ROUTERS,
} from "./networksDropDown/routersDropDown";

import {
  PAGE_NAME as PAGE_NAME_ROUTERS_DEVICES,
  PAGE_PATH as PAGE_PATH_ROUTERS_DEVICES,
} from "./networksDropDown/routersDropDown/devices/constants";

import {
  PAGE_NAME as PAGE_NAME_ROUTERS_INTERFACES,
  PAGE_PATH as PAGE_PATH_ROUTERS_INTERFACES,
} from "./networksDropDown/routersDropDown/interfaces/constants";

import {
  DROPDOWN_NAME as DROPDOWN_NAME_SWITCHES,
  DROPDOWN_PATH as DROPDOWN_PATH_SWITCHES,
} from "./networksDropDown/switchesDropDown";

import {
  PAGE_NAME as PAGE_NAME_SWITCHES_DEVICES,
  PAGE_PATH as PAGE_PATH_SWITCHES_DEVICES,
} from "./networksDropDown/switchesDropDown/devices/constants";

import {
  PAGE_NAME as PAGE_NAME_SWITCHES_INTERFACES,
  PAGE_PATH as PAGE_PATH_SWITCHES_INTERFACES,
} from "./networksDropDown/switchesDropDown/interfaces/constants";

import {
  DROPDOWN_NAME as DROPDOWN_NAME_FIREWALLS,
  DROPDOWN_PATH as DROPDOWN_PATH_FIREWALLS,
} from "./networksDropDown/firewallsDropDown";

import {
  PAGE_NAME as PAGE_NAME_FIREWALLS_DEVICES,
  PAGE_PATH as PAGE_PATH_FIREWALLS_DEVICES,
} from "./networksDropDown/firewallsDropDown/devices/constants";

import {
  PAGE_NAME as PAGE_NAME_FIREWALLS_INTERFACES,
  PAGE_PATH as PAGE_PATH_FIREWALLS_INTERFACES,
} from "./networksDropDown/firewallsDropDown/interfaces/constants";

import {
  DROPDOWN_NAME as DROPDOWN_NAME_WIRELESS,
  DROPDOWN_PATH as DROPDOWN_PATH_WIRELESS,
} from "./networksDropDown/wirelessDropDown";

import {
  PAGE_NAME as PAGE_NAME_WIRELESS_DEVICES,
  PAGE_PATH as PAGE_PATH_WIRELESS_DEVICES,
} from "./networksDropDown/wirelessDropDown/devices/constants";

import {
  PAGE_NAME as PAGE_NAME_WIRELESS_INTERFACES,
  PAGE_PATH as PAGE_PATH_WIRELESS_INTERFACES,
} from "./networksDropDown/wirelessDropDown/interfaces/constants";

//////////////////////////////////////////////////
import {
  DROPDOWN_NAME as DROPDOWN_NAME_SERVERS,
  DROPDOWN_PATH as DROPDOWN_PATH_SERVERS,
} from "./serversDropDown";

import {
  DROPDOWN_NAME as DROPDOWN_NAME_SERVERS_ALL_DEVICES,
  DROPDOWN_PATH as DROPDOWN_PATH_SERVERS_ALL_DEVICES,
} from "./serversDropDown/allDevicesDropDown";

import {
  PAGE_NAME as PAGE_NAME_SERVERS_ALL_DEVICES_DEVICES,
  PAGE_PATH as PAGE_PATH_SERVERS_ALL_DEVICES_DEVICES,
} from "./serversDropDown/allDevicesDropDown/devices/constants";

import {
  PAGE_NAME as PAGE_NAME_SERVERS_ALL_DEVICES_INTERFACES,
  PAGE_PATH as PAGE_PATH_SERVERS_ALL_DEVICES_INTERFACES,
} from "./serversDropDown/allDevicesDropDown/interfaces/constants";

import {
  DROPDOWN_NAME as DROPDOWN_NAME_LINUX,
  DROPDOWN_PATH as DROPDOWN_PATH_LINUX,
} from "./serversDropDown/linuxDropDown";

import {
  PAGE_NAME as PAGE_NAME_LINUX_DEVICES,
  PAGE_PATH as PAGE_PATH_LINUX_DEVICES,
} from "./serversDropDown/linuxDropDown/devices/constants";

import {
  PAGE_NAME as PAGE_NAME_LINUX_INTERFACES,
  PAGE_PATH as PAGE_PATH_LINUX_INTERFACES,
} from "./serversDropDown/linuxDropDown/interfaces/constants";

import {
  DROPDOWN_NAME as DROPDOWN_NAME_WINDOWS,
  DROPDOWN_PATH as DROPDOWN_PATH_WINDOWS,
} from "./serversDropDown/windowsDropDown";

import {
  PAGE_NAME as PAGE_NAME_WINDOWS_DEVICES,
  PAGE_PATH as PAGE_PATH_WINDOWS_DEVICES,
} from "./serversDropDown/windowsDropDown/devices/constants";

import {
  PAGE_NAME as PAGE_NAME_WINDOWS_INTERFACES,
  PAGE_PATH as PAGE_PATH_WINDOWS_INTERFACES,
} from "./serversDropDown/windowsDropDown/interfaces/constants";

///////////////////////////////////////////////
import {
  PAGE_NAME as PAGE_NAME_ALERTS,
  PAGE_PATH as PAGE_PATH_ALERTS,
} from "./alerts/constants";

/////////////////////////////////////////////////
import {
  DROPDOWN_NAME as DROPDOWN_NAME_CLOUDS,
  DROPDOWN_PATH as DROPDOWN_PATH_CLOUDS,
} from "./cloudsDropDown";

import {
  DROPDOWN_NAME as DROPDOWN_NAME_AWS,
  DROPDOWN_PATH as DROPDOWN_PATH_AWS,
} from "./cloudsDropDown/awsDropDown";

import {
  PAGE_NAME as PAGE_NAME_ACCOUNTS,
  PAGE_PATH as PAGE_PATH_ACCOUNTS,
} from "./cloudsDropDown/awsDropDown/accounts/constants";

import {
  PAGE_NAME as PAGE_NAME_S3,
  PAGE_PATH as PAGE_PATH_S3,
} from "./cloudsDropDown/awsDropDown/s3/constants";

import {
  PAGE_NAME as PAGE_NAME_EC2,
  PAGE_PATH as PAGE_PATH_EC2,
} from "./cloudsDropDown/awsDropDown/ec2/constants";

import {
  PAGE_NAME as PAGE_NAME_ELB,
  PAGE_PATH as PAGE_PATH_ELB,
} from "./cloudsDropDown/awsDropDown/elb/constants";

////////////////////////////////////////////////////
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

export const MODULE_NAME = "Monitoring";
export const MODULE_PATH = "monitoring_module";

function Index(props) {
  let menuItems = [
    {
      id: PAGE_PATH_DASHBOARD,
      name: PAGE_NAME_DASHBOARD,
      path: PAGE_PATH_DASHBOARD,
      icon: "ic:outline-dashboard",
    },
    {
      id: PAGE_PATH_DEVICES,
      name: PAGE_NAME_DEVICES,
      path: PAGE_PATH_DEVICES,
      icon: "tdesign:device",
    },
    {
      id: DROPDOWN_PATH_NETWORKS,
      name: DROPDOWN_NAME_NETWORKS,
      icon: "carbon:network-2",
      children: [
        {
          id: DROPDOWN_PATH_NETWORKS_ALL_DEVICES,
          name: DROPDOWN_NAME_NETWORKS_ALL_DEVICES,
          icon: "tdesign:device",
          children: [
            {
              id: PAGE_PATH_NETWORKS_ALL_DEVICES_DEVICES,
              name: PAGE_NAME_NETWORKS_ALL_DEVICES_DEVICES,
              path: `/${MAIN_LAYOUT_PATH}/${MODULE_PATH}/${DROPDOWN_PATH_NETWORKS}/${DROPDOWN_PATH_NETWORKS_ALL_DEVICES}/${PAGE_PATH_NETWORKS_ALL_DEVICES_DEVICES}`,
              icon: "tdesign:device",
            },
            {
              id: PAGE_PATH_NETWORKS_ALL_DEVICES_INTERFACES,
              name: PAGE_NAME_NETWORKS_ALL_DEVICES_INTERFACES,
              path: `/${MAIN_LAYOUT_PATH}/${MODULE_PATH}/${DROPDOWN_PATH_NETWORKS}/${DROPDOWN_PATH_NETWORKS_ALL_DEVICES}/${PAGE_PATH_NETWORKS_ALL_DEVICES_INTERFACES}`,
              icon: "carbon:network-interface",
            },
          ],
        },
        {
          id: DROPDOWN_PATH_ROUTERS,
          name: DROPDOWN_NAME_ROUTERS,
          icon: "bi:router",
          children: [
            {
              id: PAGE_PATH_ROUTERS_DEVICES,
              name: PAGE_NAME_ROUTERS_DEVICES,
              path: `/${MAIN_LAYOUT_PATH}/${MODULE_PATH}/${DROPDOWN_PATH_NETWORKS}/${DROPDOWN_PATH_ROUTERS}/${PAGE_PATH_ROUTERS_DEVICES}`,
              icon: "tdesign:device",
            },
            {
              id: PAGE_PATH_ROUTERS_INTERFACES,
              name: PAGE_NAME_ROUTERS_INTERFACES,
              path: `/${MAIN_LAYOUT_PATH}/${MODULE_PATH}/${DROPDOWN_PATH_NETWORKS}/${DROPDOWN_PATH_ROUTERS}/${PAGE_PATH_ROUTERS_INTERFACES}`,
              icon: "carbon:network-interface",
            },
          ],
        },
        {
          id: DROPDOWN_PATH_SWITCHES,
          name: DROPDOWN_NAME_SWITCHES,
          icon: "material-symbols:switch-outline",
          children: [
            {
              id: PAGE_PATH_SWITCHES_DEVICES,
              name: PAGE_NAME_SWITCHES_DEVICES,
              path: `/${MAIN_LAYOUT_PATH}/${MODULE_PATH}/${DROPDOWN_PATH_NETWORKS}/${DROPDOWN_PATH_SWITCHES}/${PAGE_PATH_SWITCHES_DEVICES}`,
              icon: "tdesign:device",
            },
            {
              id: PAGE_PATH_SWITCHES_INTERFACES,
              name: PAGE_NAME_SWITCHES_INTERFACES,
              path: `/${MAIN_LAYOUT_PATH}/${MODULE_PATH}/${DROPDOWN_PATH_NETWORKS}/${DROPDOWN_PATH_SWITCHES}/${PAGE_PATH_SWITCHES_INTERFACES}`,
              icon: "carbon:network-interface",
            },
          ],
        },
        {
          id: DROPDOWN_PATH_FIREWALLS,
          name: DROPDOWN_NAME_FIREWALLS,
          icon: "carbon:firewall",
          children: [
            {
              id: PAGE_PATH_FIREWALLS_DEVICES,
              name: PAGE_NAME_FIREWALLS_DEVICES,
              path: `/${MAIN_LAYOUT_PATH}/${MODULE_PATH}/${DROPDOWN_PATH_NETWORKS}/${DROPDOWN_PATH_FIREWALLS}/${PAGE_PATH_FIREWALLS_DEVICES}`,
              icon: "tdesign:device",
            },
            {
              id: PAGE_PATH_FIREWALLS_INTERFACES,
              name: PAGE_NAME_FIREWALLS_INTERFACES,
              path: `/${MAIN_LAYOUT_PATH}/${MODULE_PATH}/${DROPDOWN_PATH_NETWORKS}/${DROPDOWN_PATH_FIREWALLS}/${PAGE_PATH_FIREWALLS_INTERFACES}`,
              icon: "carbon:network-interface",
            },
          ],
        },
        {
          id: DROPDOWN_PATH_WIRELESS,
          name: DROPDOWN_NAME_WIRELESS,
          icon: "mdi:credit-card-wireless-outline",
          children: [
            {
              id: PAGE_PATH_WIRELESS_DEVICES,
              name: PAGE_NAME_WIRELESS_DEVICES,
              path: `/${MAIN_LAYOUT_PATH}/${MODULE_PATH}/${DROPDOWN_PATH_NETWORKS}/${DROPDOWN_PATH_WIRELESS}/${PAGE_PATH_WIRELESS_DEVICES}`,
              icon: "tdesign:device",
            },
            {
              id: PAGE_PATH_WIRELESS_INTERFACES,
              name: PAGE_NAME_WIRELESS_INTERFACES,
              path: `/${MAIN_LAYOUT_PATH}/${MODULE_PATH}/${DROPDOWN_PATH_NETWORKS}/${DROPDOWN_PATH_WIRELESS}/${PAGE_PATH_WIRELESS_INTERFACES}`,
              icon: "carbon:network-interface",
            },
          ],
        },
      ],
    },
    {
      id: DROPDOWN_PATH_SERVERS,
      name: DROPDOWN_NAME_SERVERS,
      icon: "clarity:rack-server-line",
      children: [
        {
          id: DROPDOWN_PATH_SERVERS_ALL_DEVICES,
          name: DROPDOWN_NAME_SERVERS_ALL_DEVICES,
          icon: "tdesign:device",
          children: [
            {
              id: PAGE_PATH_SERVERS_ALL_DEVICES_DEVICES,
              name: PAGE_NAME_SERVERS_ALL_DEVICES_DEVICES,
              path: `/${MAIN_LAYOUT_PATH}/${MODULE_PATH}/${DROPDOWN_PATH_SERVERS}/${DROPDOWN_PATH_SERVERS_ALL_DEVICES}/${PAGE_PATH_SERVERS_ALL_DEVICES_DEVICES}`,
              icon: "tdesign:device",
            },
            {
              id: PAGE_PATH_SERVERS_ALL_DEVICES_INTERFACES,
              name: PAGE_NAME_SERVERS_ALL_DEVICES_INTERFACES,
              path: `/${MAIN_LAYOUT_PATH}/${MODULE_PATH}/${DROPDOWN_PATH_SERVERS}/${DROPDOWN_PATH_SERVERS_ALL_DEVICES}/${PAGE_PATH_SERVERS_ALL_DEVICES_INTERFACES}`,
              icon: "carbon:network-interface",
            },
          ],
        },
        {
          id: DROPDOWN_PATH_LINUX,
          name: DROPDOWN_NAME_LINUX,
          icon: "simple-icons:linux",
          children: [
            {
              id: PAGE_PATH_LINUX_DEVICES,
              name: PAGE_NAME_LINUX_DEVICES,
              path: `/${MAIN_LAYOUT_PATH}/${MODULE_PATH}/${DROPDOWN_PATH_SERVERS}/${DROPDOWN_PATH_LINUX}/${PAGE_PATH_LINUX_DEVICES}`,
              icon: "tdesign:device",
            },
            {
              id: PAGE_PATH_LINUX_INTERFACES,
              name: PAGE_NAME_LINUX_INTERFACES,
              path: `/${MAIN_LAYOUT_PATH}/${MODULE_PATH}/${DROPDOWN_PATH_SERVERS}/${DROPDOWN_PATH_LINUX}/${PAGE_PATH_LINUX_INTERFACES}`,
              icon: "carbon:network-interface",
            },
          ],
        },
        {
          id: DROPDOWN_PATH_WINDOWS,
          name: DROPDOWN_NAME_WINDOWS,
          icon: "mingcute:windows-line",
          children: [
            {
              id: PAGE_PATH_WINDOWS_DEVICES,
              name: PAGE_NAME_WINDOWS_DEVICES,
              path: `/${MAIN_LAYOUT_PATH}/${MODULE_PATH}/${DROPDOWN_PATH_SERVERS}/${DROPDOWN_PATH_WINDOWS}/${PAGE_PATH_WINDOWS_DEVICES}`,
              icon: "tdesign:device",
            },
            {
              id: PAGE_PATH_WINDOWS_INTERFACES,
              name: PAGE_NAME_WINDOWS_INTERFACES,
              path: `/${MAIN_LAYOUT_PATH}/${MODULE_PATH}/${DROPDOWN_PATH_SERVERS}/${DROPDOWN_PATH_WINDOWS}/${PAGE_PATH_WINDOWS_INTERFACES}`,
              icon: "carbon:network-interface",
            },
          ],
        },
      ],
    },
    {
      id: PAGE_PATH_ALERTS,
      name: PAGE_NAME_ALERTS,
      path: PAGE_PATH_ALERTS,
      icon: "ri:alert-line",
    },
    {
      id: DROPDOWN_PATH_CLOUDS,
      name: DROPDOWN_NAME_CLOUDS,
      icon: "mingcute:clouds-line",
      children: [
        {
          id: DROPDOWN_PATH_AWS,
          name: DROPDOWN_NAME_AWS,
          icon: "bxl:aws",
          children: [
            {
              id: PAGE_PATH_ACCOUNTS,
              name: PAGE_NAME_ACCOUNTS,
              path: `/${MAIN_LAYOUT_PATH}/${MODULE_PATH}/${DROPDOWN_PATH_CLOUDS}/${DROPDOWN_PATH_AWS}/${PAGE_PATH_ACCOUNTS}`,
              icon: "carbon:account",
            },
            {
              id: PAGE_PATH_S3,
              name: PAGE_NAME_S3,
              path: `/${MAIN_LAYOUT_PATH}/${MODULE_PATH}/${DROPDOWN_PATH_CLOUDS}/${DROPDOWN_PATH_AWS}/${PAGE_PATH_S3}`,
              icon: "teenyicons:bitbucket-outline",
            },
            {
              id: PAGE_PATH_EC2,
              name: PAGE_NAME_EC2,
              path: `/${MAIN_LAYOUT_PATH}/${MODULE_PATH}/${DROPDOWN_PATH_CLOUDS}/${DROPDOWN_PATH_AWS}/${PAGE_PATH_EC2}`,
              icon: "simple-icons:amazonec2",
            },
            {
              id: PAGE_PATH_ELB,
              name: PAGE_NAME_ELB,
              path: `/${MAIN_LAYOUT_PATH}/${MODULE_PATH}/${DROPDOWN_PATH_CLOUDS}/${DROPDOWN_PATH_AWS}/${PAGE_PATH_ELB}`,
              icon: "carbon:load-balancer-vpc",
            },
          ],
        },
      ],
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
