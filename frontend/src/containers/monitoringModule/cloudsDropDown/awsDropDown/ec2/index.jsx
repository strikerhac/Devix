import React, { useState } from "react";
import { useSelector } from "react-redux";
import { selectTableData } from "../../../../../store/features/monitoringModule/cloudsDropDown/awsDropDown/ec2/selectors";
import {
  useFetchRecordsQuery,
  useChangeEC2StatusMutation,
} from "../../../../../store/features/monitoringModule/cloudsDropDown/awsDropDown/ec2/apis";
import { jsonToExcel } from "../../../../../utils/helpers";
import { SUCCESSFUL_FILE_EXPORT_MESSAGE } from "../../../../../utils/constants";
import useErrorHandling, {
  TYPE_FETCH,
} from "../../../../../hooks/useErrorHandling";
import useSweetAlert from "../../../../../hooks/useSweetAlert";
import useColumnsGenerator from "../../../../../hooks/useColumnsGenerator";
import useButtonsConfiguration from "../../../../../hooks/useButtonsConfiguration";
import DefaultPageTableSection from "../../../../../components/pageSections";
import DefaultTableConfigurations from "../../../../../components/tableConfigurations";
import DefaultSpinner from "../../../../../components/spinners";
import { useIndexTableColumnDefinitions } from "./columnDefinitions";
import {
  PAGE_NAME,
  FILE_NAME_EXPORT_ALL_DATA,
  TABLE_DATA_UNIQUE_ID,
  EC2_STATUS,
  ENABLED,
  DISABLED,
} from "./constants";

const Index = () => {
  // hooks
  const { handleSuccessAlert, handleInfoAlert } = useSweetAlert();
  const { columnDefinitions } = useIndexTableColumnDefinitions({
    handleMonitoringSwitchChange,
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

  // apis
  const {
    data: fetchRecordsData,
    isSuccess: isFetchRecordsSuccess,
    isLoading: isFetchRecordsLoading,
    isError: isFetchRecordsError,
    error: fetchRecordsError,
  } = useFetchRecordsQuery();

  const [
    changeStatus,
    {
      data: changeStatusData,
      isSuccess: isChangeStatusSuccess,
      isLoading: isChangeStatusLoading,
      isError: isChangeStatusError,
      error: changeStatusError,
    },
  ] = useChangeEC2StatusMutation();

  // error handling custom hooks
  useErrorHandling({
    data: fetchRecordsData,
    isSuccess: isFetchRecordsSuccess,
    isError: isFetchRecordsError,
    error: fetchRecordsError,
    type: TYPE_FETCH,
  });

  useErrorHandling({
    data: changeStatusData,
    isSuccess: isChangeStatusSuccess,
    isError: isChangeStatusError,
    error: changeStatusError,
    type: TYPE_FETCH,
  });

  // handlers
  function handleMonitoringSwitchChange(checked, record) {
    changeStatus({
      [TABLE_DATA_UNIQUE_ID]: record[TABLE_DATA_UNIQUE_ID],
      [EC2_STATUS]: checked ? ENABLED : DISABLED,
    });
  }

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
    <DefaultSpinner spinning={isFetchRecordsLoading || isChangeStatusLoading}>
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
