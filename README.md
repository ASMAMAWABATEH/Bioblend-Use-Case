# Galaxy Automation with BioBlend (Python)

## Overview

This repository demonstrates practical use cases for the BioBlend Python library to programmatically control and automate the Galaxy data analysis platform. It covers connecting to Galaxy servers, managing datasets, libraries, and workflows via Python code, with comprehensive unit tests to verify functionality.


## Key Features

Using BioBlend, the project implements and tests the following capabilities:

* Connect to Galaxy servers
* View and manage histories and datasets
* Upload datasets programmatically
* Manage Galaxy data libraries
* Export and import workflows via Python code

Each feature is covered by unit tests to ensure expected behavior and correctness.

## Technology Stack

* **Python 3.11**
* **BioBlend** (Galaxy API client)
* **Galaxy** (local instance)
* **pytest / unittest** (for automated testing)

## Project Structure

```
.
├── .venv
├── .github/
│   └── workflows/
│       └── ci.yml  
├── src/BioBlend
|   ├── auto_upload_to_library.py
│   ├── connect_to_galaxy.py      
|   ├── create_sample_workflow.py
|   ├── export_import_workflow.py
|   ├── interactive_upload_to_library.py
|   ├── invoke_workflow.py
|   ├── upload_and_run_tool.py
|   ├── view_histories_data_sets.py
│   ├── bioblend_history_run.py             
│   ├── upload_to-library.py               
│   ├── view_data_library.py            
│   └── view_workflows.py             
│
├── tests/
│   ├── test_bioblend_history_run.py
│   ├── test_connect_to_galaxy.py       
│   ├── test_create_sample_workflow.py         
│   ├── test_export_import_workflow.py           
│   ├── test_interactive_upload_to_library.py         
│   └── test_invoke_workflow.py 
│   └── test_upload_and_run_tool.py 
│   └── test_upload_to_library.py 
│   └── test_view_data_library.py
│   └── test_view_histories_datasets.py 
│   └── test_view_workflows.pyg
│
├── requirements.txt
└── README.md
```

## Setup and Installation

1. Clone the repository:

```bash
git clone https://github.com/ASMAMAWABATEH/Bioblend-Use-Case.git
cd Bioblend-Use-Case
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
pip install bioblend pytest
```

4. Configure Galaxy access:

* export GALAXY_URL="http://localhost:8080"
* export GALAXY_API_KEY="my_api_key_here"

## Usage

The scripts in the src/BioBlend/ directory provide concrete, task-oriented examples of automating Galaxy using the BioBlend Python library:

* connect_to_galaxy.py – Establishes authentication and connection to a Galaxy server
* view_histories_data_sets.py – Lists and inspects Galaxy histories and datasets
* bioblend_history_run.py – Creates and runs analyses within Galaxy histories
* upload_and_run_tool.py – Uploads datasets and executes Galaxy tools programmatically
* auto_upload_to_library.py – Automatically uploads datasets to Galaxy data libraries
* interactive_upload_to_library.py – Interactive dataset upload to Galaxy libraries
* upload_to-library.py – Handles direct uploads to Galaxy libraries
* view_data_library.py – Views and inspects Galaxy data libraries
* create_sample_workflow.py – Creates a sample Galaxy workflow using Python
* export_import_workflow.py – Exports and imports Galaxy workflows programmatically
* invoke_workflow.py – Invokes and executes workflows on Galaxy
* view_workflows.py – Lists and inspects available Galaxy workflows

Each script is designed to be modular, reusable, and easy to integrate into larger automation or bioinformatics pipelines.

## Testing

Unit tests are used to validate each operation and ensure the expected behavior of the Galaxy API interactions.

The tests/ directory provides one-to-one coverage for the scripts in src/BioBlend/:

* test_connect_to_galaxy.py – Tests Galaxy server connection and authentication
* test_view_histories_datasets.py – Tests listing and inspection of histories and datasets
* test_bioblend_history_run.py – Tests running analyses in Galaxy histories
* test_upload_and_run_tool.py – Tests dataset upload and tool execution
* test_upload_to_library.py – Tests dataset uploads to Galaxy libraries
* test_interactive_upload_to_library.py – Tests interactive library uploads
* test_view_data_library.py – Tests viewing Galaxy data libraries
* test_create_sample_workflow.py – Tests workflow creation
* test_export_import_workflow.py – Tests workflow export and import
* test_invoke_workflow.py – Tests workflow invocation and execution
* test_view_workflows.py – Tests viewing available workflows

All tests can be executed locally or automatically via the GitHub Actions CI pipeline to ensure reliability and reproducibility.

Unit tests are used to validate each operation.

Run all tests with:

```bash
pytest tests/-V
```

The tests verify that each function returns the expected results and that Galaxy API interactions behave correctly.

## Learning Outcomes

* Practical use of BioBlend for Galaxy automation
* Clean separation of functionality into testable modules
* Writing unit tests for external API-based systems
* Building reliable, reproducible Galaxy workflows using Python

## CI/CD Integration (GitHub Actions)

This project integrates CI/CD using GitHub Actions to automate testing and ensure code quality. The workflow is configured to automatically run unit tests whenever code is pushed or a pull request is opened.

CI/CD Workflow Overview

The GitHub Actions workflow performs the following steps:

* Checks out the repository code
* Sets up a Python environment
* Installs project dependencies
* Runs all unit tests for the scripts in src/BioBlend/