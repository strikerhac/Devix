import React, { Component } from "react";
import DefaultFallbackUI from "./fallbackUI";

class DefaultErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    // You can log the error to an error reporting service here
    console.error(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      // Render the fallback UI
      return <DefaultFallbackUI />;
    }

    // If there is no error, render the children
    return this.props.children;
  }
}

export default DefaultErrorBoundary;
