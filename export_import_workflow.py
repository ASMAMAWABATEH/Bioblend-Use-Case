#!/usr/bin/env python3
from bioblend.galaxy import GalaxyInstance
import json
import os

# ----------------------------
# CONFIGURATION
# ----------------------------
GALAXY_URL = "http://localhost:8080"
API_KEY = "b8ba458fe9b1c919040db8288c56ed06"  # Replace with your Galaxy API key
WORKFLOW_NAME = "First_workflow"  # Workflow to export and import
EXPORT_DIR = "exported_workflows"

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
# EXPORT WORKFLOW
# ----------------------------
workflow_dict = gi.workflows.export_workflow_dict(workflow_id)

# Ensure export directory exists
os.makedirs(EXPORT_DIR, exist_ok=True)
export_path = os.path.join(EXPORT_DIR, f"{WORKFLOW_NAME.replace(' ', '_')}.json")

with open(export_path, "w") as f:
    json.dump(workflow_dict, f, indent=2)

print(f"Workflow '{WORKFLOW_NAME}' exported to {export_path}")

# ----------------------------
# IMPORT WORKFLOW BACK INTO GALAXY
# ----------------------------
with open(export_path) as f:
    workflow_json = json.load(f)

imported_workflow = gi.workflows.import_workflow_dict(workflow_json)
print(f"Imported workflow '{imported_workflow['name']}' with new ID: {imported_workflow['id']}")

print("\n✅ Workflow export and import complete!")
