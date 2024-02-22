import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { useSelector } from "react-redux";
import { selectTableData } from "../../../../store/features/ipamModule/dnsServerDropDown/dnsZones/selectors";
import { selectSelectedDnsServer } from "../../../../store/features/ipamModule/dnsServerDropDown/dnsServers/selectors";
import { setSelectedDnsZone } from "../../../../store/features/ipamModule/dnsServerDropDown/dnsZones";
import {
  useFetchZonesLazyQuery,
  useGetIpamDnsZonesByServerIdMutation,
} from "../../../../store/features/ipamModule/dnsServerDropDown/dnsZones/apis";
import { setSelectedDnsServer } from "../../../../store/features/ipamModule/dnsServerDropDown/dnsServers";
import { jsonToExcel } from "../../../../utils/helpers";
import { SUCCESSFUL_FILE_EXPORT_MESSAGE } from "../../../../utils/constants";
import { useAuthorization } from "../../../../hooks/useAuth";
import useErrorHandling, {
  TYPE_FETCH,
} from "../../../../hooks/useErrorHandling";
import useSweetAlert from "../../../../hooks/useSweetAlert";
import useColumnsGenerator from "../../../../hooks/useColumnsGenerator";
import useButtonsConfiguration from "../../../../hooks/useButtonsConfiguration";
import DefaultPageTableSection from "../../../../components/pageSections";
import DefaultTableConfigurations from "../../../../components/tableConfigurations";
import DefaultSpinner from "../../../../components/spinners";
import DefaultDetailCards from "../../../../components/detailCards";
import firewallIcon from "../../../../resources/designRelatedSvgs/firewall.svg";
import deviceIcon from "../../../../resources/designRelatedSvgs/otherDevices.svg";
import switchIcon from "../../../../resources/designRelatedSvgs/switches.svg";
import { DROPDOWN_PATH } from "../../dnsServerDropDown";
import { indexColumnNameConstants as serversColumnNameConstants } from "../dnsServers/constants";
import { PAGE_PATH as PAGE_PATH_DNS_Records } from "../dnsRecords/constants";
import { TABLE_DATA_UNIQUE_ID as DNS_SERVER_ID } from "../dnsServers/constants";
import { useIndexTableColumnDefinitions } from "./columnDefinitions";
import {
  PAGE_NAME,
  FILE_NAME_EXPORT_ALL_DATA,
  TABLE_DATA_UNIQUE_ID,
  PAGE_PATH,
} from "./constants";
import { MODULE_PATH } from "../..";
import { MAIN_LAYOUT_PATH } from "../../../../layouts/mainLayout";

const Index = () => {
  // hooks
  const { getUserInfoFromAccessToken, isPageEditable } = useAuthorization();

  // user information
  const userInfo = getUserInfoFromAccessToken();
  const roleConfigurations = userInfo?.configuration;

  // states
  const [pageEditable, setPageEditable] = useState(
    isPageEditable(roleConfigurations, MODULE_PATH, PAGE_PATH)
  );

  // hooks
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { handleSuccessAlert, handleInfoAlert } = useSweetAlert();
  const { columnDefinitions } = useIndexTableColumnDefinitions({
    handleIpAddressClick,
  });
  const generatedColumns = useColumnsGenerator({ columnDefinitions });
  const { buttonsConfigurationList } = useButtonsConfiguration({
    configure_table: { handleClick: handleTableConfigurationsOpen },
    default_export: { handleClick: handleDefaultExport },
  });

  // states
  const [tableConfigurationsOpen, setTableConfigurationsOpen] = useState(false);
  const [columns, setColumns] = useState(generatedColumns);
  const [availableColumns, setAvailableColumns] = useState([]);
  const [displayColumns, setDisplayColumns] = useState(generatedColumns);

  // selectors
  const dataSource = useSelector(selectTableData);
  const selectedDnsServer = useSelector(selectSelectedDnsServer);

  // apis
  const [
    fetchZones,
    {
      data: fetchZonesData,
      isSuccess: isFetchZonesSuccess,
      isLoading: isFetchZonesLoading,
      isError: isFetchZonesError,
      error: fetchZonesError,
    },
  ] = useFetchZonesLazyQuery();

  const [
    getDnsZonesByServerId,
    {
      data: getDnsZonesByServerIdData,
      isSuccess: isGetDnsZonesByServerIdSuccess,
      isLoading: isGetDnsZonesByServerIdLoading,
      isError: isGetDnsZonesByServerIdError,
      error: getDnsZonesByServerIdError,
    },
  ] = useGetIpamDnsZonesByServerIdMutation();

  // error handling custom hooks
  useErrorHandling({
    data: fetchZonesData,
    isSuccess: isFetchZonesSuccess,
    isError: isFetchZonesError,
    error: fetchZonesError,
    type: TYPE_FETCH,
  });

  useErrorHandling({
    data: getDnsZonesByServerIdData,
    isSuccess: isGetDnsZonesByServerIdSuccess,
    isError: isGetDnsZonesByServerIdError,
    error: getDnsZonesByServerIdError,
    type: TYPE_FETCH,
  });

  // effects
  useEffect(() => {
    if (selectedDnsServer) {
      getDnsZonesByServerId({
        [DNS_SERVER_ID]: selectedDnsServer[DNS_SERVER_ID],
      });
    } else {
      fetchZones();
    }

    return () => {
      dispatch(setSelectedDnsServer(null));
    };
  }, []);

  // handlers
  function handleDefaultExport() {
    if (dataSource?.length > 0) {
      jsonToExcel(dataSource, FILE_NAME_EXPORT_ALL_DATA);
      handleSuccessAlert(SUCCESSFUL_FILE_EXPORT_MESSAGE);
    } else {
      handleInfoAlert("No data to export.");
    }
  }

  function handleTableConfigurationsOpen() {
    setTableConfigurationsOpen(true);
  }

  function handleIpAddressClick(record) {
    dispatch(setSelectedDnsZone(record));
    navigate(
      `/${MAIN_LAYOUT_PATH}/${MODULE_PATH}/${DROPDOWN_PATH}/${PAGE_PATH_DNS_Records}`
    );
  }

  return (
    <DefaultSpinner
      spinning={isFetchZonesLoading || isGetDnsZonesByServerIdLoading}
    >
      {tableConfigurationsOpen ? (
        <DefaultTableConfigurations
          columns={columns}
          availableColumns={availableColumns}
          setAvailableColumns={setAvailableColumns}
          displayColumns={displayColumns}
          setDisplayColumns={setDisplayColumns}
          setColumns={setColumns}
          open={tableConfigurationsOpen}
          setOpen={setTableConfigurationsOpen}
        />
      ) : null}

      {selectedDnsServer ? (
        <DefaultDetailCards
          data={{
            [serversColumnNameConstants.IP_ADDRESS]:
              selectedDnsServer[serversColumnNameConstants.IP_ADDRESS],
            [serversColumnNameConstants.SERVER_NAME]:
              selectedDnsServer[serversColumnNameConstants.SERVER_NAME],
            [serversColumnNameConstants.TYPE]:
              selectedDnsServer[serversColumnNameConstants.TYPE],
          }}
          icons={[
            "carbon:kubernetes-ip-address",
            "clarity:rack-server-line",
            "lucide:file-type",
          ]}
        />
      ) : null}

      <DefaultPageTableSection
        PAGE_NAME={PAGE_NAME}
        TABLE_DATA_UNIQUE_ID={TABLE_DATA_UNIQUE_ID}
        buttonsConfigurationList={buttonsConfigurationList}
        displayColumns={displayColumns}
        dataSource={dataSource}
      />
    </DefaultSpinner>
  );
};

export default Index;
