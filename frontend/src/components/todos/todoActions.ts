import { toast } from "sonner";
import type { TodoListEntry } from "./useSavedTodoLists";

export function handlePrint({
  todos,
  listName,
  setIsLoading,
  setSavedTodoList,
  setTodos,
  setListName,
  setSelectedSavedTodoListId,
  setCurrentView,
}: {
  todos: string[];
  listName: string;
  setIsLoading: (loading: boolean) => void;
  setSavedTodoList: (fn: (prev: TodoListEntry[]) => TodoListEntry[]) => void;
  setTodos: (todos: string[]) => void;
  setListName: (name: string) => void;
  setSelectedSavedTodoListId: (id: string | null) => void;
  setCurrentView: (view: "list" | "edit") => void;
}) {
  setIsLoading(true);
  try {
    const newEntry = {
      id: Date.now().toString(),
      name: listName || `Liste du ${new Date().toLocaleString()}`,
      todos: todos,
      date: new Date().toLocaleString(),
    };
    setSavedTodoList((prevList) => [newEntry, ...prevList]);
    setTodos([]);
    setListName("");
    setSelectedSavedTodoListId(null);
    setCurrentView("list");
    toast.success("Todo list imprimée avec succès");
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

export function handleLoadSavedTodoList({
  id,
  savedTodoList,
  setTodos,
  setListName,
  setSelectedSavedTodoListId,
  setCurrentView,
}: {
  id: string;
  savedTodoList: TodoListEntry[];
  setTodos: (todos: string[]) => void;
  setListName: (name: string) => void;
  setSelectedSavedTodoListId: (id: string | null) => void;
  setCurrentView: (view: "list" | "edit") => void;
}) {
  const entry = savedTodoList.find((h) => h.id === id);
  if (entry) {
    setTodos(entry.todos);
    setListName(entry.name || "");
    setSelectedSavedTodoListId(id);
    setCurrentView("edit");
  }
}

export function handleDeleteSavedTodoList({
  id,
  savedTodoList,
  setSavedTodoList,
  selectedSavedTodoListId,
  setSelectedSavedTodoListId,
  setTodos,
  setListName,
  setCurrentView,
}: {
  id: string;
  savedTodoList: TodoListEntry[];
  setSavedTodoList: (list: TodoListEntry[]) => void;
  selectedSavedTodoListId: string | null;
  setSelectedSavedTodoListId: (id: string | null) => void;
  setTodos: (todos: string[]) => void;
  setListName: (name: string) => void;
  setCurrentView: (view: "list" | "edit") => void;
}) {
  setSavedTodoList(savedTodoList.filter((h) => h.id !== id));
  if (selectedSavedTodoListId === id) {
    setSelectedSavedTodoListId(null);
    setTodos([]);
    setListName("");
    setCurrentView("list");
  }
}

export function handleNewList({
  setTodos,
  setListName,
  setSelectedSavedTodoListId,
  setCurrentView,
}: {
  setTodos: (todos: string[]) => void;
  setListName: (name: string) => void;
  setSelectedSavedTodoListId: (id: string | null) => void;
  setCurrentView: (view: "list" | "edit") => void;
}) {
  setTodos([]);
  setListName("");
  setSelectedSavedTodoListId(null);
  setCurrentView("edit");
}
