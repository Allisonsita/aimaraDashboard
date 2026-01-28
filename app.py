import streamlit as st
from dashboard import show_dashboard
from data_loader import load_data
from PIL import Image

# Cargar Font Awesome
st.markdown(
    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">',
    unsafe_allow_html=True
)

# Configuración de la página
try:
    logo = Image.open("src/logo_AI.png")
    st.set_page_config(
        page_title="AiMara Dashboard",
        page_icon=logo,
        layout="wide",
        initial_sidebar_state="collapsed"
    )
except FileNotFoundError:
    st.set_page_config(
        page_title="AiMara Dashboard",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    st.warning("Advertencia: No se pudo encontrar 'src/logo_AI.png'. Usando ícono por defecto.")

# GIDs por categoría
GIDS = {
    "Historia y Literatura": 888266253,
    "Noticias": 2068753571,
    "Educación": 517062553,
    "Poder Judicial": 1937765031,
    "Poder Legislativo": 1575512628,
    "Medicina": 1970051983,
    "Gatronomía": 538377057,
    "Turismo y Hotelería": 1885603225,
    "Empleo": 1224871178,
    "Desastres Naturales": 2119335982
}

# Autores por categoría
AUTORES = {
    "Historia y Literatura": "Allison Reynoso",
    "Noticias": "Sofia Quispe",
    "Educación": "Miriam Cayo",
    "Poder Judicial": "Elmer Collanqui",
    "Poder Legislativo": "Jamir Balcona",
    "Medicina": "Jesus Rocca",
    "Gatronomía": "Seline Maquera",
    "Turismo y Hotelería": "Hans Amesquita",
    "Empleo": "Seline Maquera",
    "Desastres Naturales": "Yoselin Arocutipa"
}

def main():
    st.sidebar.title("Menú")

    # Estilos del menú
    st.sidebar.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        text-align: left;
        background-color: transparent !important;
        border: none !important;
        color: #4a4a4a !important;
        font-size: 16px;
        font-weight: bold;
        padding: 10px 15px !important;
        margin: 5px 0;
        transition: background-color 0.2s;
    }
    .stButton>button:hover {
        background-color: #f0f2f6 !important;
        border-radius: 5px;
    }
    .stButton>button:active {
        background-color: #e6e8eb !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Página inicial (primera categoría)
    if 'page' not in st.session_state:
        st.session_state.page = list(GIDS.keys())[0]

    # Botones del menú
    for page_name in GIDS.keys():
        if st.sidebar.button(page_name, key=page_name):
            st.session_state.page = page_name

    current_page = st.session_state.page

    # Resaltar botón activo
    st.sidebar.markdown(
        f"""
        <script>
        const buttons = window.parent.document.querySelectorAll('.stButton>button');
        buttons.forEach(btn => {{
            if (btn.innerText.includes("{current_page}")) {{
                btn.style.backgroundColor = '#f0f2f6';
                btn.style.color = '#01c2cb';
                btn.style.borderRadius = '5px';
            }}
        }});
        </script>
        """,
        unsafe_allow_html=True
    )

    # Mostrar dashboard correspondiente
    show_dashboard(
        current_page,
        GIDS[current_page],
        AUTORES[current_page]
    )

if __name__ == "__main__":
    main()
