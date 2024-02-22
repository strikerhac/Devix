import React from "react";

export default function DefaultWrapper({ sx, children, ...rest }) {
  return (
    <div style={{ display: "block", ...sx }} {...rest}>
      {children}
    </div>
  );
}

export function InputWrapper({ sx, children, ...rest }) {
  return (
    <div
      style={{
        display: "flex",
        marginTop: "5px",
        width: "100%",
        ...sx,
      }}
      {...rest}
    >
      {children}
    </div>
  );
}
