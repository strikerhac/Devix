import storage from "redux-persist/lib/storage";

const persistConfig = {
  key: "monitoring_interfaces",
  storage,
  whitelist: ["selected_interface"],
};

export default persistConfig;
