import { atom } from "jotai";
import { atomWithStorage } from "jotai/utils";

export type TodoId = string;
export type Todo = {
  id: TodoId;
  text: string;
};

export type TodoListId = string;
export type TodoList = {
  id: TodoListId;
  name: string;
  todos: Todo[];
};

export const todoListsAtom = atomWithStorage<TodoList[]>("todoLists", []);
export const selectedTodoListIdAtom = atomWithStorage<TodoListId | null>(
  "selectedTodoListId",
  null
);

export const todoListAtom = atom(
  (get) => {
    const todoLists = get(todoListsAtom);
    const selectedTodoListId = get(selectedTodoListIdAtom);
    return todoLists.find((list) => list.id === selectedTodoListId) || null;
  },
  (get, set, newTodoList: TodoList) => {
    const todoLists = get(todoListsAtom);
    const updatedLists = todoLists.map((list) =>
      list.id === newTodoList.id ? newTodoList : list
    );
    set(todoListsAtom, updatedLists);
  }
);
