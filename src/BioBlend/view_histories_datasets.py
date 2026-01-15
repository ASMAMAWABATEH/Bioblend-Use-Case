# BioBlend/view_histories_datasets.py
from bioblend.galaxy import GalaxyInstance

GALAXY_URL = "http://localhost:8080"
API_KEY = "b8ba458fe9b1c919040db8288c56ed06"

# =========================
# Core Logic (testable)
# =========================
def get_galaxy_instance(url=GALAXY_URL, key=API_KEY):
    """Return a GalaxyInstance"""
    return GalaxyInstance(url=url, key=key)

def fetch_histories(gi):
    """
    Return structured list of histories and their datasets
    """
    histories = gi.histories.get_histories()
    result = []
    for h in histories:
        history_id = h['id']
        contents = gi.histories.show_history(history_id, contents=True)
        datasets = [
            {
                'id': d['id'],
                'name': d['name'],
                'state': d['state'],
                'deleted': d.get('deleted', False)
            } for d in contents
        ]
        result.append({
            'id': history_id,
            'name': h['name'],
            'state': h['state'],
            'datasets': datasets
        })
    return result

def format_histories_output(histories):
    """
    Return a list of strings representing histories and datasets
    """
    output_lines = []
    for h in histories:
        output_lines.append(f"History: {h['name']} | State: {h['state']}")
        if h['datasets']:
            for d in h['datasets']:
                output_lines.append(f"  Dataset: {d['name']} | State: {d['state']} | Deleted: {d['deleted']}")
        else:
            output_lines.append("  No datasets")
        output_lines.append("-" * 40)
    return output_lines

# =========================
# CLI / main wrapper
# =========================
def main():
    gi = get_galaxy_instance()
    histories = fetch_histories(gi)
    for line in format_histories_output(histories):
        print(line)

if __name__ == "__main__":
    main()
