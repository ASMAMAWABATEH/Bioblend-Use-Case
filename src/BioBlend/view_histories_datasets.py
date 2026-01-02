from bioblend.galaxy import GalaxyInstance

# --------------------------------------------------------------
# Configuration
# --------------------------------------------------------------
GALAXY_URL = "http://localhost:8080"
API_KEY = "b8ba458fe9b1c919040db8288c56ed06"
# --------------------------------------------------------------

def main():
    gi = GalaxyInstance(GALAXY_URL, API_KEY)

    print("Fetching histories...")
    histories = gi.histories.get_histories()

    if not histories:
        print("No histories found.")
        return

    print(f"Found {len(histories)} histories.\n")

    for h in histories:
        history_id = h["id"]
        history_name = h["name"]

        print(f"History: {history_name}")
        print(f"ID: {history_id}")

        # Fetch datasets inside this history
        datasets = gi.histories.show_history(history_id, contents=True)

        if not datasets:
            print("  No datasets in this history.\n")
            continue

        print("  Datasets:")
        for d in datasets:
            name = d["name"]
            ds_id = d["id"]
            state = d["state"]
            dtype = d["history_content_type"]

            print(f"    - {name} | {ds_id} | state={state} | type={dtype}")
        print("")  # blank line for spacing


if __name__ == "__main__":
    main()
