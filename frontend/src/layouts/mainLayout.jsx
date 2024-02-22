import React, { useState, useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import { styled, useTheme } from "@mui/material/styles";
import Box from "@mui/material/Box";
import MuiDrawer from "@mui/material/Drawer";
import List from "@mui/material/List";
import Divider from "@mui/material/Divider";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import { Outlet } from "react-router-dom";
import Tooltip from "@mui/material/Tooltip";
import { AppContext } from "../context/appContext";
import dashboardInactiveIcon from "../resources/svgs/dashboardInactiveIcon.svg";
import dashboardActiveIcon from "../resources/svgs/dashboardActiveIcon.svg";
import adminInactiveIcon from "../resources/svgs/adminInActiveIcon.svg";
import adminActiveIcon from "../resources/svgs/adminActiveIcon.svg";
import monitoringInactiveIcon from "../resources/svgs/monitoringInactiveIcon.svg";
import monitoringActiveIcon from "../resources/svgs/monitoringActiveIcon.svg";
import atomInactiveIcon from "../resources/svgs/atomInactiveIcon.svg";
import atomActiveIcon from "../resources/svgs/atomActiveIcon.svg";
import ipamInactiveIcon from "../resources/svgs/ipamInactiveIcon.svg";
import ipamActiveIcon from "../resources/svgs/ipamActiveIcon.svg";
import autoDiscoveryInactiveIcon from "../resources/svgs/autoDiscoveryInactiveIcon.svg";
import autoDiscoveryActiveIcon from "../resources/svgs/autoDiscoveryActiveIcon.svg";
import uamInactiveIcon from "../resources/svgs/uamInactiveIcon.svg";
import uamActiveIcon from "../resources/svgs/uamActiveIcon.svg";
import ncmInactiveIcon from "../resources/svgs/ncmInactiveIcon.svg";
import ncmActiveIcon from "../resources/svgs/ncmActiveIcon.svg";
import logo from "../resources/svgs/logo.svg";
import dayModeIcon from "../resources/svgs/dayModeIcon.svg";
import nightModeIcon from "../resources/svgs/nightModeIcon.svg";
import { useSelector } from "react-redux/es/hooks/useSelector";
import { selectIsValidAccessToken } from "../store/features/login/selectors";
import { useValidateTokenMutation } from "../store/features/login/apis";
import { getPathSegment } from "../utils/helpers";
import { useAuthentication, useAuthorization } from "../hooks/useAuth";
import { ProfilePicturePopup } from "../components/popups";
import {
  MODULE_PATH as MODULE_PATH_DASHBOARD,
  MODULE_NAME as MODULE_NAME_DASHBOARD,
} from "../containers/dashboardModule";
import {
  MODULE_PATH as MODULE_PATH_ADMIN,
  MODULE_NAME as MODULE_NAME_ADMIN,
} from "../containers/adminModule";
import {
  MODULE_PATH as MODULE_PATH_ATOM,
  MODULE_NAME as MODULE_NAME_ATOM,
} from "../containers/atomModule";
import {
  MODULE_PATH as MODULE_PATH_AUTO_DISCOVERY,
  MODULE_NAME as MODULE_NAME_AUTO_DISCOVERY,
} from "../containers/autoDiscoveryModule";
import {
  MODULE_PATH as MODULE_PATH_IPAM,
  MODULE_NAME as MODULE_NAME_IPAM,
} from "../containers/ipamModule";
import {
  MODULE_PATH as MODULE_PATH_MONITORING,
  MODULE_NAME as MODULE_NAME_MONITORING,
} from "../containers/monitoringModule";
import {
  MODULE_PATH as MODULE_PATH_NCM,
  MODULE_NAME as MODULE_NAME_NCM,
} from "../containers/ncmModule";
import {
  MODULE_PATH as MODULE_PATH_UAM,
  MODULE_NAME as MODULE_NAME_UAM,
} from "../containers/uamModule";
import { ACCESS_TOKEN } from "../containers/login/constants";

export const MAIN_LAYOUT_PATH = "monetx";
const drawerWidth = 240;

const openedMixin = (theme) => ({
  width: drawerWidth,
  transition: theme.transitions.create("width", {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.enteringScreen,
  }),
  overflowX: "hidden",
});

const closedMixin = (theme) => ({
  transition: theme.transitions.create("width", {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  overflowX: "hidden",
  width: `calc(${theme.spacing(7)} + 1px)`,
  [theme.breakpoints.up("sm")]: {
    width: `calc(${theme.spacing(8)} + 1px)`,
  },
});

const DrawerHeader = styled("div")(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  padding: theme.spacing(0, 1),
  backgroundColor: theme?.palette?.main_layout?.background,
  ...theme.mixins.toolbar,
}));

const Drawer = styled(MuiDrawer, {
  shouldForwardProp: (prop) => prop !== "open",
})(({ theme, open }) => ({
  width: drawerWidth,
  flexShrink: 0,
  whiteSpace: "nowrap",
  boxSizing: "border-box",
  backgroundColor: theme?.palette?.main_layout?.background, // Set open state background color here
  ...(open && {
    ...openedMixin(theme),
    "& .MuiDrawer-paper": {
      ...openedMixin(theme),
      backgroundColor: theme?.palette?.main_layout?.background, // Set open state background color here
    },
  }),
  ...(!open && {
    ...closedMixin(theme),
    "& .MuiDrawer-paper": {
      ...closedMixin(theme),
      backgroundColor: theme?.palette?.main_layout?.background, // Set open state background color here
    },
  }),
}));

export default function Index() {
  const navigate = useNavigate();
  const { handleLogout } = useAuthentication();
  const { getUserInfoFromAccessToken, isModuleAllowed } = useAuthorization();
  const isValidAccessToken = useSelector(selectIsValidAccessToken);

  // user information
  const userInfo = getUserInfoFromAccessToken();
  const roleConfigurations = userInfo?.configuration;

  const modulePath = getPathSegment(3);
  console.log("modulePath", modulePath);
  const theme = useTheme();
  const { isDarkMode, setDarkMode } = useContext(AppContext);
  const [open, setOpen] = useState(false);

  // post api for the form
  const [
    validateToken,
    {
      data: validateTokenData,
      isSuccess: isValidateTokenSuccess,
      isLoading: isValidateTokenLoading,
      isError: isValidateTokenError,
      error: validateTokenError,
    },
  ] = useValidateTokenMutation();

  // effects
  useEffect(() => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    if (!token) {
      navigate("/");
    } else {
      validateToken({ access_token: token });
    }
  }, []);

  useEffect(() => {
    console.log("validateTokenData", validateTokenData);
    if (validateTokenData) {
      if (!validateTokenData.data.access_token) {
        console.log("validateTokenData", validateTokenData.data.access_token);
        navigate("/");
      }
    }
  }, [validateTokenData]);

  const toggleTheme = () => {
    setDarkMode(!isDarkMode);
  };

  const drawerMenuItems = [
    {
      name: MODULE_NAME_DASHBOARD,
      inActiveIcon: (
        <img src={dashboardInactiveIcon} alt={MODULE_NAME_DASHBOARD} />
      ),
      activeIcon: <img src={dashboardActiveIcon} alt={MODULE_NAME_DASHBOARD} />,
      path: MODULE_PATH_DASHBOARD,
    },
    {
      name: MODULE_NAME_ADMIN,
      inActiveIcon: <img src={adminInactiveIcon} alt={MODULE_NAME_ADMIN} />,
      activeIcon: <img src={adminActiveIcon} alt={MODULE_NAME_ADMIN} />,
      path: MODULE_PATH_ADMIN,
    },
    {
      name: MODULE_NAME_ATOM,
      inActiveIcon: <img src={atomInactiveIcon} alt={MODULE_NAME_ATOM} />,
      activeIcon: <img src={atomActiveIcon} alt={MODULE_NAME_ATOM} />,
      path: MODULE_PATH_ATOM,
    },
    {
      name: MODULE_NAME_AUTO_DISCOVERY,
      inActiveIcon: (
        <img src={autoDiscoveryInactiveIcon} alt={MODULE_NAME_AUTO_DISCOVERY} />
      ),
      activeIcon: (
        <img src={autoDiscoveryActiveIcon} alt={MODULE_NAME_AUTO_DISCOVERY} />
      ),
      path: MODULE_PATH_AUTO_DISCOVERY,
    },
    {
      name: MODULE_NAME_IPAM,
      inActiveIcon: <img src={ipamInactiveIcon} alt={MODULE_NAME_IPAM} />,
      activeIcon: <img src={ipamActiveIcon} alt={MODULE_NAME_IPAM} />,
      path: MODULE_PATH_IPAM,
    },
    {
      name: MODULE_NAME_MONITORING,
      inActiveIcon: (
        <img src={monitoringInactiveIcon} alt={MODULE_NAME_MONITORING} />
      ),
      activeIcon: (
        <img src={monitoringActiveIcon} alt={MODULE_NAME_MONITORING} />
      ),
      path: MODULE_PATH_MONITORING,
    },
    {
      name: MODULE_NAME_NCM,
      inActiveIcon: <img src={ncmInactiveIcon} alt={MODULE_NAME_NCM} />,
      activeIcon: <img src={ncmActiveIcon} alt={MODULE_NAME_NCM} />,
      path: MODULE_PATH_NCM,
    },
    {
      name: MODULE_NAME_UAM,
      inActiveIcon: <img src={uamInactiveIcon} alt={MODULE_NAME_UAM} />,
      activeIcon: <img src={uamActiveIcon} alt={MODULE_NAME_UAM} />,
      path: MODULE_PATH_UAM,
    },
  ].filter((item) => isModuleAllowed(roleConfigurations, item.path));

  const [selectedModule, setSelectedModule] = useState(
    drawerMenuItems.find((item) => item.path === modulePath)
  );

  // effects
  useEffect(() => {
    if (validateTokenData && drawerMenuItems.length > 0) {
      setSelectedModule(
        drawerMenuItems.find((item) => item.path === modulePath)
      );
    }
  }, [validateTokenData, drawerMenuItems]);

  return (
    <>
      {isValidAccessToken ? (
        <Box sx={{ display: "flex", zIndex: "9", position: "relative" }}>
          <Drawer variant="permanent" open={open}>
            <DrawerHeader>
              <img src={logo} alt="Montex" />
            </DrawerHeader>
            <Divider />

            <List style={{ padding: 0 }}>
              {drawerMenuItems?.map((item, index) => (
                <Tooltip key={item.name} title={item.name} placement="right">
                  <Link to={item.path}>
                    <ListItem
                      key={item.name}
                      disablePadding
                      onClick={() => setSelectedModule(item)}
                    >
                      <ListItemButton
                        sx={{
                          justifyContent: open ? "initial" : "center",
                          padding: 0,
                        }}
                      >
                        <ListItemIcon
                          sx={{
                            minWidth: 0,
                            justifyContent: "center",
                          }}
                        >
                          {selectedModule?.path === item.path
                            ? item.activeIcon
                            : item.inActiveIcon}
                        </ListItemIcon>
                        <ListItemText
                          primary={item.name}
                          sx={{ opacity: open ? 1 : 0 }}
                        />
                      </ListItemButton>
                    </ListItem>
                  </Link>
                </Tooltip>
              ))}
            </List>
          </Drawer>
          <Box
            component="main"
            sx={{
              flexGrow: 1,
              p: 0,
              border: "0px solid red",
              minHeight: "100vh",
            }}
          >
            <DrawerHeader
              sx={{
                display: "flex",
                justifyContent: "space-between",
                padding: "0 20px",
                borderBottom: `0.5px solid ${theme?.palette?.main_layout?.border_bottom}`,
              }}
            >
              <div style={{ color: theme?.palette?.main_layout?.primary_text }}>
                {selectedModule?.name}
              </div>
              <div style={{ display: "flex" }}>
                <div style={{ cursor: "pointer" }}>
                  {isDarkMode ? (
                    <img
                      src={dayModeIcon}
                      alt="theme"
                      onClick={toggleTheme}
                      height={35}
                    />
                  ) : (
                    <img
                      src={nightModeIcon}
                      alt="theme"
                      onClick={toggleTheme}
                      height={35}
                    />
                  )}
                </div>
                &nbsp; &nbsp;
                <ProfilePicturePopup handleLogout={handleLogout} />
                &nbsp; &nbsp;
                <div>
                  <div
                    style={{
                      color: theme?.palette?.main_layout?.primary_text,
                      fontSize: theme.typography.textSize.medium,
                    }}
                  >
                    {userInfo?.name}
                  </div>
                  <div
                    style={{
                      color: theme?.palette?.main_layout?.secondary_text,
                      fontSize: theme.typography.textSize.small,
                    }}
                  >
                    {userInfo?.role}
                  </div>
                </div>
              </div>
            </DrawerHeader>
            <div style={{ padding: "10px 20px" }}>
              <Outlet />
            </div>
          </Box>
        </Box>
      ) : null}
    </>
  );
}
