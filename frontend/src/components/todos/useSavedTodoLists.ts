import { useState } from "react";

export type TodoListEntry = {
  id: string;
  name: string;
  todos: string[];
  date: string;
};

export function useSavedTodoLists() {
  const [savedTodoList, setSavedTodoList] = useState<TodoListEntry[]>(() => {
    const stored = localStorage.getItem("todoHistory");
    return stored ? JSON.parse(stored) : [];
  });
  const [selectedSavedTodoListId, setSelectedSavedTodoListId] = useState<
    string | null
  >(null);
  return {
    savedTodoList,
    setSavedTodoList,
    selectedSavedTodoListId,
    setSelectedSavedTodoListId,
  };
}
