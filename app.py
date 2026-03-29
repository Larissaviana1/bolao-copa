import streamlit as st
import pandas as pd
import sqlite3

# conexão
conn = sqlite3.connect("bolao.db", check_same_thread=False)
cursor = conn.cursor()

# tabelas
cursor.execute("""
CREATE TABLE IF NOT EXISTS palpites (
    usuario TEXT,
    jogo INTEGER,
    p1 INTEGER,
    p2 INTEGER
)
""")

# carregar jogos
jogos = pd.read_csv("jogos.csv")

st.title("🏆 Bolão Copa 2026")

# usuário
usuario = st.text_input("Seu nome")

# abas
aba = st.sidebar.radio("Menu", ["Palpites", "Ranking"])

# ------------------------
# PALPITES
# ------------------------
if aba == "Palpites":

    st.header("Faça seus palpites")

    for _, row in jogos.iterrows():
        st.write(f"Jogo {row['jogo']} | {row['time1']} x {row['time2']}")

        col1, col2 = st.columns(2)

        with col1:
            p1 = st.number_input(row["time1"], key=f"p1_{row['jogo']}", min_value=0)
        with col2:
            p2 = st.number_input(row["time2"], key=f"p2_{row['jogo']}", min_value=0)

        if st.button(f"Salvar {row['jogo']}"):
            cursor.execute(
                "INSERT INTO palpites VALUES (?, ?, ?, ?)",
                (usuario, row["jogo"], p1, p2)
            )
            conn.commit()
            st.success("Salvo!")

# ------------------------
# FUNÇÃO DE PONTOS
# ------------------------
def calcular_pontos(r1, r2, p1, p2):
    if pd.isna(r1) or pd.isna(r2):
        return 0
    if r1 == p1 and r2 == p2:
        return 5
    elif (r1 > r2 and p1 > p2) or (r1 < r2 and p1 < p2) or (r1 == r2 and p1 == p2):
        return 3
    elif r1 == p1 or r2 == p2:
        return 1
    else:
        return 0

# ------------------------
# RANKING
# ------------------------
if aba == "Ranking":

    st.header("Ranking")

    palpites = pd.read_sql("SELECT * FROM palpites", conn)

    resultado = []

    for _, palpite in palpites.iterrows():
        jogo = jogos[jogos["jogo"] == palpite["jogo"]].iloc[0]

        pontos = calcular_pontos(
            jogo["placar1"], jogo["placar2"],
            palpite["p1"], palpite["p2"]
        )

        resultado.append({
            "usuario": palpite["usuario"],
            "pontos": pontos
        })

    df = pd.DataFrame(resultado)

    ranking = df.groupby("usuario")["pontos"].sum().reset_index()
    ranking = ranking.sort_values(by="pontos", ascending=False)

    st.dataframe(ranking)
