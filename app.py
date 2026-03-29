import streamlit as st
import pandas as pd
import sqlite3

conn = sqlite3.connect("bolao.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS palpites (
    usuario TEXT,
    jogo INTEGER,
    time1 TEXT,
    time2 TEXT,
    p1 INTEGER,
    p2 INTEGER
)
""")

st.title("Bolão Copa 2026 ⚽")

usuario = st.text_input("Digite seu nome")

jogos = pd.DataFrame({
    "jogo": [1,2,3],
    "time1": ["Brasil", "França", "Argentina"],
    "time2": ["Espanha", "Alemanha", "Portugal"]
})

st.subheader("Faça seus palpites")

for _, row in jogos.iterrows():
    st.write(f"Jogo {row['jogo']}")

    col1, col2 = st.columns(2)

    with col1:
        p1 = st.number_input(row["time1"], key=f"p1_{row['jogo']}", min_value=0)
    with col2:
        p2 = st.number_input(row["time2"], key=f"p2_{row['jogo']}", min_value=0)

    if st.button(f"Salvar {row['jogo']}"):
        cursor.execute(
            "INSERT INTO palpites VALUES (?, ?, ?, ?, ?, ?)",
            (usuario, row["jogo"], row["time1"], row["time2"], p1, p2)
        )
        conn.commit()
        st.success("Palpite salvo!")

st.divider()

st.subheader("Palpites registrados")

df = pd.read_sql("SELECT * FROM palpites", conn)
st.dataframe(df)
