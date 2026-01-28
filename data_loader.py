import streamlit as st
import pandas as pd

@st.cache_data(ttl=600)
def load_data(gid):
    """
    Loads and caches data from a public Google Sheet.
    
    Args:
        gid (int): The Google Sheet gid (grid ID) for the main data.

    Returns:
        tuple: A tuple containing the merged DataFrame and the date dictionary.
    """
    base_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRcAXksr25-bpVxWcpFjpruvNQ5SjhJ7Ev282n1OU5JfT85blAOHAA_xqZvD4ieR1094ZxB9Jh8h7n3/pub?output=csv&gid="
    gid_fechas = 1002468456

    try:
        df_historia = pd.read_csv(f"{base_url}{gid}")
        df_fechas = pd.read_csv(f"{base_url}{gid_fechas}")
        df_historia = df_historia.merge(df_fechas, on="ID_corte", how="left")
        
        fechas_unicas = df_historia[['ID_corte', 'fecha_corte']].drop_duplicates()
        fechas_unicas = fechas_unicas.sort_values(by="ID_corte", ascending=True)
        
        fecha_dict = {row['fecha_corte']: row['ID_corte'] for _, row in fechas_unicas.iterrows()}
        
        return df_historia, fecha_dict
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return pd.DataFrame(), {}