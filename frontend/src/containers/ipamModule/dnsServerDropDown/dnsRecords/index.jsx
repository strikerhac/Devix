import React, { useEffect, useState } from "react";
import { useDispatch } from "react-redux";
import { useSelector } from "react-redux";
import { selectTableData } from "../../../../store/features/ipamModule/dnsServerDropDown/dnsRecords/selectors";
import { selectSelectedDnsZone } from "../../../../store/features/ipamModule/dnsServerDropDown/dnsZones/selectors";
import {
  useFetchRecordsLazyQuery,
  useGetIpamDnsRecordsByZoneIdMutation,
} from "../../../../store/features/ipamModule/dnsServerDropDown/dnsRecords/apis";
import { setSelectedDnsZone } from "../../../../store/features/ipamModule/dnsServerDropDown/dnsZones";
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
import { indexColumnNameConstants as zonesColumnNameConstants } from "../dnsZones/constants";
import { TABLE_DATA_UNIQUE_ID as DNS_ZONE_ID } from "../dnsZones/constants";
import { useIndexTableColumnDefinitions } from "./columnDefinitions";
import {
  PAGE_NAME,
  FILE_NAME_EXPORT_ALL_DATA,
  TABLE_DATA_UNIQUE_ID,
  PAGE_PATH,
} from "./constants";
import { MODULE_PATH } from "../..";

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
  const dispatch = useDispatch();
  const { handleSuccessAlert, handleInfoAlert } = useSweetAlert();
  const { columnDefinitions } = useIndexTableColumnDefinitions();
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
  const selectedDnsZone = useSelector(selectSelectedDnsZone);

  // apis
  const [
    fetchRecords,
    {
      data: fetchRecordsData,
      isSuccess: isFetchRecordsSuccess,
      isLoading: isFetchRecordsLoading,
      isError: isFetchRecordsError,
      error: fetchRecordsError,
    },
  ] = useFetchRecordsLazyQuery();

  const [
    getDnsRecordsByZoneId,
    {
      data: getDnsRecordsByZoneIdData,
      isSuccess: isGetDnsRecordsByZoneIdSuccess,
      isLoading: isGetDnsRecordsByZoneIdLoading,
      isError: isGetDnsRecordsByZoneIdError,
      error: getDnsRecordsByZoneIdError,
    },
  ] = useGetIpamDnsRecordsByZoneIdMutation();

  // error handling custom hooks
  useErrorHandling({
    data: fetchRecordsData,
    isSuccess: isFetchRecordsSuccess,
    isError: isFetchRecordsError,
    error: fetchRecordsError,
    type: TYPE_FETCH,
  });

  useErrorHandling({
    data: getDnsRecordsByZoneIdData,
    isSuccess: isGetDnsRecordsByZoneIdSuccess,
    isError: isGetDnsRecordsByZoneIdError,
    error: getDnsRecordsByZoneIdError,
    type: TYPE_FETCH,
  });

  // effects
  useEffect(() => {
    if (selectedDnsZone) {
      getDnsRecordsByZoneId({
        [DNS_ZONE_ID]: selectSelectedDnsZone[DNS_ZONE_ID],
      });
    } else {
      fetchRecords();
    }

    return () => {
      dispatch(setSelectedDnsZone(null));
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

  return (
    <DefaultSpinner spinning={isFetchRecordsLoading}>
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

      {selectedDnsZone ? (
        <DefaultDetailCards
          data={{
            [zonesColumnNameConstants.IP_ADDRESS]:
              selectedDnsZone[zonesColumnNameConstants.IP_ADDRESS],
            [zonesColumnNameConstants.ZONE_NAME]:
              selectedDnsZone[zonesColumnNameConstants.ZONE_NAME],
            [zonesColumnNameConstants.ZONE_TYPE]:
              selectedDnsZone[zonesColumnNameConstants.ZONE_TYPE],
            [zonesColumnNameConstants.ZONE_STATUS]:
              selectedDnsZone[zonesColumnNameConstants.ZONE_STATUS],
          }}
          icons={[
            "carbon:kubernetes-ip-address",
            "ri:time-zone-line",
            "lucide:file-type",
            "grommet-icons:status-info",
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
