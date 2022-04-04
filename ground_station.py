import pickle
import socket

from utils.models import Satellite
from utils.optimazer import get_best_task_combination
from utils.utils import log


def send_tasks(sat_name: str, tasks: list[dict],
               host: str, port: int) -> dict[str, list[str]]:
    """
    Sends tasks to every single satellite via a socket connection
    :param sat_name: (str) name of sat to send tasks
    :param tasks: (list) with tasks to send
    :param host: (str) of sat socket connection
    :param port: (int) of sat socket connection
    :return: (dict) with the result according to sat response
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        msg = f"Trying to connect with {sat_name} in {host}:{port}"
        log(msg, 'info')

        try:
            s.connect((host, port))
            msg = f"Connection established with {sat_name} in {host}:{port}"
            log(msg, 'info')
        except socket.error as exception:
            msg = f"Can not connect with {sat_name} in {host}:{port}: {exception}"
            log(msg, 'error')

            tasks_results = {"not_completed": [name for name in set().union(*(d.keys() for d in tasks))]}
            return tasks_results

        msg = f"Sending {', '.join(set().union(*(d.keys() for d in tasks)))} task(s) to {sat_name} in {host}:{port}"
        log(msg, 'info')

        s.sendall(pickle.dumps([task for task in tasks]))
        data = s.recv(1024)

        if not data:
            msg = f"No data received from {sat_name} in {host}:{port}"
            log(msg, 'error')

            tasks_results = {"not_completed": [name for name in set().union(*(d.keys() for d in tasks))]}
            return tasks_results

        tasks_results = pickle.loads(data)

        if tasks_results["completed"]:
            msg = f"{sat_name} has completed {', '.join([task for task in tasks_results['completed']])} task(s) "
            log(msg)

        if tasks_results["not_completed"]:
            msg = f"{sat_name} has not completed " \
                  f"{', '.join([task for task in tasks_results['not_completed']])} task(s) "
            log(msg, 'warn')

    return pickle.loads(data)


def manage_tasks(tasks: dict[str, dict], sats: list[Satellite]) -> dict[str, list]:
    """
    Manages tasks to assign according to the combination that optimize the payoff
    :param tasks: (dict) of tasks with names as keys, resources and payoff as values
    :param sats: (Satellite) to assign tasks
    :return: the results after distribute, assign and send tasks
    """
    tasks_results = {"unallocated": [], "completed": [], "not_completed": []}
    msg = f"{', '.join(task for task in tasks)} task(s) to manage"
    log(msg, 'info')

    for task in tasks:
        msg = f"{task} task has a payoff of {tasks[task]['payoff']} and needs {' and '.join([str(r) for r in tasks[task]['resources']])} resources"
        log(msg)

    tasks_to_assign, total_payoff = get_best_task_combination(tasks)

    if not tasks_to_assign:
        msg = "There is no a possible combination to assign the tasks."
        log(msg, 'error')

        tasks_results["not_completed"] = [task for task in tasks]
        return tasks_results

    msg = f"{', '.join([name for group in tasks_to_assign for name in group])} " \
          f"task(s) will be assign making a total of {total_payoff} payoff"
    log(msg)

    tasks_results["unallocated"] = list(
        set([task for task in tasks]).difference(
            set([name for group in tasks_to_assign for name in group])
        )
    )

    msg = f"{', '.join([name for name in tasks_results['unallocated']])} task(s) wont be assigned"
    log(msg)

    # assign tasks
    for i, sat in enumerate(sats):
        sat.assigned_tasks.append({task: tasks[task] for task in tasks_to_assign[i]})
        sat_report = send_tasks(sat.name, sat.assigned_tasks, sat.host, sat.port)
        for k in sat_report:
            tasks_results[k].extend(
                [task for task in sat_report[k]]
            )

    msg = f"{', '.join(tasks_results['completed'])} task(s) has been completed"
    log(msg, 'info')

    if tasks_results["not_completed"]:
        msg = f"{', '.join(tasks_results['not_completed'])} task(s) has not been completed"
        log(msg, 'error')

    msg = f"{', '.join(tasks_results['unallocated'])} task(s) has not been allocated as a result of payoff optimization"
    log(msg, 'warn')

    return tasks_results
