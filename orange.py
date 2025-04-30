import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib

st.set_page_config(page_title="Hashed Ledger", layout="centered")

# Initialize session state
if 'ledger' not in st.session_state:
    st.session_state.ledger = pd.DataFrame(columns=["Date", "Description", "Amount", "Hash", "Prev_Hash"])

def compute_hash(date, description, amount, prev_hash):
    tx_str = f"{date}{description}{amount}{prev_hash}"
    return hashlib.sha256(tx_str.encode()).hexdigest()

st.title("🔐 Hashed Ledger App")

# --- Input Form ---
with st.form("transaction_form"):
    st.subheader("Add New Transaction")
    date = st.date_input("Date", value=datetime.today())
    description = st.text_input("Description")
    amount = st.number_input("Amount", format="%.2f")
    submit = st.form_submit_button("Add Transaction")

    if submit:
        prev_hash = st.session_state.ledger.iloc[-1]["Hash"] if not st.session_state.ledger.empty else "0"
        new_hash = compute_hash(str(date), description, amount, prev_hash)
        new_entry = {
            "Date": date,
            "Description": description,
            "Amount": amount,
            "Prev_Hash": prev_hash,
            "Hash": new_hash
        }
        st.session_state.ledger = pd.concat([
            st.session_state.ledger,
            pd.DataFrame([new_entry])
        ], ignore_index=True)
        st.success("Transaction added with hash!")

# --- Display Ledger ---
st.subheader("📋 Ledger with Hashes")
ledger = st.session_state.ledger.copy()
ledger["Running Balance"] = ledger["Amount"].cumsum()

st.dataframe(ledger, use_container_width=True)

# --- Summary ---
st.subheader("📊 Summary")
total = ledger["Amount"].sum()
st.metric("Current Balance", f"${total:,.2f}")
