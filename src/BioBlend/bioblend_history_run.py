#!/usr/bin/env python3
import time
import sys
from bioblend.galaxy import GalaxyInstance

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
GALAXY_URL = "http://localhost:8080"          # Local Galaxy
API_KEY = "b8ba458fe9b1c919040db8288c56ed06"  # Replace with your API key
HISTORY_NAME = "biobhistory"                  # History name
INPUT_FILE = "bioblend_history.fastq"         # Local FASTQ filename
FILE_TYPE = "fastqsanger"                     # Standard FASTQ datatype in Galaxy
TOOL_ID = "cat1"                              # Simple Galaxy tool for testing
# ----------------------------------------------------------------------


def get_galaxy_instance(url=GALAXY_URL, key=API_KEY):
    """Return a GalaxyInstance object"""
    return GalaxyInstance(url=url, key=key)


def wait_for_job(gi, job_id, timeout=600, interval=5):
    """
    Poll job state until it finishes or times out.
    Returns: "ok", "error", or "timeout"
    """
    start = time.time()
    while True:
        job = gi.jobs.show_job(job_id)
        state = job["state"]

        if state in ["ok", "error"]:
            return state

        if (time.time() - start) > timeout:
            return "timeout"

        time.sleep(interval)


def create_history(gi, name=HISTORY_NAME):
    """Create a new history and return its ID"""
    history = gi.histories.create_history(name)
    return history["id"]


def upload_file_to_history(gi, file_path, history_id, file_type=FILE_TYPE, input_name="input1"):
    """
    Upload a file to the given history and return the dataset ID
    """
    upload = gi.tools.upload_file(file_path, history_id, file_type=file_type)
    dataset_id = upload["outputs"][0]["id"]
    return dataset_id


def run_tool(gi, history_id, tool_id=TOOL_ID, dataset_id=None, input_name="input1"):
    """
    Run a Galaxy tool using the given dataset in a history.
    Returns the job ID
    """
    if dataset_id is None:
        raise ValueError("dataset_id must be provided")

    run = gi.tools.run_tool(
        history_id=history_id,
        tool_id=tool_id,
        tool_inputs={input_name: {"src": "hda", "id": dataset_id}}
    )
    job_id = run["jobs"][0]["id"]
    return job_id


def show_history_contents(gi, history_id):
    """Return a list of dicts describing the datasets in the history"""
    outputs = gi.histories.show_history(history_id, contents=True)
    result = [{"name": o["name"], "id": o["id"], "state": o.get("state", "unknown")} for o in outputs]
    return result


def main():
    """Main execution function"""
    print("Connecting to Galaxy...")
    gi = get_galaxy_instance()

    # Create history
    print(f"Creating history: {HISTORY_NAME}")
    history_id = create_history(gi, HISTORY_NAME)

    # Upload file
    print(f"Uploading file '{INPUT_FILE}' as FASTQ...")
    dataset_id = upload_file_to_history(gi, INPUT_FILE, history_id)
    print(f"File uploaded with dataset ID: {dataset_id}")

    # Run tool
    print(f"Running tool: {TOOL_ID}")
    job_id = run_tool(gi, history_id, TOOL_ID, dataset_id)
    print(f"Waiting for job {job_id} to finish...")
    state = wait_for_job(gi, job_id)

    if state != "ok":
        print(f"Job finished with state: {state}")
        sys.exit(1)

    print("Job completed successfully.")

    # Show outputs
    print("History outputs:")
    for item in show_history_contents(gi, history_id):
        print(f"- {item['name']} | {item['id']} | {item['state']}")

    print("Done ✅")


if __name__ == "__main__":
    main()
