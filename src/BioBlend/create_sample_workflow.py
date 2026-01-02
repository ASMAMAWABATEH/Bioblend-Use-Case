from bioblend.galaxy import GalaxyInstance

# ----------------------------
# CONFIGURATION
# ----------------------------
GALAXY_URL = "http://localhost:8080"
API_KEY = "b8ba458fe9b1c919040db8288c56ed06"  # Replace with your Galaxy API key

# ----------------------------
# FUNCTIONS
# ----------------------------
def get_galaxy_instance():
    """Return a connected GalaxyInstance"""
    return GalaxyInstance(url=GALAXY_URL, key=API_KEY)

def create_workflow(gi, name, annotation="", steps=None):
    """
    Create a simple workflow in Galaxy.
    steps: list of dicts, each dict must have 'tool_id' and 'label'
    """
    if steps is None:
        steps = []

    workflow_dict = {
        "name": name,
        "annotation": annotation,
        "steps": {}
    }

    for idx, step in enumerate(steps):
        tool_id = step["tool_id"]
        label = step.get("label", f"Step {idx}")
        workflow_dict["steps"][str(idx)] = {
            "type": "tool",
            "tool_id": tool_id,
            "tool_version": gi.tools.show_tool(tool_id)["version"],
            "label": label,
            "inputs": {}
        }

    imported_workflow = gi.workflows.import_workflow_dict(workflow_dict)
    return imported_workflow["id"]

def show_workflows(gi):
    """Return list of all workflows"""
    return gi.workflows.get_workflows()


# ----------------------------
# SCRIPT ENTRY
# ----------------------------
if __name__ == "__main__":
    gi = get_galaxy_instance()
    workflow_id = create_workflow(
        gi,
        name="Sample_Workflow",
        annotation="This is a sample workflow created via Bioblend",
        steps=[{"tool_id": "cat1", "label": "Concatenate Step"}]
    )
    print(f"Workflow created with ID: {workflow_id}")

    workflows = show_workflows(gi)
    print("\nCurrent workflows on server:")
    for wf in workflows:
        print(f"- {wf['name']} | ID: {wf['id']} | Published: {wf.get('published', False)}")

    print("\n✅ Workflow creation and verification complete!")
