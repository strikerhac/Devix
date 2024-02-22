import React from "react";
import { Navigate } from "react-router-dom";
import IpamModule from "../containers/ipamModule";

import { MODULE_PATH } from "../containers/ipamModule";
import Dashboard from "../containers/ipamModule/dashboard";
import Devices from "../containers/ipamModule/devices";

import SubnetsDropDown from "../containers/ipamModule/subnetsDropDown";
import Subnets from "../containers/ipamModule/subnetsDropDown/subnets";
import DiscoveredSubnets from "../containers/ipamModule/subnetsDropDown/discoveredSubnets";
import IPDetails from "../containers/ipamModule/subnetsDropDown/ipDetails";
import IPHistory from "../containers/ipamModule/subnetsDropDown/ipHistory";

import DNSServersDropDown from "../containers/ipamModule/dnsServerDropDown";
import DNSRecords from "../containers/ipamModule/dnsServerDropDown/dnsRecords";
import DNSServers from "../containers/ipamModule/dnsServerDropDown/dnsServers";
import DNSZones from "../containers/ipamModule/dnsServerDropDown/dnsZones";

import VIPDropDown from "../containers/ipamModule/vipDropDown";
import Firewalls from "../containers/ipamModule/vipDropDown/firewalls";
import LoadBalancers from "../containers/ipamModule/vipDropDown/loadBalancers";

import { PAGE_PATH as PAGE_PATH_DASHBOARD } from "../containers/ipamModule/dashboard/constants";
import { PAGE_PATH as PAGE_PATH_DEVICES } from "../containers/ipamModule/devices/constants";

import { DROPDOWN_PATH as DROPDOWN_PATH_SUBNETS } from "../containers/ipamModule/subnetsDropDown";
import { PAGE_PATH as PAGE_PATH_SUBNETS } from "../containers/ipamModule/subnetsDropDown/subnets/constants";
import { PAGE_PATH as PAGE_PATH_DISCOVERED_SUBNETS } from "../containers/ipamModule/subnetsDropDown/discoveredSubnets/constants";
import { PAGE_PATH as PAGE_PATH_IP_DETAILS } from "../containers/ipamModule/subnetsDropDown/ipDetails/constants";
import { PAGE_PATH as PAGE_PATH_IP_HISTORY } from "../containers/ipamModule/subnetsDropDown/ipHistory/constants";

import { DROPDOWN_PATH as DROPDOWN_PATH_DNS_SERVERS } from "../containers/ipamModule/dnsServerDropDown";
import { PAGE_PATH as PAGE_PATH_DNS_RECORDS } from "../containers/ipamModule/dnsServerDropDown/dnsRecords/constants";
import { PAGE_PATH as PAGE_PATH_DNS_SERVERS } from "../containers/ipamModule/dnsServerDropDown/dnsServers/constants";
import { PAGE_PATH as PAGE_PATH_DNS_ZONES } from "../containers/ipamModule/dnsServerDropDown/dnsZones/constants";

import { DROPDOWN_PATH as DROPDOWN_PATH_VIP } from "../containers/ipamModule/vipDropDown";
import { PAGE_PATH as PAGE_PATH_FIREWALLS } from "../containers/ipamModule/vipDropDown/firewalls/constants";
import { PAGE_PATH as PAGE_PATH_LOAD_BALANCERS } from "../containers/ipamModule/vipDropDown/loadBalancers/constants";

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
      path: DROPDOWN_PATH_SUBNETS,
      element: <SubnetsDropDown />,
      children: [
        {
          path: PAGE_PATH_SUBNETS,
          element: <Subnets />,
        },
        {
          path: PAGE_PATH_DISCOVERED_SUBNETS,
          element: <DiscoveredSubnets />,
        },
        {
          path: PAGE_PATH_IP_DETAILS,
          element: <IPDetails />,
        },
        {
          path: PAGE_PATH_IP_HISTORY,
          element: <IPHistory />,
        },
      ],
    },
    {
      path: DROPDOWN_PATH_DNS_SERVERS,
      element: <DNSServersDropDown />,
      children: [
        {
          path: PAGE_PATH_DNS_RECORDS,
          element: <DNSRecords />,
        },
        {
          path: PAGE_PATH_DNS_SERVERS,
          element: <DNSServers />,
        },
        {
          path: PAGE_PATH_DNS_ZONES,
          element: <DNSZones />,
        },
      ],
    },
    {
      path: DROPDOWN_PATH_VIP,
      element: <VIPDropDown />,
      children: [
        {
          path: PAGE_PATH_FIREWALLS,
          element: <Firewalls />,
        },
        {
          path: PAGE_PATH_LOAD_BALANCERS,
          element: <LoadBalancers />,
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
    element: <IpamModule />,
    children: authorizedPageRoutes,
  };
}
