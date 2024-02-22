import React, { useState, createContext } from "react";

export const AppContext = createContext();

const Index = (props) => {
  const [isDarkMode, setDarkMode] = useState(false);

  return (
    <AppContext.Provider value={{ isDarkMode, setDarkMode }}>
      {props.children}
    </AppContext.Provider>
  );
};
export default Index;
