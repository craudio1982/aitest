# 이 앱은 HelloAI의 AI용품을 파는 회사 홈페이지이다.
# 고객관리 기능을 추가하는데 기본적인 CRUD 기능이 모두 구현되어야 한다.
# 기본적인 관리자 로그인 기능이 구현되어야 한다.
# 필요한 고객 정보는 고객ID(일련번호), 이름, 이메일, 전화번호, 가입일시
# 데이터는 MySQL 데이터베이스로 관리한다. (접속 정보는 .env 파일에서 로드)

import os

import pandas as pd
import pymysql
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin1234"


def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        ssl={"ssl": {}},
    )


def init_db():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS customers (
                    customer_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    phone VARCHAR(20),
                    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS products (
                    product_id INT AUTO_INCREMENT PRIMARY KEY,
                    product_name VARCHAR(10) NOT NULL,
                    price DECIMAL(10,2) NOT NULL DEFAULT 0.00,
                    stock_quantity INT NOT NULL DEFAULT 0,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
                """
            )
        conn.commit()
    finally:
        conn.close()


def load_customers():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT customer_id, name, email, phone, create_at FROM customers ORDER BY customer_id"
            )
            return cursor.fetchall()
    finally:
        conn.close()


def add_customer(name, email, phone):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO customers (name, email, phone) VALUES (%s, %s, %s)",
                (name, email, phone),
            )
        conn.commit()
    finally:
        conn.close()


def update_customer(customer_id, name, email, phone):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE customers SET name=%s, email=%s, phone=%s WHERE customer_id=%s",
                (name, email, phone, customer_id),
            )
        conn.commit()
    finally:
        conn.close()


def delete_customer(customer_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM customers WHERE customer_id=%s", (customer_id,))
        conn.commit()
    finally:
        conn.close()


def load_products():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT product_id, product_name, price, stock_quantity, last_updated FROM products ORDER BY product_id"
            )
            return cursor.fetchall()
    finally:
        conn.close()


def add_product(product_name, price, stock_quantity):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO products (product_name, price, stock_quantity) VALUES (%s, %s, %s)",
                (product_name, price, stock_quantity),
            )
        conn.commit()
    finally:
        conn.close()


def update_product(product_id, product_name, price, stock_quantity):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE products SET product_name=%s, price=%s, stock_quantity=%s WHERE product_id=%s",
                (product_name, price, stock_quantity, product_id),
            )
        conn.commit()
    finally:
        conn.close()


def delete_product(product_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM products WHERE product_id=%s", (product_id,))
        conn.commit()
    finally:
        conn.close()


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


def render_header(title):
    st.title(title)
    col1, col2 = st.columns([5, 1])
    with col1:
        st.caption(f"관리자: {ADMIN_USERNAME}")
    with col2:
        if st.button("로그아웃"):
            st.session_state.logged_in = False
            st.rerun()


def render_customer_management():
    render_header("고객 관리")

    customers = load_customers()

    st.subheader("고객 목록")
    if customers:
        df = pd.DataFrame(customers)
        df = df.rename(
            columns={
                "customer_id": "고객ID",
                "name": "이름",
                "email": "이메일",
                "phone": "전화번호",
                "create_at": "가입일시",
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
        id_to_customer = {c["customer_id"]: c for c in customers}
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


def render_product_management():
    render_header("상품 관리")

    products = load_products()

    st.subheader("상품 목록")
    if products:
        df = pd.DataFrame(products)
        df = df.rename(
            columns={
                "product_id": "상품ID",
                "product_name": "상품명",
                "price": "가격",
                "stock_quantity": "재고수량",
                "last_updated": "최종수정일시",
            }
        )
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("등록된 상품이 없습니다.")

    st.subheader("상품 등록")
    with st.form("add_product_form", clear_on_submit=True):
        name = st.text_input("상품명 (최대 10자)", max_chars=10)
        price = st.number_input("가격", min_value=0.0, step=100.0, format="%.2f")
        stock_quantity = st.number_input("재고수량", min_value=0, step=1)
        submitted = st.form_submit_button("등록")
        if submitted:
            if name:
                add_product(name, price, stock_quantity)
                st.success(f"'{name}' 상품이 등록되었습니다.")
                st.rerun()
            else:
                st.warning("상품명을 입력해주세요.")

    if products:
        st.subheader("상품 수정 / 삭제")
        id_to_product = {p["product_id"]: p for p in products}
        selected_id = st.selectbox(
            "상품 선택",
            options=list(id_to_product.keys()),
            format_func=lambda pid: f"{pid} - {id_to_product[pid]['product_name']}",
        )
        selected = id_to_product[selected_id]

        with st.form("edit_product_form"):
            edit_name = st.text_input(
                "상품명 (최대 10자)", value=selected["product_name"], max_chars=10
            )
            edit_price = st.number_input(
                "가격", min_value=0.0, step=100.0, format="%.2f", value=float(selected["price"])
            )
            edit_stock = st.number_input(
                "재고수량", min_value=0, step=1, value=int(selected["stock_quantity"])
            )
            col_update, col_delete = st.columns(2)
            with col_update:
                update_clicked = st.form_submit_button("수정", use_container_width=True)
            with col_delete:
                delete_clicked = st.form_submit_button("삭제", use_container_width=True)

            if update_clicked:
                update_product(selected_id, edit_name, edit_price, edit_stock)
                st.success("상품 정보가 수정되었습니다.")
                st.rerun()
            if delete_clicked:
                delete_product(selected_id)
                st.success("상품이 삭제되었습니다.")
                st.rerun()


def main():
    st.set_page_config(page_title="HelloAI 고객관리", page_icon="🤖")

    try:
        init_db()
    except pymysql.MySQLError as e:
        st.error(f"데이터베이스 연결에 실패했습니다: {e}")
        st.stop()

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        menu = st.sidebar.radio("메뉴", ["고객 관리", "상품 관리"])
        if menu == "고객 관리":
            render_customer_management()
        else:
            render_product_management()
    else:
        render_login()


if __name__ == "__main__":
    main()
