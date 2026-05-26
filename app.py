import streamlit as st
from ecosystem_logic import *

st.set_page_config(page_title="Ecosystem Game")

# -------------------
# INITIAL STATE
# -------------------

if "oxygen" not in st.session_state:

    st.session_state.oxygen = 50
    st.session_state.co2 = 40
    st.session_state.biodiversity = 0.0

    st.session_state.bottom = [EMPTY] * MAX_BOTTOM_PATCHES
    st.session_state.birds = [EMPTY] * MAX_BIRD_PATCHES

# -------------------
# TITLE
# -------------------

st.title("🌍 Ecosystem Game")

# -------------------
# METRICS
# -------------------

col1, col2, col3 = st.columns(3)

col1.metric("Oxygen", int(st.session_state.oxygen))
col2.metric("CO2", int(st.session_state.co2))
col3.metric(
    "Biodiversity",
    f"{st.session_state.biodiversity*100:.1f}%"
)

# -------------------
# BUTTONS
# -------------------

st.subheader("Add Organisms")

c1, c2, c3, c4 = st.columns(4)

if c1.button("🌳 Tree"):
    for i in range(MAX_BOTTOM_PATCHES):
        if st.session_state.bottom[i] == EMPTY:
            st.session_state.bottom[i] = TREE
            break

if c2.button("💧 Lake"):
    for i in range(MAX_BOTTOM_PATCHES):
        if st.session_state.bottom[i] == EMPTY:
            st.session_state.bottom[i] = LAKE
            break

if c3.button("🦖 Dino"):
    for i in range(MAX_BOTTOM_PATCHES):
        if st.session_state.bottom[i] == EMPTY:
            st.session_state.bottom[i] = DINO
            break

if c4.button("🦅 Bird"):
    for i in range(MAX_BIRD_PATCHES):
        if st.session_state.birds[i] == EMPTY:
            st.session_state.birds[i] = BIRD
            break

# -------------------
# UPDATE BUTTON
# -------------------

if st.button("Run Simulation Step"):
    state = {
        "oxygen": st.session_state.oxygen,
        "co2": st.session_state.co2,
        "biodiversity": st.session_state.biodiversity,
        "bottom": st.session_state.bottom,
        "birds": st.session_state.birds,
    }

    state = update_ecosystem(state)

    st.session_state.oxygen = state["oxygen"]
    st.session_state.co2 = state["co2"]
    st.session_state.biodiversity = state["biodiversity"]

# -------------------
# SHOW ECOSYSTEM
# -------------------

st.subheader("Bottom Layer")
st.write(st.session_state.bottom)

st.subheader("Bird Layer")
st.write(st.session_state.birds)