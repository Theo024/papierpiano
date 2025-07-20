import { useState } from "react";

export function useTodoView() {
  const [listName, setListName] = useState("");
  const [currentView, setCurrentView] = useState<"list" | "edit">("list");
  const [isLoading, setIsLoading] = useState(false);
  return {
    listName,
    setListName,
    currentView,
    setCurrentView,
    isLoading,
    setIsLoading,
  };
}
