#!/usr/bin/env python3
from bioblend.galaxy import GalaxyInstance
import os
import time

# ----------------------------
# CONFIGURATION
# ----------------------------
GALAXY_URL = "http://localhost:8080"   # Change if needed
API_KEY = "b8ba458fe9b1c919040db8288c56ed06"          # Replace with your Galaxy API key
HISTORY_NAME = "biobhistory"
FILE_NAME = "biobhistory.fastq"
FILE_TYPE = "fastqsanger"  # FASTQ format in Galaxy
TOOL_ID = "cat1"           # Example: concatenate datasets

# ----------------------------
# CONNECT TO GALAXY
# ----------------------------
gi = GalaxyInstance(url=GALAXY_URL, key=API_KEY)
print("Connected to Galaxy.")

# ----------------------------
# CHECK OR CREATE HISTORY
# ----------------------------
histories = gi.histories.get_histories()
history_id = None

for h in histories:
    if h['name'] == HISTORY_NAME:
        history_id = h['id']
        print(f"Using existing history: {HISTORY_NAME} (ID: {history_id})")
        break

if not history_id:
    history = gi.histories.create_history(name=HISTORY_NAME)
    history_id = history['id']
    print(f"Created history: {HISTORY_NAME} (ID: {history_id})")

# ----------------------------
# UPLOAD DATASET
# ----------------------------
if not os.path.exists(FILE_NAME):
    print(f"Error: File '{FILE_NAME}' not found!")
    exit(1)

print(f"Uploading file '{FILE_NAME}' as {FILE_TYPE}...")
dataset = gi.tools.upload_file(FILE_NAME, history_id, file_type=FILE_TYPE)

# Wait for dataset to finish uploading
dataset_id = dataset['outputs'][0]['id']
state = ""
while state != "ok":
    time.sleep(2)
    d = gi.datasets.show_dataset(dataset_id)
    state = d['state']
print(f"File uploaded successfully! Dataset ID: {dataset_id}")

# ----------------------------
# RUN TOOL ON DATASET
# ----------------------------
print(f"\nRunning tool '{TOOL_ID}' on the uploaded dataset...")
# Input mapping depends on the tool; cat1 uses "input1" for first dataset
tool_inputs = {
    "input1": {"src": "hda", "id": dataset_id}
}

run = gi.tools.run_tool(history_id, TOOL_ID, tool_inputs)
job_id = run["jobs"][0]["id"]
print(f"Job submitted. Job ID: {job_id}")

# Wait for job to finish
job_state = ""
while job_state not in ["ok", "error", "failed"]:
    time.sleep(3)
    job_info = gi.jobs.show_job(job_id)
    job_state = job_info["state"]

if job_state == "ok":
    print(f"Tool finished successfully! Job ID: {job_id}")
else:
    print(f"Tool failed! Job ID: {job_id}, state={job_state}")

# ----------------------------
# LIST DATASETS IN HISTORY
# ----------------------------
print(f"\nDatasets in history '{HISTORY_NAME}':")
contents = gi.histories.show_history(history_id, contents=True)
for d in contents:
    print(f"- {d['name']} | {d['id']} | state={d['state']} | type={d['type']}")

print("\nDone ✅ All automated!")
