from bioblend.galaxy import GalaxyInstance
import os

# --------------------------------------------------------------
# Configuration
# --------------------------------------------------------------
GALAXY_URL = "http://localhost:8080"
API_KEY = "b8ba458fe9b1c919040db8288c56ed06"

# --------------------------------------------------------------
# Core Functions
# --------------------------------------------------------------
def get_galaxy_instance(url=GALAXY_URL, key=API_KEY):
    """Create and return a GalaxyInstance."""
    return GalaxyInstance(url=url, key=key)


def create_history(gi, history_name):
    """Create a new history."""
    return gi.histories.create_history(history_name)


def upload_file(gi, history_id, file_path, file_type="fastqsanger"):
    """Upload a local file to a Galaxy history."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found!")
    uploaded = gi.tools.upload_file(file_path, history_id, file_type=file_type)
    return uploaded[0]["id"]  # Return the dataset ID


def run_tool(gi, tool_id, history_id, tool_inputs):
    """
    Run a tool in Galaxy.

    tool_inputs should be a dictionary, e.g.,
        {"input_file": {"src": "hda", "id": "dataset-001"}}
    """
    result = gi.tools.run_tool(history_id, tool_id, tool_inputs=tool_inputs)
    return result


# --------------------------------------------------------------
# Script Execution
# --------------------------------------------------------------
def main():
    gi = get_galaxy_instance()
    print("Connected to Galaxy.")

    # Example usage
    history = create_history(gi, "Test_History")
    print(f"Created history ID: {history['id']}")

    file_name = "bioblend_history.fastq"
    dataset_id = upload_file(gi, history["id"], file_name)
    print(f"Uploaded dataset ID: {dataset_id}")

    tool_result = run_tool(gi, "fastqc", history["id"],
                           {"input_file": {"src": "hda", "id": dataset_id}})
    print(f"Tool run result: {tool_result}")


if __name__ == "__main__":
    main()
