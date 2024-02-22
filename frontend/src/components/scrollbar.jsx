import React from "react";
import "../styles/main.styles.css";

export default function DefaultScrollbar({ children, sx, ...rest }) {
  return (
    <div style={{ ...sx }} {...rest}>
      {children}
    </div>
  );
}
