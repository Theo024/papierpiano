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
      <div className="flex flex-col gap-2 mt-4">
        <div className="font-bold">Listes sauvegardées</div>
        <div className="grid grid-cols-[1fr_auto] gap-2">
          <Button
            className="justify-start font-semibold col-span-2"
            variant="outline"
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
          {savedTodoList.map((entry) => (
            <>
              <Button
                key={entry.id + "-btn"}
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
                className="col-start-1 justify-start font-normal"
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
            </>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SavedTodoLists;
