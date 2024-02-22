import React, { useRef, useEffect } from "react";
import Highlighter from "react-highlight-words";
import { useSelector } from "react-redux";
import { selectConfigurationBackupDetails } from "../../../../store/features/ncmModule/manageConfigurations/configurationBackups/selectors";
import {
  useDeleteRecordsMutation,
  useGetNcmConfigurationBackupDetailsByNcmHistoryIdMutation,
} from "../../../../store/features/ncmModule/manageConfigurations/configurationBackups/apis";
import { jsonToExcel } from "../../../../utils/helpers";
import useErrorHandling, {
  TYPE_SINGLE,
  TYPE_BULK,
  TYPE_BULK_DELETE,
} from "../../../../hooks/useErrorHandling";
import useSweetAlert from "../../../../hooks/useSweetAlert";
import useButtonsConfiguration from "../../../../hooks/useButtonsConfiguration";
import DefaultCard from "../../../../components/cards";
import DefaultPageHeader from "../../../../components/pageHeaders";
import { FloatingHighlighterSearch } from "../../../../components/search";
import DefaultSpinner from "../../../../components/spinners";
import { FILE_NAME_EXPORT_ALL_DATA, TABLE_DATA_UNIQUE_ID } from "./constants";
import {
  DELETE_PROMPT,
  SUCCESSFUL_FILE_EXPORT_MESSAGE,
} from "../../../../utils/constants";

const Index = ({ ncmHistoryId, pageEditable }) => {
  // selectors
  const dataSource = useSelector(selectConfigurationBackupDetails);

  // states required in hooks
  const targetRef = useRef(null);

  // hooks
  const { handleSuccessAlert, handleInfoAlert, handleCallbackAlert } =
    useSweetAlert();
  const { buttonsConfigurationList } = useButtonsConfiguration({
    default_export: { handleClick: handleDefaultExport },
    default_delete: { handleClick: handleDelete, visible: pageEditable },
  });

  // apis
  const [
    getBackupDetails,
    {
      data: getBackupDetailsData,
      isSuccess: isGetBackupDetailsSuccess,
      isLoading: isGetBackupDetailsLoading,
      isError: isGetBackupDetailsError,
      error: getBackupDetailsError,
    },
  ] = useGetNcmConfigurationBackupDetailsByNcmHistoryIdMutation();

  const [
    deleteRecords,
    {
      data: deleteRecordsData,
      isSuccess: isDeleteRecordsSuccess,
      isLoading: isDeleteRecordsLoading,
      isError: isDeleteRecordsError,
      error: deleteRecordsError,
    },
  ] = useDeleteRecordsMutation();

  // error handling custom hooks
  useErrorHandling({
    data: getBackupDetailsData,
    isSuccess: isGetBackupDetailsSuccess,
    isError: isGetBackupDetailsError,
    error: getBackupDetailsError,
    type: TYPE_SINGLE,
  });

  useErrorHandling({
    data: deleteRecordsData,
    isSuccess: isDeleteRecordsSuccess,
    isError: isDeleteRecordsError,
    error: deleteRecordsError,
    type: TYPE_BULK_DELETE,
  });

  // effects
  useEffect(() => {
    if (ncmHistoryId) {
      getBackupDetails({ [TABLE_DATA_UNIQUE_ID]: ncmHistoryId });
    }
  }, [ncmHistoryId]);

  // handlers
  function deleteData(allowed) {
    if (allowed) {
      deleteRecords([ncmHistoryId]);
    }
  }

  function handleDelete() {
    handleCallbackAlert(DELETE_PROMPT, deleteData);
  }

  function handleDefaultExport() {
    if (dataSource?.length > 0) {
      jsonToExcel(dataSource, FILE_NAME_EXPORT_ALL_DATA);
      handleSuccessAlert(SUCCESSFUL_FILE_EXPORT_MESSAGE);
    } else {
      handleInfoAlert("No data to export.");
    }
  }

  return (
    <DefaultSpinner
      spinning={isGetBackupDetailsLoading || isDeleteRecordsLoading}
    >
      {dataSource ? (
        <DefaultCard sx={{ paddingBottom: "50px" }}>
          <DefaultPageHeader
            pageName="Backup Details"
            buttons={buttonsConfigurationList}
          />

          <FloatingHighlighterSearch />

          <div
            style={{
              backgroundColor: "white",
              padding: "10px",
            }}
          >
            <span style={{ color: "grey" }}>Output:</span>

            <code class="line-numbers">
              <pre style={{ padding: "8px" }}>
                <Highlighter
                  highlightClassName="rc-highlight"
                  searchWords={[`${targetRef}`]}
                  autoEscape={true}
                  activeStyle={{ color: "red" }}
                  textToHighlight={dataSource}
                />
              </pre>
            </code>
          </div>
        </DefaultCard>
      ) : null}
    </DefaultSpinner>
  );
};

export default Index;
