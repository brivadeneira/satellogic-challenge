from typing import Dict

from more_itertools import set_partitions


def get_all_tasks_combinations(task_names: list[str], n_sat: int = 2) -> list[list[list[str]]]:
    """
    Returns all possible combination of tasks in 'n_sat' groups
    including 'no tasks' which allows a full assignation of tasks
    :param task_names: (list[str]) all tasks names to assign
    :param n_sat: (int) number of satellites that will receive the tasks, default value: 3
    :return: (list) with all possible combination of tasks for `n_sat` groups
                    (without taken care of resources or payoff at all)
    """
    return [
        combinations[0:2] for combinations in set_partitions(task_names, k=n_sat + 1)
    ]


def get_possible_task_combinations(tasks_list: list[list[list[str]]],
                                   tasks_resources: Dict[str, dict]) -> list[list[list[str]]]:
    """
    Returns the combination of tasks that is possible according to the resources uses
    :param tasks_list: (list) with all possible combination of name tasks in 'n_sat' groups, including 'no tasks'
    :param tasks_resources: (dict) like {"<task_name>": {"resources": [<res_num>, <res_num>],
                                         "<task_name_2>": {"resources": [<res_num>, <res_num>],
                                           ... }
    :return: (list) of list with combinations of tasks grouped by 'n_sat'
    """
    possible_combinations = []
    possible = True

    for combinations in tasks_list:
        for combination in combinations[0:2]:
            possible = True
            all_resources = []
            for task in combination:
                try:
                    all_resources.extend([r for r in tasks_resources[task]])
                except KeyError:
                    pass
            all_resources.sort()
            if all_resources != list(set(all_resources)):
                possible = False
                break
        if possible:
            possible_combinations.append(combinations)

    return possible_combinations


def get_best_task_combinations(tasks_to_assign: dict[str, dict]) -> tuple[list[list[str]], float]:
    """
    Returns the best way to assign tasks in groups optimising their payoff
    :param tasks_to_assign: (dict) like {'<task_name>': {'resources': [<res_1>, <res_2>], 'payoff': <payoff>},
                                        ... }
    :return: (tuple) with a list of 'n_sat' lists that contains the best combinations of tasks to be assigned
    like (['<task_1>', '<task_3>'], ['<task_2>', '<task_4>', '<task_5>']) and the total_payoff reported
    for that combination
    """
    # build some structures from tasks dict
    list_tasks = list(tasks_to_assign)
    tasks_resources = {
        task: tasks_to_assign[task]["resources"] for task in tasks_to_assign
    }
    tasks_payoff = {name: tasks_to_assign[name]["payoff"] for name in tasks_to_assign}

    all_task_combinations = get_all_tasks_combinations(list_tasks)
    possible_combinations = get_possible_task_combinations(
        all_task_combinations, tasks_resources
    )

    combination_payoff = {}

    for combination in possible_combinations:
        total_payoff = 0
        for pair in combination:
            total_payoff += sum([tasks_payoff[task] for task in pair])
        combination_payoff[round(total_payoff, 2)] = combination

    best_combination = sorted(combination_payoff.items(), reverse=True)[0][1]
    accumulated_payoff = sorted(combination_payoff.items(), reverse=True)[0][0]

    return best_combination, accumulated_payoff
