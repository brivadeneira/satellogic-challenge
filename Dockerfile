FROM python:3.9

COPY . /
RUN pip3 install -r requirements.txt --no-cache-dir
RUN pip3 install -r requirements_test.txt --no-cache-dir

ENV LEVEL, TASKS, RESOURCES, PAYOFF

CMD ["python", "-m", "pytest", "-vv", "tests/"]
CMD ["make", "all", "LOG_LEVEL=${LEVEL}", "N_TASKS=${TASKS}", "N_RESOURCES=${RESOURCES}", "MAX_PAYOFF=${PAYOFF}"]
