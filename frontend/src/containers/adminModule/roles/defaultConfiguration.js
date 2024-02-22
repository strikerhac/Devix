// dashboard module
import { MODULE_PATH as MODULE_PATH_DASHBOARD } from "../../dashboardModule";
import { PAGE_PATH as PAGE_PATH_DASHBOARD } from "../../dashboardModule/dashboard/constants";

// admin module
import { MODULE_PATH as MODULE_PATH_ADMIN } from "..";
import { PAGE_PATH as PAGE_PATH_ADMIN_MEMBERS } from "../members/constants";
import { PAGE_PATH as PAGE_PATH_ADMIN_FAILED_DEVICES_AUTO_DISCOVERY } from "../failedDevicesLanding/autoDiscovery/constants";
import { PAGE_PATH as PAGE_PATH_ADMIN_FAILED_DEVICES_IPAM } from "../failedDevicesLanding/ipam/constants";
import { PAGE_PATH as PAGE_PATH_ADMIN_FAILED_DEVICES_MONITORING } from "../failedDevicesLanding/monitoring/constants";
import { PAGE_PATH as PAGE_PATH_ADMIN_FAILED_DEVICES_NCM } from "../failedDevicesLanding/ncm/constants";
import { PAGE_PATH as PAGE_PATH_ADMIN_FAILED_DEVICES_UAM } from "../failedDevicesLanding/uam/constants";
import { PAGE_PATH as PAGE_PATH_ADMIN_ROLES } from "../roles/constants";

// atom module
import { MODULE_PATH as MODULE_PATH_ATOM } from "../../atomModule";
import { PAGE_PATH as PAGE_PATH_ATOM_ATOMS } from "../../atomModule/atoms/constants";
import { PAGE_PATH as PAGE_PATH_ATOM_PASSWORD_GROUPS } from "../../atomModule/passwordGroups/constants";

// auto_discovery module
import { MODULE_PATH as MODULE_PATH_AUTO_DISCOVERY } from "../../autoDiscoveryModule";
import { PAGE_PATH as PAGE_PATH_AUTO_DISCOVERY_DASHBOARD } from "../../autoDiscoveryModule/dashboard/constants";
import { PAGE_PATH as PAGE_PATH_AUTO_DISCOVERY_DISCOVERY } from "../../autoDiscoveryModule/discovery/constants";
import { PAGE_PATH as PAGE_PATH_AUTO_DISCOVERY_LOGIN_CREDENTIALS } from "../../autoDiscoveryModule/manageCredentialsDropDown/loginCredentials/constants";
import { PAGE_PATH as PAGE_PATH_AUTO_DISCOVERY_V1_V2_CREDENTIALS } from "../../autoDiscoveryModule/manageCredentialsDropDown/snmpDropDown/v1V2Credentials/constants";
import { PAGE_PATH as PAGE_PATH_AUTO_DISCOVERY_V3_CREDENTIALS } from "../../autoDiscoveryModule/manageCredentialsDropDown/snmpDropDown/v3Credentials/constants";
import { PAGE_PATH as PAGE_PATH_AUTO_DISCOVERY_MANAGE_DEVICES } from "../../autoDiscoveryModule/manageDevices/constants";
import { PAGE_PATH as PAGE_PATH_AUTO_DISCOVERY_MANAGE_NETWORKS } from "../../autoDiscoveryModule/manageNetworks/constants";

// ipam module
import { MODULE_PATH as MODULE_PATH_IPAM } from "../../ipamModule";
import { PAGE_PATH as PAGE_PATH_IPAM_DASHBOARD } from "../../ipamModule/dashboard/constants";
import { PAGE_PATH as PAGE_PATH_IPAM_DEVICES } from "../../ipamModule/devices/constants";
import { PAGE_PATH as PAGE_PATH_IPAM_SUBNETS } from "../../ipamModule/subnetsDropDown/subnets/constants";
import { PAGE_PATH as PAGE_PATH_IPAM_IP_DETAILS } from "../../ipamModule/subnetsDropDown/ipDetails/constants";
import { PAGE_PATH as PAGE_PATH_IPAM_IP_HISTORY } from "../../ipamModule/subnetsDropDown/ipHistory/constants";
import { PAGE_PATH as PAGE_PATH_IPAM_DISCOVERED_SUBNETS } from "../../ipamModule/subnetsDropDown/discoveredSubnets/constants";
import { PAGE_PATH as PAGE_PATH_IPAM_DNS_SERVERS } from "../../ipamModule/dnsServerDropDown/dnsServers/constants";
import { PAGE_PATH as PAGE_PATH_IPAM_DNS_ZONES } from "../../ipamModule/dnsServerDropDown/dnsZones/constants";
import { PAGE_PATH as PAGE_PATH_IPAM_DNS_RECORDS } from "../../ipamModule/dnsServerDropDown/dnsRecords/constants";
import { PAGE_PATH as PAGE_PATH_IPAM_FIREWALLS } from "../../ipamModule/vipDropDown/firewalls/constants";
import { PAGE_PATH as PAGE_PATH_IPAM_LOAD_BALANCERS } from "../../ipamModule/vipDropDown/loadBalancers/constants";

// monitoring module
import { MODULE_PATH as MODULE_PATH_MONITORING } from "../../monitoringModule";

import { PAGE_PATH as PAGE_PATH_MONITORING_DASHBOARD } from "../../monitoringModule/dashboard/constants";
import { PAGE_PATH as PAGE_PATH_MONITORING_DEVICES } from "../../monitoringModule/devices/constants";
import { PAGE_PATH as PAGE_PATH_MONITORING_ALERTS } from "../../monitoringModule/alerts/constants";

import { PAGE_PATH as PAGE_PATH_MONITORING_LOGIN_CREDENTIALS } from "../../monitoringModule/manageCredentialsDropDown/loginCredentials/constants";
import { PAGE_PATH as PAGE_PATH_MONITORING_V1_V2_CREDENTIALS } from "../../monitoringModule/manageCredentialsDropDown/snmpDropDown/v1V2Credentials/constants";
import { PAGE_PATH as PAGE_PATH_MONITORING_V3_CREDENTIALS } from "../../monitoringModule/manageCredentialsDropDown/snmpDropDown/v3Credentials/constants";
//networks
import { PAGE_PATH as PAGE_PATH_MONITORING_NETWORKS_ALL_DEVICES_DEVICES } from "../../monitoringModule/networksDropDown/allDevicesDropDown/devices/constants";
import { PAGE_PATH as PAGE_PATH_MONITORING_NETWORKS_ALL_DEVICES_INTERFACES } from "../../monitoringModule/networksDropDown/allDevicesDropDown/interfaces/constants";

import { PAGE_PATH as PAGE_PATH_MONITORING_NETWORKS_ROUTERS_DEVICES } from "../../monitoringModule/networksDropDown/routersDropDown/devices/constants";
import { PAGE_PATH as PAGE_PATH_MONITORING_NETWORKS_ROUTERS_INTERFACES } from "../../monitoringModule/networksDropDown/routersDropDown/interfaces/constants";

import { PAGE_PATH as PAGE_PATH_MONITORING_NETWORKS_SWITCHES_DEVICES } from "../../monitoringModule/networksDropDown/switchesDropDown/devices/constants";
import { PAGE_PATH as PAGE_PATH_MONITORING_NETWORKS_SWITCHES_INTERFACES } from "../../monitoringModule/networksDropDown/switchesDropDown/interfaces/constants";

import { PAGE_PATH as PAGE_PATH_MONITORING_NETWORKS_FIREWALLS_DEVICES } from "../../monitoringModule/networksDropDown/firewallsDropDown/devices/constants";
import { PAGE_PATH as PAGE_PATH_MONITORING_NETWORKS_FIREWALLS_INTERFACES } from "../../monitoringModule/networksDropDown/firewallsDropDown/interfaces/constants";

import { PAGE_PATH as PAGE_PATH_MONITORING_NETWORKS_WIRELESS_DEVICES } from "../../monitoringModule/networksDropDown/wirelessDropDown/devices/constants";
import { PAGE_PATH as PAGE_PATH_MONITORING_NETWORKS_WIRELESS_INTERFACES } from "../../monitoringModule/networksDropDown/wirelessDropDown/interfaces/constants";
// servers
import { PAGE_PATH as PAGE_PATH_MONITORING_SERVERS_ALL_DEVICES_DEVICES } from "../../monitoringModule/serversDropDown/allDevicesDropDown/devices/constants";
import { PAGE_PATH as PAGE_PATH_MONITORING_SERVERS_ALL_DEVICES_INTERFACES } from "../../monitoringModule/serversDropDown/allDevicesDropDown/interfaces/constants";

import { PAGE_PATH as PAGE_PATH_MONITORING_SERVERS_LINUX_DEVICES } from "../../monitoringModule/serversDropDown/linuxDropDown/devices/constants";
import { PAGE_PATH as PAGE_PATH_MONITORING_SERVERS_LINUX_INTERFACES } from "../../monitoringModule/serversDropDown/linuxDropDown/interfaces/constants";

import { PAGE_PATH as PAGE_PATH_MONITORING_SERVERS_WINDOWS_DEVICES } from "../../monitoringModule/serversDropDown/windowsDropDown/devices/constants";
import { PAGE_PATH as PAGE_PATH_MONITORING_SERVERS_WINDOWS_INTERFACES } from "../../monitoringModule/serversDropDown/windowsDropDown/interfaces/constants";

// ncm module
import { MODULE_PATH as MODULE_PATH_NCM } from "../../ncmModule";
import { PAGE_PATH as PAGE_PATH_NCM_DASHBOARD } from "../../ncmModule/dashboard/constants";
import { PAGE_PATH as PAGE_PATH_NCM_MANAGE_CONFIGURATIONS } from "../../ncmModule/manageConfigurations/constants";
import { PAGE_PATH as PAGE_PATH_NCM_CONFIGURATION_BACKUPS } from "../../ncmModule/manageConfigurationsLanding/configurationBackups/constants";
import { PAGE_PATH as PAGE_PATH_NCM_REMOTE_COMMAND_SENDER } from "../../ncmModule/manageConfigurationsLanding/remoteCommandSender/constants";

// uam module
import { MODULE_PATH as MODULE_PATH_UAM } from "../../uamModule";
import { PAGE_PATH as PAGE_PATH_UAM_APS } from "../../uamModule/aps/constants";
import { PAGE_PATH as PAGE_PATH_UAM_BOARDS } from "../../uamModule/boards/constants";
import { PAGE_PATH as PAGE_PATH_UAM_DEVICES } from "../../uamModule/devices/constants";
import { PAGE_PATH as PAGE_PATH_UAM_HW_LIFECYCLES } from "../../uamModule/hwLifeCycles/constants";
import { PAGE_PATH as PAGE_PATH_UAM_LICENSES } from "../../uamModule/licenses/constants";
import { PAGE_PATH as PAGE_PATH_UAM_RACKS } from "../../uamModule/racks/constants";
import { PAGE_PATH as PAGE_PATH_UAM_SFPS } from "../../uamModule/sfps/constants";
import { PAGE_PATH as PAGE_PATH_UAM_SITES } from "../../uamModule/sites/constants";
import { PAGE_PATH as PAGE_PATH_UAM_SUB_BOARDS } from "../../uamModule/subBoards/constants";

export const defaultConfiguration = {
  [MODULE_PATH_DASHBOARD]: {
    view: true,
    pages: {
      [PAGE_PATH_DASHBOARD]: { view: true, read_only: false },
    },
  },
  [MODULE_PATH_ADMIN]: {
    view: true,
    pages: {
      [PAGE_PATH_ADMIN_MEMBERS]: { view: true, read_only: false },
      [PAGE_PATH_ADMIN_ROLES]: { view: true, read_only: false },
      [PAGE_PATH_ADMIN_FAILED_DEVICES_AUTO_DISCOVERY]: {
        view: true,
        read_only: false,
      },
      [PAGE_PATH_ADMIN_FAILED_DEVICES_IPAM]: { view: true, read_only: false },
      [PAGE_PATH_ADMIN_FAILED_DEVICES_MONITORING]: {
        view: true,
        read_only: false,
      },
      [PAGE_PATH_ADMIN_FAILED_DEVICES_NCM]: { view: true, read_only: false },
      [PAGE_PATH_ADMIN_FAILED_DEVICES_UAM]: { view: true, read_only: false },
    },
  },

  [MODULE_PATH_ATOM]: {
    view: true,
    pages: {
      [PAGE_PATH_ATOM_ATOMS]: { view: true, read_only: false },
      [PAGE_PATH_ATOM_PASSWORD_GROUPS]: { view: true, read_only: false },
    },
  },

  [MODULE_PATH_AUTO_DISCOVERY]: {
    view: true,
    pages: {
      [PAGE_PATH_AUTO_DISCOVERY_DASHBOARD]: { view: true, read_only: false },
      [PAGE_PATH_AUTO_DISCOVERY_DISCOVERY]: { view: true, read_only: false },
      [PAGE_PATH_AUTO_DISCOVERY_MANAGE_DEVICES]: {
        view: true,
        read_only: false,
      },
      [PAGE_PATH_AUTO_DISCOVERY_MANAGE_NETWORKS]: {
        view: true,
        read_only: false,
      },
      [PAGE_PATH_AUTO_DISCOVERY_LOGIN_CREDENTIALS]: {
        view: true,
        read_only: false,
      },
      [PAGE_PATH_AUTO_DISCOVERY_V1_V2_CREDENTIALS]: {
        view: true,
        read_only: false,
      },
      [PAGE_PATH_AUTO_DISCOVERY_V3_CREDENTIALS]: {
        view: true,
        read_only: false,
      },
    },
  },

  [MODULE_PATH_IPAM]: {
    view: true,
    pages: {
      [PAGE_PATH_IPAM_DASHBOARD]: { view: true, read_only: false },
      [PAGE_PATH_IPAM_DEVICES]: { view: true, read_only: false },
      [PAGE_PATH_IPAM_SUBNETS]: { view: true, read_only: false },
      [PAGE_PATH_IPAM_IP_DETAILS]: { view: true, read_only: false },
      [PAGE_PATH_IPAM_IP_HISTORY]: { view: true, read_only: false },
      [PAGE_PATH_IPAM_DISCOVERED_SUBNETS]: { view: true, read_only: false },
      [PAGE_PATH_IPAM_DNS_SERVERS]: { view: true, read_only: false },
      [PAGE_PATH_IPAM_DNS_ZONES]: { view: true, read_only: false },
      [PAGE_PATH_IPAM_DNS_RECORDS]: { view: true, read_only: false },
      [PAGE_PATH_IPAM_FIREWALLS]: { view: true, read_only: false },
      [PAGE_PATH_IPAM_LOAD_BALANCERS]: { view: true, read_only: false },
    },
  },

  [MODULE_PATH_MONITORING]: {
    view: true,
    pages: {
      [PAGE_PATH_MONITORING_DASHBOARD]: { view: true, read_only: false },
      [PAGE_PATH_MONITORING_DEVICES]: { view: true, read_only: false },
      [PAGE_PATH_MONITORING_ALERTS]: { view: true, read_only: false },
      [PAGE_PATH_MONITORING_LOGIN_CREDENTIALS]: {
        view: true,
        read_only: false,
      },
      [PAGE_PATH_MONITORING_V1_V2_CREDENTIALS]: {
        view: true,
        read_only: false,
      },
      [PAGE_PATH_MONITORING_V3_CREDENTIALS]: { view: true, read_only: false },
      [PAGE_PATH_MONITORING_NETWORKS_ALL_DEVICES_DEVICES]: {
        view: true,
        read_only: false,
      },
      [PAGE_PATH_MONITORING_NETWORKS_ALL_DEVICES_INTERFACES]: {
        view: true,
        read_only: false,
      },
      [PAGE_PATH_MONITORING_NETWORKS_ROUTERS_DEVICES]: {
        view: true,
        read_only: false,
      },
      [PAGE_PATH_MONITORING_NETWORKS_ROUTERS_INTERFACES]: {
        view: true,
        read_only: false,
      },
      [PAGE_PATH_MONITORING_NETWORKS_SWITCHES_DEVICES]: {
        view: true,
        read_only: false,
      },
      [PAGE_PATH_MONITORING_NETWORKS_SWITCHES_INTERFACES]: {
        view: true,
        read_only: false,
      },
      [PAGE_PATH_MONITORING_NETWORKS_FIREWALLS_DEVICES]: {
        view: true,
        read_only: false,
      },
      [PAGE_PATH_MONITORING_NETWORKS_FIREWALLS_INTERFACES]: {
        view: true,
        read_only: false,
      },
      [PAGE_PATH_MONITORING_NETWORKS_WIRELESS_DEVICES]: {
        view: true,
        read_only: false,
      },
      [PAGE_PATH_MONITORING_NETWORKS_WIRELESS_INTERFACES]: {
        view: true,
        read_only: false,
      },
      [PAGE_PATH_MONITORING_SERVERS_ALL_DEVICES_DEVICES]: {
        view: true,
        read_only: false,
      },
      [PAGE_PATH_MONITORING_SERVERS_ALL_DEVICES_INTERFACES]: {
        view: true,
        read_only: false,
      },
      [PAGE_PATH_MONITORING_SERVERS_LINUX_DEVICES]: {
        view: true,
        read_only: false,
      },
      [PAGE_PATH_MONITORING_SERVERS_LINUX_INTERFACES]: {
        view: true,
        read_only: false,
      },
      [PAGE_PATH_MONITORING_SERVERS_WINDOWS_DEVICES]: {
        view: true,
        read_only: false,
      },
      [PAGE_PATH_MONITORING_SERVERS_WINDOWS_INTERFACES]: {
        view: true,
        read_only: false,
      },
    },
  },

  [MODULE_PATH_NCM]: {
    view: true,
    pages: {
      [PAGE_PATH_NCM_DASHBOARD]: { view: true, read_only: false },
      [PAGE_PATH_NCM_MANAGE_CONFIGURATIONS]: { view: true, read_only: false },
      [PAGE_PATH_NCM_CONFIGURATION_BACKUPS]: { view: true, read_only: false },
      [PAGE_PATH_NCM_REMOTE_COMMAND_SENDER]: { view: true, read_only: false },
    },
  },

  [MODULE_PATH_UAM]: {
    view: true,
    pages: {
      [PAGE_PATH_UAM_DEVICES]: { view: true, read_only: false },
      [PAGE_PATH_UAM_SITES]: { view: true, read_only: false },
      [PAGE_PATH_UAM_RACKS]: { view: true, read_only: false },
      [PAGE_PATH_UAM_BOARDS]: { view: true, read_only: false },
      [PAGE_PATH_UAM_SUB_BOARDS]: { view: true, read_only: false },
      [PAGE_PATH_UAM_HW_LIFECYCLES]: { view: true, read_only: false },
      [PAGE_PATH_UAM_LICENSES]: { view: true, read_only: false },
      [PAGE_PATH_UAM_APS]: { view: true, read_only: false },
      [PAGE_PATH_UAM_SFPS]: { view: true, read_only: false },
    },
  },
};
