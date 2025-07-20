import { Button } from "@/components/ui/button";
import { useState } from "react";
import { toast } from "sonner";
import { Input } from "../ui/input";

const TodoTab = () => {
  const [todos, setTodos] = useState<string[]>([]);
  const [newTodo, setNewTodo] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handlePrint = async () => {
    setIsLoading(true);
    try {
      const response = await fetch("/api/todo", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ todos: todos }),
      });
      if (response.ok) {
        setTodos([]);
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
  };

  return (
    <div className="flex flex-col gap-6 py-4">
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
    </div>
  );
};

export default TodoTab;
