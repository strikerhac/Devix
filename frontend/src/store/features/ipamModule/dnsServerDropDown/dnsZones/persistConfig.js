import storage from "redux-persist/lib/storage";

const persistConfig = {
  key: "ipam_dns_zones",
  storage,
  whitelist: ["selected_dns_zone"],
};

export default persistConfig;
