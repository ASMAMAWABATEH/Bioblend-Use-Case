# BioBlend/invoke_workflow.py
import time

def find_workflow(gi, name):
    """
    Find a workflow by name and return its ID.
    """
    for wf in gi.workflows.get_workflows():
        if wf['name'] == name:
            return wf['id']
    return None

def invoke_workflow(gi, workflow_id, history_id, dataset_id, max_wait=300, interval=5):
    """
    Invoke a workflow on a history with a dataset input and wait for completion.
    
    Args:
        gi: GalaxyInstance object
        workflow_id: str, ID of workflow to run
        history_id: str, ID of history to use
        dataset_id: str, ID of input dataset
        max_wait: int, max seconds to wait for workflow completion
        interval: int, polling interval in seconds

    Returns:
        tuple: (invocation_id, state)
    """
    # Start workflow invocation
    run = gi.workflows.invoke_workflow(
        workflow_id=workflow_id,
        history_id=history_id,
        inputs={"0": {"id": dataset_id}}
    )
    invocation_id = run['id']

    elapsed = 0
    while True:
        invocation = gi.workflows.show_invocation(workflow_id, invocation_id)
        state = invocation['state']

        if state in ['ok', 'error', 'failed']:
            break

        time.sleep(interval)
        elapsed += interval
        if elapsed >= max_wait:
            state = "timeout"
            break

    return invocation_id, state
