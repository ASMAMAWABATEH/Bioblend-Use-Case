#!/usr/bin/env python3
from bioblend.galaxy import GalaxyInstance
import json

# ----------------------------
# CONFIGURATION
# ----------------------------
GALAXY_URL = "http://localhost:8080"
API_KEY = "b8ba458fe9b1c919040db8288c56ed06"  # Replace with your Galaxy API key

# Sample workflow details
WORKFLOW_NAME = "Sample_Workflow"
WORKFLOW_DESC = "This is a sample workflow created via Bioblend"
TOOL_ID = "cat1"  # Simple tool for testing
STEP_LABEL = "Concatenate Step"

# ----------------------------
# CONNECT TO GALAXY
# ----------------------------
gi = GalaxyInstance(url=GALAXY_URL, key=API_KEY)
print("Connected to Galaxy.")

# ----------------------------
# CREATE A NEW WORKFLOW
# ----------------------------
workflow_dict = {
    "name": WORKFLOW_NAME,
    "annotation": WORKFLOW_DESC,
    "steps": {
        "0": {
            "type": "tool",
            "tool_id": TOOL_ID,
            "tool_version": gi.tools.show_tool(TOOL_ID)['version'],
            "label": STEP_LABEL,
            "inputs": {}
        }
    }
}

# Import workflow to Galaxy
imported_workflow = gi.workflows.import_workflow_dict(workflow_dict)
workflow_id = imported_workflow['id']
print(f"\nSample workflow '{WORKFLOW_NAME}' created successfully with ID: {workflow_id}")

# ----------------------------
# LIST ALL WORKFLOWS TO VERIFY
# ----------------------------
workflows = gi.workflows.get_workflows()
print("\nCurrent workflows on the server:")
for wf in workflows:
    print(f"- {wf['name']} | ID: {wf['id']} | Published: {wf.get('published', False)}")

print("\n✅ Workflow creation and verification complete!")
