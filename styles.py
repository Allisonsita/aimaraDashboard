def get_custom_css(is_dark_mode):
    if is_dark_mode:
        bg_color = "#262730"
        card_bg = "#2F313E"
        text_color = "#E0E0E0"
        sub_text_color = "#B0B0B0"
        border_color = "#3A3A3A"
        shadow = "rgba(0,0,0,0.4)"
    else:
        bg_color = "#FFFFFF"
        card_bg = "#FFFFFF"
        text_color = "#4a4a4a"
        sub_text_color = "#7c7c7c"
        border_color = "#E0E0E0"
        shadow = "rgba(0,0,0,0.08)"

    return f"""
    <style>
        /* Import a nice font if not already present, though Streamlit uses sans-serif by default */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}

        /* Container for metrics ensuring responsive grid */
        .metrics-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
            margin-top: 1rem;
        }}

        /* Individual Metric Card Style */
        .metric-card {{
            background-color: {card_bg};
            border: 1px solid {border_color};
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 12px {shadow};
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}

        .metric-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 24px {shadow};
        }}

        .metric-info {{
            display: flex;
            flex-direction: column;
        }}

        .metric-value {{
            font-size: 28px;
            font-weight: 700;
            color: {text_color};
            margin-bottom: 4px;
        }}

        .metric-label {{
            font-size: 14px;
            color: {sub_text_color};
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .metric-icon {{
            font-size: 32px;
            color: #01c2cb;
            opacity: 0.9;
            background: rgba(1, 194, 203, 0.1);
            padding: 12px;
            border-radius: 50%;
            height: 56px;
            width: 56px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        /* Data Grid / Subcategory Grid Styles */
        .data-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1rem;
        }}
        
        /* Custom Header for tables/grids */
        .grid-header {{
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1.2fr;
            padding: 12px 16px;
            background-color: {bg_color};
            border-bottom: 2px solid {border_color};
            color: {text_color};
            font-weight: 700;
            font-size: 14px;
            border-radius: 8px 8px 0 0;
        }}

        .grid-row {{
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1.2fr;
            padding: 12px 16px;
            background-color: {card_bg};
            border-bottom: 1px solid {border_color};
            color: {text_color};
            align-items: center;
            font-size: 14px;
            transition: background-color 0.1s;
        }}

        .grid-row:hover {{
            background-color: rgba(1, 194, 203, 0.05);
        }}

        .grid-row:last-child {{
            border-bottom: none;
            border-radius: 0 0 8px 8px;
        }}

    </style>
    """
