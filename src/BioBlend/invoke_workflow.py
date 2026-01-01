#!/usr/bin/env python3
from bioblend.galaxy import GalaxyInstance
import time
import os

# ----------------------------
# CONFIGURATION
# ----------------------------
GALAXY_URL = "http://localhost:8080"
API_KEY = "b8ba458fe9b1c919040db8288c56ed06"  # Replace with your Galaxy API key
WORKFLOW_NAME = "First_workflow"  # Use your fixed workflow with available tool
HISTORY_NAME = "Workflow_Run_History"
FILE_NAME = "bioblend_history.fastq"
FILE_TYPE = "fastqsanger"

MAX_WAIT = 300  # seconds
INTERVAL = 5    # seconds

# ----------------------------
# CONNECT TO GALAXY
# ----------------------------
gi = GalaxyInstance(url=GALAXY_URL, key=API_KEY)
print("Connected to Galaxy.")

# ----------------------------
# FIND WORKFLOW BY NAME
# ----------------------------
workflows = gi.workflows.get_workflows()
workflow_id = None
for wf in workflows:
    if wf['name'] == WORKFLOW_NAME:
        workflow_id = wf['id']
        break

if not workflow_id:
    print(f"Workflow '{WORKFLOW_NAME}' not found!")
    exit(1)

print(f"Found workflow '{WORKFLOW_NAME}' with ID: {workflow_id}")

# ----------------------------
# CREATE HISTORY
# ----------------------------
history = gi.histories.create_history(HISTORY_NAME)
history_id = history['id']
print(f"Created history '{HISTORY_NAME}' with ID: {history_id}")

# ----------------------------
# UPLOAD DATASET
# ----------------------------
if not os.path.exists(FILE_NAME):
    print(f"File '{FILE_NAME}' not found!")
    exit(1)

dataset = gi.tools.upload_file(FILE_NAME, history_id, file_type=FILE_TYPE)
dataset_id = dataset['outputs'][0]['id']
print(f"Uploaded dataset '{FILE_NAME}' with ID: {dataset_id}")

# ----------------------------
# INVOKE WORKFLOW
# ----------------------------
run = gi.workflows.invoke_workflow(
    workflow_id=workflow_id,
    history_id=history_id,
    inputs={"0": {"id": dataset_id}}  # Map first workflow input
)
invocation_id = run['id']
print(f"Workflow started with invocation ID: {invocation_id}")

# ----------------------------
# WAIT FOR COMPLETION WITH TIMEOUT
# ----------------------------
print("Waiting for workflow to complete...")
elapsed = 0
while True:
    invocation = gi.workflows.show_invocation(workflow_id, invocation_id)
    state = invocation['state']
    print(f"Workflow state: {state}")
    if state in ['ok', 'error', 'failed']:
        break
    time.sleep(INTERVAL)
    elapsed += INTERVAL
    if elapsed >= MAX_WAIT:
        print("Timeout reached. Workflow still not finished.")
        break

print("Workflow finished or timed out.")

# ----------------------------
# LIST OUTPUT DATASETS
# ----------------------------
datasets = gi.histories.show_history(history_id, contents=True)
print("\nDatasets in history after workflow run:")
for ds in datasets:
    print(f"- {ds['name']} | ID: {ds['id']} | State: {ds['state']}")

print("\n✅ Workflow invocation complete!")
