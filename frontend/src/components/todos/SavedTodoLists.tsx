import { Button } from "@/components/ui/button";
import { Trash } from "lucide-react";
import {
  handleDeleteSavedTodoList,
  handleLoadSavedTodoList,
  handleNewList,
} from "./todoActions";
import { useSavedTodoLists } from "./useSavedTodoLists";
import { useTodos } from "./useTodos";
import { useTodoView } from "./useTodoView";

const SavedTodoLists = () => {
  const {
    savedTodoList,
    setSavedTodoList,
    selectedSavedTodoListId,
    setSelectedSavedTodoListId,
  } = useSavedTodoLists();
  const { setTodos } = useTodos();
  const { setListName, setCurrentView } = useTodoView();

  return (
    <div className="flex flex-col gap-6 py-4">
      <Button
        className="justify-start font-semibold"
        // variant="outline"
        onClick={() =>
          handleNewList({
            setTodos,
            setListName,
            setSelectedSavedTodoListId,
            setCurrentView,
          })
        }
      >
        Nouvelle liste
      </Button>

      <div className="flex flex-col gap-2">
        {savedTodoList.map((entry) => (
          <div className="flex gap-2" key={entry.id}>
            <Button
              variant={"outline"}
              onClick={() =>
                handleLoadSavedTodoList({
                  id: entry.id,
                  savedTodoList,
                  setTodos,
                  setListName,
                  setSelectedSavedTodoListId,
                  setCurrentView,
                })
              }
              className="grow justify-start font-normal"
            >
              {entry.name}
            </Button>

            <Button
              size="icon"
              onClick={() =>
                handleDeleteSavedTodoList({
                  id: entry.id,
                  savedTodoList,
                  setSavedTodoList,
                  selectedSavedTodoListId,
                  setSelectedSavedTodoListId,
                  setTodos,
                  setListName,
                  setCurrentView,
                })
              }
            >
              <Trash />
            </Button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SavedTodoLists;
