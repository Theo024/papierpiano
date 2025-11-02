import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import { GripVertical, Trash } from "lucide-react";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import type { Todo, TodoId } from "./atoms";

const TodoItem = ({
  todo,
  handleTodoChange,
  handleTodoDelete,
}: {
  todo: Todo;
  handleTodoChange: (newTodo: Todo) => void;
  handleTodoDelete: (todoId: TodoId) => void;
}) => {
  const { attributes, listeners, setNodeRef, transform, transition } =
    useSortable({ id: todo.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  return (
    <div className="flex gap-2" ref={setNodeRef} style={style}>
      <Input
        className="md:text-base font-[Courier_New]"
        type="text"
        value={todo.text}
        onChange={(event) => {
          handleTodoChange({ ...todo, text: event.target.value });
        }}
      />
      <Button
        size="icon"
        variant="outline"
        className="touch-none"
        {...attributes}
        {...listeners}
      >
        <GripVertical />
      </Button>
      <Button size="icon" onClick={() => handleTodoDelete(todo.id)}>
        <Trash />
      </Button>
    </div>
  );
};

export default TodoItem;
