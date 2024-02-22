import * as React from "react";
import { useContext } from "react";
import { Provider } from "react-redux";
import { RouterProvider } from "react-router-dom";
import { ThemeProvider } from "@mui/material/styles";
import { PersistGate } from "redux-persist/integration/react";
import { AppContext } from "./context/appContext";
import { lightTheme, darkTheme } from "./themes";
import { store, persistor } from "./store";
// import router from "./routes";
import "./index.css";
import { defaultConfiguration } from "./containers/adminModule/roles/defaultConfiguration";
import useBrowserRouter from "./routes/useBrowserRouter";

const App = () => {
  localStorage.setItem(
    "monetx_jwt_token",
    JSON.stringify(defaultConfiguration)
  );

  const { isDarkMode } = useContext(AppContext);
  const browserRouter = useBrowserRouter();
  const theme = isDarkMode ? darkTheme : lightTheme;

  return (
    <div
      className="relative"
      style={{
        backgroundColor: theme.palette.background.default,
        height: "auto",
        width: "100%",
      }}
    >
      <Provider store={store}>
        <PersistGate loading={null} persistor={persistor}>
          <ThemeProvider theme={theme}>
            <RouterProvider router={browserRouter} />
          </ThemeProvider>
        </PersistGate>
      </Provider>
    </div>
  );
};

export default App;
