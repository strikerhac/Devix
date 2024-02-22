import storage from "redux-persist/lib/storage";

const persistConfig = {
  key: "ipam_subnets",
  storage,
  whitelist: ["selected_subnet"],
};

export default persistConfig;
