import streamlit as st
import plotly.express as px
import pandas as pd
from data_loader import load_data
import plotly.graph_objects as go
from styles import get_custom_css


def show_dashboard(page_title, gid, autor):
    df_historia, fecha_dict = load_data(gid)

    is_dark_mode = st.get_option("theme.base") == "dark"
    st.markdown(get_custom_css(is_dark_mode), unsafe_allow_html=True)
    
    font_color = "#E0E0E0" if is_dark_mode else "#4a4a4a"
    border_color = "#3A3A3A" if is_dark_mode else "#E0E0E0"
    
    plot_bg = "rgba(0,0,0,0)"
    paper_bg = "rgba(0,0,0,0)"
    grid_color = "#3A3A3A" if is_dark_mode else "#E0E0E0"

    st.markdown(f"<h3>{page_title}</h3>", unsafe_allow_html=True)

    col_encargado, col_tarjetas = st.columns((1, 3))
    with col_encargado:
        st.markdown(
            f'<div style="font-size: 16px; font-weight: bold;">{autor}</div>',
            unsafe_allow_html=True
        )
        df_filtrado = pd.DataFrame(columns=["r_registros", "r_archivos", "r_almacenamiento", "sub_categoria"])
        fecha_sel = None
        if fecha_dict:
            fechas_ordenadas_por_id = sorted(fecha_dict, key=fecha_dict.get, reverse=True)
            fecha_sel = st.selectbox("Fecha de corte:", fechas_ordenadas_por_id)
            id_sel = fecha_dict[fecha_sel]
            df_filtrado = df_historia[df_historia["ID_corte"] == id_sel]
        else:
            st.warning("No se encontraron datos para mostrar.")

    total_registros = df_filtrado["r_registros"].sum()
    total_archivos = df_filtrado["r_archivos"].sum()
    total_almacenamiento = df_filtrado["r_almacenamiento"].sum()
    
    delta_registros_porcentual = 0
    if fecha_dict and fecha_sel:
        fechas_ordenadas_por_id = sorted(fecha_dict, key=fecha_dict.get, reverse=True)
        idx_fecha_sel = fechas_ordenadas_por_id.index(fecha_sel)
        if idx_fecha_sel + 1 < len(fechas_ordenadas_por_id):
            fecha_anterior = fechas_ordenadas_por_id[idx_fecha_sel + 1]
            id_anterior = fecha_dict[fecha_anterior]
            df_anterior = df_historia[df_historia["ID_corte"] == id_anterior]
            total_registros_anterior = df_anterior["r_registros"].sum()
            if total_registros_anterior != 0:
                delta_registros_porcentual = ((total_registros - total_registros_anterior) / total_registros_anterior) * 100

    with col_tarjetas:
        st.markdown(f"""
        <div class="metrics-container">
            <div class="metric-card">
                <div class="metric-info">
                    <div class="metric-value">{total_registros:,}</div>
                    <div class="metric-label">Registros</div>
                </div>
                <div class="metric-icon"><i class="fa-solid fa-file-lines"></i></div>
            </div>
            <div class="metric-card">
                <div class="metric-info">
                    <div class="metric-value">{total_archivos:,}</div>
                    <div class="metric-label">Archivos</div>
                </div>
                <div class="metric-icon"><i class="fa-solid fa-folder"></i></div>
            </div>
            <div class="metric-card">
                <div class="metric-info">
                    <div class="metric-value">{total_almacenamiento:,.2f} GB</div>
                    <div class="metric-label">Almacenamiento</div>
                </div>
                <div class="metric-icon"><i class="fa-solid fa-hard-drive"></i></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    col_resumen, col_rendimiento = st.columns((1, 3))
    with col_resumen:
        with st.container(border=True):
            st.markdown(
                f"""
                <div style="font-size: 20px; font-weight: bold; margin: 5; color: {font_color} !important;">Resumen por Sub Categorias</div>
                <div style="height: 20px;"></div>
                """,
                unsafe_allow_html=True
            )
            

            st.markdown(f"""
            <div class="grid-header">
                <div>Subcategoría</div>
                <div style="text-align: right;">Reg.</div>
                <div style="text-align: right;">Arch.</div>
                <div style="text-align: right;">Alm.</div>
            </div>
            """, unsafe_allow_html=True)
            
            for _, row in df_filtrado.iterrows():
                st.markdown(f"""
                <div class="grid-row">
                    <div style="color: #01c2cb !important; font-weight: bold;">{row['sub_categoria']}</div>
                    <div style="text-align: right;">{row['r_registros']:,}</div>
                    <div style="text-align: right;">{row['r_archivos']:,}</div>
                    <div style="text-align: right;">{row['r_almacenamiento']:,.1f} GB</div>
                </div>
                """, unsafe_allow_html=True)
            

        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="
            border: 1px solid {border_color};
            border-radius: 0.5rem;
            padding: 0;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        ">
            <div style="
                background-color: #01c2cb;
                padding: 20px;
                height: 375px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                color: white;
                width: 100%;
                margin: 0;
            ">
                <h4 style="color: white; margin: 0 0 5px 0; padding: 0; font-size: 20px;">Crecimiento de Registros</h4>
                <div style="font-size: 4em; font-weight: bold; margin: 5px 0;">{total_registros:,.0f}</div>
                <div style="
                    font-size: 20px;
                    font-weight: bold;
                    display: flex;
                    align-items: center;
                    gap: 5px;
                ">
                    <div style="color: white; font-size: 20px; padding: 0; font-weight: normal">Cambio vs. Periodo Anterior:</div>
                    <div style="
                        font-size: 20px; 
                        font-weight: bold; 
                        color: {'green' if delta_registros_porcentual >= 0 else 'red'} !important;
                    ">{delta_registros_porcentual:,.2f}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_rendimiento:
        with st.container(border=True):
            st.markdown(f'<div style="font-size: 20px; font-weight: bold; margin: 5; color: {font_color} !important;">Evolución histórica de registros</div>', unsafe_allow_html=True)
            df_linea = df_historia.groupby(['ID_corte', 'fecha_corte'])['r_registros']\
                                 .sum().reset_index(name='Registros')\
                                 .sort_values('ID_corte', ascending=True)
            fig_linea = px.line(df_linea, x='fecha_corte', y='Registros', markers=True,
                                 line_shape='linear', color_discrete_sequence=['#01c2cb'])
            fig_linea.update_traces(line=dict(width=4), fill='tozeroy', fillcolor='rgba(1, 194, 203, 0.2)', mode='lines+markers')
            fig_linea.update_layout(
                height=400, 
                xaxis_title="Fecha de Corte", 
                yaxis_title="Cantidad de Registros",
                hovermode="x unified", 
                plot_bgcolor=plot_bg,
                paper_bgcolor=paper_bg,
                font=dict(color=font_color),
                title_font=dict(color='rgba(0,0,0,0)'),
                xaxis=dict(gridcolor=grid_color),
                yaxis=dict(gridcolor=grid_color)
            )
            st.plotly_chart(fig_linea, use_container_width=True)

        subcol1, subcol2 = st.columns((1.5, 1.5))

        with subcol1:
            with st.container(border=True):
                st.markdown(f'<div style="font-size: 20px; font-weight: bold; margin: 5; color: {font_color} !important;">Distribución de registros por subcategoría</div>', unsafe_allow_html=True)
                umbral = 0.05
                df_pie = df_filtrado[["sub_categoria", "r_registros"]].copy()
                df_pie.rename(columns={"sub_categoria": "Subcategoría", "r_registros": "Registros"}, inplace=True)
                total = df_pie["Registros"].sum()
                df_pie["Porcentaje"] = df_pie["Registros"] / total
                grandes = df_pie[df_pie["Porcentaje"] >= umbral]
                pequeñas = df_pie[df_pie["Porcentaje"] < umbral]
                df_final_pie = (
                    pd.concat([grandes[["Subcategoría", "Registros"]],
                                pd.DataFrame({"Subcategoría": ["Otros"], "Registros": [pequeñas["Registros"].sum()]})],
                                ignore_index=True)
                    if not pequeñas.empty
                    else grandes[["Subcategoría", "Registros"]]
                )
                fig_pie = px.pie(df_final_pie, names="Subcategoría", values="Registros", hole=0.4,
                                 color_discrete_sequence=["#016F75", "#5DF6FE", "#019AA2","#B8FBFF", "#004447", "#0BF3FE"])
                fig_pie.update_layout(
                    height=400, 
                    margin=dict(t=30, b=30, l=20, r=20),
                    plot_bgcolor=plot_bg,
                    paper_bgcolor=paper_bg,
                    font=dict(color=font_color)
                )
                st.plotly_chart(fig_pie, use_container_width=True)

        with subcol2:
            with st.container(border=True):
                st.markdown(f'<div style="font-size: 20px; font-weight: bold; margin: 5; color: {font_color} !important;">Almacenamiento utilizado por subcategoría</div>', unsafe_allow_html=True)
                
                df_barras = df_filtrado[df_filtrado['sub_categoria'].notna() & (df_filtrado['sub_categoria'].str.strip() != '')]
                
                if df_barras.empty:
                    st.info("No hay datos disponibles para mostrar el gráfico de almacenamiento por subcategoría.")
                else:
                    fig_barras_2 = px.bar(df_barras, x="sub_categoria", y="r_almacenamiento", color_discrete_sequence=['#01c2cb'])
                    fig_barras_2.update_layout(
                        title=None, 
                        height=400, 
                        margin=dict(t=30, b=30, l=20, r=20),
                        xaxis_title="Subcategoría", 
                        yaxis_title="Almacenamiento (GB)",
                        plot_bgcolor=plot_bg,
                        paper_bgcolor=paper_bg,
                        font=dict(color=font_color),
                        title_font=dict(color='rgba(0,0,0,0)'),
                        hovermode="x unified",
                        xaxis=dict(gridcolor=grid_color),
                        yaxis=dict(gridcolor=grid_color)
                    )
                    st.plotly_chart(fig_barras_2, use_container_width=True)