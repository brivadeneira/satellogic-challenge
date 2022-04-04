import logging
import random
from datetime import datetime
from typing import Dict

from faker import Faker

fake = Faker(locale="en")


def config_log(level: str = 'info') -> None:
    """
    Set the logging level config
    :param level: (str) 'debug', 'info', 'warn' or 'error'
    :return: None
    """
    if level == 'debug':
        logging.basicConfig(level=logging.DEBUG)

    if level == 'info':
        logging.basicConfig(level=logging.INFO)

    if level == 'warn':
        logging.basicConfig(level=logging.WARN)

    if level == 'error':
        logging.basicConfig(level=logging.ERROR)


def log(msg: str, level: str = 'debug') -> None:
    """
    Log a given message in a given level
    :param msg: to log
    :param level: 'debug', 'info', 'warn', or 'error'
    :return:
    """
    if level == 'debug':
        logging.debug(
            f"{datetime.now()}:from ground station:{msg}"
        )
    if level == 'info':
        logging.info(
            f"{datetime.now()}:from ground station:{msg}"
        )
    if level == 'warn':
        logging.warn(
            f"{datetime.now()}:from ground station:{msg}"
        )
    if level == 'error':
        logging.error(
            f"{datetime.now()}:from ground station:{msg}"
        )


def build_fake_tasks(n_tasks: int = 3, n_resources: int = 3,
                     max_payoff: float = 10) -> Dict[str, dict]:
    """
    Builds some fake tasks for satellites
    :param n_tasks: (int) number of fake tasks to build, default value: 3
    :param n_resources: (int) stop number for range of resources
    :param max_payoff: (float) maximum value of payoff that a single task can take
    :return: (dict) of fake tasks like
    { "<fake_task_name>": {"resources": [<res_num>, <res_num>], "payoff": <task_payoff>},
      "<fake_task_name_2>": {"resources": [<res_num>, <res_num>], "payoff": <task_payoff>}, ... }
    """
    fake_tasks = {}

    for word in fake.words(n_tasks):
        first_resource = random.randint(1, n_resources)
        second_resource = random.randint(1, n_resources)
        while first_resource == second_resource:
            second_resource = random.randint(1, n_resources)

        fake_tasks[word] = {
            "resources": [first_resource, second_resource],
            "payoff": round(random.uniform(1, max_payoff), 2),
        }
    return fake_tasks
