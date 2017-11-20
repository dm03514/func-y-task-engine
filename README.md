# Functional (pronounced funky) Task Engine

An extensible asynchronous task execution framework, aimed at supporting functional/acceptance (e2e) testing.
Func-y allows for modeling of tasks as statemachines, using a delcaritive yaml syntax.
Func-y then schedules, executes instructions, applies task state transitions, and reports on task statuses.  Func-y is a great use for:

- Language agnostic tests
- Simple declaritave test configuration, suited for both programmers and non-programmers
- Extensible shared test framework: A python core allows for leveraging of rich python client library ecosystem
- Easily extensible component-based design

Func-y helps to accelerate you and your team by enforcing a strict seperation of test code and service code.  It removes manual effort by having "batteries-included" for the most popular protocols and services, and allowing easy extension, through a flexible plugin system written in python.

Writing tests in func-y is amazingly fast after learning the test executing flow and toolkit.  It enables reliable standardized and uniform tests which can be written in minutes.  Enables tests to be written in the same framework regardless of service language.  Func-y is a powerful test framework which benefits from a composable, extensible, component based approach.  Effort to extending the framework is minimal and then accessible by all service teams independent of service language.

Functional Tests shouldn't have logic, they should have states.  Let func-y transition your tests through those states and worry about the concurrency, allowing you to focus on what your service does, and not the test infrastructure.

## Problem
Writing reliable functional/acceptance (e2e) tests is hard.  They are notorious for being flaky, time consuming, and difficult 
to maintain because they require:

- multiple protocols
- multiple systems
- waiting (timing)
- asynchronous systems
- complex test logic

func-y task engine aims to separate the task definition, from how it is executed, and how each step of the task is transitioned.  
It should allow for complex multi-step functional/acceptance (e2e) tests, often involving concurrent operations, to be statically 
defined as a list of state definitions.

## Goals
- Provide Simple Easy Task definition
    - Define tasks as yaml
- Flexible plugins written in python
    - Provide module plugin system which easily allows addition of new service clients
- Various task runners
    - input yaml
    - reports to stdout/junit xml
- Reduces test related flakiness due to concurrency, and false positives related to timing by taking a concurrency first approach to state transitions
    
    
## Use cases
- Functional/Acceptance (e2e) tests live in service repo along side code
- Asynchronous service testing
    - consider many functional tests have test like
    - ```
    do_something()
    sleep(10)
    make_assertions()
    ```
    - Funcy solves these timeing related failures by providing primitives for polling or asyncrhonously registering event listeners and performing an action only after events occur
- Test configuration simple enough for QA or non-programmers
- SLA e2e latencies (future API release)


# Getting Started

Right now the easiest way to see how func-y task engine works may be to read the
tutorial.

https://github.com/dm03514/func-y-task-engine/wiki/Tutorial---Creating-a-Task

More in depth documentation to come.
