# src/BioBlend/export_import_workflow.py
from bioblend.galaxy import GalaxyInstance
import json
import os

# ----------------------------
# CONFIGURATION
# ----------------------------
GALAXY_URL = "http://localhost:8080"
API_KEY = "b8ba458fe9b1c919040db8288c56ed06"  # Replace with your Galaxy API key
EXPORT_DIR = "exported_workflows"              # Directory to save exported workflows

# ----------------------------
# GALAXY CONNECTION
# ----------------------------
def get_galaxy_instance():
    """Return a GalaxyInstance connection."""
    return GalaxyInstance(url=GALAXY_URL, key=API_KEY)

# ----------------------------
# EXPORT WORKFLOW
# ----------------------------
def export_workflow(gi, workflow_id, output_dir=EXPORT_DIR):
    """
    Export a Galaxy workflow to a JSON file.
    """
    workflow = gi.workflows.export_workflow_dict(workflow_id)
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{workflow['name']}.ga")
    with open(file_path, "w") as f:
        json.dump(workflow, f, indent=4)
    return file_path

# ----------------------------
# IMPORT WORKFLOW
# ----------------------------
def import_workflow(gi, workflow_file):
    """
    Import a workflow from a JSON (.ga) file into Galaxy.
    """
    if not os.path.exists(workflow_file):
        raise FileNotFoundError(f"Workflow file not found: {workflow_file}")

    with open(workflow_file, "r") as f:
        workflow_dict = json.load(f)

    imported = gi.workflows.import_workflow_dict(workflow_dict)
    return imported["id"]

# ----------------------------
# SHOW WORKFLOWS
# ----------------------------
def show_workflows(gi):
    """Return all workflows on the server."""
    return gi.workflows.get_workflows()

# ----------------------------
# MAIN FUNCTION
# ----------------------------
def main():
    gi = get_galaxy_instance()
    print("Connected to Galaxy.")

    workflows = show_workflows(gi)
    if not workflows:
        print("No workflows available to export.")
        return

    workflow_id = workflows[0]["id"]
    print(f"Exporting workflow: {workflows[0]['name']}")
    exported_file = export_workflow(gi, workflow_id)
    print(f"Workflow exported to: {exported_file}")

    print("Importing workflow back into Galaxy...")
    imported_id = import_workflow(gi, exported_file)
    print(f"Workflow imported successfully with ID: {imported_id}")

    print("All workflows on the server:")
    for wf in show_workflows(gi):
        print(f"- {wf['name']} | ID: {wf['id']}")

    print("Done ✅")

if __name__ == "__main__":
    main()
