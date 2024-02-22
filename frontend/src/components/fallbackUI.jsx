import React from "react";
import { Typography, Box, Button } from "@mui/material";
import { useNavigate } from "react-router-dom";

export default function DefaultFallbackUI({ resetErrorBoundary }) {
  const navigate = useNavigate();

  const handleTryAgain = () => {
    window.location.reload();
  };

  const handleGoBack = () => {
    // Go back to the previous page
    navigate(-1);
  };

  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      height="100vh"
    >
      <Typography variant="h4" color="error" gutterBottom>
        Oops! Something went wrong.
      </Typography>
      <Typography variant="body1" align="center" color="textSecondary">
        We're sorry, but an error occurred. Please try again later.
      </Typography>
      <div style={{ display: "flex" }}>
        <Button
          variant="contained"
          color="primary"
          onClick={handleTryAgain}
          style={{ marginTop: "20px" }}
        >
          Try Again
        </Button>
        &nbsp;
        <Button
          variant="contained"
          color="primary"
          onClick={handleGoBack}
          style={{ marginTop: "20px" }}
        >
          Go Back
        </Button>
      </div>
    </Box>
  );
}
