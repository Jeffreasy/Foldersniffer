# Developer Documentation

## Overview

This document provides a comprehensive overview of the components used in the project, detailing their responsibilities, attributes, and methods.

## Dashboard Component

The `Dashboard` component is responsible for displaying various statistics and charts related to files in the selected directory. It includes the following functionalities:

- **File Type Chart**: Displays the distribution of different file types in a pie chart.
- **File Size Chart**: Shows the distribution of file sizes in a bar chart.
- **File Modification Timeline**: Visualizes the timeline of file modifications.
- **File Events Chart**: Shows the count of different file events such as created, modified, and deleted.
- **Summary**: Provides an overview of the total number of files, total size, and average file size.
- **Quick Actions Button**: A button that allows users to quickly identify large files.
- **Recent Events Table**: A table displaying recent file events.

### Dashboard Methods

- `update_dashboard`: Updates all charts and the summary on the dashboard with new scan results and summary.
- `update_file_type_chart`: Refreshes the file type chart.
- `update_file_size_chart`: Refreshes the file size chart.
- `update_modification_timeline`: Refreshes the modification timeline.
- `update_event_chart`: Refreshes the file events chart.
- `update_summary`: Refreshes the scan summary.
- `update_recent_events_table`: Refreshes the recent events table.
- `show_large_files`: Displays a message with a list of large files identified during the scan.
- `handle_file_event`: Handles file events such as modifications, additions, and deletions.
- `format_size`: Formats file sizes into readable units (B, KB, MB, etc.).

## ResultDisplay Component

The `ResultDisplay` component is responsible for displaying textual results within the GUI.

### ResultDisplay Methods

- `__init__`: Initializes the `ResultDisplay` component and sets the text field to read-only.
- `display_results`: Displays the results in the text field. It shows directories and files and displays the content of files if available.

## Utils Component

The `utils.py` file contains helper functions for obtaining file information. This file uses standard Python libraries such as `os`, `time`, and `logging`.

### Utils Functions

- `get_file_info`: Retrieves information about a file, such as size, last modification, creation date, mode, owner, number of lines, and number of characters. Logs an error and returns `None` on failure.

## FolderComparison Component

The `FolderComparison` component is responsible for comparing two directories and identifying differences between them.

### FolderComparison Functions

- `compare_folders`: Compares the contents of two directories and identifies common files, files only in the left or right directories, differing files, and possibly "funny" files (files that could not be compared).

## FileTypeSelector Component

The `FileTypeSelector` component is responsible for managing and displaying a list of file types as checkboxes in a scrollable area. Users can select or deselect file types.

### FileTypeSelector Attributes

- `file_types`: A list of tuples, each consisting of a file type (extension) and a description.
- `checkboxes`: A list of `QCheckBox` objects for each file type.

### FileTypeSelector Methods

- `__init__`: Initializes the list of file types and creates checkboxes for each file type.
- `select_all`: Selects all checkboxes.
- `deselect_all`: Deselects all checkboxes.
- `get_selected_file_types`: Returns a list of selected file types.

## FileTypeDialog Component

The `FileTypeDialog` component is a dialog window that allows users to select file types using the `FileTypeSelector` component.

### FileTypeDialog Methods

- `__init__`: Initializes the dialog and adds the `FileTypeSelector` component along with buttons to select/deselect all file types and accept/cancel the dialog.

## DirectorySelector Component

The `DirectorySelector` component is responsible for selecting a directory and displaying the selected directory within the GUI.

### DirectorySelector Attributes

- `directory_path`: The path to the selected directory.

### DirectorySelector Methods

- `__init__`: Initializes the GUI elements for directory selection.
- `browse_directory`: Opens a dialog to select a directory.
- `update_directory_path`: Updates the path of the selected directory.
- `get_directory`: Returns the path of the selected directory.

## Scanner Component

The `Scanner` component is responsible for scanning a selected directory and collecting data about the files in that directory.

### Scanner Methods

- `__init__`: Initializes the `Scanner` component and sets the necessary attributes.
- `start_scan`: Starts the scan of the selected directory.
- `scan_directory`: Performs the scan and collects data about the files.
- `log_scan_results`: Logs the results of the scan.
- `get_scan_summary`: Returns a summary of the scan results.

## EditMenuDialog Component

The `EditMenuDialog` component is a dialog window that allows users to edit settings or configurations.

### EditMenuDialog Methods

- `__init__`: Initializes the dialog and adds the necessary GUI elements.
- `accept`: Called when the user accepts the changes.
- `reject`: Called when the user rejects the changes.

## FileMonitor Component

The `FileMonitor` component is responsible for monitoring changes to files within a directory. It uses an `Observer` to assign event handlers to files.

### FileMonitor Methods

- `__init__`: Initializes the `FileMonitor` with a directory and a callback function. Creates an `Observer` and assigns a `FileChangeHandler` to the given directory.
- `start`: Starts the `Observer` to detect file changes.
- `stop`: Stops the `Observer` and waits for it to fully stop.

## FileChangeHandler Component

The `FileChangeHandler` component is an event handler that handles file changes and calls a callback function when a change is detected.

### FileChangeHandler Methods

- `__init__`: Initializes the `FileChangeHandler` with a callback function.
- `on_modified`: Calls the callback function when a file is modified.
- `on_created`: Calls the callback function when a new file is created.
- `on_deleted`: Calls the callback function when a file is deleted.
- `on_moved`: Calls the callback function when a file is moved or renamed.

## Exporter Component

The `Exporter` component is responsible for exporting scan results to a text file.

### Exporter Methods

- `export_as_txt`: Exports the scan results to a text file with details such as path, size, last modification, creation date, mode, owner, and content.

## ResultsDialog Component

The `ResultsDialog` component is responsible for loading and displaying results in a dialog window. It uses various GUI elements to display the results in a structured manner.

### ResultsDialog Methods

- `load_results`: Loads the results and displays them in the dialog. This method processes the results and adds them to the GUI elements.

## FileScanner Component

The `FileScanner` component is responsible for scanning a directory and collecting data about files. This component uses multithreading to perform the scan efficiently.

### FileScanner Methods

- `count_scannable_items`: Counts the number of scannable items in a directory, considering ignored files and directories and selected file types.
- `scan_directory`: Performs the scan on the selected directory. Creates a log file, performs the scan using a `ThreadPoolExecutor`, and logs the results. This method also uses callback functions to track progress.

## Search Component

The `Search` component is responsible for performing regex searches in a directory. This component can search for specific patterns in files and filter by file types.

### Search Methods

- `regex_search`: Performs a regex search in a directory. It searches files based on a given pattern and file types and returns a list of results.

## GUI Integration Component

This component integrates various GUI elements for configuring and performing scans, including options for selecting file types, excluding certain files/folders, and setting log fields.

### GUI Integration Attributes

- `filetype_selector`: A `FileTypeSelector` component for selecting file types.
- `exclude_selector`: An `ExcludeSelector` component for excluding certain files/folders.
- `log_size_checkbox`: A checkbox for logging file sizes.
- `log_last_modified_checkbox`: A checkbox for logging the last modification time.
- `log_created_checkbox`: A checkbox for logging the creation time.
- `log_mode_checkbox`: A checkbox for logging the file access mode.
- `log_owner_checkbox`: A checkbox for logging the file owner.
- `log_content_checkbox`: A checkbox for logging the content of files.
- `regex_input`: An input field for entering a regex pattern.
- `search_button`: A button for performing the regex search.

### GUI Integration Methods

- `perform_regex_search`: Performs a regex search based on the entered patterns and settings.

## FileMonitoring Component

The `FileMonitoring` component is responsible for monitoring changes in files within a directory and detecting encryption. It includes functions for starting and stopping monitoring and handling file events.

### FileMonitoring Methods

- `toggle_file_monitoring`: Starts or stops monitoring files in the selected directory.
- `handle_file_change`: Handles changes in files such as creation, deletion, and modification, and updates the GUI with the changes.
- `detect_encryption`: Detects the presence of encryption in files within the directory.

## SaveResults Component

The `SaveResults` component is responsible for saving scan results in various formats, such as JSON, text, and ZIP files. This component provides a dialog window for users to select the file type and location.

### SaveResults Methods

- `save_results`: Opens a dialog to select the file type and storage location.
- `save_as_json`: Saves the results in a JSON file.
- `save_as_txt`: Saves the results in a text file.
- `save_as_zip`: Saves the results in a text file and compresses it into a ZIP file.

## ScanWorker Component

The `ScanWorker` component is a background thread responsible for performing directory scans. This component uses PyQt6 signals to relay scan progress and results back to the GUI.

### ScanWorker Attributes

- `progress`: A PyQt6 signal indicating the progress of the scan.
- `results`: A PyQt6 signal returning the results of the scan, including the scan summary.

### ScanWorker Methods

- `__init__`: Initializes the `ScanWorker` with the required parameters for the scan.
- `run`: Performs the scan by calling the `scan_directory` function and returns the results and progress through the signals.

## PyQtSignals Component

The `PyQtSignals` component contains custom PyQt signals for use in the GUI. These signals facilitate communication and updates between various components.

### PyQtSignals Methods

- `__init__`: Initializes the PyQt signals.

## GUI Components

This section includes various GUI components enabling user interaction and displaying scan results.

### GUI Components Attributes

- `start_button`: A button to start the scan.
- `stop_button`: A button to stop the scan.
- `progress_bar`: A progress bar displaying the scan progress.
- `result_display`: A text field to display the results.
- `scan_summary`: A field to display the scan summary.

### GUI Components Methods

- `init_gui`: Initializes the GUI elements.
- `connect_signals`: Connects the PyQt signals to their respective methods.

## EventHandler Component

The `EventHandler` component handles various events within the application, such as starting and stopping scans and updating the GUI.

### EventHandler Methods

- `start_scan`: Starts a new scan and initializes the required components.
- `stop_scan`: Stops the ongoing scan and updates the GUI.
- `update_progress`: Updates the progress bar based on received signals.
- `display_results`: Displays the scan results in the GUI.
- `show_summary`: Displays a summary of the scan in the GUI.

## ConfigManager Component

The `ConfigManager` component manages configuration settings of the application, such as user preferences and scan options.

### ConfigManager Attributes

- `config_file`: The path to the configuration file.
- `settings`: A dictionary containing the configuration settings.

### ConfigManager Methods

- `load_config`: Loads the configuration settings from the configuration file.
- `save_config`: Saves the current configuration settings to the configuration file.
- `get_setting`: Retrieves a specific setting from the configuration.
- `set_setting`: Modifies a specific setting in the configuration.

## Logger Component

The `Logger` component is responsible for logging events and errors within the application. This component uses Python's standard logging library.

### Logger Methods

- `init_logger`: Initializes the logger with the desired settings, such as log level and log file.
- `log_info`: Logs informational messages.
- `log_warning`: Logs warning messages.
- `log_error`: Logs error messages.
