# BioBlend/view_workflows.py
from bioblend.galaxy import GalaxyInstance

GALAXY_URL = "http://localhost:8080"
API_KEY = "b8ba458fe9b1c919040db8288c56ed06"

def get_galaxy_instance(url=GALAXY_URL, key=API_KEY):
    """Create and return a GalaxyInstance"""
    return GalaxyInstance(url=url, key=key)

def list_workflows(gi):
    """Return structured list of workflows"""
    workflows = gi.workflows.get_workflows()
    result = []
    for wf in workflows:
        wf_details = gi.workflows.show_workflow(wf['id'])
        result.append({
            'id': wf['id'],
            'name': wf['name'],
            'published': wf.get('published', False),
            'owner': wf.get('owner', 'N/A'),
            'steps': wf_details.get('steps', {})
        })
    return result

def main():
    """Main execution function"""
    gi = get_galaxy_instance()
    workflows = list_workflows(gi)
    for wf in workflows:
        print(f"Workflow: {wf['name']}")
        print(f"Published: {wf['published']}, Owner: {wf['owner']}")
        print(f"Steps: {list(wf['steps'].keys())}")
        print("-" * 40)

if __name__ == "__main__":
    main()
