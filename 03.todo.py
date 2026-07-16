import json
import os
import streamlit as st

FILE_PATH = "todos.txt"


def load_todos():
    if not os.path.exists(FILE_PATH):
        return []

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        return []

    try:
        data = json.loads(content)
        if isinstance(data, list):
            todos = []
            for item in data:
                if isinstance(item, dict):
                    text = str(item.get("text", "")).strip()
                    done = bool(item.get("done", False))
                    if text:
                        todos.append({"text": text, "done": done})
                elif isinstance(item, str):
                    text = item.strip()
                    if text:
                        todos.append({"text": text, "done": False})
            return todos
    except json.JSONDecodeError:
        pass

    return [{"text": line.strip(), "done": False} for line in content.splitlines() if line.strip()]


def save_todos(todos):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)


def sorted_todos(todos):
    return sorted(todos, key=lambda item: item["done"])


st.set_page_config(page_title="Todo 앱", page_icon="✅", layout="centered")
st.title("✅ Todo 앱")
st.write("할 일을 추가하고 관리해보세요.")

if "todos" not in st.session_state:
    st.session_state.todos = load_todos()

new_todo = st.text_input("새 할 일", key="new_todo_input")
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("추가"):
        if new_todo.strip():
            st.session_state.todos.append({"text": new_todo.strip(), "done": False})
            save_todos(st.session_state.todos)
            st.session_state.new_todo_input = ""
            st.success("할 일이 추가되었습니다.")
            st.rerun()
with col2:
    if st.button("초기화"):
        st.session_state.todos = []
        save_todos(st.session_state.todos)
        st.warning("모든 할 일이 초기화되었습니다.")
        st.rerun()

st.subheader("할 일 목록")
if st.session_state.todos:
    ordered_indices = sorted(range(len(st.session_state.todos)), key=lambda i: st.session_state.todos[i]["done"])
    for position, index in enumerate(ordered_indices, start=1):
        item = st.session_state.todos[index]
        col_a, col_b = st.columns([4, 2])
        with col_a:
            if item["done"]:
                st.markdown(f"{position}. <s>{item['text']}</s>", unsafe_allow_html=True)
            else:
                st.write(f"{position}. {item['text']}")
        with col_b:
            button_label = "취소" if item["done"] else "완료"
            if st.button(button_label, key=f"toggle_{index}_{item['text']}"):
                st.session_state.todos[index]["done"] = not item["done"]
                save_todos(st.session_state.todos)
                st.rerun()
            if st.button("삭제", key=f"delete_{index}_{item['text']}"):
                del st.session_state.todos[index]
                save_todos(st.session_state.todos)
                st.rerun()
else:
    st.info("할 일이 없습니다.")
