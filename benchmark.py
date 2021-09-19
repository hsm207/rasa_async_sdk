import logging
import time
from multiprocessing import cpu_count

import ray
import requests
from ray.worker import remote

logging.basicConfig(
    format="%(asctime)s %(message)s", datefmt="%Y-%m-%d %I:%M:%S %p", level=logging.INFO
)
logger = logging.getLogger(__name__)

N_CPU = cpu_count()
ACTION_SERVER_ENDPOINT = "http://localhost:5055/webhook"


def build_payload(next_action="action_hello_world", sender_id="test_user"):
    return {
        "next_action": next_action,
        "tracker": {
            "sender_id": sender_id,
            "slots": {"name": "John"},
            "latest_message": {
                "entities": [],
                "intent": {"confidence": 0.6323, "name": "greet"},
                "intent_ranking": [{"confidence": 0.6323, "name": "greet"}],
                "text": "Hello!",
            },
            "latest_event_time": 1537645578.314389,
            "followup_action": "string",
            "paused": False,
            "events": [{"event": "slot", "timestamp": 1559744410}],
            "latest_input_channel": "rest",
            "latest_action_name": "action_listen",
            "latest_action": {"action_name": "string", "action_text": "string"},
            "active_loop": {"name": "restaurant_form"},
        },
        "domain": {
            "config": {"store_entities_as_slots": False},
            "intents": [
                {
                    "property1": {"use_entities": True},
                    "property2": {"use_entities": True},
                }
            ],
            "entities": ["person", "location"],
            "slots": {
                "property1": {
                    "auto_fill": True,
                    "initial_value": "string",
                    "type": "string",
                    "values": ["string"],
                },
                "property2": {
                    "auto_fill": True,
                    "initial_value": "string",
                    "type": "string",
                    "values": ["string"],
                },
            },
            "responses": {
                "property1": [{"text": "string"}],
                "property2": [{"text": "string"}],
            },
            "actions": ["action_greet", "action_goodbye", "action_listen"],
        },
        "version": "2.8.6",
    }


logging.info(f"Found {N_CPU} cores")

ray.init(num_cpus=N_CPU)


@ray.remote
def request_action(action_name, sender_id):
    payload = build_payload(action_name, sender_id=sender_id)
    r = requests.post(ACTION_SERVER_ENDPOINT, json=payload)

    return r.status_code


def benchmark(action_name):
    print(f"Benchmarking calls to {action_name} ...")
    start_time = time.perf_counter()

    results = []
    for i in range(N_CPU):
        sender_id = f"user_{i+1}"
        results.append(request_action.remote(action_name, sender_id))

    results = ray.get(results)

    elapsed_time = time.perf_counter() - start_time

    print(f"{N_CPU} calls finished executing in {elapsed_time:.2f} seconds\n")


if __name__ == "__main__":
    benchmark("action_long_backend_call_sync")
    benchmark("action_long_backend_call_async")
