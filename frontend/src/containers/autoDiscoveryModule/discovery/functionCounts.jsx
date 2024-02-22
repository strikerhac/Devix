import React from "react";
import { useSelector } from "react-redux";
import { selectDeviceCounts } from "../../../store/features/autoDiscoveryModule/discovery/selectors";
import DefaultDetailCards from "../../../components/detailCards";

function Index(props) {
  const deviceCounts = useSelector(selectDeviceCounts);

  return (
    <>
      {deviceCounts ? (
        <DefaultDetailCards
          data={deviceCounts}
          icons={[
            "tdesign:device",
            "carbon:firewall",
            "bi:router",
            "material-symbols:switch-outline",
            "icon-park-outline:other",
          ]}
        />
      ) : null}
    </>
  );
}

export default Index;
