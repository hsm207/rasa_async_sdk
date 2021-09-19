run-action-server:
	ACTION_SERVER_SANIC_WORKERS=$(threads) python -m rasa_sdk --actions actions

benchmark-action-server:
	python benchmark.py