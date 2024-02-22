import React, { useRef, useEffect, useState } from "react";
import { useTheme } from "@mui/material/styles";
import { CaretRightOutlined, CaretLeftOutlined } from "@ant-design/icons";

export function FloatingHighlighterSearch({ sx, ...rest }) {
  const theme = useTheme();
  const findInput = useRef(null);
  const [isFixed, setIsFixed] = useState(false);

  function handleFindNext() {
    const searchTerm = findInput.current.value;
    window.find(searchTerm, false, false, false, false, true, true);
  }

  function handleFindPrevious() {
    const searchTerm = findInput.current.value;
    window.find(searchTerm, false, true, false, false, true, true);
  }

  useEffect(() => {
    const handleScroll = (findInputInitialCenter) => {
      const scrollY = window.scrollY || document.documentElement.scrollTop;
      const scrollHeight = document.documentElement.scrollHeight;
      const windowHeight = window.innerHeight;
      const findInputRect = findInput.current?.getBoundingClientRect();
      const findInputCenter = findInputRect?.top + findInputRect?.height / 2;
      if (scrollY < 560) {
        setIsFixed(false);
      } else {
        setIsFixed(findInputCenter < windowHeight / 2);
      }
    };

    const findInputInitialRect = findInput.current?.getBoundingClientRect();
    const findInputInitialCenter =
      findInputInitialRect?.top + findInputInitialRect?.height / 2;

    window.addEventListener("scroll", () =>
      handleScroll(findInputInitialCenter)
    );

    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  return (
    <div
      style={{
        position: isFixed ? "fixed" : "absolute",
        top: isFixed ? "50%" : "auto",
        transform: isFixed ? "translateY(-50%)" : "none",
        right: isFixed ? "30px" : "10px",
      }}
    >
      <div>
        <button
          onClick={handleFindPrevious}
          style={{
            backgroundColor: "#3D9E47",
            color: "white",
            borderRadius: "100px 0 0 100px",
            height: "30px",
            outline: "none",
            border: "none",
            width: "35px",
          }}
        >
          <CaretLeftOutlined />
        </button>

        <input
          style={{
            border: "1px solid silver",
            paddingLeft: "10px",
            height: "26px",
            outline: "none",
          }}
          type="text"
          ref={findInput}
          placeholder="Search"
          onKeyDown={(e) => {
            if (e.keyCode === 13) {
              handleFindNext();
            }
          }}
        />
        <button
          onClick={handleFindNext}
          style={{
            backgroundColor: "#3D9E47",
            color: "white",
            borderRadius: "0 100px 100px 0",
            height: "30px",
            outline: "none",
            border: "none",
            width: "35px",
          }}
        >
          <CaretRightOutlined />
        </button>
      </div>
    </div>
  );
}
