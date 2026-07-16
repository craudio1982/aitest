# 이 앱은 HelloAI의 AI용품을 파는 회사 홈페이지이다.
# 고객관리 기능을 추가하는데 기본적인 CRUD 기능이 모두 구현되어야 한다.
# 기본적인 관리자 로그인 기능이 구현되어야 한다.
# 필요한 고객 정보는 고객ID(일련번호), 이름, 이메일, 전화번호, 가입일시
# 데이터는 파일로 관리 한다.

import json
import os
from datetime import datetime

import pandas as pd
import streamlit as st

DATA_FILE = os.path.join(os.path.dirname(__file__), "customers.json")

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin1234"


def load_customers():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_customers(customers):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(customers, f, ensure_ascii=False, indent=2)


def next_customer_id(customers):
    if not customers:
        return 1
    return max(c["id"] for c in customers) + 1


def add_customer(name, email, phone):
    customers = load_customers()
    customer = {
        "id": next_customer_id(customers),
        "name": name,
        "email": email,
        "phone": phone,
        "joined_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    customers.append(customer)
    save_customers(customers)


def update_customer(customer_id, name, email, phone):
    customers = load_customers()
    for c in customers:
        if c["id"] == customer_id:
            c["name"] = name
            c["email"] = email
            c["phone"] = phone
            break
    save_customers(customers)


def delete_customer(customer_id):
    customers = load_customers()
    customers = [c for c in customers if c["id"] != customer_id]
    save_customers(customers)


def render_login():
    st.title("HelloAI 관리자 로그인")
    with st.form("login_form"):
        username = st.text_input("아이디")
        password = st.text_input("비밀번호", type="password")
        submitted = st.form_submit_button("로그인")
        if submitted:
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("아이디 또는 비밀번호가 올바르지 않습니다.")


def render_customer_management():
    st.title("고객 관리")

    col1, col2 = st.columns([5, 1])
    with col1:
        st.caption(f"관리자: {ADMIN_USERNAME}")
    with col2:
        if st.button("로그아웃"):
            st.session_state.logged_in = False
            st.rerun()

    customers = load_customers()

    st.subheader("고객 목록")
    if customers:
        df = pd.DataFrame(customers)
        df = df.rename(
            columns={
                "id": "고객ID",
                "name": "이름",
                "email": "이메일",
                "phone": "전화번호",
                "joined_at": "가입일시",
            }
        )
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("등록된 고객이 없습니다.")

    st.subheader("고객 등록")
    with st.form("add_customer_form", clear_on_submit=True):
        name = st.text_input("이름")
        email = st.text_input("이메일")
        phone = st.text_input("전화번호")
        submitted = st.form_submit_button("등록")
        if submitted:
            if name and email and phone:
                add_customer(name, email, phone)
                st.success(f"'{name}' 고객이 등록되었습니다.")
                st.rerun()
            else:
                st.warning("이름, 이메일, 전화번호를 모두 입력해주세요.")

    if customers:
        st.subheader("고객 수정 / 삭제")
        id_to_customer = {c["id"]: c for c in customers}
        selected_id = st.selectbox(
            "고객 선택",
            options=list(id_to_customer.keys()),
            format_func=lambda cid: f"{cid} - {id_to_customer[cid]['name']}",
        )
        selected = id_to_customer[selected_id]

        with st.form("edit_customer_form"):
            edit_name = st.text_input("이름", value=selected["name"])
            edit_email = st.text_input("이메일", value=selected["email"])
            edit_phone = st.text_input("전화번호", value=selected["phone"])
            col_update, col_delete = st.columns(2)
            with col_update:
                update_clicked = st.form_submit_button("수정", use_container_width=True)
            with col_delete:
                delete_clicked = st.form_submit_button("삭제", use_container_width=True)

            if update_clicked:
                update_customer(selected_id, edit_name, edit_email, edit_phone)
                st.success("고객 정보가 수정되었습니다.")
                st.rerun()
            if delete_clicked:
                delete_customer(selected_id)
                st.success("고객이 삭제되었습니다.")
                st.rerun()


def main():
    st.set_page_config(page_title="HelloAI 고객관리", page_icon="🤖")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        render_customer_management()
    else:
        render_login()


if __name__ == "__main__":
    main()
