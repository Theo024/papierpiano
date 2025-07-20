import { useAtomValue } from "jotai";
import TodoEditor from "./TodoEditor";
import TodoLists from "./TodoLists";
import { selectedTodoListIdAtom } from "./atoms";

const TodoTab = () => {
  const selectedTodoListId = useAtomValue(selectedTodoListIdAtom);

  if (selectedTodoListId === null) {
    return <TodoLists />;
  }

  return <TodoEditor />;
};

export default TodoTab;
