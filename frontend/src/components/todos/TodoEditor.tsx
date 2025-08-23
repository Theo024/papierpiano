import { Button } from "@/components/ui/button";
import {
  closestCenter,
  DndContext,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  type DragEndEvent,
} from "@dnd-kit/core";
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
} from "@dnd-kit/sortable";
import { useAtom, useSetAtom } from "jotai";
import { Plus } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";
import { v7 as uuidv7 } from "uuid";
import { Input } from "../ui/input";
import {
  selectedTodoListIdAtom,
  todoListAtom,
  type Todo,
  type TodoId,
} from "./atoms";
import TodoItem from "./TodoItem";

const TodoEditor = () => {
  const [newTodo, setNewTodo] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const setSelectedTodoListId = useSetAtom(selectedTodoListIdAtom);
  const [todoList, setTodoList] = useAtom(todoListAtom);

  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  function handleDragEnd(event: DragEndEvent) {
    const { active, over } = event;

    if (todoList && over && active.id !== over.id) {
      const oldIndex = todoList.todos.findIndex(
        (todo) => todo.id === active.id
      );
      const newIndex = todoList.todos.findIndex((todo) => todo.id === over.id);
      const updatedTodos = arrayMove(todoList.todos, oldIndex, newIndex);
      setTodoList({ ...todoList, todos: updatedTodos });
    }
  }

  function handleNameChange(value: string) {
    if (!todoList) return;

    setTodoList({ ...todoList, name: value });
  }

  function handleNewTodo() {
    if (!todoList) return;

    if (newTodo.trim()) {
      setTodoList({
        ...todoList,
        todos: [...todoList.todos, { id: uuidv7(), text: newTodo.trim() }],
      });
      setNewTodo("");
    }
  }

  function handleTodoChange(newTodo: Todo) {
    if (!todoList) return;

    const updatedTodos = todoList.todos.map((todo) =>
      todo.id === newTodo.id ? newTodo : todo
    );
    setTodoList({ ...todoList, todos: updatedTodos });
  }

  function handleTodoDelete(todoId: TodoId) {
    if (!todoList) return;

    const updatedTodos = todoList.todos.filter((todo) => todo.id !== todoId);
    setTodoList({ ...todoList, todos: updatedTodos });
  }

  async function handlePrint() {
    if (!todoList) return;

    setIsLoading(true);
    try {
      const response = await fetch("/api/todo", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ todos: todoList.todos.map((todo) => todo.text) }),
      });
      if (response.ok) {
        setSelectedTodoListId(null);
        toast.success("Todo list imprimée avec succès");
      } else {
        const errorData = await response.json().catch(() => null);
        toast.error(
          errorData?.message ||
            `Erreur lors de l'impression (${response.status}): ${response.statusText}`
        );
      }
    } catch (error: unknown) {
      console.error("Print error:", error);
      const errorMessage =
        error instanceof Error
          ? error.message
          : "Erreur de connexion au serveur d'impression";
      toast.error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }

  if (!todoList) {
    setSelectedTodoListId(null);
    return;
  }

  return (
    <div className="flex flex-col gap-6 py-4">
      <div className="flex flex-col gap-2">
        <Input
          type="text"
          placeholder="Nom de la liste"
          value={todoList.name}
          onChange={(e) => handleNameChange(e.target.value)}
        />
        <div className="flex gap-2">
          <Input
            className="md:text-base font-[Courier_New]"
            type="text"
            placeholder="Nouvelle tâche"
            value={newTodo}
            onChange={(e) => setNewTodo(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleNewTodo();
              }
            }}
          />
          <Button
            size="icon"
            variant="outline"
            onClick={() => {
              handleNewTodo();
            }}
            disabled={!newTodo.trim()}
          >
            <Plus />
          </Button>
        </div>
      </div>

      {todoList.todos.length > 0 && (
        <div className="flex flex-col gap-2">
          <DndContext
            sensors={sensors}
            collisionDetection={closestCenter}
            onDragEnd={handleDragEnd}
          >
            <SortableContext
              items={todoList.todos}
              strategy={verticalListSortingStrategy}
            >
              {todoList.todos.map((todo) => (
                <TodoItem
                  key={todo.id}
                  todo={todo}
                  handleTodoChange={handleTodoChange}
                  handleTodoDelete={handleTodoDelete}
                />
              ))}
            </SortableContext>
          </DndContext>
        </div>
      )}

      <div className="flex gap-2">
        <Button
          className="grow"
          disabled={todoList.todos.length === 0 || isLoading}
          onClick={() => handlePrint()}
        >
          {isLoading ? "Impression..." : "Imprimer"}
        </Button>
        <Button
          className="px-8"
          variant="outline"
          onClick={() => setSelectedTodoListId(null)}
        >
          Retour
        </Button>
      </div>
    </div>
  );
};

export default TodoEditor;
