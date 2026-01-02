from bioblend.galaxy import GalaxyInstance
import time
import sys

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
GALAXY_URL = "http://localhost:8080"          # Local Galaxy
API_KEY = "b8ba458fe9b1c919040db8288c56ed06"                 # Replace with your API key

HISTORY_NAME = "biobhistory"                  # History name
INPUT_FILE = "bioblend_history.fastq"              # Your local FASTQ filename
FILE_TYPE = "fastqsanger"                     # Standard FASTQ datatype in Galaxy
TOOL_ID = "cat1"                              # Simple Galaxy tool for testing
# ----------------------------------------------------------------------


def wait_for_job(gi, job_id, timeout=600, interval=5):
    """
    Poll job state until it finishes or times out.
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


def main():
    print("Connecting to Galaxy...")
    gi = GalaxyInstance(url=GALAXY_URL, key=API_KEY)

    # Create a new history
    print(f"Creating history: {HISTORY_NAME}")
    history = gi.histories.create_history(HISTORY_NAME)
    history_id = history["id"]

    # Upload FASTQ file
    print(f"Uploading file '{INPUT_FILE}' as FASTQ...")
    upload = gi.tools.upload_file(
        INPUT_FILE,
        history_id,
        file_type=FILE_TYPE
    )
    dataset_id = upload["outputs"][0]["id"]

    print(f"File uploaded with dataset ID: {dataset_id}")

    # Run the test tool (cat1)
    print("Running tool: cat1")
    run = gi.tools.run_tool(
        history_id=history_id,
        tool_id=TOOL_ID,
        tool_inputs={"input1": {"src": "hda", "id": dataset_id}}
    )
    job_id = run["jobs"][0]["id"]

    # Wait for completion
    print(f"Waiting for job {job_id} to finish...")
    state = wait_for_job(gi, job_id)

    if state != "ok":
        print(f"Job finished with state: {state}")
        sys.exit(1)

    print("Job completed successfully.")

    # Show outputs
    print("History outputs:")
    outputs = gi.histories.show_history(history_id, contents=True)
    for item in outputs:
        print(f"- {item['name']} | {item['id']} | {item['state']}")

    print("Done.")


if __name__ == "__main__":
    main()