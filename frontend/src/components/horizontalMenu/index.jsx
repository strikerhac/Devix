import React from "react";
// import MobileNav from "./mobileNav";
import Navbar from "./navbar";
import "./main.css";

const Header = ({ menuItems, defaultPagePath }) => {
  return (
    <header>
      <div className="nav-area">
        {/* for large screens */}
        <Navbar menuItems={menuItems} defaultPagePath={defaultPagePath} />

        {/* for small screens */}
        {/* <MobileNav /> */}
      </div>
    </header>
  );
};

export default Header;
