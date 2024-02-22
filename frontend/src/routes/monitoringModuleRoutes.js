import React from "react";
import { Navigate } from "react-router-dom";

import Dashboard from "../containers/monitoringModule/dashboard";
import { PAGE_PATH as PAGE_PATH_DASHBOARD } from "../containers/monitoringModule/dashboard/constants";

///////////////////////////////
import MonitoringModule from "../containers/monitoringModule";
import { MODULE_PATH } from "../containers/monitoringModule";

///////////////////////////////
import Devices from "../containers/monitoringModule/devices";
import { PAGE_PATH as PAGE_PATH_DEVICES } from "../containers/monitoringModule/devices/constants";

///////////////////////////////
import NetworksDropDown from "../containers/monitoringModule/networksDropDown";
import { DROPDOWN_PATH as DROPDOWN_PATH_NETWORKS } from "../containers/monitoringModule/networksDropDown";

import NetworksAllDevicesDropDown from "../containers/monitoringModule/networksDropDown/allDevicesDropDown";
import { DROPDOWN_PATH as DROPDOWN_PATH_NETWORKS_ALL_DEVICES } from "../containers/monitoringModule/networksDropDown/allDevicesDropDown";

import NetworksAllDevicesDevices from "../containers/monitoringModule/networksDropDown/allDevicesDropDown/devices";
import { PAGE_PATH as PAGE_PATH_NETWORKS_ALL_DEVICES_DEVICES } from "../containers/monitoringModule/networksDropDown/allDevicesDropDown/devices/constants";

import NetworksAllDevicesInterfaces from "../containers/monitoringModule/networksDropDown/allDevicesDropDown/interfaces";
import { PAGE_PATH as PAGE_PATH_NETWORKS_ALL_DEVICES_INTERFACES } from "../containers/monitoringModule/networksDropDown/allDevicesDropDown/interfaces/constants";

import RoutersDropDown from "../containers/monitoringModule/networksDropDown/routersDropDown";
import { DROPDOWN_PATH as DROPDOWN_PATH_ROUTERS } from "../containers/monitoringModule/networksDropDown/routersDropDown";

import RoutersDevices from "../containers/monitoringModule/networksDropDown/routersDropDown/devices";
import { PAGE_PATH as PAGE_PATH_ROUTERS_DEVICES } from "../containers/monitoringModule/networksDropDown/routersDropDown/devices/constants";

import RoutersInterfaces from "../containers/monitoringModule/networksDropDown/routersDropDown/interfaces";
import { PAGE_PATH as PAGE_PATH_ROUTERS_INTERFACES } from "../containers/monitoringModule/networksDropDown/routersDropDown/interfaces/constants";

import SwitchesDropDown from "../containers/monitoringModule/networksDropDown/switchesDropDown";
import { DROPDOWN_PATH as DROPDOWN_PATH_SWITCHES } from "../containers/monitoringModule/networksDropDown/switchesDropDown";

import SwitchesDevices from "../containers/monitoringModule/networksDropDown/switchesDropDown/devices";
import { PAGE_PATH as PAGE_PATH_SWITCHES_DEVICES } from "../containers/monitoringModule/networksDropDown/switchesDropDown/devices/constants";

import SwitchesInterfaces from "../containers/monitoringModule/networksDropDown/switchesDropDown/interfaces";
import { PAGE_PATH as PAGE_PATH_SWITCHES_INTERFACES } from "../containers/monitoringModule/networksDropDown/switchesDropDown/interfaces/constants";

import FirewallsDropDown from "../containers/monitoringModule/networksDropDown/firewallsDropDown";
import { DROPDOWN_PATH as DROPDOWN_PATH_FIREWALLS } from "../containers/monitoringModule/networksDropDown/firewallsDropDown";

import FirewallsDevices from "../containers/monitoringModule/networksDropDown/firewallsDropDown/devices";
import { PAGE_PATH as PAGE_PATH_FIREWALLS_DEVICES } from "../containers/monitoringModule/networksDropDown/firewallsDropDown/devices/constants";

import FirewallsInterfaces from "../containers/monitoringModule/networksDropDown/firewallsDropDown/interfaces";
import { PAGE_PATH as PAGE_PATH_FIREWALLS_INTERFACES } from "../containers/monitoringModule/networksDropDown/firewallsDropDown/interfaces/constants";

import WirelessDropDown from "../containers/monitoringModule/networksDropDown/wirelessDropDown";
import { DROPDOWN_PATH as DROPDOWN_PATH_WIRELESS } from "../containers/monitoringModule/networksDropDown/wirelessDropDown";

import WirelessDevices from "../containers/monitoringModule/networksDropDown/wirelessDropDown/devices";
import { PAGE_PATH as PAGE_PATH_WIRELESS_DEVICES } from "../containers/monitoringModule/networksDropDown/wirelessDropDown/devices/constants";

import WirelessInterfaces from "../containers/monitoringModule/networksDropDown/wirelessDropDown/interfaces";
import { PAGE_PATH as PAGE_PATH_WIRELESS_INTERFACES } from "../containers/monitoringModule/networksDropDown/wirelessDropDown/interfaces/constants";

///////////////////////////////////////////
import ServersDropDown from "../containers/monitoringModule/serversDropDown";
import { DROPDOWN_PATH as DROPDOWN_PATH_SERVERS } from "../containers/monitoringModule/serversDropDown";

import ServerAllDevicesDropDown from "../containers/monitoringModule/serversDropDown/allDevicesDropDown";
import { DROPDOWN_PATH as DROPDOWN_PATH_SERVER_ALL_DEVICES } from "../containers/monitoringModule/serversDropDown/allDevicesDropDown";

import ServerAllDevicesDevices from "../containers/monitoringModule/serversDropDown/allDevicesDropDown/devices";
import { PAGE_PATH as PAGE_PATH_SERVER_All_DEVICES_DEVICES } from "../containers/monitoringModule/serversDropDown/allDevicesDropDown/devices/constants";

import ServerAllDevicesInterfaces from "../containers/monitoringModule/serversDropDown/allDevicesDropDown/interfaces";
import { PAGE_PATH as PAGE_PATH_SERVER_All_DEVICES_INTERFACES } from "../containers/monitoringModule/serversDropDown/allDevicesDropDown/interfaces/constants";

import WindowsDropDown from "../containers/monitoringModule/serversDropDown/windowsDropDown";
import { DROPDOWN_PATH as DROPDOWN_PATH_WINDOWS } from "../containers/monitoringModule/serversDropDown/windowsDropDown";

import WindowsDevices from "../containers/monitoringModule/serversDropDown/windowsDropDown/devices";
import { PAGE_PATH as PAGE_PATH_WINDOWS_DEVICES } from "../containers/monitoringModule/serversDropDown/windowsDropDown/devices/constants";

import WindowsInterfaces from "../containers/monitoringModule/serversDropDown/windowsDropDown/interfaces";
import { PAGE_PATH as PAGE_PATH_WINDOWS_INTERFACES } from "../containers/monitoringModule/serversDropDown/windowsDropDown/interfaces/constants";

import LinuxDropDown from "../containers/monitoringModule/serversDropDown/linuxDropDown";
import { DROPDOWN_PATH as DROPDOWN_PATH_LINUX } from "../containers/monitoringModule/serversDropDown/linuxDropDown";

import LinuxDevices from "../containers/monitoringModule/serversDropDown/linuxDropDown/devices";
import { PAGE_PATH as PAGE_PATH_LINUX_DEVICES } from "../containers/monitoringModule/serversDropDown/linuxDropDown/devices/constants";

import LinuxInterfaces from "../containers/monitoringModule/serversDropDown/linuxDropDown/interfaces";
import { PAGE_PATH as PAGE_PATH_LINUX_INTERFACES } from "../containers/monitoringModule/serversDropDown/linuxDropDown/interfaces/constants";

////////////////////////////////////////////
import Alerts from "../containers/monitoringModule/alerts";
import { PAGE_PATH as PAGE_PATH_ALERTS } from "../containers/monitoringModule/alerts/constants";

////////////////////////////////////////////
import CloudsDropDown from "../containers/monitoringModule/cloudsDropDown";
import { DROPDOWN_PATH as DROPDOWN_PATH_CLOUDS } from "../containers/monitoringModule/cloudsDropDown";

import AWSDropDown from "../containers/monitoringModule/cloudsDropDown/awsDropDown";
import { DROPDOWN_PATH as DROPDOWN_PATH_AWS } from "../containers/monitoringModule/cloudsDropDown/awsDropDown";

import AwsAccounts from "../containers/monitoringModule/cloudsDropDown/awsDropDown/accounts";
import { PAGE_PATH as PAGE_PATH_AWS_ACCOUNTS } from "../containers/monitoringModule/cloudsDropDown/awsDropDown/accounts/constants";

import EC2 from "../containers/monitoringModule/cloudsDropDown/awsDropDown/ec2";
import { PAGE_PATH as PAGE_PATH_EC2 } from "../containers/monitoringModule/cloudsDropDown/awsDropDown/ec2/constants";

import S3 from "../containers/monitoringModule/cloudsDropDown/awsDropDown/s3";
import { PAGE_PATH as PAGE_PATH_S3 } from "../containers/monitoringModule/cloudsDropDown/awsDropDown/s3/constants";

import ELB from "../containers/monitoringModule/cloudsDropDown/awsDropDown/elb";
import { PAGE_PATH as PAGE_PATH_ELB } from "../containers/monitoringModule/cloudsDropDown/awsDropDown/elb/constants";

////////////////////////////////////////////
import ManageCredentialsDropDown from "../containers/monitoringModule/manageCredentialsDropDown";
import { DROPDOWN_PATH as DROPDOWN_PATH_MANAGE_CREDENTIALS } from "../containers/monitoringModule/manageCredentialsDropDown";

import LoginCredentials from "../containers/monitoringModule//manageCredentialsDropDown/loginCredentials";
import { PAGE_PATH as PAGE_PATH_LOGIN_CREDENTIALS } from "../containers/monitoringModule/manageCredentialsDropDown/loginCredentials/constants";

import SNMPDropDown from "../containers/monitoringModule/manageCredentialsDropDown/snmpDropDown";
import { DROPDOWN_PATH as DROPDOWN_PATH_SNMP } from "../containers/monitoringModule/manageCredentialsDropDown/snmpDropDown";

import V1V2Credentials from "../containers/monitoringModule/manageCredentialsDropDown/snmpDropDown/v1V2Credentials";
import { PAGE_PATH as PAGE_PATH_V1_V2_CREDENTIALS } from "../containers/monitoringModule/manageCredentialsDropDown/snmpDropDown/v1V2Credentials/constants";

import V3Credentials from "../containers/monitoringModule/manageCredentialsDropDown/snmpDropDown/v3Credentials";
import { PAGE_PATH as PAGE_PATH_V3_CREDENTIALS } from "../containers/monitoringModule/manageCredentialsDropDown/snmpDropDown/v3Credentials/constants";

////////////////////////////////////////
import DevicesLanding from "../containers/monitoringModule/devicesLanding";
import { LANDING_PAGE_PATH as LANDING_PAGE_PATH_DEVICES } from "../containers/monitoringModule/devicesLanding";

import DevicesSummary from "../containers/monitoringModule/devicesLanding/summary";
import { PAGE_PATH as PAGE_PATH_DEVICES_SUMMARY } from "../containers/monitoringModule/devicesLanding/summary/constants";

import DevicesInterfaces from "../containers/monitoringModule/devicesLanding/interfaces";
import { PAGE_PATH as PAGE_PATH_DEVICES_INTERFACES } from "../containers/monitoringModule/devicesLanding/interfaces/constants";

import InterfacesBandwidths from "../containers/monitoringModule/devicesLanding/bandwidths";
import { PAGE_PATH as PAGE_PATH_INTERFACES_BANDWIDTHS } from "../containers/monitoringModule/devicesLanding/bandwidths/constants";

import { MAIN_LAYOUT_PATH } from "../layouts/mainLayout";

export default function moduleRoutes(roleConfigurations, authorizePageRoutes) {
  const routes = [
    {
      path: PAGE_PATH_DASHBOARD,
      element: <Dashboard />,
    },
    {
      path: PAGE_PATH_DEVICES,
      element: <Devices />,
    },
    {
      path: DROPDOWN_PATH_NETWORKS,
      element: <NetworksDropDown />,
      children: [
        {
          path: DROPDOWN_PATH_NETWORKS_ALL_DEVICES,
          element: <NetworksAllDevicesDropDown />,
          children: [
            {
              path: PAGE_PATH_NETWORKS_ALL_DEVICES_DEVICES,
              element: <NetworksAllDevicesDevices />,
            },
            {
              path: PAGE_PATH_NETWORKS_ALL_DEVICES_INTERFACES,
              element: <NetworksAllDevicesInterfaces />,
            },
          ],
        },
        {
          path: DROPDOWN_PATH_ROUTERS,
          element: <RoutersDropDown />,
          children: [
            {
              path: PAGE_PATH_ROUTERS_DEVICES,
              element: <RoutersDevices />,
            },
            {
              path: PAGE_PATH_ROUTERS_INTERFACES,
              element: <RoutersInterfaces />,
            },
          ],
        },
        {
          path: DROPDOWN_PATH_SWITCHES,
          element: <SwitchesDropDown />,
          children: [
            {
              path: PAGE_PATH_SWITCHES_DEVICES,
              element: <SwitchesDevices />,
            },
            {
              path: PAGE_PATH_SWITCHES_INTERFACES,
              element: <SwitchesInterfaces />,
            },
          ],
        },
        {
          path: DROPDOWN_PATH_FIREWALLS,
          element: <FirewallsDropDown />,
          children: [
            {
              path: PAGE_PATH_FIREWALLS_DEVICES,
              element: <FirewallsDevices />,
            },
            {
              path: PAGE_PATH_FIREWALLS_INTERFACES,
              element: <FirewallsInterfaces />,
            },
          ],
        },
        {
          path: DROPDOWN_PATH_WIRELESS,
          element: <WirelessDropDown />,
          children: [
            {
              path: PAGE_PATH_WIRELESS_DEVICES,
              element: <WirelessDevices />,
            },
            {
              path: PAGE_PATH_WIRELESS_INTERFACES,
              element: <WirelessInterfaces />,
            },
          ],
        },
      ],
    },
    {
      path: DROPDOWN_PATH_SERVERS,
      element: <ServersDropDown />,
      children: [
        {
          path: DROPDOWN_PATH_SERVER_ALL_DEVICES,
          element: <ServerAllDevicesDropDown />,
          children: [
            {
              path: PAGE_PATH_SERVER_All_DEVICES_DEVICES,
              element: <ServerAllDevicesDevices />,
            },
            {
              path: PAGE_PATH_SERVER_All_DEVICES_INTERFACES,
              element: <ServerAllDevicesInterfaces />,
            },
          ],
        },
        {
          path: DROPDOWN_PATH_WINDOWS,
          element: <WindowsDropDown />,
          children: [
            {
              path: PAGE_PATH_WINDOWS_DEVICES,
              element: <WindowsDevices />,
            },
            {
              path: PAGE_PATH_WINDOWS_INTERFACES,
              element: <WindowsInterfaces />,
            },
          ],
        },
        {
          path: DROPDOWN_PATH_LINUX,
          element: <LinuxDropDown />,
          children: [
            {
              path: PAGE_PATH_LINUX_DEVICES,
              element: <LinuxDevices />,
            },
            {
              path: PAGE_PATH_LINUX_INTERFACES,
              element: <LinuxInterfaces />,
            },
          ],
        },
      ],
    },
    {
      path: PAGE_PATH_ALERTS,
      element: <Alerts />,
    },
    {
      path: DROPDOWN_PATH_CLOUDS,
      element: <CloudsDropDown />,
      children: [
        {
          path: DROPDOWN_PATH_AWS,
          element: <AWSDropDown />,
          children: [
            {
              path: PAGE_PATH_AWS_ACCOUNTS,
              element: <AwsAccounts />,
            },
            {
              path: PAGE_PATH_S3,
              element: <S3 />,
            },
            {
              path: PAGE_PATH_EC2,
              element: <EC2 />,
            },
            {
              path: PAGE_PATH_ELB,
              element: <ELB />,
            },
          ],
        },
      ],
    },
    {
      path: DROPDOWN_PATH_MANAGE_CREDENTIALS,
      element: <ManageCredentialsDropDown />,
      children: [
        {
          path: PAGE_PATH_LOGIN_CREDENTIALS,
          element: <LoginCredentials />,
        },
        {
          path: DROPDOWN_PATH_SNMP,
          element: <SNMPDropDown />,
          children: [
            {
              path: PAGE_PATH_V1_V2_CREDENTIALS,
              element: <V1V2Credentials />,
            },
            {
              path: PAGE_PATH_V3_CREDENTIALS,
              element: <V3Credentials />,
            },
          ],
        },
      ],
    },
    {
      path: LANDING_PAGE_PATH_DEVICES,
      element: <DevicesLanding />,
      children: [
        {
          path: PAGE_PATH_DEVICES_SUMMARY,
          element: <DevicesSummary />,
        },
        {
          path: PAGE_PATH_DEVICES_INTERFACES,
          element: <DevicesInterfaces />,
        },
        {
          path: PAGE_PATH_INTERFACES_BANDWIDTHS,
          element: <InterfacesBandwidths />,
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
    element: <MonitoringModule />,
    children: authorizedPageRoutes,
  };
}
