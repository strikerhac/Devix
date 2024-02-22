import React from "react";
import { Navigate } from "react-router-dom";
import { ACCESS_TOKEN } from "../containers/login/constants";
import { useNavigate } from "react-router-dom";
import { clearLocalStorageOnLogout } from "../store";
import { MAIN_LAYOUT_PATH } from "../layouts/mainLayout";
import CryptoJS from "crypto-js";
import jwt from "jsonwebtoken";
import { defaultConfiguration } from "../containers/adminModule/roles/defaultConfiguration";

export function useAuthorization() {
  function getUserInfoFromAccessToken() {
    const accessToken = localStorage.getItem(ACCESS_TOKEN);
    if (accessToken) {
      let userInfo = jwt.decode(accessToken);
      if (userInfo) {
        userInfo = {
          ...userInfo,
          configuration: JSON.parse(userInfo?.configuration),
          // configuration: defaultConfiguration,
        };
        return userInfo;
      } else return null;
    } else {
      return null;
    }
  }

  function isModuleAllowed(roleConfigurations, module) {
    return roleConfigurations ? roleConfigurations[module]?.view : true;
  }

  function isPageAllowed(roleConfigurations, module, page) {
    if (page && page?.indexOf("/") !== -1) {
      let pageParts = page?.split("/");
      page = pageParts[pageParts?.length - 1];
    }

    if (roleConfigurations && roleConfigurations[module]?.pages[page]) {
      return roleConfigurations
        ? roleConfigurations[module]?.pages[page]?.view
        : true;
    } else {
      return true;
    }
  }

  function isPageEditable(roleConfigurations, module, page) {
    return roleConfigurations
      ? !roleConfigurations[module]?.pages[page]?.read_only
      : true;
  }

  function removeEmptyChildren(data) {
    console.log("removeEmptyChildren");
    return data.reduce((acc, item) => {
      const newItem = { ...item };

      if (newItem.children && newItem.children.length > 0) {
        newItem.children = removeEmptyChildren(newItem.children);
      }

      if (newItem.children && newItem.children.length > 0) {
        acc.push(newItem);
      } else if (!newItem.children) {
        acc.push(newItem);
      }

      return acc;
    }, []);
  }

  // Define a recursive function to filter menus and their children
  function filterPageMenus(menus, roleConfigurations, modulePath) {
    console.log("filterPageMenus");
    menus = menus
      ?.filter((item) =>
        isPageAllowed(roleConfigurations, modulePath, item.path)
      )
      .map((item) => {
        if (item.children) {
          return {
            ...item,
            children: filterPageMenus(
              item.children,
              roleConfigurations,
              modulePath
            ),
          };
        }
        return item;
      });
    return removeEmptyChildren(menus);
  }

  // Define a recursive function to filter routes and their children
  function filterPageRoutes(routes, roleConfigurations, modulePath) {
    console.log("filterPageRoutes");
    return routes
      ?.filter((item) =>
        isPageAllowed(roleConfigurations, modulePath, item.path)
      )
      .map((item) => {
        if (item.children) {
          return {
            ...item,
            children: filterPageRoutes(
              item.children,
              roleConfigurations,
              modulePath
            ),
          };
        }
        return item;
      });
  }

  function createDefaultPageRoute(routes, defaultPath) {
    if (routes?.length > 0) {
      if (routes[0].path) {
        routes = [
          {
            path: defaultPath,
            element: <Navigate to={routes[0].path} replace />,
          },
          ...routes,
        ];
      }
    }
    return routes;
  }

  function authorizePageRoutes({
    module,
    pageRoutes,
    roleConfigurations,
    defaultPagePath,
  }) {
    let authorizedPageRoutes = filterPageRoutes(
      pageRoutes,
      roleConfigurations,
      module
    );
    return createDefaultPageRoute(authorizedPageRoutes, defaultPagePath);
  }

  function decryptData(encryptedData, key) {
    // const key = "Sixteen byte key";
    // if (decodedToken) {
    //   let str = decodedToken.encrypted_data }
    //   const decryptedData = decryptDataNew(
    //     JSON.stringify({ str),
    //     key
    //   );
    //   console.log("decryptedData", decryptedData);
    // }

    // Decode URL-safe base64
    const decodedData = CryptoJS.enc.Base64.parse(encryptedData);

    // Extract IV (first 16 bytes) and encrypted data
    const iv = decodedData.words.slice(0, 4);
    const encryptedBytes = decodedData.words.slice(4);

    // Convert key to WordArray
    const keyWordArray = CryptoJS.enc.Utf8.parse(key);

    // Create an AES cipher object
    const cipher = CryptoJS.algo.AES.createDecryptor(keyWordArray, {
      iv: CryptoJS.lib.WordArray.create(iv),
      mode: CryptoJS.mode.CFB,
      padding: CryptoJS.pad.Pkcs7,
    });

    // Decrypt the data
    const decryptedBytes = cipher.process(
      CryptoJS.lib.WordArray.create(encryptedBytes)
    );
    const finalBytes = cipher.finalize();

    // Convert to UTF-8
    const decryptedData = CryptoJS.enc.Utf8.stringify(
      decryptedBytes.concat(finalBytes)
    );
    return decryptedData;
  }

  return {
    getUserInfoFromAccessToken,
    isModuleAllowed,
    isPageAllowed,
    isPageEditable,
    filterPageMenus,
    filterPageRoutes,
    createDefaultPageRoute,
    authorizePageRoutes,
  };
}

export function useAuthentication() {
  const navigate = useNavigate();

  function onSuccessfulLogin() {
    navigate(`/${MAIN_LAYOUT_PATH}`);
  }

  function handleLogout() {
    localStorage.removeItem(ACCESS_TOKEN);
    clearLocalStorageOnLogout();
    navigate("/");
  }

  return {
    onSuccessfulLogin,
    handleLogout,
  };
}
