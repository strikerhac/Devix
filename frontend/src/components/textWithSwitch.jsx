import React, { useState } from "react";
import { convertToAsterisks } from "../utils/helpers";
import { Switch } from "antd";

export function DefaultTextWithSwitch({ text }) {
  const [checked, setChecked] = useState(false);
  return (
    <div style={{ display: "flex", justifyContent: "space-between" }}>
      {checked ? text : convertToAsterisks(text)} &nbsp;&nbsp;
      <Switch
        checked={checked}
        onChange={(checked) => setChecked(checked)}
        style={{
          transform: "scale(0.6)",
          backgroundColor: checked ? "green" : "silver",
        }}
      />
    </div>
  );
}
