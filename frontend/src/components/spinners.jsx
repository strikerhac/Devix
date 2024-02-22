import React from "react";
import { useTheme } from "@mui/material/styles";
import { Spin } from "antd";
import { LoadingOutlined } from "@ant-design/icons";

export default function DefaultSpinner({ spinning, sx, children }) {
  const theme = useTheme();
  const styledLoadingIndicator = (
    <LoadingOutlined style={{ fontSize: 24, color: "#3D9E47" }} spin />
  );

  return (
    <Spin spinning={spinning} indicator={styledLoadingIndicator}>
      {children}
    </Spin>
  );
}
