# async-states-task-engine
An asynchronous task execution framework.  
Allows for modeling of tasks as statemachines, using a delcaritive yaml syntax.
Schedules, executes instructions, applies task state transitions, and reports on task statuses.

## Tasks
- Modeled as a State machine
- Declared as a yaml file
- Declares all states
- Defines legal transitions
- Declares transition conditions
- Define the entry state
- Define execution instructions for each state

## Execution engine (framework)
- Schedules tasks
- Monitors task states
- Checks for condition fulfilment
- Applies transitions 

### State
- Execution engine needs to keep track of multiple tasks being executed, and all potentially may be in different states
- Expose a list of all tasks executing
- Expose each state of each task executing
- Historic results (what retention policy?)

### Conditions
- Wait
- Poll
- Subscribe

### Instructions
- HTTP
- RPC?
- Message?


--------
Tasks are static and will be declared statically as a file.
Tasks scheduling will be exposes as a restful service.
