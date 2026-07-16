import random
import streamlit as st


st.set_page_config(page_title="숫자 맞추기 게임", page_icon="🎯", layout="centered")


def start_new_game():
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.message = "새 게임이 시작되었습니다. 숫자를 입력해 주세요."
    st.session_state.game_over = False


if "secret_number" not in st.session_state:
    start_new_game()


st.title("🎯 숫자 맞추기 게임")
st.write("1부터 100 사이의 숫자를 맞춰보세요.")

col1, col2 = st.columns([1, 1])
with col1:
    st.metric("시도 횟수", st.session_state.attempts)
with col2:
    if st.button("새 게임 시작", use_container_width=True):
        start_new_game()

st.info(st.session_state.message)

guess = st.number_input(
    "숫자를 입력하세요",
    min_value=1,
    max_value=100,
    step=1,
    key="guess_input",
)

if st.button("확인", use_container_width=True):
    if st.session_state.game_over:
        st.success("게임이 끝났습니다. 새 게임을 시작해 주세요.")
    else:
        st.session_state.attempts += 1

        if guess < st.session_state.secret_number:
            st.session_state.message = "업! 더 큰 숫자입니다."
        elif guess > st.session_state.secret_number:
            st.session_state.message = "다운! 더 작은 숫자입니다."
        else:
            st.session_state.message = (
                f"정답입니다! {st.session_state.attempts}번 만에 맞추셨습니다."
            )
            st.session_state.game_over = True

        st.rerun()
