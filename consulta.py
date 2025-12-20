import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "remedios.db"

# -------- Funções de banco --------

@st.cache_data(ttl=300)
def listar_remedios():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        'SELECT DISTINCT "Remédio" AS remedio FROM remedios ORDER BY remedio;',
        conn
    )
    conn.close()
    return df["remedio"].dropna().tolist()

@st.cache_data(ttl=300)
def query_prices(remedio: str):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        """
        SELECT "Remédio" AS remedio,
               "Preço"  AS preco,
               "Nome"   AS nome,
               "Farmácia" AS farmacia
        FROM remedios
        WHERE "Remédio" = ?
        ORDER BY preco ASC
        """,
        conn,
        params=[remedio],
    )
    conn.close()
    return df

# -------- Interface --------

st.title("Melhor preço de remédios")

remedios = listar_remedios()

if not remedios:
    st.error("Banco vazio ou 'remedios.db' não encontrado.")
else:
    escolhido = st.selectbox(
        "Selecione um remédio da base",
        options=remedios,
        index=0
    )

    if escolhido:
        df = query_prices(escolhido)

        if df.empty:
            st.warning("Não encontrei esse remédio no banco.")
        else:
            st.subheader("Melhor opção")
            st.dataframe(df.head(1), use_container_width=True)

            st.subheader("Todas as opções")
            st.dataframe(df, use_container_width=True)
