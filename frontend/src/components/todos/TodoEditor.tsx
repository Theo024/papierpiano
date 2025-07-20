import { Button } from "@/components/ui/button";
import { Input } from "../ui/input";
import { handlePrint } from "./todoActions";
import { useSavedTodoLists } from "./useSavedTodoLists";
import { useTodos } from "./useTodos";
import { useTodoView } from "./useTodoView";

const TodoEditor = () => {
  const { todos, setTodos, newTodo, setNewTodo } = useTodos();
  const { listName, setListName, isLoading, setIsLoading, setCurrentView } =
    useTodoView();
  const { setSavedTodoList, setSelectedSavedTodoListId } = useSavedTodoLists();

  return (
    <div className="flex flex-col gap-6 py-4">
      <div className="flex flex-col gap-2">
        <Input
          type="text"
          placeholder="Nom de la liste"
          value={listName}
          onChange={(e) => setListName(e.target.value)}
        />
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
          onClick={() =>
            handlePrint({
              todos,
              listName,
              setIsLoading,
              setSavedTodoList,
              setTodos,
              setListName,
              setSelectedSavedTodoListId,
              setCurrentView,
            })
          }
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

export default TodoEditor;
