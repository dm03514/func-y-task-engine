package usertasks

import (
	"github.com/dm03514/async-states-task-engine/task"
	"fmt"
	"github.com/looplab/fsm"
	"time"
	"github.com/satori/go.uuid"
)


type tripleTimeoutTask struct {
	task.Task
}

func NewTripleTimeoutTask(events chan *task.TaskEvent) task.ITask {

	tcs := task.TransitionConditions{
		"first_timeout": func(t *task.Task, nextState chan string) {
			t.Emit(
				fmt.Sprintf("Executing transition 'first_timeout'\n"),
			)
			time.Sleep(2 * time.Second)
			nextState <- "second"
			return
		},
		"second_timeout": func(t *task.Task, nextState chan string) {
			t.Emit(
				fmt.Sprintf("Executing transition 'second_timeout'\n"),
			)
			time.Sleep(2 * time.Second)
			nextState <- "third"
			return
		},
		"third_timeout": func(t *task.Task, nextState chan string) {
			t.Emit(
				fmt.Sprintf("Executing transition 'third_timeout'\n"),
			)
			time.Sleep(2 * time.Second)
			nextState <- "finished"
			return
		},
	}

	ttt := &tripleTimeoutTask{
		task.Task{
			StartState: "first",
			FinalState: "finished",
			TCs: tcs,
			EventChannel: events,
			Id: uuid.NewV4(),
		},
	}
	ttt.Task.FSM = fsm.NewFSM(
		"pending",
		fsm.Events{
			{Name: "initial", Src: []string{"unitialized"}, Dst: "pending"},
			{Name: "first", Src: []string{"pending"}, Dst: "first_timeout"},
			{Name: "second", Src: []string{"first_timeout"}, Dst: "second_timeout"},
			{Name: "third", Src: []string{"second_timeout"}, Dst: "third_timeout"},
			{Name: "finished", Src: []string{"third_timeout"}, Dst: "finished"},
		},
		fsm.Callbacks{},
	)
	return ttt
}
