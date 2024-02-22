import storage from "redux-persist/lib/storage";

const persistConfig = {
  key: "ipam_dns_servers",
  storage,
  whitelist: ["selected_dns_server"],
};

export default persistConfig;
