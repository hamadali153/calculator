import streamlit as st
import re
import pandas as pd

st.set_page_config(page_title="Value Separator", layout="wide")

# Glassmorphic Dark Theme CSS
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins&display=swap');

    /* Base body */
    body, .css-1d391kg, .css-1d391kg h1 {
        background: #0a0a0a !important;
        color: #eee !important;
        font-family: 'Poppins', sans-serif;
    }

    /* Frosted translucent panels */
    .css-1hynsf2 {
        background: rgba(30, 30, 30, 0.4) !important;
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(255, 170, 0, 0.15);
        box-shadow: 0 8px 32px 0 rgba(255, 170, 0, 0.1);
        padding: 20px;
        margin-bottom: 24px;
        transition: box-shadow 0.3s ease;
    }
    .css-1hynsf2:hover {
        box-shadow: 0 12px 48px 0 rgba(255, 111, 60, 0.3);
    }

    /* Titles */
    .css-1d391kg h1 {
        color: #ffb74d !important;
        font-weight: 700;
        letter-spacing: 2px;
        text-shadow: 0 0 6px #ff8c00;
        margin-bottom: 1rem;
    }

    /* Markdown text */
    .css-1d391kg p, .css-1d391kg div.stMarkdown > p {
        font-size: 1.1rem;
        color: #ddd !important;
    }

    /* Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #ff8c00, #ffaa00);
        border: none;
        color: #0a0a0a;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 12px 28px;
        border-radius: 18px;
        box-shadow: 0 4px 15px rgba(255, 170, 0, 0.3);
        cursor: pointer;
        transition: all 0.3s ease;
        font-family: 'Poppins', sans-serif;
        user-select: none;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #ffaa00, #ff8c00);
        color: #fff;
        box-shadow: 0 6px 25px rgba(255, 140, 0, 0.7);
        transform: translateY(-2px);
    }
    div.stButton > button:focus {
        outline: none;
        box-shadow: 0 0 16px 4px #ffaa00;
    }

    /* Dataframe container */
    .css-1hynsf2 > div[data-testid="stDataFrame"] {
        background: transparent !important;
        border-radius: 18px !important;
        padding: 0 !important;
        box-shadow: none !important;
    }

    /* Table headers */
    .stDataFrame th {
        background: rgba(255, 170, 0, 0.3) !important;
        color: #0a0a0a !important;
        font-weight: 700;
        font-size: 1rem !important;
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(255, 170, 0, 0.4) !important;
        user-select: none;
    }

    /* Table rows */
    .stDataFrame tbody tr {
        background: rgba(40, 40, 40, 0.3);
        transition: background-color 0.3s ease;
        cursor: default;
        user-select: none;
    }
    .stDataFrame tbody tr:hover {
        background-color: rgba(255, 140, 0, 0.25) !important;
        color: #fff !important;
    }

    /* Success and warning messages */
    .stAlert.success {
        background-color: rgba(255, 170, 0, 0.15) !important;
        color: #ffbb33 !important;
        border-left: 6px solid #ffaa00 !important;
        font-weight: 600;
        font-size: 1.1rem;
        font-family: 'Poppins', sans-serif;
        user-select: none;
    }
    .stAlert.warning {
        background-color: rgba(255, 140, 0, 0.15) !important;
        color: #ff9f00 !important;
        border-left: 6px solid #ff8c00 !important;
        font-weight: 600;
        font-size: 1.1rem;
        font-family: 'Poppins', sans-serif;
        user-select: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🔢 Value Separator and Calculator")
st.markdown(
    "Paste or write your values below. Lines with `+` will be separated from the rest."
)

if "processed" not in st.session_state:
    st.session_state.processed = False
if "positive_lines" not in st.session_state:
    st.session_state.positive_lines = []
if "other_lines" not in st.session_state:
    st.session_state.other_lines = []

user_input = st.text_area("Enter values here:", height=300)

if st.button("🚀 Start Processing"):
    if not user_input.strip():
        st.warning("Please enter some values to process.")
    else:
        lines = user_input.strip().splitlines()
        st.session_state.positive_lines = [
            line.strip() for line in lines if line.strip().startswith("+")
        ]
        st.session_state.other_lines = [
            line.strip() for line in lines if not line.strip().startswith("+")
        ]
        st.session_state.processed = True


def extract_table_data(lines):
    data = []
    for line in lines:
        match = re.match(r"[+]?(\d+)", line)
        amount = int(match.group(1)) if match else 0
        data.append({"Entry": line, "Amount": amount})
    return pd.DataFrame(data)


if st.session_state.processed:
    pos_df = extract_table_data(st.session_state.positive_lines)
    other_df = extract_table_data(st.session_state.other_lines)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✅ Positive (+) Entries")
        st.dataframe(pos_df.sort_values(by="Amount", ascending=False), use_container_width=True)
    with col2:
        st.subheader("🔻 Other Entries")
        st.dataframe(other_df.sort_values(by="Amount", ascending=False), use_container_width=True)

    if st.button("🧮 Calculate Totals"):
        positive_sum = pos_df["Amount"].sum()
        other_sum = other_df["Amount"].sum()
        st.success(f"**Total of Positive (+) Values:** RS {positive_sum:,}")
        st.warning(f"**Total of Other Values:** RS {other_sum:,}")
