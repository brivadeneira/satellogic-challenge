import pickle
import random
import socket
import time


def solve_tasks(tasks: dict[str, dict]) -> dict[str, list[str]]:
    """
    Simulates the process of solving tasks (10% of times a task will fail)
    :param tasks: (dict) to solve
    :return: (dict) with the result of solving tasks as completed and not_completed
    """
    tasks_results = {"completed": [], "not_completed": []}
    for task in [task for task in set().union(*(d.keys() for d in tasks))]:
        if random.random() < 0.1:
            tasks_results["not_completed"].append(task)
        else:
            tasks_results["completed"].append(task)
    return tasks_results


def listen_for_tasks(host: str, port: int) -> None:
    """
    Runs a socket server that listens for entry tasks
    and sends the results of solving those tasks back
    :param host: (str) to listen
    :param port: (int) to listen
    :return: None
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            conn, addr = s.accept()

            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    tasks = pickle.loads(data)
                    time.sleep(random.randint(0, 5))
                    task_results = solve_tasks(tasks)
                    conn.sendall(pickle.dumps(task_results))

    except socket.error:
        pass

