import { Button } from "@/components/ui/button";
import { useAtom, useSetAtom } from "jotai";
import { useState } from "react";
import { toast } from "sonner";
import { Input } from "../ui/input";
import { selectedTodoListIdAtom, todoListAtom } from "./atoms";

const TodoEditor = () => {
  const [newTodo, setNewTodo] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const setSelectedTodoListId = useSetAtom(selectedTodoListIdAtom);
  const [todoList, setTodoList] = useAtom(todoListAtom);

  function handleNameChange(value: string) {
    if (!todoList) return;

    setTodoList({ ...todoList, name: value });
  }

  function handleNewTodo() {
    if (!todoList) return;

    if (newTodo.trim()) {
      setTodoList({
        ...todoList,
        todos: [...todoList.todos, newTodo.trim()],
      });
      setNewTodo("");
    }
  }

  function handleTodoChange(index: number, value: string) {
    if (!todoList) return;

    const updatedTodos = [...todoList.todos];
    updatedTodos[index] = value;
    setTodoList({ ...todoList, todos: updatedTodos });
  }

  function handleTodoDelete(index: number) {
    if (!todoList) return;

    const updatedTodos = todoList.todos.filter((_, idx) => idx !== index);
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
        body: JSON.stringify({ todos: todoList.todos }),
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
            className="px-[15px]"
            variant="outline"
            onClick={() => {
              handleNewTodo();
            }}
            disabled={!newTodo.trim()}
          >
            +
          </Button>
        </div>
      </div>

      {todoList.todos.length > 0 && (
        <div className="flex flex-col gap-2">
          {todoList.todos.map((todo, idx) => (
            <div key={idx} className="flex gap-2">
              <Input
                className="md:text-base font-[Courier_New]"
                type="text"
                value={todo}
                onChange={(e) => {
                  handleTodoChange(idx, e.target.value);
                }}
              />
              <Button onClick={() => handleTodoDelete(idx)}>×</Button>
            </div>
          ))}
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
