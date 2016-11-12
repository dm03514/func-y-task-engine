package main

import (
	"github.com/dm03514/async-states-task-engine/task"
)

func main() {
	tfs := NewServer()

	lr := task.LogReader{
		Events: tfs.events,
	}
	go lr.Consume()

	tfs.Serve()
}