import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Page configuration
st.set_page_config(
    page_title="Student Selection Dashboard",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS - Gray theme, minimal colors
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .main {
        background-color: #f5f7fa;
    }

    .block-container {
        padding-top: 3rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* Header */
    .dashboard-header {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: white;
        padding: 2rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .dashboard-header h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: 600;
        color: white;
    }

    .dashboard-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-size: 1rem;
    }

    /* Metrics */
    .stMetric {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #2c3e50;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }

    .stMetric label {
        color: #64748b !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .stMetric [data-testid="stMetricValue"] {
        color: #1e293b;
        font-size: 2rem;
        font-weight: 600;
    }

    /* Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border-left: 4px solid #64748b;
        margin-bottom: 1rem;
    }

    .metric-card h3 {
        margin: 0;
        color: #64748b;
        font-size: 0.875rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .metric-card h2 {
        margin: 0.5rem 0 0 0;
        color: #1e293b;
        font-size: 2rem;
        font-weight: 600;
        border: none;
    }

    .metric-card p {
        margin: 0.25rem 0 0 0;
        color: #94a3b8;
        font-size: 0.875rem;
    }

    /* Student Cards */
    .student-card {
        background: white;
        padding: 1rem 1.25rem;
        margin: 0.5rem 0;
        border-radius: 6px;
        border-left: 3px solid #cbd5e1;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }

    .student-card:hover {
        border-left-color: #2c3e50;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .student-card h4 {
        margin: 0;
        color: #1e293b;
        font-size: 1rem;
        font-weight: 600;
    }

    .student-card p {
        margin: 0.25rem 0 0 0;
        color: #64748b;
        font-size: 0.875rem;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background-color: white;
        border-radius: 8px;
        padding: 0.25rem;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 0.75rem 1.5rem;
        color: #64748b;
        font-weight: 500;
        background-color: transparent;
    }

    .stTabs [aria-selected="true"] {
        background-color: #2c3e50;
        color: white;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1e293b;
        padding-top: 2rem;
    }

    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }

    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: white !important;
    }

    [data-testid="stSidebar"] .stRadio > label {
        font-weight: 500;
    }

    /* Buttons */
    .stButton > button {
        background-color: #2c3e50;
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background-color: #34495e;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* DataFrames */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }

    /* Headers */
    h1 {
        color: #1e293b;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    h2 {
        color: #1e293b;
        font-weight: 600;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }

    h3 {
        color: #475569;
        font-weight: 600;
    }

    /* Info boxes */
    .info-box {
        background-color: #f8fafc;
        border-left: 4px solid #64748b;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
    }

    .success-box {
        background-color: #f0fdf4;
        border-left: 4px solid #22c55e;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
    }

    .warning-box {
        background-color: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
    }

    /* Search input */
    .stTextInput > div > div > input {
        border-radius: 6px;
        border: 1px solid #cbd5e1;
        padding: 0.5rem 1rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #94a3b8;
        padding: 2rem 0;
        margin-top: 3rem;
        border-top: 1px solid #e2e8f0;
        font-size: 0.875rem;
    }

    /* Remove streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class='dashboard-header'>
        <h1>📋 Student Selection Results 2026</h1>
        <p>Alternance & Career Support Program - Official Results</p>
    </div>
""", unsafe_allow_html=True)


# Load data
@st.cache_data
def load_data():
    try:
        possible_paths = [
            'selected_students.csv',
            './selected_students.csv',
            os.path.join(os.getcwd(), 'selected_students.csv')
        ]

        selected_df = None
        for path in possible_paths:
            if os.path.exists(path):
                selected_df = pd.read_csv(path)
                waiting_df = pd.read_csv(path.replace('selected_students', 'waiting_list_students'))
                all_df = pd.read_csv(path.replace('selected_students', 'all_students_selected_and_waiting'))
                break

        if selected_df is None:
            raise FileNotFoundError("CSV files not found")

        return selected_df, waiting_df, all_df

    except FileNotFoundError:
        st.error("⚠️ CSV files not found. Please run the selection script first.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()


selected_df, waiting_df, all_df = load_data()

# Sidebar
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["Overview", "Selected Students", "Waiting List", "Statistics"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### Summary")

    st.markdown(f"""
        <div style='background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 6px; margin: 0.5rem 0;'>
            <p style='margin: 0; font-size: 0.75rem; opacity: 0.7; text-transform: uppercase; letter-spacing: 0.05em;'>Selected</p>
            <h2 style='margin: 0.25rem 0 0 0; font-size: 2rem; font-weight: 600; border: none;'>{len(selected_df)}</h2>
        </div>

        <div style='background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 6px; margin: 0.5rem 0;'>
            <p style='margin: 0; font-size: 0.75rem; opacity: 0.7; text-transform: uppercase; letter-spacing: 0.05em;'>Waiting List</p>
            <h2 style='margin: 0.25rem 0 0 0; font-size: 2rem; font-weight: 600; border: none;'>{len(waiting_df)}</h2>
        </div>

        <div style='background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 6px; margin: 0.5rem 0;'>
            <p style='margin: 0; font-size: 0.75rem; opacity: 0.7; text-transform: uppercase; letter-spacing: 0.05em;'>Total</p>
            <h2 style='margin: 0.25rem 0 0 0; font-size: 2rem; font-weight: 600; border: none;'>{len(all_df)}</h2>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Filters")

    filter_group = st.multiselect(
        "Group",
        options=all_df['Group'].unique(),
        default=all_df['Group'].unique()
    )

    filter_country = st.multiselect(
        "Country",
        options=all_df['Country'].unique(),
        default=all_df['Country'].unique()
    )

# Filter data
filtered_df = all_df[
    (all_df['Group'].isin(filter_group)) &
    (all_df['Country'].isin(filter_country))
    ]

# ==================== OVERVIEW PAGE ====================
if page == "Overview":
    st.markdown("## Overview")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        data_count = len(selected_df[selected_df['Group'] == 'Data'])
        data_waiting = len(waiting_df[waiting_df['Group'] == 'Data'])
        st.markdown(f"""
            <div class='metric-card'>
                <h3>Data</h3>
                <h2>{data_count}</h2>
                <p>+{data_waiting} waiting</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        cyber_count = len(selected_df[selected_df['Group'] == 'Cybersecurity/Development'])
        cyber_waiting = len(waiting_df[waiting_df['Group'] == 'Cybersecurity/Development'])
        st.markdown(f"""
            <div class='metric-card'>
                <h3>Cyber/Dev</h3>
                <h2>{cyber_count}</h2>
                <p>+{cyber_waiting} waiting</p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        other_count = len(selected_df[selected_df['Group'] == 'Other Fields'])
        other_waiting = len(waiting_df[waiting_df['Group'] == 'Other Fields'])
        st.markdown(f"""
            <div class='metric-card'>
                <h3>Other Fields</h3>
                <h2>{other_count}</h2>
                <p>+{other_waiting} waiting</p>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div class='metric-card' style='border-left-color: #2c3e50;'>
                <h3>Total Selected</h3>
                <h2>{len(selected_df)}</h2>
                <p>students</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        status_counts = all_df['Status'].value_counts()
        fig_status = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Selection Status",
            color_discrete_map={'Selected': '#2c3e50', 'Waiting List': '#64748b'},
            hole=0.5
        )
        fig_status.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont_size=13,
            marker=dict(line=dict(color='white', width=2))
        )
        fig_status.update_layout(
            font=dict(family="Inter, sans-serif", size=12, color='#1e293b'),
            title_font_size=16,
            title_font_weight=600,
            showlegend=False,
            paper_bgcolor='white',
            plot_bgcolor='white'
        )
        st.plotly_chart(fig_status, use_container_width=True)

    with col2:
        group_counts = selected_df['Group'].value_counts()
        fig_groups = px.bar(
            x=group_counts.index,
            y=group_counts.values,
            title="Selected by Group",
            labels={'x': '', 'y': 'Students'},
            color_discrete_sequence=['#2c3e50']
        )
        fig_groups.update_layout(
            font=dict(family="Inter, sans-serif", size=12, color='#1e293b'),
            title_font_size=16,
            title_font_weight=600,
            showlegend=False,
            paper_bgcolor='white',
            plot_bgcolor='white',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#f1f5f9')
        )
        fig_groups.update_traces(marker_line_color='white', marker_line_width=1.5)
        st.plotly_chart(fig_groups, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        edu_counts = all_df['Education Level'].value_counts()
        fig_edu = px.bar(
            x=edu_counts.index,
            y=edu_counts.values,
            title="Education Level Distribution",
            labels={'x': '', 'y': 'Students'},
            color_discrete_sequence=['#475569']
        )
        fig_edu.update_layout(
            font=dict(family="Inter, sans-serif", size=12, color='#1e293b'),
            title_font_size=16,
            title_font_weight=600,
            showlegend=False,
            paper_bgcolor='white',
            plot_bgcolor='white',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#f1f5f9')
        )
        fig_edu.update_traces(marker_line_color='white', marker_line_width=1.5)
        st.plotly_chart(fig_edu, use_container_width=True)

    with col2:
        country_counts = all_df['Country'].value_counts()
        fig_country = px.pie(
            values=country_counts.values,
            names=country_counts.index,
            title="Country Distribution",
            color_discrete_sequence=['#2c3e50', '#64748b'],
            hole=0.5
        )
        fig_country.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont_size=13,
            marker=dict(line=dict(color='white', width=2))
        )
        fig_country.update_layout(
            font=dict(family="Inter, sans-serif", size=12, color='#1e293b'),
            title_font_size=16,
            title_font_weight=600,
            showlegend=False,
            paper_bgcolor='white',
            plot_bgcolor='white'
        )
        st.plotly_chart(fig_country, use_container_width=True)

    # Stacked bar
    st.markdown("### Group Analysis")
    group_status = pd.crosstab(all_df['Group'], all_df['Status'])
    fig_stacked = go.Figure(data=[
        go.Bar(
            name='Selected',
            x=group_status.index,
            y=group_status['Selected'],
            marker_color='#2c3e50',
            marker_line_color='white',
            marker_line_width=1.5
        ),
        go.Bar(
            name='Waiting List',
            x=group_status.index,
            y=group_status['Waiting List'],
            marker_color='#64748b',
            marker_line_color='white',
            marker_line_width=1.5
        )
    ])
    fig_stacked.update_layout(
        barmode='stack',
        font=dict(family="Inter, sans-serif", size=12, color='#1e293b'),
        title_font_size=16,
        title_font_weight=600,
        paper_bgcolor='white',
        plot_bgcolor='white',
        xaxis=dict(title='', showgrid=False),
        yaxis=dict(title='Students', showgrid=True, gridcolor='#f1f5f9'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_stacked, use_container_width=True)

# ==================== SELECTED STUDENTS PAGE ====================
elif page == "Selected Students":
    st.markdown("## Selected Students")

    st.markdown(f"""
        <div class='success-box'>
            <strong>Congratulations!</strong> {len(selected_df)} students have been selected for the program.
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["Data", "Cybersecurity/Development", "Other Fields", "All"])

    with tab1:
        data_selected = selected_df[selected_df['Group'] == 'Data'].sort_values('Name')
        st.markdown(f"**{len(data_selected)} students**")
        st.markdown("<br>", unsafe_allow_html=True)

        for idx, row in data_selected.iterrows():
            st.markdown(f"""
                <div class='student-card'>
                    <h4>{row['Name']}</h4>
                    <p>{row['Specialization']} • {row['Education Level']} • {row['Country']}</p>
                </div>
            """, unsafe_allow_html=True)

    with tab2:
        cyber_selected = selected_df[selected_df['Group'] == 'Cybersecurity/Development'].sort_values('Name')
        st.markdown(f"**{len(cyber_selected)} students**")
        st.markdown("<br>", unsafe_allow_html=True)

        for idx, row in cyber_selected.iterrows():
            st.markdown(f"""
                <div class='student-card'>
                    <h4>{row['Name']}</h4>
                    <p>{row['Specialization']} • {row['Education Level']} • {row['Country']}</p>
                </div>
            """, unsafe_allow_html=True)

    with tab3:
        other_selected = selected_df[selected_df['Group'] == 'Other Fields'].sort_values('Name')
        st.markdown(f"**{len(other_selected)} students**")
        st.markdown("<br>", unsafe_allow_html=True)

        for idx, row in other_selected.iterrows():
            st.markdown(f"""
                <div class='student-card'>
                    <h4>{row['Name']}</h4>
                    <p>{row['Specialization']} • {row['Education Level']} • {row['Country']}</p>
                </div>
            """, unsafe_allow_html=True)

    with tab4:
        all_selected_sorted = selected_df.sort_values('Name')
        st.markdown(f"**{len(selected_df)} students**")

        search = st.text_input("Search by name", "", placeholder="Enter student name...")

        if search:
            filtered_selected = all_selected_sorted[
                all_selected_sorted['Name'].str.contains(search, case=False, na=False)]
        else:
            filtered_selected = all_selected_sorted

        st.markdown(
            f"<p style='color: #64748b; font-size: 0.875rem;'>Showing {len(filtered_selected)} of {len(selected_df)} students</p>",
            unsafe_allow_html=True)

        for idx, row in filtered_selected.iterrows():
            st.markdown(f"""
                <div class='student-card'>
                    <h4>{row['Name']}</h4>
                    <p>{row['Group']} • {row['Specialization']} • {row['Education Level']} • {row['Country']}</p>
                </div>
            """, unsafe_allow_html=True)

# ==================== WAITING LIST PAGE ====================
elif page == "Waiting List":
    st.markdown("## Waiting List")

    st.markdown(f"""
        <div class='warning-box'>
            <strong>Note:</strong> {len(waiting_df)} students are on the waiting list and will be contacted if positions become available.
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["Data", "Cybersecurity/Development", "Other Fields", "All"])

    with tab1:
        data_waiting = waiting_df[waiting_df['Group'] == 'Data'].sort_values('Name')
        st.markdown(f"**{len(data_waiting)} students**")
        st.markdown("<br>", unsafe_allow_html=True)

        for idx, row in data_waiting.iterrows():
            st.markdown(f"""
                <div class='student-card'>
                    <h4>{row['Name']}</h4>
                    <p>{row['Specialization']} • {row['Education Level']} • {row['Country']}</p>
                </div>
            """, unsafe_allow_html=True)

    with tab2:
        cyber_waiting = waiting_df[waiting_df['Group'] == 'Cybersecurity/Development'].sort_values('Name')
        st.markdown(f"**{len(cyber_waiting)} students**")
        st.markdown("<br>", unsafe_allow_html=True)

        for idx, row in cyber_waiting.iterrows():
            st.markdown(f"""
                <div class='student-card'>
                    <h4>{row['Name']}</h4>
                    <p>{row['Specialization']} • {row['Education Level']} • {row['Country']}</p>
                </div>
            """, unsafe_allow_html=True)

    with tab3:
        other_waiting = waiting_df[waiting_df['Group'] == 'Other Fields'].sort_values('Name')
        st.markdown(f"**{len(other_waiting)} students**")
        st.markdown("<br>", unsafe_allow_html=True)

        for idx, row in other_waiting.iterrows():
            st.markdown(f"""
                <div class='student-card'>
                    <h4>{row['Name']}</h4>
                    <p>{row['Specialization']} • {row['Education Level']} • {row['Country']}</p>
                </div>
            """, unsafe_allow_html=True)

    with tab4:
        all_waiting_sorted = waiting_df.sort_values('Name')
        st.markdown(f"**{len(waiting_df)} students**")

        search = st.text_input("Search by name", "", placeholder="Enter student name...", key="search_waiting")

        if search:
            filtered_waiting = all_waiting_sorted[all_waiting_sorted['Name'].str.contains(search, case=False, na=False)]
        else:
            filtered_waiting = all_waiting_sorted

        st.markdown(
            f"<p style='color: #64748b; font-size: 0.875rem;'>Showing {len(filtered_waiting)} of {len(waiting_df)} students</p>",
            unsafe_allow_html=True)

        for idx, row in filtered_waiting.iterrows():
            st.markdown(f"""
                <div class='student-card'>
                    <h4>{row['Name']}</h4>
                    <p>{row['Group']} • {row['Specialization']} • {row['Education Level']} • {row['Country']}</p>
                </div>
            """, unsafe_allow_html=True)

# ==================== STATISTICS PAGE ====================
elif page == "Statistics":
    st.markdown("## Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### By Group")
        group_stats = all_df.groupby(['Group', 'Status']).size().unstack(fill_value=0)
        st.dataframe(group_stats, use_container_width=True)

    with col2:
        st.markdown("### By Education")
        edu_stats = all_df.groupby(['Education Level', 'Status']).size().unstack(fill_value=0)
        st.dataframe(edu_stats, use_container_width=True)

    with col3:
        st.markdown("### By Country")
        country_stats = all_df.groupby(['Country', 'Status']).size().unstack(fill_value=0)
        st.dataframe(country_stats, use_container_width=True)

    st.markdown("---")

    st.markdown("### Specialization Breakdown")
    spec_stats = all_df.groupby(['Specialization', 'Group']).size().unstack(fill_value=0)
    fig_spec = px.bar(
        spec_stats,
        title="Students by Specialization and Group",
        barmode='stack',
        color_discrete_sequence=['#2c3e50', '#475569', '#64748b']
    )
    fig_spec.update_layout(
        font=dict(family="Inter, sans-serif", size=12, color='#1e293b'),
        title_font_size=16,
        title_font_weight=600,
        paper_bgcolor='white',
        plot_bgcolor='white',
        xaxis=dict(title='', showgrid=False),
        yaxis=dict(title='Students', showgrid=True, gridcolor='#f1f5f9'),
        legend=dict(title='Group')
    )
    fig_spec.update_traces(marker_line_color='white', marker_line_width=1.5)
    st.plotly_chart(fig_spec, use_container_width=True)

    st.markdown("### Summary Table")
    summary_stats = all_df.groupby(['Group', 'Status', 'Country']).size().reset_index(name='Count')
    st.dataframe(summary_stats, use_container_width=True, hide_index=True)

# Footer
st.markdown("""
    <div class='footer'>
        <p>Student Selection Dashboard 2026 | Alternance & Career Support Program</p>
        <p style='margin-top: 0.5rem; opacity: 0.7;'>Randomly selected for fairness and equal opportunity</p>
    </div>
""", unsafe_allow_html=True)