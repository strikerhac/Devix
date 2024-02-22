import storage from "redux-persist/lib/storage";

const persistConfig = {
  key: "ipam_ip_details",
  storage,
  whitelist: ["selected_ip_detail"],
};

export default persistConfig;
