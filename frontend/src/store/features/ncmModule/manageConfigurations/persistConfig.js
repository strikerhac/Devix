import storage from "redux-persist/lib/storage";

const persistConfig = {
  key: "ncm_manage_configurations",
  storage,
  whitelist: ["selected_device"],
};

export default persistConfig;
