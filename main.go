package main

import (
	"github.com/dm03514/async-states-task-engine/task"
	"github.com/dm03514/async-states-task-engine/tasks"
)

func main() {

	ts := tasks.Init()

	tfs := NewServer(ts)

	lr := task.LogReader{
		Events: ts.Events,
	}
	go lr.Consume()

	tfs.Serve()
}
