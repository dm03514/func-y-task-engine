package task

import (
	"fmt"
	"encoding/json"
)

type LogReader struct {
	Events chan *TaskEvent
}

// Should be able to emit as JSON so that we can
// automatically consume the output
func (lr *LogReader) Consume() {
	for event := range lr.Events {
		e, err := json.Marshal(event)
		if err != nil {
			panic("LogReader.Consume() invalid event")
		}
		fmt.Println(string(e))
	}
}
