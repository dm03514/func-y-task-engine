package main

import (
	"fmt"
	"github.com/dm03514/async-states-task-engine/tasks"
	"log"
	"net/http"
)

type TaskFrameworkServer struct {
	tasks *tasks.Tasks
}

func (tfs *TaskFrameworkServer) Serve() {
	// fmt.Printf("Server listening :8080\n")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func (tfs *TaskFrameworkServer) runTask(w http.ResponseWriter, r *http.Request) {

	taskname := r.URL.Query().Get("taskname")

	if taskname == "" {
		fmt.Printf("Server: Taskname not present\n")
		return
	}
	taskId := tfs.tasks.Start(taskname)

	fmt.Fprintf(w, "%s\n", taskId)
}

func (tfs *TaskFrameworkServer) status(w http.ResponseWriter, r *http.Request) {
	taskId := r.URL.Query().Get("taskId")
	state, ok := tfs.tasks.State(taskId)
	if !ok {
		fmt.Fprintf(w, tfs.tasks.String())
	}
	fmt.Fprintf(w, "%s\n", state)
}

func NewServer(tasks *tasks.Tasks) *TaskFrameworkServer {
	tfs := &TaskFrameworkServer{
		tasks: tasks,
	}
	http.HandleFunc("/runtask", tfs.runTask)
	http.HandleFunc("/status", tfs.status)
	return tfs
}
