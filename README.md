# Functional (func-y) Task Engine

An extensible asynchronous task execution framework, aimed at supporting functional (e2e) testing.
Allows for modeling of tasks as statemachines, using a delcaritive yaml syntax.
Schedules, executes instructions, applies task state transitions, and reports on task statuses.  Use for:

- Language agnostic tests
- Simple declaritave test configuration, suited for both programmers and non-programmers
- Python core leverages rich python client library ecosystem
- Easily extensible component-based design

## Problem
Writing reliable functional (e2e) tests is hard.  They are notorious for being flaky, time consuming, and difficult 
to maintain because they require:

- multiple protocols
- multiple systems
- waiting (timing)
- asynchronous systems
- complex test logic

func-y task engine aims to separate the task definition, from how it is executed, and how each step of the task is transitioned.  
It should allow for complex multi-step functional (e2e) tests, often involving concurrent operations, to be statically 
defined as a list of state definitions.

## Goals
- Provide Simple Easy Task definition
    - Define tasks as yaml
- Flexible plugins written in python
    - Provide module plugin system which easily allows addition of new service clients
- Various task runners
    - input yaml
    - reports to stdout/junit xml

## Use cases
- Functional/e2e live in service repo along side code
- Test configuration simple enough for QA or non-programmers
- SLA e2e latencies (future API release)


# Getting Started

Right now the easiest way to see how func-y task engine works may be to read the
tutorial.

https://github.com/dm03514/func-y-task-engine/wiki/Tutorial---Creating-a-Task

More in depth documentation to come.
