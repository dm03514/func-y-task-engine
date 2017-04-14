# Functional (funcy) Task Engine

An asynchronous task execution framework.  
Allows for modeling of tasks as statemachines, using a delcaritive yaml syntax.
Schedules, executes instructions, applies task state transitions, and reports on task statuses.

## Problem
Writing reliable function tests are hard.  They often involve multiple protocols, multiple systems, waiting, and asyncronous systems.
funcy aims to separate the task definition, from how it is executed, and how each step of the task is transitioned.  It should allow for complex multi-step functional tests, often involving concurrent opertations, to be statically defined as a list of state definitions.

## Goals
- Provide Simple Easy Task definition
- Provide module plugin system which easily allows addition of new service clients
- Auditable
