import { createTheme } from "@mui/material/styles";
import { lightThemeColors, darkThemeColors } from "../utils/constants/colors";

export const lightTheme = createTheme({
  palette: {
    background: {
      default: "#F6F6F6",
    },

    main_layout: {
      background: "#FFFFFF",
      profile_picture_background: "#ACACAC",
      primary_text: "#000000",
      secondary_text: "#ACACAC",
      border_bottom: "#D9D9D9",
    },

    default_card: {
      background: "#FFFFFF",
    },

    horizontal_menu: {
      primary_text: "#000000",
      secondary_text: "#3D9E47",
    },

    default_table: {
      header_row: "#FAFAFA",
      odd_row: "#FAFAFA",
      even_row: "#FFFFFF",
      hovered_row: "#F1F6EE",
      selected_row: "#F1F6EE",
      search_icon: "#ACACAC",
      search_filtered_icon: "#3E9F48",
      header_text: "#262626",
      primary_text: "#262626",
      secondary_text: "#3E9F48",
      hovered_text: "#262626",
      selected_text: "#262626",
      link_text: "#3E9F48",
      border: "#EBEBEB",
      check_box_border: "#EBEBEB",
      check_box_inner: "#FFFFFF",
      check_box_checked: "#3E9F48",
      delete_icon: "#262626",
      edit_icon: "#262626",
      pagination_text: "#3E9F48",
      pagination_background: "transparent",
      pagination_background_active: "#EBEBEB",
      pagination_border: "#3E9F48",
    },

    default_button: {
      delete_background: "#E34444",
      import_background: "#3D9E47",
      onboard_background: "#478778",
      add_background: "#3D9E47",
      cancel_background: "#E34444",
      submit_background: "#3D9E47",
      success_alert_background: "#3D9E47",
      info_alert_background: "#7F7F7F",
      error_alert_background: "#E34444",
      warning_alert_background: "#E34444",
      configure_table_background: "#EAEAEA",
      configure_table_text: "#7F7F7F",
      left_background: "#EAEAEA",
      right_background: "#EAEAEA",
      up_background: "#EAEAEA",
      down_background: "#EAEAEA",
      primary_text: "#FFFFFF",
      secondary_text: "#262626",
    },

    drop_down_button: {
      add_background: "#3D9E47",
      add_text: "#FFFFFF",

      export_background: "#FFFFFF",
      export_text: "#000000",

      border: "#EAEAEA",
      options_text: "#000000",
      options_background: "#FFFFFF",
      options_hover_text: "#7F7F7F",
      options_hover_background: "#E4F1E5",
    },

    page_header: {
      primary_text: "#000000",
    },

    dialog: {
      title_background: "#EBEBEB",
      content_background: "#FFFFFF",
      title_text: "#000000",
      content_text: "#000000",
    },

    form_unit: {
      error_text: "red",
    },

    default_input: {
      border: "#F5F5F5",
      primary_text: "#000000",
      background: "#FFFFFF",
    },

    default_select: {
      border: "#F5F5F5",
      primary_text: "#000000",
      background: "#FFFFFF",
      place_holder: "#B9B9B9",
    },

    default_option: {
      border: "#F5F5F5",
      primary_text: "#000000",
      background: "#FFFFFF",
    },

    default_label: {
      primary_text: "#000000",
      required_star: "#E34444",
    },

    icon: {
      complete: "#66B127",
      incomplete: "#F1B92A",
    },

    default_table_Configurations: {
      item_hover_text: "#000000",
      item_select_text: "#000000",
      item_hover_background: "#F1F6EE",
      item_select_background: "#F1F6EE",
    },

    sweet_alert: {
      primary_text: "#545454",
      background: "#FFFFFF",
    },
  },

  typography: {
    font_family: "Arial, sans-serif",

    textSize: {
      small: "12px",
      medium: "14px",
      large: "16px",
      extraLarge: "",
    },

    fontWeight: {
      thin: 100,
      normal: 400,
      bold: 700,
    },
  },
});

export const darkTheme = createTheme({
  palette: {
    background: {
      default: "#131B15",
    },

    main_layout: {
      background: "#09120C",
      profile_picture_background: "#ACACAC",
      primary_text: "#FFFFFF",
      secondary_text: "#ACACAC",
      border_bottom: "#09120C",
    },

    default_card: {
      background: "#09120C",
    },

    horizontal_menu: {
      primary_text: "#FFFFFF",
      secondary_text: "#3D9E47",
    },

    default_table: {
      header_row: "#3A403C",
      odd_row: "#3A403C",
      even_row: "#09120C",
      hovered_row: "#5A5A5A",
      selected_row: "#5A5A5A",
      search_icon: "#FFFFFF",
      search_filtered_icon: "#3E9F48",
      header_text: "#FFFFFF",
      primary_text: "#FFFFFF",
      secondary_text: "#3E9F48",
      hovered_text: "#FFFFFF",
      selected_text: "#FFFFFF",
      link_text: "#3E9F48",
      border: "#EBEBEB",
      check_box_border: "#EBEBEB",
      check_box_inner: "#09120C",
      check_box_checked: "#3E9F48",
      delete_icon: "#262626",
      edit_icon: "#262626",
      pagination_text: "#3E9F48",
      pagination_background: "transparent",
      pagination_background_active: "#EBEBEB",
      pagination_border: "#3E9F48",
    },

    default_button: {
      delete_background: "#E34444",
      import_background: "#3D9E47",
      onboard_background: "#478778",
      add_background: "#3D9E47",
      cancel_background: "#E34444",
      submit_background: "#3D9E47",
      success_alert_background: "#3D9E47",
      info_alert_background: "#7F7F7F",
      error_alert_background: "#E34444",
      warning_alert_background: "#7F7F7F",
      configure_table_background: "#7F7F7F",
      configure_table_text: "#FFFFFF",
      left_background: "#09120C",
      right_background: "#09120C",
      up_background: "#09120C",
      down_background: "#09120C",
      primary_text: "#FFFFFF",
      secondary_text: "#EAEAEA",
    },

    drop_down_button: {
      add_background: "#3D9E47",
      add_text: "#FFFFFF",

      export_background: "#000000",
      export_text: "#FFFFFF",

      border: "#EAEAEA",
      options_text: "#FFFFFF",
      options_background: "#000000",
      options_hover_text: "#7F7F7F",
      options_hover_background: "#C8EF9E",
    },

    page_header: {
      primary_text: "#FFFFFF",
    },

    dialog: {
      title_background: "#09120C",
      content_background: "#131B15",
      title_text: "#FFFFFF",
      content_text: "#FFFFFF",
    },

    form_unit: {
      error_text: "#E34444",
    },

    default_input: {
      border: "#09120C",
      primary_text: "#ACACAC",
      background: "#09120C",
    },

    default_select: {
      border: "#09120C",
      primary_text: "#ACACAC",
      background: "#09120C",
      place_holder: "#B9B9B9",
    },

    default_option: {
      border: "#09120C",
      primary_text: "#ACACAC",
      background: "#09120C",
    },

    default_label: {
      primary_text: "#FFFFFF",
      required_star: "#E34444",
    },

    icon: {
      complete: "#66B127",
      incomplete: "#F1B92A",
    },

    default_table_Configurations: {
      primary_text: "#FFFFFF",
      item_hover_text: "#FFFFFF",
      item_select_text: "#FFFFFF",
      item_hover_background: "#ACACAC",
      item_select_background: "#09120C",
    },

    sweet_alert: {
      primary_text: "#FFFFFF",
      background: "#09120C",
    },
  },

  typography: {
    font_family: "Arial, sans-serif",

    textSize: {
      small: "12px",
      medium: "14px",
      large: "16px",
      extraLarge: "18px",
    },

    fontWeight: {
      thin: 100,
      normal: 400,
      bold: 700,
    },
  },
});
