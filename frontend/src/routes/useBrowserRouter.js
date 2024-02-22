import React from "react";
import { Navigate } from "react-router-dom";
import { createBrowserRouter } from "react-router-dom";
import { useAuthorization } from "../hooks/useAuth";
import Login from "../containers/login";
import MainLayout from "../layouts/mainLayout";
import dashboardModuleRoutes from "./dashboardModuleRoutes";
import adminModuleRoutes from "./adminModuleRoutes";
import atomModuleRoutes from "./atomModuleRoutes";
import uamModuleRoutes from "./uamModuleRoutes";
import monitoringModuleRoutes from "./monitoringModuleRoutes";
import autoDiscoveryModuleRoutes from "./autoDiscoveryModuleRoutes";
import ncmModuleRoutes from "./ncmModuleRoutes";
import ipamModuleRoutes from "./ipamModuleRoutes";
import DefaultFallbackUI from "../components/fallbackUI";
import { MAIN_LAYOUT_PATH } from "../layouts/mainLayout";

export default function useBrowserRouter() {
  const { getUserInfoFromAccessToken, isModuleAllowed, authorizePageRoutes } =
    useAuthorization();

  function generateRoutes(roleConfigurations, authorizePageRoutes) {
    let routes = [
      {
        path: "/",
        element: <Login />,
      },
      {
        path: MAIN_LAYOUT_PATH,
        element: <MainLayout />,
        children: [
          dashboardModuleRoutes(roleConfigurations, authorizePageRoutes),
          adminModuleRoutes(roleConfigurations, authorizePageRoutes),
          atomModuleRoutes(roleConfigurations, authorizePageRoutes),
          autoDiscoveryModuleRoutes(roleConfigurations, authorizePageRoutes),
          ipamModuleRoutes(roleConfigurations, authorizePageRoutes),
          monitoringModuleRoutes(roleConfigurations, authorizePageRoutes),
          ncmModuleRoutes(roleConfigurations, authorizePageRoutes),
          uamModuleRoutes(roleConfigurations, authorizePageRoutes),
        ].filter((item) => isModuleAllowed(roleConfigurations, item.path)),

        errorElement: <DefaultFallbackUI />,
      },
    ];

    const modules = routes[1].children;
    if (modules?.length > 0) {
      if (modules[0].path) {
        routes[1].children = [
          {
            path: `/${MAIN_LAYOUT_PATH}`,
            element: <Navigate to={modules[0].path} replace />,
          },
          ...modules,
        ];
      }
    }

    return routes;
  }

  // user information
  const userInfo = getUserInfoFromAccessToken();
  const roleConfigurations = userInfo?.configuration;

  const routes = generateRoutes(roleConfigurations, authorizePageRoutes);
  const browserRouter = createBrowserRouter(routes);

  return browserRouter;
}
