import React, { useEffect, useState } from "react";
import { useDispatch } from "react-redux";
import { useSelector } from "react-redux";
import { selectTableData } from "../../../../store/features/monitoringModule/devicesLanding/bandwidths/selectors";
import { selectSelectedInterface } from "../../../../store/features/monitoringModule/devicesLanding/interfaces/selectors";
import { setSelectedInterface } from "../../../../store/features/monitoringModule/devicesLanding/interfaces";
import { useFetchRecordsMutation } from "../../../../store/features/monitoringModule/devicesLanding/bandwidths/apis";
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
import { indexColumnNameConstants as interfacesColumnNameConstants } from "../interfaces/constants";
import { useIndexTableColumnDefinitions } from "./columnDefinitions";
import {
  PAGE_NAME,
  PAGE_PATH,
  FILE_NAME_EXPORT_ALL_DATA,
  TABLE_DATA_UNIQUE_ID,
  indexColumnNameConstants,
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
  const selectedInterface = useSelector(selectSelectedInterface);

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
  ] = useFetchRecordsMutation();

  // error handling custom hooks
  useErrorHandling({
    data: fetchRecordsData,
    isSuccess: isFetchRecordsSuccess,
    isError: isFetchRecordsError,
    error: fetchRecordsError,
    type: TYPE_FETCH,
  });

  // effects
  useEffect(() => {
    if (selectedInterface) {
      fetchRecords({
        [indexColumnNameConstants.IP_ADDRESS]:
          selectedInterface[indexColumnNameConstants.IP_ADDRESS],
      });
    }
    return () => {
      dispatch(setSelectedInterface(null));
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

      {selectedInterface ? (
        <DefaultDetailCards
          data={{
            [interfacesColumnNameConstants.IP_ADDRESS]:
              selectedInterface[interfacesColumnNameConstants.IP_ADDRESS],
            [interfacesColumnNameConstants.DEVICE_NAME]:
              selectedInterface[interfacesColumnNameConstants.DEVICE_NAME],
            [interfacesColumnNameConstants.INTERFACE_NAME]:
              selectedInterface[interfacesColumnNameConstants.INTERFACE_NAME],
            [interfacesColumnNameConstants.INTERFACE_STATUS]:
              selectedInterface[interfacesColumnNameConstants.INTERFACE_STATUS],
          }}
          icons={[
            "carbon:kubernetes-ip-address",
            "tdesign:device",
            "carbon:network-interface",
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
