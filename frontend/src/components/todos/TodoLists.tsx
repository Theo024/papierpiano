import { Button } from "@/components/ui/button";
import { useAtom, useSetAtom } from "jotai";
import { Trash } from "lucide-react";
import { v7 as uuidv7 } from "uuid";
import {
  selectedTodoListIdAtom,
  todoListsAtom,
  type TodoListId,
} from "./atoms";

const SavedTodoLists = () => {
  const [todoLists, setTodoLists] = useAtom(todoListsAtom);
  const setSelectedTodoListId = useSetAtom(selectedTodoListIdAtom);

  function handleNewList() {
    const newTodoListId = uuidv7();
    setTodoLists((prev) => [
      {
        id: newTodoListId,
        name: "",
        todos: [],
      },
      ...prev,
    ]);
    setSelectedTodoListId(newTodoListId);
  }

  function handleLoadTodoList(id: TodoListId) {
    setSelectedTodoListId(id);
  }

  function handleDeleteTodoList(id: TodoListId) {
    setTodoLists(todoLists.filter((x) => x.id !== id));
  }

  return (
    <div className="flex flex-col gap-6 py-4">
      <Button
        className="justify-start font-semibold"
        onClick={() => handleNewList()}
      >
        Créer une nouvelle liste
      </Button>

      <div className="flex flex-col gap-2">
        {todoLists.map((entry) => (
          <div className="flex gap-2" key={entry.id}>
            <Button
              variant={"outline"}
              onClick={() => handleLoadTodoList(entry.id)}
              className="grow justify-start font-normal"
            >
              {entry.name.length > 0 ? (
                entry.name
              ) : (
                <span className="italic">(Liste sans nom)</span>
              )}
            </Button>

            <Button size="icon" onClick={() => handleDeleteTodoList(entry.id)}>
              <Trash />
            </Button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SavedTodoLists;
