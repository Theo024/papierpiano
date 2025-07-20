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
  const [history, setHistory] = useState<
    { id: string; name: string; todos: string[]; date: string }[]
  >(() => {
    const stored = localStorage.getItem("todoHistory");
    return stored ? JSON.parse(stored) : [];
  });
  const [selectedHistoryId, setSelectedHistoryId] = useState<string | null>(
    null
  );
  const [listName, setListName] = useState("");

  useEffect(() => {
    if (todos.length > 0 || listName.trim() !== "") {
      if (!selectedHistoryId) {
        // Create new entry and select it
        const newEntry = {
          id: Date.now().toString(),
          name: listName || "(Sans titre)",
          todos: todos,
          date: new Date().toLocaleString(),
        };
        setHistory((prevHistory) => {
          const updatedHistory = [newEntry, ...prevHistory];
          localStorage.setItem("todoHistory", JSON.stringify(updatedHistory));
          return updatedHistory;
        });
        setSelectedHistoryId(newEntry.id);
      } else {
        // Update selected entry
        setHistory((prevHistory) => {
          const updatedHistory = prevHistory.map((entry) =>
            entry.id === selectedHistoryId
              ? {
                  ...entry,
                  name: listName || "(Sans titre)",
                  todos: todos,
                  date: new Date().toLocaleString(),
                }
              : entry
          );
          localStorage.setItem("todoHistory", JSON.stringify(updatedHistory));
          return updatedHistory;
        });
      }
    }
  }, [todos, listName]);

  const handlePrint = async () => {
    setIsLoading(true);
    try {
      const newEntry = {
        id: Date.now().toString(),
        name: listName || `Liste du ${new Date().toLocaleString()}`,
        todos: todos,
        date: new Date().toLocaleString(),
      };
      setHistory((prevHistory) => [newEntry, ...prevHistory]);
      setTodos([]);
      setListName("");
      setSelectedHistoryId(null);
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

  const handleLoadHistory = (id: string) => {
    const entry = history.find((h) => h.id === id);
    if (entry) {
      setTodos(entry.todos);
      setListName(entry.name || "");
      setSelectedHistoryId(id);
    }
  };

  const handleDeleteHistory = (id: string) => {
    setHistory(history.filter((h) => h.id !== id));
    if (selectedHistoryId === id) {
      setSelectedHistoryId(null);
      setTodos([]);
      setListName("");
    }
  };

  return (
    <div className="flex flex-col gap-6 py-4">
      <div className="flex flex-col gap-2">
        {/* List name input */}
        <Input
          // className="md:text-base"
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

      <div className="flex">
        <Button
          className="flex-1"
          disabled={todos.length === 0 || isLoading}
          onClick={handlePrint}
        >
          {isLoading ? "Impression..." : "Imprimer"}
        </Button>
      </div>

      {/* History section with grid layout */}
      {history.length > 0 && (
        <div className="flex flex-col gap-2 mt-4">
          <div className="font-bold">Historique</div>
          <div className="grid grid-cols-[1fr_auto] gap-2">
            <Button
              className="justify-start font-semibold col-span-2"
              variant="outline"
              onClick={() => {
                setTodos([]);
                setListName("");
                setSelectedHistoryId(null);
              }}
            >
              Nouvelle liste
            </Button>
            {history.map((entry) => (
              <>
                <Button
                  key={entry.id + "-btn"}
                  variant={
                    selectedHistoryId === entry.id ? "default" : "outline"
                  }
                  onClick={() => handleLoadHistory(entry.id)}
                  className="col-start-1 justify-start font-normal"
                >
                  {entry.name}
                  {/* <span className="font-semibold"></span> */}
                </Button>
                {/* <div className="flex items-center text-xs text-gray-500 col-span-1">
                  {entry.date}
                </div> */}
                <Button
                  size="icon"
                  // variant="destructive"
                  onClick={() => handleDeleteHistory(entry.id)}
                >
                  <Trash />
                </Button>
                {/* <div className="flex justify-end col-span-1">
                </div> */}
              </>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default TodoTab;
