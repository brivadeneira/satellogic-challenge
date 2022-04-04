from pydantic import BaseModel


class Satellite(BaseModel):
    """
    Creates a satellite to assign it tasks from the ground station
    """

    name: str
    host: str
    port: int
    busy_resources: list[int] = []
    assigned_tasks: list[dict] = []


# class Task(BaseModel):
#     """
#     Creates a new single task to be managed by the earth station
#     """
#
#     name: str
#     resources: list[int]
#     payoff: float
#
#
# class Batch(BaseModel):
#     """
#     Creates a batch of tasks stored into a dict
#     to be processed at the same time by the earth station
#     """
#     tasks: list[Task]
