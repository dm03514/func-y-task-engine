package tasks

import (
	"encoding/json"
	"fmt"
	"github.com/dm03514/async-states-task-engine/task"
	"github.com/dm03514/async-states-task-engine/usertasks"
	"sync"
)

type Tasks struct {
	activeTasks map[string]task.ITask
	Events      chan *task.TaskEvent
	Done        chan string
	mu          *sync.Mutex
}

func (ts *Tasks) String() string {
	e, err := json.Marshal(ts.activeTasks)
	if err != nil {
		panic(err)
	}
	return string(e)
}

func (ts *Tasks) Task(taskname string) task.ITask {
	var t task.ITask

	switch taskname {
	case "DoubleSearchTask":
		t = usertasks.NewDoubleSearchTask(ts.Events)
	case "TripleTimeoutTask":
		t = usertasks.NewTripleTimeoutTask(ts.Events)
	default:
		panic(fmt.Sprintf("no task named: %s", taskname))
	}
	return t
}

func (ts *Tasks) Start(taskname string) string {
	task := ts.Task(taskname)
	go task.Run(ts.Done)

	ts.mu.Lock()
	ts.activeTasks[task.IdString()] = task
	ts.mu.Unlock()

	return task.IdString()
}

func (ts *Tasks) State(taskId string) (string, bool) {
	ts.mu.Lock()
	defer ts.mu.Unlock()
	task, ok := ts.activeTasks[taskId]
	if !ok {
		return "", ok
	}
	return task.CurrentState(), ok
}

func (ts *Tasks) consumeDone() {
	for id := range ts.Done {
		ts.mu.Lock()
		delete(ts.activeTasks, id)
		ts.mu.Unlock()
	}
}

// Instantiates tasks and starts the finished task consume, in a new
// go routine
func Init() *Tasks {
	ts := &Tasks{
		activeTasks: make(map[string]task.ITask),
		Events:      make(chan *task.TaskEvent),
		Done:        make(chan string),
		mu:          &sync.Mutex{},
	}
	go ts.consumeDone()
	return ts
}
