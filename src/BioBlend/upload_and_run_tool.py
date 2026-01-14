# src/BioBlend/upload_and_run_tool.py
import os
from bioblend.galaxy import GalaxyInstance

# ----------------------------
# Configuration
# ----------------------------
GALAXY_URL = "http://localhost:8080"
API_KEY = "b8ba458fe9b1c919040db8288c56ed06"
DEFAULT_HISTORY_NAME = "Test_History"
DEFAULT_FILE_NAME = "bioblend_history.fastq"
DEFAULT_TOOL_ID = "fastqc"
DEFAULT_TOOL_INPUTS = {}  # Example: {"input_file": {"src": "hda", "id": "dataset-001"}}

# ----------------------------
# Core Functions (testable)
# ----------------------------
def get_galaxy_instance(url=GALAXY_URL, key=API_KEY):
    """Create and return a GalaxyInstance."""
    return GalaxyInstance(url=url, key=key)

def create_history(gi, history_name=DEFAULT_HISTORY_NAME):
    """Create a new history in Galaxy and return its dict."""
    return gi.histories.create_history(history_name)

def upload_file(gi, history_id, file_path, file_type="fastqsanger"):
    """
    Upload a local file to a Galaxy history.
    
    Raises FileNotFoundError if file does not exist.
    Returns the dataset ID.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found!")
    uploaded = gi.tools.upload_file(file_path, history_id, file_type=file_type)
    return uploaded[0]["id"]

def run_tool(gi, tool_id, history_id, tool_inputs):
    """
    Run a tool in Galaxy with given inputs.
    
    Returns the result dictionary.
    """
    return gi.tools.run_tool(history_id, tool_id, tool_inputs=tool_inputs)

def perform_full_workflow(
    gi,
    history_name=DEFAULT_HISTORY_NAME,
    file_path=DEFAULT_FILE_NAME,
    tool_id=DEFAULT_TOOL_ID,
    tool_inputs=None
):
    """
    High-level wrapper: create history, upload file, run tool.
    
    Returns (history_id, dataset_id, tool_result)
    """
    history = create_history(gi, history_name)
    dataset_id = upload_file(gi, history["id"], file_path)
    
    # Prepare tool inputs
    if tool_inputs is None:
        tool_inputs = {"input_file": {"src": "hda", "id": dataset_id}}
    
    result = run_tool(gi, tool_id, history["id"], tool_inputs)
    return history["id"], dataset_id, result

# ----------------------------
# CLI / Script Execution
# ----------------------------
def main():
    gi = get_galaxy_instance()
    print("Connected to Galaxy.")

    try:
        history_id, dataset_id, tool_result = perform_full_workflow(gi)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    print(f"Created history ID: {history_id}")
    print(f"Uploaded dataset ID: {dataset_id}")
    print(f"Tool run result: {tool_result}")


if __name__ == "__main__":
    main()
