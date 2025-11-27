#!/usr/bin/env python3
from bioblend.galaxy import GalaxyInstance
import sys

# ----------------------------
# CONFIGURATION
# ----------------------------
GALAXY_URL = "http://localhost:8080"
API_KEY = "b8ba458fe9b1c919040db8288c56ed06"  # Replace with your Galaxy API key

# ----------------------------
# CONNECT TO GALAXY
# ----------------------------
try:
    gi = GalaxyInstance(url=GALAXY_URL, key=API_KEY)
    print("Connected to Galaxy.")
except Exception as e:
    print(f"Error connecting to Galaxy: {e}")
    sys.exit(1)

# ----------------------------
# LIST ALL WORKFLOWS
# ----------------------------
workflows = gi.workflows.get_workflows()
print(f"\nFound {len(workflows)} workflows on the server.\n")

if not workflows:
    print("No workflows found.")
    sys.exit(0)

# ----------------------------
# VIEW WORKFLOW DETAILS AND STEPS
# ----------------------------
for wf in workflows:
    wf_id = wf['id']
    wf_name = wf['name']
    published = wf.get('published', False)
    owner = wf.get('owner', 'N/A')

    print(f"\nWorkflow: {wf_name}")
    print(f"- ID: {wf_id}")
    print(f"- Published: {published}")
    print(f"- Owner: {owner}")

    try:
        # Retrieve full workflow details to show steps
        wf_details = gi.workflows.show_workflow(wf_id)
        steps = wf_details.get('steps', {})
        print(f"- Total Steps: {len(steps)}")
        
        # Print details for each step
        for step_id, step in steps.items():
            print(f"  Step {step_id}: Tool ID: {step.get('tool_id')} | Label: {step.get('label')}")

    except Exception as e:
        print(f"- ERROR: Could not retrieve details for workflow {wf_name}. Reason: {e}")
        continue # Move to the next workflow

print("\n✅ Workflow viewing complete.")
