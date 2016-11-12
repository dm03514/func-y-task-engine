package main

import (
	"github.com/dm03514/async-states-task-engine/tasks"
	"github.com/dm03514/async-states-task-engine/task"
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
