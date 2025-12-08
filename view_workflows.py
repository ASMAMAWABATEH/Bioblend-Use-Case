#!/usr/bin/env python3
from bioblend.galaxy import GalaxyInstance

# ----------------------------
# CONFIGURATION
# ----------------------------
GALAXY_URL = "http://localhost:8080"
API_KEY = "b8ba458fe9b1c919040db8288c56ed06"  # Replace with your Galaxy API key

# ----------------------------
# CONNECT TO GALAXY
# ----------------------------
gi = GalaxyInstance(url=GALAXY_URL, key=API_KEY)
print("Connected to Galaxy.")

# ----------------------------
# LIST ALL WORKFLOWS
# ----------------------------
workflows = gi.workflows.get_workflows()
print(f"\nFound {len(workflows)} workflows on the server.\n")

if not workflows:
    print("No workflows found.")
else:
    for wf in workflows:
        wf_id = wf['id']
        wf_name = wf['name']
        published = wf.get('published', False)
        owner = wf.get('owner', 'N/A')

        print(f"Workflow: {wf_name}")
        print(f"- ID: {wf_id}")
        print(f"- Published: {published}")
        print(f"- Owner: {owner}")

        # Show workflow steps
        wf_details = gi.workflows.show_workflow(wf_id)
        steps = wf_details.get('steps', {})
        print(f"- Total Steps: {len(steps)}")
        for step_id, step in steps.items():
            print(f"  Step {step_id}: Tool ID: {step.get('tool_id')} | Label: {step.get('label')}")
        print()
