import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "remedios.db"

@st.cache_data(ttl=300)  # 5 min (evita reabrir toda hora)
def query_prices(remedio: str):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        """
        SELECT "Remédio" AS remedio,
               "Preço"  AS preco,
               "Nome"   AS nome,
               "Farmácia" AS farmacia
        FROM remedios
        WHERE lower("Remédio") = lower(?)
        ORDER BY preco ASC
        """,
        conn,
        params=[remedio],
    )
    conn.close()
    return df

st.title("Melhor preço de remédios")
q = st.text_input("Digite o remédio")

if q:
    df = query_prices(q)
    if df.empty:
        st.warning("Não encontrei esse remédio no banco.")
    else:
        st.subheader("Melhor opção")
        st.dataframe(df.head(1), use_container_width=True)
        st.subheader("Todas as opções")
        st.dataframe(df, use_container_width=True)