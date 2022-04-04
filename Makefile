all: up_milanesat up_hamburguesat up_groundstation

up_milanesat: satellites/milanesat.py
	cd satellites && python milanesat.py &

up_hamburguesat: satellites/hamburguesat.py
	cd satellites && python hamburguesat.py &

up_groundstation: main.py
	python main.py $(LOG_LEVEL) $(N_TASKS) $(N_RESOURCES) $(MAX_PAYOFF)
