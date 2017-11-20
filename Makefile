

test-unit:
	nosetests tests.unit

test-functional:
	python bin/funcy-task-engine.py run -t tests/funcy/simple_http_test.yml
	python bin/funcy-task-engine.py run -t tests/funcy/timeout-single-message-streamed.yml
	python bin/funcy-task-engine.py run -t tests/funcy/uuid-nsq-postgres.yml