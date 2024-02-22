import React, { useState, useEffect, useRef } from "react";
import { Button, Input, Space } from "antd";
import { SearchOutlined, RestOutlined } from "@ant-design/icons";
import Highlighter from "react-highlight-words";
import { useTheme } from "@mui/material/styles";
import { getTitle } from "../utils/helpers";

export default function useColumnSearchProps() {
  const theme = useTheme();
  const searchInput = useRef(null);
  const [searchText, setSearchText] = useState("");
  const [searchedColumn, setSearchedColumn] = useState("");

  const handleSearch = (selectedKeys, confirm, dataIndex) => {
    confirm();
    setSearchText(selectedKeys[0]);
    setSearchedColumn(dataIndex);
  };

  const handleReset = (clearFilters, setSelectedKeys) => {
    clearFilters();
    setSearchText("");
    setSelectedKeys([]);
  };

  const getColumnSearchProps = (dataIndex) => ({
    filterDropdown: ({
      setSelectedKeys,
      selectedKeys,
      confirm,
      clearFilters,
      close,
    }) => (
      <div
        style={{
          padding: 8,
          backgroundColor: theme?.palette?.default_table?.header_row,
        }}
        onKeyDown={(e) => e.stopPropagation()}
      >
        <Input
          ref={searchInput}
          placeholder={`Search ${getTitle(dataIndex)}`}
          value={selectedKeys[0]}
          onChange={(e) =>
            setSelectedKeys(e.target.value ? [e.target.value] : [])
          }
          onPressEnter={() => handleSearch(selectedKeys, confirm, dataIndex)}
          style={{
            marginBottom: 8,
            display: "block",
            borderColor: "gray",
            backgroundColor: theme?.palette?.default_table?.header_row,
            color: theme?.palette?.default_table?.header_text,
          }}
        />
        <Space>
          <Button
            type="primary"
            onClick={() => {
              handleSearch(selectedKeys, confirm, dataIndex);
              close();
            }}
            icon={<SearchOutlined />}
            size="small"
            style={{
              width: "100px",
              backgroundColor: "#3D9E47",
            }}
          >
            Search
          </Button>
          <Button
            type="primary"
            onClick={() => {
              setSelectedKeys([]);
              handleSearch([], confirm, dataIndex);
              // clearFilters && handleReset(clearFilters, setSelectedKeys);
              close();
            }}
            icon={<RestOutlined />}
            size="small"
            style={{
              width: "100px",
              backgroundColor: "#3D9E47",
            }}
          >
            Reset
          </Button>
        </Space>
      </div>
    ),
    filterIcon: (filtered) => (
      <SearchOutlined
        style={{
          color: filtered
            ? theme?.palette?.default_table?.search_filtered_icon
            : theme?.palette?.default_table?.search_icon,

          fontWeight: filtered ? "bolder" : "normal",
          fontSize: filtered ? "18px" : "14px",
        }}
      />
    ),
    onFilter: (value, record) =>
      record[dataIndex]?.toString().toLowerCase().includes(value.toLowerCase()),
    onFilterDropdownOpenChange: (visible) => {
      if (visible) {
        setTimeout(() => searchInput.current?.select(), 100);
      }
    },
    render: (text) =>
      searchedColumn === dataIndex ? (
        <Highlighter
          highlightStyle={{
            backgroundColor: "#ffc069",
            padding: 0,
          }}
          searchWords={[searchText]}
          autoEscape
          textToHighlight={text ? text.toString() : ""}
        />
      ) : (
        text
      ),
  });

  return getColumnSearchProps;
}
