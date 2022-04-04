import pytest
from utils.optimazer import *


@pytest.fixture
def tasks_to_assign() -> dict[str, dict]:
    """
    Builds a dict of fake tasks for testing proposes
    :return: (dict) of fake tasks
    """
    return {
        "service": {"resources": [1, 2], "payoff": 1.19},
        "tax": {"resources": [5, 1], "payoff": 2.9},
        "change": {"resources": [1, 2], "payoff": 9.67},
        "until": {"resources": [5, 1], "payoff": 9.09},
        "energy": {"resources": [4, 2], "payoff": 5.38},
    }


@pytest.fixture
def tasks_resources(tasks_to_assign) -> dict[str, list[int]]:
    return {task: tasks_to_assign[task]["resources"] for task in tasks_to_assign}


@pytest.fixture
def tasks_payoff(tasks_to_assign) -> dict[str, float]:
    return {name: tasks_to_assign[name]["payoff"] for name in tasks_to_assign}


@pytest.fixture
def all_combinations() -> list[list]:
    return [
        [["service"], ["tax"]],
        [["service"], ["tax", "change"]],
        [["service"], ["change"]],
        [["service"], ["tax", "change", "until"]],
        [["service"], ["change", "until"]],
        [["service"], ["tax", "until"]],
        [["service"], ["until"]],
        [["service", "tax"], ["change"]],
        [["tax"], ["service", "change"]],
        [["tax"], ["change"]],
        [["service", "tax"], ["change", "until"]],
        [["tax"], ["service", "change", "until"]],
        [["tax"], ["change", "until"]],
        [["service", "tax"], ["until"]],
        [["tax"], ["service", "until"]],
        [["tax"], ["until"]],
        [["service", "tax", "change"], ["until"]],
        [["tax", "change"], ["service", "until"]],
        [["tax", "change"], ["until"]],
        [["service", "change"], ["tax", "until"]],
        [["change"], ["service", "tax", "until"]],
        [["change"], ["tax", "until"]],
        [["service", "change"], ["until"]],
        [["change"], ["service", "until"]],
        [["change"], ["until"]],
    ]


def test_get_all_tasks_combinations(tasks_to_assign, all_combinations):
    """
    Test get_all_tasks_combination function
    :param tasks_to_assign: (dict) a clean one for test proposes
    :param all_combinations: (list) expected combinations of tasks
    :return: None
    """
    assert get_all_combinations([task for task in tasks_to_assign]) == all_combinations


@pytest.fixture
def task_resources(tasks_to_assign) -> dict[list]:
    """
    dict with task names as keys and resources required as values
    :return: (dict)
    """
    return {task: tasks_to_assign[task]["resources"] for task in tasks_to_assign}


@pytest.fixture
def task_payoff(tasks_to_assign) -> dict[list]:
    """
    dict with task names as keys and payoff as values
    :return: (dict)
    """
    return {name: tasks_to_assign[name]["payoff"] for name in tasks_to_assign}


@pytest.fixture
def possible_combinations() -> list[list]:
    """
    LIst of possible combinations, a clean one for testing proposes
    :return: (list)
    """
    return [
        [["service"], ["tax"]],
        [["service"], ["change"]],
        [["service"], ["until"]],
        [["tax"], ["change"]],
        [["tax"], ["until"]],
        [["change"], ["until"]],
    ]


def test_get_possible_combinations(
    all_combinations, task_resources, possible_combinations
):
    """
    Test get_possible_task_combinations function
    :param all_combinations: (list) expected combinations of tasks
    :param task_resources: (dict) a clean one for test proposes
    :return: None
    """
    assert (
        get_possible_combinations(all_combinations, task_resources)
        == possible_combinations
    )


@pytest.fixture
def expected_best_combination() -> tuple[list[list[str]], float]:
    """
    LIst of best combinations, a clean one for testing proposes
    :return: (list)
    """
    return [["change"], ["until"]], 18.76


def test_get_best_combination(
    tasks_to_assign: dict[str, dict], expected_best_combination: tuple[list, float]
):
    """
    Test get_best_combination function
    :param tasks_to_assign: (dict) a clean one for test proposes
    :param expected_best_combination: (tuple) with the best combination result and total payoff
    :return:
    """
    assert get_best_task_combination(tasks_to_assign) == expected_best_combination
