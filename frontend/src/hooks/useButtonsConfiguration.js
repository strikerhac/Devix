import React, { useState, useEffect } from "react";
import { Icon } from "@iconify/react";
import { useTheme } from "@mui/material/styles";

export default function useButtonsConfiguration(buttonDetails) {
  const theme = useTheme();

  const optionConstants = {
    atom_export: {
      ALL_DATA: "all_data",
      TEMPLATE: "template",
      COMPLETE: "complete",
      INCOMPLETE: "incomplete",
    },
    default_atom_export: {
      ALL_DATA: "all_data",
      COMPLETE: "complete",
      INCOMPLETE: "incomplete",
    },
    atom_add: {
      ADD_MANUALLY: "add_manually",
      FROM_DISCOVERY: "from_discovery",
    },
    template_export: {
      ALL_DATA: "all_data",
      TEMPLATE: "template",
    },
    inventory_sync: {
      SYNC_FROM_INVENTORY: "sync_from_inventory",
      SYNC_TO_INVENTORY: "sync_to_inventory",
    },
    default_scan: {
      PORT_SCAN: "port_scan",
      DNS_SCAN: "dns_scan",
    },
  };

  const configurations = {
    default_button: {
      name: "Default Button",
      handleClick: () =>
        alert(
          "Configuration for this button key does not exist in useButtonsConfiguration hook"
        ),
      sx: {
        backgroundColor: theme?.palette?.default_button?.import_background,
        color: theme?.palette?.default_button?.primary_text,
      },
    },
    configure_table: {
      icon: <Icon fontSize="20px" icon="fluent:stack-32-regular" />,
      sx: {
        backgroundColor: theme?.palette?.drop_down_button?.export_background,
        color: theme?.palette?.drop_down_button?.export_text,
        border: `1px solid ${theme?.palette?.drop_down_button?.border}`,
      },
    },
    default_export: {
      name: "Export",
      icon: <Icon fontSize="16px" icon="fe:export" />,
      sx: {
        backgroundColor: theme?.palette?.drop_down_button?.export_background,
        color: theme?.palette?.drop_down_button?.export_text,
        border: `1px solid ${theme?.palette?.drop_down_button?.border}`,
      },
    },
    default_delete: {
      name: "Delete",
      icon: <Icon fontSize="16px" icon="mingcute:delete-line" />,
      sx: {
        backgroundColor: theme?.palette?.default_button?.delete_background,
        color: theme?.palette?.default_button?.primary_text,
      },
    },
    default_add: {
      name: "Add",
      icon: <Icon fontSize="16px" icon="gridicons:add-outline" />,
      postfix: true,
      sx: {
        backgroundColor: theme?.palette?.drop_down_button?.add_background,
        color: theme?.palette?.default_button?.primary_text,
      },
    },
    default_import: {
      name: "Import",
      icon: <Icon fontSize="16px" icon="pajamas:import" />,
      sx: {
        backgroundColor: theme?.palette?.default_button?.import_background,
        color: theme?.palette?.default_button?.primary_text,
      },
    },
    default_atom_export: {
      category: "dropDown",
      name: "Export",
      icon: <Icon fontSize="16px" icon="fe:export" />,
      options: [
        {
          type: optionConstants.atom_export.ALL_DATA,
          icon: <Icon fontSize="16px" icon="icon-park-outline:data-all" />,
        },
        {
          type: optionConstants.atom_export.COMPLETE,
          icon: (
            <Icon
              fontSize="16px"
              icon="ep:success-filled"
              color={theme?.palette?.icon?.complete}
            />
          ),
        },
        {
          type: optionConstants.atom_export.INCOMPLETE,
          icon: (
            <Icon
              fontSize="16px"
              icon="material-symbols:info"
              color={theme?.palette?.icon?.incomplete}
            />
          ),
        },
      ],
      sx: {
        backgroundColor: theme?.palette?.drop_down_button?.export_background,
        color: theme?.palette?.drop_down_button?.export_text,
      },
    },
    atom_export: {
      category: "dropDown",
      name: "Export",
      icon: <Icon fontSize="16px" icon="fe:export" />,
      options: [
        {
          type: optionConstants.atom_export.ALL_DATA,
          icon: <Icon fontSize="16px" icon="icon-park-outline:data-all" />,
        },
        {
          type: optionConstants.atom_export.TEMPLATE,
          icon: (
            <Icon fontSize="16px" icon="streamline:chat-bubble-square-write" />
          ),
        },
        {
          type: optionConstants.atom_export.COMPLETE,
          icon: (
            <Icon
              fontSize="16px"
              icon="ep:success-filled"
              color={theme?.palette?.icon?.complete}
            />
          ),
        },
        {
          type: optionConstants.atom_export.INCOMPLETE,
          icon: (
            <Icon
              fontSize="16px"
              icon="material-symbols:info"
              color={theme?.palette?.icon?.incomplete}
            />
          ),
        },
      ],
      sx: {
        backgroundColor: theme?.palette?.drop_down_button?.export_background,
        color: theme?.palette?.drop_down_button?.export_text,
      },
    },
    default_onboard: {
      name: "Onboard",
      icon: <Icon fontSize="16px" icon="fluent:board-20-regular" />,
      sx: {
        backgroundColor: theme?.palette?.default_button?.onboard_background,
        color: theme?.palette?.default_button?.primary_text,
      },
    },
    atom_add: {
      category: "dropDown",
      name: "Add",
      icon: <Icon fontSize="16px" icon="gridicons:add-outline" />,
      options: [
        {
          type: optionConstants.atom_add.ADD_MANUALLY,
          icon: <Icon fontSize="16px" icon="icon-park-outline:manual-gear" />,
        },
        {
          type: optionConstants.atom_add.FROM_DISCOVERY,
          icon: (
            <Icon fontSize="16px" icon="icon-park-outline:discovery-index" />
          ),
        },
      ],
      sx: {
        backgroundColor: theme?.palette?.drop_down_button?.add_background,
        color: theme?.palette?.drop_down_button?.add_text,
      },
    },
    inventory_sync: {
      category: "dropDown",
      name: "Sync",
      icon: (
        <Icon fontSize="16px" icon="streamline:arrow-reload-horizontal-1" />
      ),
      options: [
        {
          type: optionConstants.inventory_sync.SYNC_FROM_INVENTORY,
          icon: <Icon fontSize="16px" icon="icon-park-outline:to-right" />,
        },
        {
          type: optionConstants.inventory_sync.SYNC_TO_INVENTORY,
          icon: <Icon fontSize="16px" icon="icon-park-outline:to-left" />,
        },
      ],
      sx: {
        backgroundColor: theme?.palette?.drop_down_button?.add_background,
        color: theme?.palette?.drop_down_button?.add_text,
      },
    },
    template_export: {
      category: "dropDown",
      name: "Export",
      icon: <Icon fontSize="16px" icon="fe:export" />,
      options: [
        {
          type: optionConstants.template_export.ALL_DATA,
          icon: <Icon fontSize="16px" icon="icon-park-outline:data-all" />,
        },
        {
          type: optionConstants.template_export.TEMPLATE,
          icon: (
            <Icon fontSize="16px" icon="streamline:chat-bubble-square-write" />
          ),
        },
      ],
      sx: {
        backgroundColor: theme?.palette?.drop_down_button?.export_background,
        color: theme?.palette?.drop_down_button?.export_text,
      },
    },
    default_dismantle: {
      name: "Dismantle",
      icon: <Icon fontSize="16px" icon="fluent:board-20-regular" />,
      sx: {
        backgroundColor: theme?.palette?.default_button?.delete_background,
        color: theme?.palette?.default_button?.primary_text,
      },
    },

    default_cancel: {
      name: "Cancel",
      sx: {
        backgroundColor: theme?.palette?.default_button?.delete_background,
        color: theme?.palette?.default_button?.primary_text,
      },
    },

    default_submit: {
      name: "Submit",
      type: "submit",
      sx: {
        backgroundColor: theme?.palette?.default_button?.add_background,
        color: theme?.palette?.default_button?.primary_text,
      },
    },

    start_scanning_devices: {
      name: "Start Scanning Devices",
      icon: <Icon fontSize="16px" icon="bx:scan" />,
      type: "submit",
      sx: {
        backgroundColor: theme?.palette?.default_button?.add_background,
        color: theme?.palette?.default_button?.primary_text,
      },
    },

    default_compare_submit: {
      name: "Compare",
      type: "submit",
      sx: {
        backgroundColor: theme?.palette?.default_button?.add_background,
        color: theme?.palette?.default_button?.primary_text,
      },
    },
    default_login: {
      name: "Login",
      type: "submit",
      sx: {
        backgroundColor: theme?.palette?.default_button?.add_background,
        color: theme?.palette?.default_button?.primary_text,
      },
    },
    default_register: {
      name: "Register",
      type: "submit",
      sx: {
        backgroundColor: theme?.palette?.default_button?.add_background,
        color: theme?.palette?.default_button?.primary_text,
      },
    },
    default_reset: {
      name: "Reset",
      sx: {
        backgroundColor: theme?.palette?.default_button?.add_background,
        color: theme?.palette?.default_button?.primary_text,
      },
    },
    default_save: {
      name: "Save",
      sx: {
        backgroundColor: theme?.palette?.default_button?.add_background,
        color: theme?.palette?.default_button?.primary_text,
      },
    },
    default_ok: {
      name: "Ok",
      sx: {
        backgroundColor: theme?.palette?.default_button?.add_background,
        color: theme?.palette?.default_button?.primary_text,
      },
    },
    default_fetch: {
      name: "Fetch",
      icon: <Icon fontSize="16px" icon="fluent:board-20-regular" />,
      sx: {
        backgroundColor: theme?.palette?.default_button?.add_background,
        color: theme?.palette?.default_button?.primary_text,
      },
    },
    default_restore: {
      name: "Restore",
      icon: <Icon fontSize="16px" icon="mdi:restore" />,
      sx: {
        backgroundColor: theme?.palette?.drop_down_button?.export_background,
        color: theme?.palette?.drop_down_button?.export_text,
        border: `1px solid ${theme?.palette?.drop_down_button?.border}`,
      },
    },
    default_backup: {
      name: "Backup",
      icon: <Icon fontSize="16px" icon="tabler:restore" />,
      sx: {
        backgroundColor: theme?.palette?.default_button?.add_background,
        color: theme?.palette?.default_button?.primary_text,
      },
    },
    default_compare: {
      name: "Compare",
      icon: <Icon fontSize="16px" icon="tabler:git-compare" />,
      sx: {
        backgroundColor: theme?.palette?.default_button?.add_background,
        color: theme?.palette?.default_button?.primary_text,
      },
    },

    bulk_scan: {
      category: "dropDownCheckbox",
      name: "Bulk Scan",
      icon: <Icon fontSize="16px" icon="bx:scan" />,
      options: [
        optionConstants.default_scan.PORT_SCAN,
        optionConstants.default_scan.DNS_SCAN,
      ],
      sx: {
        backgroundColor: theme?.palette?.drop_down_button?.export_background,
        color: theme?.palette?.drop_down_button?.export_text,
      },
    },

    default_scan: {
      category: "dropDownCheckbox",
      name: "Scan",
      icon: <Icon fontSize="16px" icon="bx:scan" />,
      options: [
        optionConstants.default_scan.PORT_SCAN,
        optionConstants.default_scan.DNS_SCAN,
      ],
      sx: {
        backgroundColor: theme?.palette?.drop_down_button?.export_background,
        color: theme?.palette?.drop_down_button?.export_text,
      },
    },
    default_update: {
      name: "Update",
      sx: {
        backgroundColor: theme?.palette?.default_button?.add_background,
        color: theme?.palette?.default_button?.primary_text,
      },
    },
    default_submit_update: {
      name: "Update",
      type: "submit",
      sx: {
        backgroundColor: theme?.palette?.default_button?.add_background,
        color: theme?.palette?.default_button?.primary_text,
      },
    },
    default_submit_add: {
      name: "Add",
      type: "submit",
      sx: {
        backgroundColor: theme?.palette?.default_button?.add_background,
        color: theme?.palette?.default_button?.primary_text,
      },
    },
    start_monitoring: {
      name: "Start Monitoring",
      icon: <Icon fontSize="16px" icon="eos-icons:monitoring" />,
      sx: {
        backgroundColor: theme?.palette?.default_button?.add_background,
        color: theme?.palette?.default_button?.primary_text,
      },
    },
    default_next: {
      name: "Next",
      type: "submit",
      sx: {
        backgroundColor: theme?.palette?.default_button?.add_background,
        color: theme?.palette?.default_button?.primary_text,
      },
    },
    default_register: {
      name: "Register",
      type: "submit",
      sx: {
        backgroundColor: theme?.palette?.default_button?.add_background,
        color: theme?.palette?.default_button?.primary_text,
      },
    },
    default_back: {
      name: "Back",
      sx: {
        backgroundColor: theme?.palette?.default_button?.add_background,
        color: theme?.palette?.default_button?.primary_text,
      },
    },
  };

  const dropdownButtonOptionsConstants = Object.keys(buttonDetails).reduce(
    (accumulator, key) => {
      if (optionConstants[key]) {
        accumulator[key] = optionConstants[key];
        return accumulator;
      }
      return accumulator;
    },
    {}
  );

  const buttonsConfigurationList = Object.keys(buttonDetails).map((key) => {
    if (configurations[key]) {
      if (!buttonDetails[key]) {
        buttonDetails[key] = { ...buttonDetails[key], sx: {} };
      }
      const { sx = {}, ...rest } = buttonDetails[key];
      configurations[key].sx = { ...configurations[key].sx, ...sx };
      return { ...configurations[key], ...rest };
    } else {
      return configurations.default_button;
    }
  });

  const buttonsConfigurationObject = Object.keys(buttonDetails).reduce(
    (generatedConfiguration, key) => {
      if (!buttonDetails[key]) {
        buttonDetails[key] = { ...buttonDetails[key], sx: {} };
      }
      const { sx = {}, ...rest } = buttonDetails[key];
      if (configurations[key]) {
        configurations[key].sx = { ...configurations[key].sx, ...sx };
        generatedConfiguration[key] = {
          ...configurations[key],
          ...rest,
        };
        return generatedConfiguration;
      } else {
        generatedConfiguration[key] = {
          ...configurations.default_button,
          ...rest,
        };
        return generatedConfiguration;
      }
    },
    {}
  );

  return {
    dropdownButtonOptionsConstants,
    buttonsConfigurationList,
    buttonsConfigurationObject,
  };
}
