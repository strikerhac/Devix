import React from "react";
import { Outlet } from "react-router-dom";
import { useSelector } from "react-redux";
import { selectFailedDevicesCounts } from "../../../store/features/adminModule/failedDevices/landing/selectors";
import { useFetchRecordsQuery } from "../../../store/features/adminModule/failedDevices/landing/apis";
import { getPathAllSegments } from "../../../utils/helpers";
import { useAuthorization } from "../../../hooks/useAuth";
import useErrorHandling, { TYPE_FETCH } from "../../../hooks/useErrorHandling";
import DefaultDetailCards from "../../../components/detailCards";
import Card from "../../../components/cards";
import HorizontalMenu from "../../../components/horizontalMenu/index";
import DefaultSpinner from "../../../components/spinners";
import {
  PAGE_NAME as PAGE_NAME_AUTO_DISCOVERY,
  PAGE_PATH as PAGE_PATH_AUTO_DISCOVERY,
} from "./autoDiscovery/constants";
import {
  PAGE_NAME as PAGE_NAME_IPAM,
  PAGE_PATH as PAGE_PATH_IPAM,
} from "./ipam/constants";
import {
  PAGE_NAME as PAGE_NAME_MONITORING,
  PAGE_PATH as PAGE_PATH_MONITORING,
} from "./monitoring/constants";
import {
  PAGE_NAME as PAGE_NAME_NCM,
  PAGE_PATH as PAGE_PATH_NCM,
} from "./ncm/constants";
import {
  PAGE_NAME as PAGE_NAME_UAM,
  PAGE_PATH as PAGE_PATH_UAM,
} from "./uam/constants";
import { MODULE_PATH } from "..";

export const LANDING_PAGE_NAME = "Failed Devices";
export const LANDING_PAGE_PATH = "failed_devices_landing";

function Index(props) {
  let menuItems = [
    {
      id: PAGE_PATH_AUTO_DISCOVERY,
      name: PAGE_NAME_AUTO_DISCOVERY,
      path: PAGE_PATH_AUTO_DISCOVERY,
      icon: "iconamoon:discover-light",
    },
    {
      id: PAGE_PATH_IPAM,
      name: PAGE_NAME_IPAM,
      path: PAGE_PATH_IPAM,
      icon: "carbon:kubernetes-ip-address",
    },
    {
      id: PAGE_PATH_MONITORING,
      name: PAGE_NAME_MONITORING,
      path: PAGE_PATH_MONITORING,
      icon: "eos-icons:monitoring",
    },
    {
      id: PAGE_PATH_NCM,
      name: PAGE_NAME_NCM,
      path: PAGE_PATH_NCM,
      icon: "carbon:network-2",
    },
    {
      id: PAGE_PATH_UAM,
      name: PAGE_NAME_UAM,
      path: PAGE_PATH_UAM,
      icon: "icon-park-outline:category-management",
    },
  ];

  // hooks
  const { getUserInfoFromAccessToken, filterPageMenus } = useAuthorization();

  // user information
  const userInfo = getUserInfoFromAccessToken();
  const roleConfigurations = userInfo?.configuration;

  menuItems = filterPageMenus(menuItems, roleConfigurations, MODULE_PATH);

  const selectedFailedDevicesCounts = useSelector(selectFailedDevicesCounts);

  // apis
  const {
    data: fetchRecordsData,
    isSuccess: isFetchRecordsSuccess,
    isLoading: isFetchRecordsLoading,
    isError: isFetchRecordsError,
    error: fetchRecordsError,
  } = useFetchRecordsQuery();

  // error handling custom hooks
  useErrorHandling({
    data: fetchRecordsData,
    isSuccess: isFetchRecordsSuccess,
    isError: isFetchRecordsError,
    error: fetchRecordsError,
    type: TYPE_FETCH,
  });

  let pagePath = getPathAllSegments();
  if (pagePath.length === 4 && pagePath[3] === LANDING_PAGE_PATH) {
    pagePath = [PAGE_PATH_AUTO_DISCOVERY];
  } else pagePath = pagePath.splice(4);

  return (
    <DefaultSpinner spinning={isFetchRecordsLoading}>
      {selectedFailedDevicesCounts ? (
        <DefaultDetailCards
          data={{
            [PAGE_PATH_AUTO_DISCOVERY]:
              selectedFailedDevicesCounts[PAGE_PATH_AUTO_DISCOVERY],
            [PAGE_PATH_IPAM]: selectedFailedDevicesCounts[PAGE_PATH_IPAM],
            [PAGE_PATH_MONITORING]:
              selectedFailedDevicesCounts[PAGE_PATH_MONITORING],
            [PAGE_PATH_NCM]: selectedFailedDevicesCounts[PAGE_PATH_NCM],
            [PAGE_PATH_UAM]: selectedFailedDevicesCounts[PAGE_PATH_UAM],
          }}
          icons={[
            "iconamoon:discover-light",
            "carbon:kubernetes-ip-address",
            "eos-icons:monitoring",
            "carbon:network-2",
            "icon-park-outline:category-management",
          ]}
        />
      ) : null}
      <Card>
        <HorizontalMenu menuItems={menuItems} defaultPagePath={pagePath} />
      </Card>
      <Outlet />
      <br />
      <br />
      <br />
    </DefaultSpinner>
  );
}

export default Index;
