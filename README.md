# GitHub Download

GitHub Download is a tool for downloading commit comments and select issues metadata from GitHub repositories, saving the raw JSON and writing summary .csv files.

## Purpose

- **Retrieve Metadata**: Downloads commit comments and select issues metadata from GitHub repositories.
- **Data Storage**: Saves the retrieved metadata in raw JSON format.
- **Summary Files**: Generates summary .csv files to provide an overview of the downloaded data.

## Installation

1. **Download**: Obtain the `.jar` file from the [latest release](https://github.com/PovertyAction/github-download/releases/latest).
2. **Dependencies**: The `.jar` file includes all dependencies.
3. **Java Runtime Environment**: Ensure you have Java Runtime Environment (JRE) version 7 or above installed on your system.

## Usage

GitHub Download can be utilized from the command line with the following flags:

- `-repo`: Specifies the full repository name, e.g., `PovertyAction/github-download`.
- `-to`: Specifies the directory to save the metadata. If it doesn't exist, it will be created.
- `-token`: Specifies the name of a text file containing a GitHub OAuth token.

To download all supported metadata, include the `-issues` and `-cc` flags.

**Note**: You may encounter a warning message about SLF4J, which can be safely ignored.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
