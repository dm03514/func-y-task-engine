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

## Components

### Tasks
- Modeled as a State machine
- Declared as a yaml file
- Declares all states (events)
- Declares transition (fulfillment) conditions
- Define execution instructions for each state

### Execution engine (framework)
- Schedules tasks
- Monitors task states
- Checks for condition fulfilment
- Applies transitions
- Execution engine needs to potentially keep track of multiple tasks being executed, and all potentially may be in different states
- Provides both programmatic and visual interfaces to schedule, run, monitor, and report on tasks

### State (Event)
- Tasks are FSM
- Expose each state of each task executing
- Each task execution is logged

#### Execution Strategy
- Wait
- Poll
- Subscribe

#### Transition Conditions

#### Instructions
- HTTP
- RPC?
- Message?
- DB


## old alpha alpha thoughts
--------
--------
Tasks are static and will be declared statically as a file.
Tasks scheduling will be exposes as a restful service.


Each task is modeled as a state machine:

https://github.com/looplab/fsm


Task
  - version
  - start_state
  - final_state
  - state1
    - instructions
      - instruction 1
      - instruction 2
  - state2
    - instructions
      - instruction 1
    - transition_condition
  - end state
  - max_global_transition_timeout
  
  
Framework:
  - Input
    - Task struct
  - Spawns a main goroutine for each new task
  - Creates a main_task_channel that will be passed to all sub go routines
  - Inspects task for initial state, assigned to next_state
  - main_loop: Task is put into next_state
    - Check if state is final_state
    - Valid transfer states are identified 
    - State instructions are executed
    - Transition timeout is set
    - Each dependent state transition_condition is started in a goroutine, passed main_task_channel
    - When a condition is fufilled or failed
      - results is sent back to main task routine
      - main task routine cancels all running tasks
      - applies next_state
  - transition_timeout
    - reset per transition
    - when reached:
      - task is marked as failure
      - all goroutines are stopped
      - task metrics are logged
 

    
