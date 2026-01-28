import streamlit as st
from dashboard import show_dashboard
from data_loader import load_data
from PIL import Image
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from styles import get_custom_css

st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">', unsafe_allow_html=True)

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

GIDS = {
    "Historia y Literatura": 888266253,
    "Noticias": 2068753571,
    "Educación": 517062553,
    "Poder Judicial": 1937765031,
    "Poder Legislativo": 1185292120,
    "Medicina": 1970051983,
    "Gatronomía": 538377057,
    "Turismo y Hotelería": 1885603225,
    "Empleo": 1224871178
}

AUTORES = {
    "Historia y Literatura": "Allison Reynoso",
    "Noticias": "Sofia Quispe",
    "Educación": "Miriam Cayo",
    "Poder Judicial": "Elmer Collanqui",
    "Poder Legislativo": "Jamir Balcona",
    "Medicina": "Jesus Rocca",
    "Gatronomía": "Seline Maquera",
    "Turismo y Hotelería": "Hans Amesquita",
    "Empleo": "Seline Maquera"
}

#--- New Function for General Dashboard ---
def show_general_dashboard(page_title, autor):
    st.markdown(f"### {page_title}")
    st.markdown(f'<div style="font-size: 16px; font-weight: bold; color: #4a4a4a;">{autor}</div>', unsafe_allow_html=True)
    st.markdown("---")

    is_dark_mode = st.get_option("theme.base") == "dark"
    st.markdown(get_custom_css(is_dark_mode), unsafe_allow_html=True)

    font_color = "#E0E0E0" if is_dark_mode else "#4a4a4a"
    plot_bg = "rgba(0,0,0,0)"
    paper_bg = "rgba(0,0,0,0)"
    grid_color = "#3A3A3A" if is_dark_mode else "#E0E0E0"
    
    all_data = []
    
    for _, gid in GIDS.items():
        if gid != 0: #Exclude any placeholder GID
            df, _ = load_data(gid)
            if not df.empty:
                all_data.append(df)
    
    #If no data is found, show a warning
    if not all_data:
        st.warning("No se encontraron datos para mostrar en el dashboard general.")
        return

    df_historia = pd.concat(all_data, ignore_index=True)

    ultima_fecha = df_historia['ID_corte'].max()
    df_ultimo_corte = df_historia[df_historia["ID_corte"] == ultima_fecha].copy()
    
    total_registros_general = df_ultimo_corte["r_registros"].sum()
    total_archivos_general = df_ultimo_corte["r_archivos"].sum()
    total_almacenamiento_general = df_ultimo_corte["r_almacenamiento"].sum()

    #--- Total Metric Cards via Custom CSS Grid ---
    st.markdown(f"""
    <div class="metrics-container">
        <div class="metric-card">
            <div class="metric-info">
                <div class="metric-value">{total_registros_general:,}</div>
                <div class="metric-label">Total Registros</div>
            </div>
            <div class="metric-icon"><i class="fa-solid fa-file-lines"></i></div>
        </div>
        <div class="metric-card">
            <div class="metric-info">
                <div class="metric-value">{total_archivos_general:,}</div>
                <div class="metric-label">Total Archivos</div>
            </div>
            <div class="metric-icon"><i class="fa-solid fa-folder"></i></div>
        </div>
        <div class="metric-card">
            <div class="metric-info">
                <div class="metric-value">{total_almacenamiento_general:,.2f} GB</div>
                <div class="metric-label">Total Almacenamiento</div>
            </div>
            <div class="metric-icon"><i class="fa-solid fa-hard-drive"></i></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    
    #--- General Summary Charts ---
    col_izq, col_der = st.columns((2, 1))
    
    #Bar Chart: Records by Category
    with col_izq:
        with st.container(border=True):
            st.markdown(f'<div style="font-size: 20px; font-weight: bold; margin: 5; color: {font_color} !important;">Registros por Categoría</div>', unsafe_allow_html=True)
            df_categoría = df_ultimo_corte.groupby("categoría")["r_registros"].sum().reset_index()
            fig_barras_cat = px.bar(
                df_categoría,
                x="categoría",
                y="r_registros",
                color_discrete_sequence=['#01c2cb']
            )
            fig_barras_cat.update_layout(
                height=400,
                xaxis_title="Categoría",
                yaxis_title="Total de Registros",
                plot_bgcolor=plot_bg,
                paper_bgcolor=paper_bg,
                font=dict(color=font_color),
                xaxis=dict(gridcolor=grid_color),
                yaxis=dict(gridcolor=grid_color)
            )
            st.plotly_chart(fig_barras_cat, use_container_width=True)

    #Pie Chart: Storage Distribution by Category
    with col_der:
        with st.container(border=True):
            st.markdown(f'<div style="font-size: 20px; font-weight: bold; margin: 5; color: {font_color} !important;">Almacenamiento por Categoría</div>', unsafe_allow_html=True)
            df_almacenamiento_cat = df_ultimo_corte.groupby("categoría")["r_almacenamiento"].sum().reset_index()
            fig_pie_alm = px.pie(
                df_almacenamiento_cat,
                names="categoría",
                values="r_almacenamiento",
                hole=0.4,
                color_discrete_sequence=["#016F75", "#5DF6FE", "#019AA2","#B8FBFF", "#004447", "#0BF3FE"]
            )
            fig_pie_alm.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie_alm.update_layout(
                height=400,
                margin=dict(t=30, b=30, l=20, r=20),
                plot_bgcolor=plot_bg,
                paper_bgcolor=paper_bg,
                font=dict(color=font_color)
            )
            st.plotly_chart(fig_pie_alm, use_container_width=True)
    
    st.markdown("---")

    #--- Historical Evolution CHART ---
    with st.container(border=True):
        st.markdown(f'<div style="font-size: 20px; font-weight: bold; margin: 5; color: {font_color} !important;">Evolución histórica total de Registros y Almacenamiento</div>', unsafe_allow_html=True)
        df_evolucion = df_historia.groupby(['ID_corte', 'fecha_corte']).agg(
            total_registros=('r_registros', 'sum'),
            total_almacenamiento=('r_almacenamiento', 'sum')
        ).reset_index().sort_values('ID_corte', ascending=True)

        fig_evolucion = go.Figure()
        fig_evolucion.add_trace(go.Scatter(
            x=df_evolucion['fecha_corte'], y=df_evolucion['total_registros'], mode='lines+markers',
            name='Registros', line=dict(color='#01c2cb', width=4)
        ))
        fig_evolucion.add_trace(go.Scatter(
            x=df_evolucion['fecha_corte'], y=df_evolucion['total_almacenamiento'], mode='lines+markers',
            name='Almacenamiento (GB)', line=dict(color='#A3B18A', width=4), yaxis='y2'
        ))
        fig_evolucion.update_layout(
            height=500,
            xaxis=dict(title="Fecha de Corte", gridcolor=grid_color),
            yaxis=dict(title="Total de Registros", title_font=dict(color='#01c2cb'), tickfont=dict(color='#01c2cb'), gridcolor=grid_color),
            yaxis2=dict(title="Total de Almacenamiento (GB)", title_font=dict(color='#A3B18A'), tickfont=dict(color='#A3B18A'), overlaying='y', side='right', gridcolor=grid_color),
            hovermode="x unified",
            legend=dict(x=0, y=1.1, orientation="h"),
            plot_bgcolor=plot_bg, paper_bgcolor=paper_bg, font=dict(color=font_color)
        )
        st.plotly_chart(fig_evolucion, use_container_width=True)

    st.markdown("---")

    col_treemap, col_tabla = st.columns((1, 1))

    with col_treemap:
        with st.container(border=True):
            st.markdown(f'<div style="font-size: 20px; font-weight: bold; margin: 5; color: {font_color} !important;">Detalle por Categoría y Subcategoría</div>', unsafe_allow_html=True)
            df_treemap = df_ultimo_corte.groupby(["categoría", "sub_categoría"])["r_registros"].sum().reset_index()
            fig_treemap = px.treemap(
                df_treemap,
                path=['categoría', 'sub_categoría'],
                values='r_registros',
                color='r_registros',
                color_continuous_scale='Mint',
                title=None
            )
            fig_treemap.update_layout(
                height=500,
                margin=dict(t=30, b=30, l=20, r=20),
                plot_bgcolor=plot_bg, paper_bg=paper_bg, font=dict(color=font_color)
            )
            st.plotly_chart(fig_treemap, use_container_width=True)

    #Detailed Data Table
    with col_tabla:
        with st.container(border=True):
            st.markdown(f'<div style="font-size: 20px; font-weight: bold; margin: 5; color: {font_color} !important;">Tabla de Datos del Último Corte</div>', unsafe_allow_html=True)
            df_display = df_ultimo_corte[["categoría", "sub_categoría", "r_registros", "r_archivos", "r_almacenamiento"]].copy()
            df_display.rename(columns={
                "categoría": "Categoría", "sub_categoría": "Subcategoría", "r_registros": "Registros",
                "r_archivos": "Archivos", "r_almacenamiento": "Almacenamiento (GB)"
            }, inplace=True)
            df_display['Registros'] = df_display['Registros'].apply(lambda x: f'{x:,.0f}')
            df_display['Archivos'] = df_display['Archivos'].apply(lambda x: f'{x:,.0f}')
            df_display['Almacenamiento (GB)'] = df_display['Almacenamiento (GB)'].apply(lambda x: f'{x:,.2f}')
            
            st.dataframe(df_display, use_container_width=True, hide_index=True, height=500)

def main():
    st.sidebar.title("Menú")
    
    GIDS["Dashboard General"] = "general" 
    AUTORES["Dashboard General"] = "Equipo de Datos"

    if 'page' not in st.session_state:
        st.session_state.page = "Dashboard General"

    for page_name in GIDS.keys():
        if st.sidebar.button(page_name, key=page_name):
            st.session_state.page = page_name

    current_page = st.session_state.page
    

    if current_page == "Dashboard General":
        show_general_dashboard(current_page, AUTORES[current_page])
    else:
        gid = GIDS[current_page]
        autor = AUTORES[current_page]
        show_dashboard(current_page, gid, autor)

if __name__ == "__main__":
    main()