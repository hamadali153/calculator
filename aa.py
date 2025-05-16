import streamlit as st
import re
import pandas as pd

st.set_page_config(page_title="Value Separator", layout="wide")

# ----------------------- Custom Dark Theme (Glassmorphism) -----------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins&display=swap');

    body, .css-1d391kg, .css-1d391kg h1 {
        background: #0a0a0a !important;
        color: #eee !important;
        font-family: 'Poppins', sans-serif;
    }

    .css-1hynsf2 {
        background: rgba(30, 30, 30, 0.4) !important;
        backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(255, 170, 0, 0.15);
        box-shadow: 0 8px 32px 0 rgba(255, 170, 0, 0.1);
        padding: 20px;
        margin-bottom: 24px;
    }

    .css-1d391kg h1 {
        color: #ffb74d !important;
        font-weight: 700;
        letter-spacing: 2px;
        text-shadow: 0 0 6px #ff8c00;
        margin-bottom: 1rem;
    }

    .css-1d391kg p, .css-1d391kg div.stMarkdown > p {
        font-size: 1.1rem;
        color: #ddd !important;
    }

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

    .stDataFrame th {
        background: rgba(255, 170, 0, 0.3) !important;
        color: #0a0a0a !important;
        font-weight: 700;
        font-size: 1rem !important;
        backdrop-filter: blur(10px);
    }

    .stDataFrame tbody tr {
        background: rgba(40, 40, 40, 0.3);
        transition: background-color 0.3s ease;
    }

    .stDataFrame tbody tr:hover {
        background-color: rgba(255, 140, 0, 0.25) !important;
        color: #fff !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------- App Title -----------------------
st.title("🔢 Value Separator and Calculator")
st.markdown("Paste your values below. Lines with `+` will be separated and summed.")

# ----------------------- Session State -----------------------
if "processed" not in st.session_state:
    st.session_state.processed = False
if "positive_lines" not in st.session_state:
    st.session_state.positive_lines = []
if "other_lines" not in st.session_state:
    st.session_state.other_lines = []

# ----------------------- Data Processing Function -----------------------
def extract_table_data(lines):
    data = []
    for line in lines:
        # Skip empty lines
        if not line.strip():
            continue
        match = re.search(r"[+]?(-?\d+)", line.replace(",", ""))
        if match:
            amount = int(match.group(1))
            data.append({"Entry": line, "Amount": amount})
    return pd.DataFrame(data) if data else pd.DataFrame(columns=["Entry", "Amount"])

# ----------------------- Input Area -----------------------
text_input = st.text_area("Enter values here:", height=300)

# ----------------------- Start Processing -----------------------
if st.button("🚀 Start Processing"):
    if not text_input.strip():
        st.warning("Please provide some input to process.")
    else:
        lines = text_input.strip().splitlines()
        st.session_state.positive_lines = [line.strip() for line in lines if line.strip().startswith("+")]
        st.session_state.other_lines = [line.strip() for line in lines if not line.strip().startswith("+")]
        st.session_state.processed = True

# ----------------------- Show DataFrames -----------------------
if st.session_state.processed:
    pos_df = extract_table_data(st.session_state.positive_lines)
    other_df = extract_table_data(st.session_state.other_lines)

    if not pos_df.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("✅ Positive (+) Entries")
            st.dataframe(pos_df.sort_values(by="Amount", ascending=False), use_container_width=True)
        with col2:
            st.subheader("🔻 Other Entries")
            st.dataframe(other_df.sort_values(by="Amount", ascending=False), use_container_width=True)
    else:
        if not other_df.empty:
            st.subheader("📊 All Entries")
            st.dataframe(other_df.sort_values(by="Amount", ascending=False), use_container_width=True)

    if st.button("🧮 Calculate Totals"):
        positive_sum = pos_df["Amount"].sum() if not pos_df.empty else 0
        other_sum = other_df["Amount"].sum() if not other_df.empty else 0
        
        if not pos_df.empty:
            st.success(f"**Total of Positive (+) Values:** RS {positive_sum:,}")
            if not other_df.empty:
                st.warning(f"**Total of Other Values:** RS {other_sum:,}")
                st.info(f"**Grand Total:** RS {positive_sum + other_sum:,}")
        elif not other_df.empty:
            st.success(f"**Total of All Values:** RS {other_sum:,}")
        else:
            st.warning("No valid numerical values found to calculate totals.")
