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
- Each task execution is logged
  - Each state transition in the task is logged

### Conditions
- Wait
- Poll
- Subscribe

### Instructions
- HTTP
- RPC?
- Message?
- DB


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
 

    
