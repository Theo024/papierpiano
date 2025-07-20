import { Button } from "@/components/ui/button";
import { Trash } from "lucide-react";
import { useEffect, useState } from "react";
import { toast } from "sonner";
import { Input } from "../ui/input";

const TodoTab = () => {
  const [todos, setTodos] = useState<string[]>(() => {
    const storedTodos = localStorage.getItem("todos");
    return storedTodos ? JSON.parse(storedTodos) : [];
  });
  const [newTodo, setNewTodo] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [savedTodoList, setSavedTodoList] = useState<
    { id: string; name: string; todos: string[]; date: string }[]
  >(() => {
    const stored = localStorage.getItem("todoHistory");
    return stored ? JSON.parse(stored) : [];
  });
  const [selectedSavedTodoListId, setSelectedSavedTodoListId] = useState<
    string | null
  >(null);
  const [listName, setListName] = useState("");
  const [currentView, setCurrentView] = useState<"list" | "edit">("list");

  useEffect(() => {
    if (
      currentView === "edit" &&
      (todos.length > 0 || listName.trim() !== "")
    ) {
      if (!selectedSavedTodoListId) {
        // Create new entry and select it
        const newEntry = {
          id: Date.now().toString(),
          name: listName || "(Sans titre)",
          todos: todos,
          date: new Date().toLocaleString(),
        };
        setSavedTodoList((prevList) => {
          const updatedList = [newEntry, ...prevList];
          localStorage.setItem("todoHistory", JSON.stringify(updatedList));
          return updatedList;
        });
        setSelectedSavedTodoListId(newEntry.id);
      } else {
        // Update selected entry
        setSavedTodoList((prevList) => {
          const updatedList = prevList.map((entry) =>
            entry.id === selectedSavedTodoListId
              ? {
                  ...entry,
                  name: listName || "(Sans titre)",
                  todos: todos,
                  date: new Date().toLocaleString(),
                }
              : entry
          );
          localStorage.setItem("todoHistory", JSON.stringify(updatedList));
          return updatedList;
        });
      }
    }
  }, [todos, listName, currentView, selectedSavedTodoListId]);

  const handlePrint = async () => {
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
  };

  const handleLoadSavedTodoList = (id: string) => {
    const entry = savedTodoList.find((h) => h.id === id);
    if (entry) {
      setTodos(entry.todos);
      setListName(entry.name || "");
      setSelectedSavedTodoListId(id);
      setCurrentView("edit");
    }
  };

  const handleDeleteSavedTodoList = (id: string) => {
    setSavedTodoList(savedTodoList.filter((h) => h.id !== id));
    if (selectedSavedTodoListId === id) {
      setSelectedSavedTodoListId(null);
      setTodos([]);
      setListName("");
      setCurrentView("list");
    }
  };

  const handleNewList = () => {
    setTodos([]);
    setListName("");
    setSelectedSavedTodoListId(null);
    setCurrentView("edit");
  };

  // --- Views ---
  if (currentView === "list") {
    return (
      <div className="flex flex-col gap-6 py-4">
        <div className="flex flex-col gap-2 mt-4">
          <div className="font-bold">Listes sauvegardées</div>
          <div className="grid grid-cols-[1fr_auto] gap-2">
            <Button
              className="justify-start font-semibold col-span-2"
              variant="outline"
              onClick={handleNewList}
            >
              Nouvelle liste
            </Button>
            {savedTodoList.map((entry) => (
              <>
                <Button
                  key={entry.id + "-btn"}
                  variant={"outline"}
                  onClick={() => handleLoadSavedTodoList(entry.id)}
                  className="col-start-1 justify-start font-normal"
                >
                  {entry.name}
                </Button>
                <Button
                  size="icon"
                  onClick={() => handleDeleteSavedTodoList(entry.id)}
                >
                  <Trash />
                </Button>
              </>
            ))}
          </div>
        </div>
      </div>
    );
  }

  // --- Edit view ---
  return (
    <div className="flex flex-col gap-6 py-4">
      <div className="flex flex-col gap-2">
        {/* List name input */}
        <Input
          type="text"
          placeholder="Nom de la liste"
          value={listName}
          onChange={(e) => setListName(e.target.value)}
        />

        {/* New todo input */}
        <div className="flex gap-2">
          <Input
            className="md:text-base font-[Courier_New]"
            type="text"
            placeholder="Nouvelle tâche"
            value={newTodo}
            onChange={(e) => setNewTodo(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && newTodo.trim()) {
                setTodos([...todos, newTodo.trim()]);
                setNewTodo("");
              }
            }}
          />
          <Button
            className="grow"
            variant="outline"
            onClick={() => {
              if (newTodo.trim()) {
                setTodos([...todos, newTodo.trim()]);
                setNewTodo("");
              }
            }}
            disabled={!newTodo.trim()}
          >
            +
          </Button>
        </div>
      </div>

      {/* Current todos (moved before print button) */}
      {todos.length > 0 && (
        <div className="flex flex-col gap-2">
          {todos.map((todo, idx) => (
            <div key={idx} className="flex gap-2">
              <Input
                className="md:text-base font-[Courier_New]"
                type="text"
                value={todo}
                onChange={(e) => {
                  const updatedTodos = [...todos];
                  updatedTodos[idx] = e.target.value;
                  setTodos(updatedTodos);
                }}
              />
              <Button
                className="grow"
                onClick={() => setTodos(todos.filter((_, i) => i !== idx))}
              >
                ×
              </Button>
            </div>
          ))}
        </div>
      )}

      <div className="flex gap-2">
        <Button
          className="flex-1"
          disabled={todos.length === 0 || isLoading}
          onClick={handlePrint}
        >
          {isLoading ? "Impression..." : "Imprimer"}
        </Button>
        <Button
          className="flex-1"
          variant="outline"
          onClick={() => setCurrentView("list")}
        >
          Retour
        </Button>
      </div>
    </div>
  );
};

export default TodoTab;
