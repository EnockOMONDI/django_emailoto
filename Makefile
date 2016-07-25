test:
	export REDIS_HOST='localhost' && \
	export REDIS_PORT=6379 && \
	export REDIS_DB=2 && \
	python runtests.py