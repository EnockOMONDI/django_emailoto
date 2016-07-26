test:
	export EMAILOTO_REDIS_HOST='localhost' && \
	export EMAILOTO_REDIS_PORT=6379 && \
	export EMAILOTO_REDIS_DB=2 && \
	python runtests.py