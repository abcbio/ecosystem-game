import streamlit as st
import time

# ------------------------
# Constants
# ------------------------
MAX_BOTTOM = 12
MAX_BIRDS = 12

TREE_O2, LAKE_O2, DINO_O2, BIRD_O2 = 0.8, 0.5, -1.0, -0.4
DINO_CO2, BIRD_CO2, TREE_CO2, LAKE_CO2 = 1.2, 0.4, -0.8, -0.5

ROUND_DURATION = 20

# ------------------------
# Session state init
# ------------------------
def init():
    st.session_state.oxygen = 50
    st.session_state.co2 = 40
    st.session_state.trees = 0
    st.session_state.lakes = 0
    st.session_state.dinos = 0
    st.session_state.birds = 0
    st.session_state.running = False
    st.session_state.start_time = None
    st.session_state.leaderboard = []
    st.session_state.name_input = ""

if "oxygen" not in st.session_state:
    init()

# ------------------------
# Title
# ------------------------
st.title("🌍 Ecosystem Game")

# ------------------------
# Start button
# ------------------------
if st.button("▶ START GAME"):
    init()
    st.session_state.running = True
    st.session_state.start_time = time.time()

# ------------------------
# Controls
# ------------------------
st.subheader("Controls")

c1, c2, c3, c4 = st.columns(4)

# Trees
with c1:
    st.write("🌳 Trees")
    if st.button("+", key="t_plus"):
        st.session_state.trees = min(MAX_BOTTOM, st.session_state.trees + 1)
    if st.button("-", key="t_minus"):
        st.session_state.trees = max(0, st.session_state.trees - 1)

# Lakes
with c2:
    st.write("💧 Lakes")
    if st.button("+", key="l_plus"):
        st.session_state.lakes = min(MAX_BOTTOM, st.session_state.lakes + 1)
    if st.button("-", key="l_minus"):
        st.session_state.lakes = max(0, st.session_state.lakes - 1)

# Dinos
with c3:
    st.write("🦖 Dinos")
    if st.button("+", key="d_plus"):
        st.session_state.dinos = min(MAX_BOTTOM, st.session_state.dinos + 1)
    if st.button("-", key="d_minus"):
        st.session_state.dinos = max(0, st.session_state.dinos - 1)

# Birds
with c4:
    st.write("🐦 Birds")
    if st.button("+", key="b_plus"):
        st.session_state.birds = min(MAX_BIRDS, st.session_state.birds + 1)
    if st.button("-", key="b_minus"):
        st.session_state.birds = max(0, st.session_state.birds - 1)

# ------------------------
# Game update
# ------------------------
if st.session_state.running:

    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, int(ROUND_DURATION - elapsed))

    # Update gases
    st.session_state.oxygen += (
        st.session_state.trees * TREE_O2 +
        st.session_state.lakes * LAKE_O2 +
        st.session_state.dinos * DINO_O2 +
        st.session_state.birds * BIRD_O2
    )

    st.session_state.co2 += (
        st.session_state.dinos * DINO_CO2 +
        st.session_state.birds * BIRD_CO2 +
        st.session_state.trees * TREE_CO2 +
        st.session_state.lakes * LAKE_CO2
    )

    # Clamp values
    st.session_state.oxygen = max(0, min(100, st.session_state.oxygen))
    st.session_state.co2 = max(0, min(100, st.session_state.co2))

    # Death conditions
    if st.session_state.oxygen < 10 or st.session_state.co2 > 80:
        st.session_state.dinos = max(0, st.session_state.dinos - 1)

    if st.session_state.oxygen < 20 or st.session_state.co2 > 60:
        st.session_state.birds = max(0, st.session_state.birds - 1)

    biodiversity = (
        st.session_state.birds + st.session_state.dinos
    ) / (MAX_BIRDS + MAX_BOTTOM)

    # ------------------------
    # Display stats
    # ------------------------
    st.subheader("Game State")

    st.write(f"⏱ Time left: {remaining}s")

    st.progress(int(st.session_state.oxygen),
                text=f"Oxygen: {int(st.session_state.oxygen)}")

    st.progress(int(st.session_state.co2),
                text=f"CO₂: {int(st.session_state.co2)}")

    st.metric("🌱 Biodiversity", f"{biodiversity*100:.1f}%")

    # ------------------------
    # Visual ecosystem
    # ------------------------
    st.subheader("Ecosystem")

    ground = (
        ["🌳"] * st.session_state.trees +
        ["💧"] * st.session_state.lakes +
        ["🦖"] * st.session_state.dinos
    )

    sky = ["🐦"] * st.session_state.birds

    st.write("Ground layer:")
    st.write(" ".join(ground) if ground else "Empty")

    st.write("Sky layer:")
    st.write(" ".join(sky) if sky else "Empty")

    # ------------------------
    # End game
    # ------------------------
    if remaining <= 0:
        st.session_state.running = False
        st.success("✅ Round finished!")

        st.session_state.name_input = st.text_input(
            "Enter your name", value=st.session_state.name_input
        )

        if st.button("Save score"):
            st.session_state.leaderboard.append(
                (st.session_state.name_input or "NoName", biodiversity)
            )
            st.session_state.leaderboard.sort(
                key=lambda x: x[1], reverse=True
            )

# ------------------------
# Leaderboard
# ------------------------
st.subheader("🏆 Leaderboard")

if st.session_state.leaderboard:
    for i, (name, score) in enumerate(st.session_state.leaderboard[:10]):
        st.write(f"{i+1}. {name} — {score*100:.1f}%")
else:
    st.write("No scores yet.")
