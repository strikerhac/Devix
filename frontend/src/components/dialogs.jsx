import React from "react";
import Dialog from "@mui/material/Dialog";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import { useTheme, styled } from "@mui/material/styles";
import Paper from "@mui/material/Paper";

const StyledPaper = styled(Paper)`
  & {
    border-radius: 10px;
    background-color: transparent;
    padding: "15px";
    border: "1px solid red";
  }
`;

export default function DefaultDialog({ title, open, sx, children, ...rest }) {
  const theme = useTheme();

  return (
    <Dialog
      open={open}
      maxWidth="xl"
      sx={{ zIndex: "999", ...sx?.dialog, border: "1px solid red" }}
      PaperComponent={StyledPaper}
      {...rest}
    >
      <DialogTitle
        sx={{
          ...sx?.title,
          color: theme?.palette?.dialog?.title_text,
          backgroundColor: theme?.palette?.dialog?.title_background,
        }}
      >
        {title}
      </DialogTitle>
      <DialogContent
        sx={{
          ...sx?.content,
          color: theme?.palette?.dialog?.content_text,
          backgroundColor: theme?.palette?.dialog?.content_background,
          padding: "25px !important",
        }}
      >
        {children}
      </DialogContent>
    </Dialog>
  );
}
