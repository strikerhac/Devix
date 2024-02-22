import storage from "redux-persist/lib/storage";

const persistConfig = {
  key: "monitoring_devices",
  storage,
  whitelist: ["selected_device"],
};

export default persistConfig;
