# BioBlend Galaxy Automation (Python)

## Overview

This repository demonstrates practical automation of the [Galaxy](https://galaxyproject.org/) platform using the **BioBlend** Python library. It provides scripts to programmatically manage Galaxy servers, histories, datasets, libraries, and workflows. All functionality is fully tested with unit tests, ensuring correctness and reproducibility.  

---

## Key Features

- Connect to Galaxy servers programmatically  
- View and manage histories and datasets  
- Upload datasets and run Galaxy tools  
- Manage Galaxy data libraries  
- Create, export, import, and invoke workflows  
- Modular, reusable Python scripts for bioinformatics pipelines  

---

## Technology Stack

- **Python 3.12**  
- **BioBlend** – Galaxy API client  
- **Galaxy** – Local or remote instance  
- **pytest** – Unit testing  
- **GitHub Actions** – CI/CD pipeline  

---

## Project Structure

.
├── .github/
│ └── workflows/
│ └── ci.yml # GitHub Actions CI workflow
├── data/
│ ├── bioblend_history.fastq # Example input dataset
│ └── first_workflows.json # Example workflows export
├── src/BioBlend/
│ ├── auto_upload_to_library.py
│ ├── bioblend_history_run.py
│ ├── connect_to_galaxy.py
│ ├── create_sample_workflow.py
│ ├── export_import_workflow.py
│ ├── interactive_upload_to_library.py
│ ├── invoke_workflow.py
│ ├── upload_and_run_tool.py
│ ├── upload_to_library.py
│ ├── view_data_library.py
│ ├── view_histories_datasets.py
│ └── view_workflows.py
├── tests/
│ ├── test_bioblend_history_run.py
│ ├── test_connect_to_galaxy.py
│ ├── test_create_sample_workflow.py
│ ├── test_export_import_workflow.py
│ ├── test_interactive_upload_to_library.py
│ ├── test_invoke_workflow.py
│ ├── test_upload_and_run_tool.py
│ ├── test_upload_to_library.py
│ ├── test_view_data_library.py
│ ├── test_view_histories_datasets.py
│ └── test_view_workflows.py
├── .gitignore
├── LICENSE
├── Makefile
├── README.md
├── requirements.txt
├── poetry.lock
├── poetry.toml
└── pytest.ini


---

## Setup and Installation

1. **Clone the repository**:

```bash
git clone https://github.com/ASMAMAWABATEH/Bioblend-Use-Case.git
cd Bioblend-Use-Case

    Create and activate a virtual environment:

python -m venv .venv
source .venv/bin/activate

    Install dependencies:

pip install -r requirements.txt
pip install bioblend pytest

    Configure Galaxy access:

export GALAXY_URL="http://localhost:8080"
export GALAXY_API_KEY="your_api_key_here"

Usage

The scripts in src/BioBlend/ automate Galaxy tasks:
Script	                    Purpose
-connect_to_galaxy.py	Establishes authentication and connection to a Galaxy server
-view_histories_datasets.py	Lists and inspects Galaxy histories and datasets
-bioblend_history_run.py	Creates and runs analyses in Galaxy histories
-upload_and_run_tool.py	Uploads datasets and executes Galaxy tools
-auto_upload_to_library.py	Automatically uploads datasets to Galaxy data libraries
-interactive_upload_to_library.py	Interactive upload of datasets to libraries
-upload_to_library.py	Direct uploads to Galaxy libraries
-view_data_library.py	Views and inspects Galaxy data libraries
-create_sample_workflow.py	Creates a sample Galaxy workflow
-export_import_workflow.py	Exports and imports Galaxy workflows
-invoke_workflow.py	Invokes and executes workflows
-view_workflows.py	Lists and inspects available workflows

All scripts are modular and reusable for integration into larger pipelines.
Testing

Unit tests are located in the tests/ folder and mirror the scripts in src/BioBlend/.

Run all tests locally:

make run_test

Or using pytest directly:

pytest tests/ -v

All tests mock Galaxy interactions where appropriate and validate:

    Dataset uploads and tool execution

    History creation and inspection

    Workflow creation, export/import, and invocation

CI/CD Integration

This project includes a GitHub Actions workflow (.github/workflows/ci.yml) that:

    Checks out the repository code

    Sets up a Python environment

    Installs dependencies

    Runs all unit tests automatically

Every push or pull request triggers the CI workflow to maintain code quality and reliability.