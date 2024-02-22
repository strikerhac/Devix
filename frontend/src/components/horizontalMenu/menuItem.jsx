import React from "react";
import Dropdown from "./dropdown";
import { useState, useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import "./main.css";
import { Icon } from "@iconify/react";

const MenuItems = ({
  item,
  depthLevel,
  menuPath,
  handleAddMenuPath,
  handleRemoveMenuPath,
  selectedMenuPath,
  setSelectedMenuPath,
}) => {
  const menuItemClassName =
    depthLevel === 0 ? "root-menu-item menu-item" : "menu-item";
  const menuItemTextClassName =
    depthLevel === 0 ? "root-menu-item-text" : "menu-item-text";
  const [dropdown, setDropdown] = useState(false);
  let ref = useRef();

  useEffect(() => {
    const handler = (event) => {
      if (dropdown && ref.current && !ref.current.contains(event.target)) {
        setDropdown(false);
      }
    };
    document.addEventListener("mousedown", handler);
    document.addEventListener("touchstart", handler);
    return () => {
      // Cleanup the event listener
      document.removeEventListener("mousedown", handler);
      document.removeEventListener("touchstart", handler);
    };
  }, [dropdown]);

  const onMouseEnter = () => {
    handleAddMenuPath(item.id);
    setDropdown(true);
  };

  const onMouseLeave = () => {
    handleRemoveMenuPath();
    setDropdown(false);
  };

  const toggleDropdown = () => {
    setDropdown((prev) => !prev);
  };

  const closeDropdown = () => {
    dropdown && setDropdown(false);
  };

  return (
    <li
      className={menuItemClassName}
      ref={ref}
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
      onClick={closeDropdown}
      style={{ cursor: "pointer", border: "0px solid red" }}
    >
      {
        /* {item.path && item.children ? (
        <div
          className={`${menuItemTextClassName} ${
            selectedMenuPath[depthLevel] === item.id ? "selected" : ""
          }`}
          style={{ display: "flex", padding: "0 10px", height: "5px" }}
        >
          <button
            type="button"
            aria-haspopup="menu"
            aria-expanded={dropdown ? "true" : "false"}
            onClick={() => toggleDropdown()}

            // style={{ border: "0px solid red", height: "51px" }}
          >
            <div style={{ display: "flex" }}>
              <div>
                <Icon
                  fontSize={"20px"}
                  icon={item.icon ? item.icon : ""}
                  style={{
                    paddingRight: "10px",
                    marginBottom: "-4px",
                  }}
                />
              </div>
              <div>
                <Link to={item.path}>{item.name}</Link>
              </div>
              {depthLevel > 0 ? (
                <span>&raquo;</span>
              ) : (
                <span className="arrow" />
              )}
            </div>
          </button>
          <Dropdown
            depthLevel={depthLevel}
            submenus={item.children}
            dropdown={dropdown}
            menuPath={menuPath}
            handleAddMenuPath={handleAddMenuPath}
            handleRemoveMenuPath={handleRemoveMenuPath}
            selectedMenuPath={selectedMenuPath}
            setSelectedMenuPath={setSelectedMenuPath}
          />
        </div>
      ) : */
        !item.path && item.children ? (
          <div
            style={{
              display: "flex",
              padding: "0 10px",
              height: "50px",
              marginBottom: "-1px",
            }}
          >
            <button
              className={`${menuItemTextClassName} ${
                selectedMenuPath[depthLevel] === item.id ? "selected" : ""
              }`}
              type="button"
              aria-haspopup="menu"
              aria-expanded={dropdown ? "true" : "false"}
              onClick={() => toggleDropdown()}
            >
              <div
                style={{
                  display: "flex",
                  fontSize: `${depthLevel > 0 ? "14px" : "15px"}`,
                }}
              >
                <div>
                  <Icon
                    fontSize={"20px"}
                    icon={item.icon ? item.icon : ""}
                    style={{
                      paddingRight: "10px",
                      marginBottom: "-4px",
                    }}
                  />
                </div>
                <div>{item.name}</div>
                {depthLevel > 0 ? (
                  <span>&raquo;</span>
                ) : (
                  <span className="arrow" />
                )}
              </div>
            </button>
            <Dropdown
              depthLevel={depthLevel}
              submenus={item.children}
              dropdown={dropdown}
              menuPath={menuPath}
              handleAddMenuPath={handleAddMenuPath}
              handleRemoveMenuPath={handleRemoveMenuPath}
              selectedMenuPath={selectedMenuPath}
              setSelectedMenuPath={setSelectedMenuPath}
            />
          </div>
        ) : (
          <div
            className={`${menuItemTextClassName} ${
              selectedMenuPath[depthLevel] === item.id ? "selected" : ""
            }`}
            style={{
              display: "flex",
              padding: "0 10px",
              height: "50px",
              margin: "0 10px",
              marginBottom: "-1px",
            }}
          >
            <Link
              to={item.path}
              onClick={() => setSelectedMenuPath([...menuPath])}
              style={{
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
              }}
            >
              <div style={{ display: "flex" }}>
                <div>
                  <Icon
                    fontSize={"20px"}
                    icon={item.icon ? item.icon : ""}
                    style={{
                      paddingRight: "10px",
                      marginBottom: "-4px",
                    }}
                  />
                </div>
                <div
                  style={{ fontSize: `${depthLevel > 0 ? "14px" : "16px"}` }}
                >
                  {item.name}
                </div>
              </div>
            </Link>
          </div>
        )
      }
    </li>
  );
};

export default MenuItems;
