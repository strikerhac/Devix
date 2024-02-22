import React from "react";
import { Outlet } from "react-router-dom";
import { useSelector } from "react-redux";
import { selectSelectedDevice } from "../../../store/features/monitoringModule/devices/selectors";
import { getPathAllSegments } from "../../../utils/helpers";
import { useAuthorization } from "../../../hooks/useAuth";
import HorizontalMenu from "../../../components/horizontalMenu/index";
import Card from "../../../components/cards";
import DefaultDetailCards from "../../../components/detailCards";
import firewallIcon from "../../../resources/designRelatedSvgs/firewall.svg";
import deviceIcon from "../../../resources/designRelatedSvgs/otherDevices.svg";
import switchIcon from "../../../resources/designRelatedSvgs/switches.svg";
import { indexColumnNameConstants } from "../devices/constants";
import {
  PAGE_NAME as PAGE_NAME_DEVICES_SUMMARY,
  PAGE_PATH as PAGE_PATH_DEVICES_SUMMARY,
} from "./summary/constants";
import {
  PAGE_NAME as PAGE_NAME_DEVICES_INTERFACES,
  PAGE_PATH as PAGE_PATH_DEVICES_INTERFACES,
} from "./interfaces/constants";
import { MODULE_PATH } from "..";

export const LANDING_PAGE_NAME = "Device Details";
export const LANDING_PAGE_PATH = "devices_landing";

function Index(props) {
  let menuItems = [
    {
      id: PAGE_PATH_DEVICES_SUMMARY,
      name: PAGE_NAME_DEVICES_SUMMARY,
      path: PAGE_PATH_DEVICES_SUMMARY,
      icon: "solar:graph-broken",
    },
    {
      id: PAGE_PATH_DEVICES_INTERFACES,
      name: PAGE_NAME_DEVICES_INTERFACES,
      path: PAGE_PATH_DEVICES_INTERFACES,
      icon: "carbon:network-interface",
    },
  ];

  // hooks
  const { getUserInfoFromAccessToken, filterPageMenus } = useAuthorization();

  // user information
  const userInfo = getUserInfoFromAccessToken();
  const roleConfigurations = userInfo?.configuration;

  menuItems = filterPageMenus(menuItems, roleConfigurations, MODULE_PATH);

  const selectedDevice = useSelector(selectSelectedDevice);

  let pagePath = getPathAllSegments();
  if (pagePath.length === 4 && pagePath[3] === LANDING_PAGE_PATH) {
    pagePath = [PAGE_PATH_DEVICES_SUMMARY];
  } else pagePath = pagePath.splice(4);

  return (
    <>
      {selectedDevice ? (
        <DefaultDetailCards
          data={{
            [indexColumnNameConstants.IP_ADDRESS]:
              selectedDevice[indexColumnNameConstants.IP_ADDRESS],
            [indexColumnNameConstants.DEVICE_NAME]:
              selectedDevice[indexColumnNameConstants.DEVICE_NAME],
            [indexColumnNameConstants.DEVICE_TYPE]:
              selectedDevice[indexColumnNameConstants.DEVICE_TYPE],
            [indexColumnNameConstants.FUNCTION]:
              selectedDevice[indexColumnNameConstants.FUNCTION],
            [indexColumnNameConstants.VENDOR]:
              selectedDevice[indexColumnNameConstants.VENDOR],
          }}
          icons={[
            "carbon:kubernetes-ip-address",
            "tdesign:device",
            "lucide:file-type",
            "lucide:function-square",
            "material-symbols:source-environment",
          ]}
        />
      ) : null}
      <Card>
        <HorizontalMenu menuItems={menuItems} defaultPagePath={pagePath} />
      </Card>
      <Outlet />
    </>
  );
}

export default Index;
