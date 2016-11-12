package tasks

import (
	"github.com/dm03514/async-states-task-engine/usertasks"
	"github.com/dm03514/async-states-task-engine/task"
	"sync"
	"fmt"
)


type Tasks struct {
	activeTasks map[string]task.ITask
	Events chan *task.TaskEvent
	mu *sync.Mutex
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
	ts.mu.Lock()
	go task.Start()
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


func Init() *Tasks {
	return &Tasks{
		activeTasks: make(map[string]task.ITask),
		Events:      make(chan *task.TaskEvent),
		mu:          &sync.Mutex{},
	}
}
