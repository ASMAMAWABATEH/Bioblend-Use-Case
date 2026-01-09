# Galaxy Automation with BioBlend (Python)

## Overview
This repository demonstrates practical use cases for the **BioBlend** Python library to programmatically control and automate the **Galaxy** data analysis platform. It covers connecting to Galaxy servers, managing datasets, libraries, and workflows via Python code, with comprehensive unit tests to verify functionality.

## Key Features
Using BioBlend, the project implements and tests the following capabilities:

- Connect to Galaxy servers
- View and manage histories and datasets
- Upload datasets programmatically
- Manage Galaxy data libraries
- Export and import workflows via Python code

Each feature is covered by unit tests to ensure expected behavior and correctness.

## Technology Stack
- Python 3.11+
- BioBlend (Galaxy API client)
- Galaxy (local instance)
- pytest / unittest (for automated testing)

## Project Structure
```text
.
├── .github/
│   └── workflows/
│       └── ci.yml # GitHub Actions CI workflow
├── data/
│   ├── bioblend_history.fastq # Example input dataset
│   └── first_workflows.json   # Example workflows export
├── src/BioBlend/
│   ├── auto_upload_to_library.py
│   ├── bioblend_history_run.py
│   ├── connect_to_galaxy.py
│   ├── create_sample_workflow.py
│   ├── export_import_workflow.py
│   ├── interactive_upload_to_library.py
│   ├── invoke_workflow.py
│   ├── upload_and_run_tool.py
│   ├── upload_to_library.py
│   ├── view_data_library.py
│   ├── view_histories_datasets.py
│   └── view_workflows.py
├── tests/
│   ├── test_auto_upload_to_library.py
│   ├── test_bioblend_history_run.py
│   ├── test_connect_to_galaxy.py
│   ├── test_create_sample_workflow.py
│   ├── test_export_import_workflow.py
│   ├── test_interactive_upload_to_library.py
│   ├── test_invoke_workflow.py
│   ├── test_upload_and_run_tool.py
│   ├── test_upload_to_library.py
│   ├── test_view_data_library.py
│   ├── test_view_histories_datasets.py
│   └── test_view_workflows.py
├── .gitignore
├── LICENSE
├── Makefile
├── README.md
├── requirements.txt
├── poetry.lock
├── poetry.toml
└── pytest.ini
```

## Setup and Installation

Clone the repository:

```bash
git clone https://github.com/ASMAMAWABATEH/Bioblend-Use-Case.git
cd Bioblend-Use-Case
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
pip install bioblend pytest
```

Configure Galaxy access:

```bash
export GALAXY_URL="http://localhost:8080"
export GALAXY_API_KEY="my_api_key_here"
```

## Usage
The scripts in `src/BioBlend/` provide concrete, task-oriented examples of automating Galaxy using BioBlend:

- `auto_upload_to_library.py` – Automatically uploads datasets to Galaxy data libraries.
- `connect_to_galaxy.py` – Establishes authentication and connection to a Galaxy server
- `view_histories_datasets.py` – Lists and inspects Galaxy histories and datasets
- `bioblend_history_run.py` – Creates and runs analyses within Galaxy histories
- `upload_and_run_tool.py` – Uploads datasets and executes Galaxy tools programmatically
- `interactive_upload_to_library.py` – Interactive dataset upload to Galaxy libraries
- `upload_to_library.py` – Handles direct uploads to Galaxy libraries
- `view_data_library.py` – Views and inspects Galaxy data libraries
- `create_sample_workflow.py` – Creates a sample Galaxy workflow using Python
- `export_import_workflow.py` – Exports and imports Galaxy workflows programmatically
- `invoke_workflow.py` – Invokes and executes workflows on Galaxy
- `view_workflows.py` – Lists and inspects available Galaxy workflows

Each script is modular, reusable, and easy to integrate into larger automation pipelines.

## Testing

Unit tests are provided in `tests/` and mirror the scripts in `src/BioBlend/`:

- `test_auto_upload_to_library.py` – Tests automatic uploads to Galaxy libraries.
- `test_connect_to_galaxy.py` – Tests Galaxy server connection and authentication
- `test_view_histories_datasets.py` – Tests listing and inspection of histories and datasets
- `test_bioblend_history_run.py` – Tests running analyses in Galaxy histories
- `test_upload_and_run_tool.py` – Tests dataset upload and tool execution
- `test_upload_to_library.py` – Tests dataset uploads to Galaxy libraries
- `test_interactive_upload_to_library.py` – Tests interactive library uploads
- `test_view_data_library.py` – Tests viewing Galaxy data libraries
- `test_create_sample_workflow.py` – Tests workflow creation
- `test_export_import_workflow.py` – Tests workflow export and import
- `test_invoke_workflow.py` – Tests workflow invocation and execution
- `test_view_workflows.py` – Tests viewing available workflows

Run all tests locally:

```bash
pytest
```

## CI/CD Integration (GitHub Actions)
This project uses GitHub Actions for CI/CD:

- Checks out the repository
- Sets up a Python environment
- Installs project dependencies
- Runs all unit tests automatically on push or pull requests
