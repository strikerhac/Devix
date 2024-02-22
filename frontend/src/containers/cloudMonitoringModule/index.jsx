import React from "react";
import { Outlet } from "react-router-dom";
import { getDefaultPagePath } from "../../utils/helpers";
import { useAuthorization } from "../../hooks/useAuth";
import Card from "../../components/cards";
import HorizontalMenu from "../../components/horizontalMenu/index";
import {
  PAGE_NAME as PAGE_NAME_RUNNING_SERVICES,
  PAGE_PATH as PAGE_PATH_RUNNING_SERVICES,
} from "./aws/runningServices/constants";
import {
  PAGE_NAME as PAGE_NAME_EC2,
  PAGE_PATH as PAGE_PATH_EC2,
} from "./aws/ec2/constants";
import {
  PAGE_NAME as PAGE_NAME_ELB,
  PAGE_PATH as PAGE_PATH_ELB,
} from "./aws/elb/constants";
import {
  PAGE_NAME as PAGE_NAME_S3,
  PAGE_PATH as PAGE_PATH_S3,
} from "./aws/s3/constants";

import { MAIN_LAYOUT_PATH } from "../../layouts/mainLayout";

export const MODULE_NAME = "Cloud Monitoring";
export const MODULE_PATH = "cloud_monitoring_module";

function Index(props) {
  let menuItems = [
    {
      id: PAGE_PATH_RUNNING_SERVICES,
      name: PAGE_NAME_RUNNING_SERVICES,
      path: PAGE_PATH_RUNNING_SERVICES,
      icon: "tdesign:device",
    },
    {
      id: PAGE_PATH_EC2,
      name: PAGE_NAME_EC2,
      path: PAGE_PATH_EC2,
      icon: "ic:outline-dashboard",
    },
    {
      id: PAGE_PATH_ELB,
      name: PAGE_NAME_ELB,
      path: PAGE_PATH_ELB,
      icon: "tdesign:device",
    },
    {
      id: PAGE_PATH_S3,
      name: PAGE_NAME_S3,
      path: PAGE_PATH_S3,
      icon: "tdesign:device",
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
