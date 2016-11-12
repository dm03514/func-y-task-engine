package main

import (
	"log"
	"net/http"
	"github.com/dm03514/async-states-task-engine/task"
	"github.com/dm03514/async-states-task-engine/usertasks"
	"fmt"
	"sync"
)


type TaskFrameworkServer struct {
	activeTasks map[string]task.ITask
	events chan *task.TaskEvent
}


func (tfs *TaskFrameworkServer) Serve() {
	// fmt.Printf("Server listening :8080\n")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func (tfs *TaskFrameworkServer) runTask(w http.ResponseWriter, r *http.Request) {
	var mu = &sync.Mutex{}

	taskname := r.URL.Query().Get("taskname")
	if taskname == "" {
		fmt.Printf("Server: Taskname not present\n")
		return
	}
	// create a uuid update the
	task := tfs.getTask(taskname)

	mu.Lock()
	go task.Start()
	tfs.activeTasks[task.IdString()] = task
	mu.Unlock()

	fmt.Fprintf(w, "%s\n", task.IdString())
}

func (tfs *TaskFrameworkServer) status(w http.ResponseWriter, r *http.Request) {
	var mu = &sync.Mutex{}
	taskId := r.URL.Query().Get("taskId")

	mu.Lock()
	defer mu.Unlock()

	task, ok := tfs.activeTasks[taskId]
	if !ok {
		fmt.Fprintf(w, "Task %v not found", task)
		return
	}
	fmt.Fprintf(w, "%s\n", task.CurrentState())
}

func (tfs *TaskFrameworkServer) getTask(taskname string) task.ITask {
	// fmt.Printf("getTask(\"%s\")\n", taskname)
	var t task.ITask

	switch taskname {
	case "DoubleSearchTask":
		t = usertasks.NewDoubleSearchTask(tfs.events)
	case "TripleTimeoutTask":
		t = usertasks.NewTripleTimeoutTask(tfs.events)
	}
	// fmt.Printf("Instantiated task %+v\n", t)
	return t
}

func NewServer() *TaskFrameworkServer {
	tfs := &TaskFrameworkServer{
		activeTasks: make(map[string]task.ITask),
		events: make(chan *task.TaskEvent),
	}
	http.HandleFunc("/runtask", tfs.runTask)
	http.HandleFunc("/status", tfs.status)
	return tfs
}

