

start-functional-stack:
	docker-compose down
	docker-compose up -d
	./bin/wait-for-it.sh localhost:5432

test-unit:
	nosetests tests.unit

test-functional:
	python bin/funcy-task-engine.py run -t tests/funcy/simple-http-test.yml
	python bin/funcy-task-engine.py run -t tests/funcy/timeout-single-message-streamed.yml
	python bin/funcy-task-engine.py run -t tests/funcy/uuid-nsq-postgres.yml
	TEST_NSQ_SUBPROCESS_PUBLISH_EXECUTABLE="`pwd`/bin/test-nsq-publish.py" python bin/funcy-task-engine.py run -t tests/funcy/subprocess-nsq-transformations-dict-assertion.yml
	TEST_NSQ_SUBPROCESS_PUBLISH_EXECUTABLE="`pwd`/bin/test-nsq-publish.py" python ./bin/funcy-task-engine.py xmltest -c tests/fixtures/functional-suite.yml