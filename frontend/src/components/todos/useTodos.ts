import { useState } from "react";

export function useTodos() {
  const [todos, setTodos] = useState<string[]>(() => {
    const storedTodos = localStorage.getItem("todos");
    return storedTodos ? JSON.parse(storedTodos) : [];
  });
  const [newTodo, setNewTodo] = useState("");
  return { todos, setTodos, newTodo, setNewTodo };
}
