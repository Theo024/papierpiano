import SavedTodoLists from "./SavedTodoLists";
import TodoEditor from "./TodoEditor";
import { useTodoView } from "./useTodoView";

const TodoTab = () => {
  const { currentView } = useTodoView();

  if (currentView === "list") {
    return <SavedTodoLists />;
  }

  return <TodoEditor />;
};

export default TodoTab;
