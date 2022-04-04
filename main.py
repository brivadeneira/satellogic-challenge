import logging
import sys
from ground_station import manage_tasks
from utils.models import Satellite
from utils.utils import build_fake_tasks, config_log

args = sys.argv[1:]

level = args[0] if args and args[0] in ['debug', 'info', 'warn', 'error'] else 'info'

logging.getLogger("faker.factory").setLevel(logging.ERROR)
config_log(level)

if __name__ == "__main__":
    sats = [
        Satellite(name="Milanesat", host="127.0.0.1", port=65432),
        Satellite(name="Hamburguesat", host="127.0.0.1", port=65433),
    ]  # TODO init from .env

    # TODO read tasks (from a json file?)
    # TODO get tasks from a Batch model

    if len(args) > 1:
        try:
            n_tasks = int(args[1]) if args[1]else 3
            n_resources = int(args[2]) if (len(args) > 2 and args[2]) else 3
            max_payoff = int(args[3]) if (len(args) > 3 and args[3]) else 10

            required_tasks = build_fake_tasks(n_tasks, n_resources, max_payoff)
        except ValueError:
            print("ERROR: Parameteters must be int. Default values will be used.")
            required_tasks = build_fake_tasks()
    else:
        required_tasks = build_fake_tasks()

    results = manage_tasks(required_tasks, sats)
