import streamlit as st
import pandas as pd
import os
# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Captain Sparrow's Lost Treasure",
    page_icon="🏴‍☠️",
    layout="wide"
)
# ---------------- SESSION STATE ----------------
defaults = {
    "started": False,
    "pirate_name": "",
    "step": 0,
    "score": 0,
    "clues_used": {1: False, 2: False, 3: False, 4: False, 5: False},
    "progress": {1: False, 2: False, 3: False, 4: False, 5: False},
    "error": "",
    "console": ">>> Ready...",
    "score_saved": False
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v
locations = [
    "⚓ Dock",
    "🧭 Camp",
    "🔑 Hideout",
    "🌴 Jungle",
    "🏛 Temple"
]
# ---------------- HELPERS ----------------
def use_clue(challenge_id, clue_text):
    if not st.session_state.clues_used[challenge_id]:
        st.session_state.clues_used[challenge_id] = True
        st.session_state.score -= 5
    st.session_state.console = f"""💡 CLUE:
{clue_text}
"""
def save_score():
    file = "scores.csv"
    new_data = pd.DataFrame([{
        "Pirate": st.session_state.pirate_name,
        "Score": st.session_state.score
    }])
    if os.path.exists(file):
        old = pd.read_csv(file)
        old = pd.concat([old, new_data], ignore_index=True)
        old.to_csv(file, index=False)
    else:
        new_data.to_csv(file, index=False)
def update_console(msg):
    st.session_state.console = msg
def reset_game():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
# ---------------- PIRATE THEME CSS ----------------
st.markdown("""
<style>
.stApp {
    background-color: #0B1F3A;
    color: white;
}
.main-title {
    text-align: center;
    font-size: 40px;
    color: #D4AF37;
    font-weight: bold;
    margin-bottom: 10px;
}
.card {
    background-color: #F5E8C7;
    color: black;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
}
.console {
    background-color: black;
    color: #00FF66;
    padding: 15px;
    border-radius: 10px;
    font-family: monospace;
    height: 300px;
    overflow-y: auto;
    white-space: pre-wrap;
}
button {
    background-color: #D4AF37 !important;
    color: black !important;
    border-radius: 8px !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)
# ---------------- TITLE ----------------
st.markdown('<div class="main-title">🏴‍☠️ Captain Sparrow\'s Lost Treasure</div>', unsafe_allow_html=True)
# ---------------- START SCREEN ----------------
if not st.session_state.started:
    st.markdown("""
    <div class="card">
    <h3>📜 Prologue</h3>
    Captain Sparrow hid a treasure worth millions on a mysterious island.<br><br>
    He split his treasure map into five pieces and hid them across the island.<br><br>
    Solve Python challenges, recover all map pieces, and become a Pirate Legend!
    </div>
    """, unsafe_allow_html=True)
    name = st.text_input("Enter Pirate Name")
    if st.button("🏴‍☠️ Begin Adventure"):
        if name.strip() != "":
            st.session_state.pirate_name = name.strip()
            st.session_state.started = True
            st.session_state.console = f">>> Welcome aboard, Captain {name.strip()}!"
            st.rerun()
        else:
            st.warning("Enter your pirate name first!")
# ---------------- MAIN GAME LAYOUT ----------------
else:
    col1, col2, col3 = st.columns([1, 2, 1])
    # ---------------- LEFT PANEL (MAP) ----------------
    with col1:
        st.markdown("### 🗺 Treasure Map")
        for i, location in enumerate(locations, start=1):
            st.write(f"✅ {location}" if st.session_state.progress[i] else f"⬜ {location}")
        st.progress(sum(st.session_state.progress.values()) / 5)
        st.write("---")
        st.markdown("### 🧩 Pieces Collected")
        pieces = sum(st.session_state.progress.values())
        st.write("🧩 " * pieces + "⬜ " * (5 - pieces))
        st.write("---")
        st.markdown("### ⭐ Score")
        st.write(st.session_state.score)
    # ---------------- CENTER PANEL ----------------
    with col2:
        st.markdown(f"### ⚓ Welcome, Captain {st.session_state.pirate_name}")
        st.info("Your adventure begins. Solve challenges to recover the lost treasure.")
        # ---------------- CHALLENGE 1 ----------------
        if not st.session_state.progress[1]:
            st.markdown("### ⚓ Challenge 1 – The Dock")
            st.markdown("""
            Captain Sparrow's legendary ship **Midnight Pearl** is hidden among docked ships.
            Find it to recover the first map piece.
            """)
            st.code("""
ships = [
    "Sea Wolf",
    "Ocean Queen",
    "Midnight Pearl",
    "Crimson Tide"
]
captain_ship = ships[____]
print(__________)
""", language="python")
            c1_blank1 = st.text_input("Index value", key="c1b1")
            c1_blank2 = st.text_input("Print statement", key="c1b2")
            st.button(
                "💡 Need a Clue (-5 points)",
                key="clue1",
                disabled=st.session_state.clues_used[1],
                on_click=use_clue,
                args=(1, "Think about how lists are indexed in Python.")
            )
            if st.button("Submit Challenge 1"):
                a1 = c1_blank1.strip().replace(" ", "")
                a2 = c1_blank2.strip().replace(" ", "").lower()
                if a1 in {"2", "ships[2]"} and a2 == "captain_ship":
                    st.session_state.progress[1] = True
                    st.session_state.score += 20
                    update_console(f">>> Correct!\n\n🧩 Map Piece Acquired\nScore +20\n\nCaptain {st.session_state.pirate_name}, the map reveals the Abandoned Camp...")
                    st.rerun()
                else:
                    update_console("""Traceback (most recent call last):
File "<challenge1>", line 2
NameError:
Incorrect answer. Try again.
""")
        # ---------------- CHALLENGE 2 ----------------
        elif not st.session_state.progress[2]:
            st.markdown("### 🧭 Challenge 2 – Abandoned Camp")
            st.markdown("""
            Old supplies are scattered across the camp.
            Count the number of compasses left behind.
            """)
            st.code("""
supplies = [
    "Lantern",
    "Compass",
    "Sword",
    "Compass",
    "Map"
]
compass_count = supplies.____________
print(____________)
""", language="python")
            c2_blank1 = st.text_input("Complete method", key="c2b1")
            c2_blank2 = st.text_input("Print output", key="c2b2")
            st.button(
                "💡 Need a Clue (-5 points)",
                key="clue2",
                disabled=st.session_state.clues_used[2],
                on_click=use_clue,
                args=(2, "Look at the list method used to find repeated items.")
            )
            if st.button("Submit Challenge 2"):
                if (
                    c2_blank1.strip().replace('"', "'").replace(" ", "") == "count('Compass')"
                    and c2_blank2.strip().lower() == "compass_count"
                ):
                    st.session_state.progress[2] = True
                    st.session_state.score += 20
                    update_console(f">>> Correct!\n\n🧩 Map Piece Acquired\nScore +20\n\nCaptain {st.session_state.pirate_name}, the Pirate Hideout awaits...")
                    st.rerun()
                else:
                    update_console("""Traceback (most recent call last):
File "<challenge2>", line 2
NameError:
Incorrect answer. Try again.
""")
        # ---------------- CHALLENGE 3 ----------------
        elif not st.session_state.progress[3]:
            st.markdown("### 🔑 Challenge 3 – Pirate Hideout")
            st.markdown("""
            Deep inside the hideout, only one pirate holds the **Golden Key**.
            Find it from the pirate records.
            """)
            st.code("""
pirates = {
    "Finn":{"item":"Sword","gold":120},
    "Henry":{"item":"Golden Key","gold":80},
    "Jack":{"item":"Compass","gold":50}
}
key = pirates[________][________]
print(________)
""", language="python")
            c3b1 = st.text_input("Pirate name", key="c3b1")
            c3b2 = st.text_input("Key field", key="c3b2")
            c3b3 = st.text_input("Print output", key="c3b3")
            st.button(
                "💡 Need a Clue (-5 points)",
                key="clue3",
                disabled=st.session_state.clues_used[3],
                on_click=use_clue,
                args=(3, "You first select a pirate, then access their stored information.")
            )
            if st.button("Submit Challenge 3"):
                name = c3b1.strip().strip("\"'").lower()
                if (
                    name == "henry"
                    and c3b2.strip().lower() == "item"
                    and c3b3.strip().lower() == "key"
                ):
                    st.session_state.progress[3] = True
                    st.session_state.score += 20
                    update_console(f">>> Correct!\n\n🧩 Map Piece Acquired\nScore +20\n\nCaptain {st.session_state.pirate_name}, the jungle trail awaits...")
                    st.rerun()
                else:
                    update_console("""Traceback (most recent call last):
File "<challenge3>", line 2
NameError:
Incorrect answer. Try again.
""")
        # ---------------- CHALLENGE 4 ----------------
        elif not st.session_state.progress[4]:
            st.markdown("### 🌴 Challenge 4 – Jungle Trail")
            st.markdown("""
            Three paths lie ahead. Only one leads safely forward.
            """)
            st.code("""
paths = [
    {"name":"Path A","danger":"Crocodiles"},
    {"name":"Path B","danger":"Quicksand"},
    {"name":"Path C","danger":"Safe"}
]
for path in paths:
    if _________________________:
        print(_____________________)
""", language="python")
            c4b1 = st.text_input("Condition", key="c4b1")
            c4b2 = st.text_input("Print statement", key="c4b2")
            st.button(
                "💡 Need a Clue (-5 points)",
                key="clue4",
                disabled=st.session_state.clues_used[4],
                on_click=use_clue,
                args=(4, "Check the condition that identifies the safe path.")
            )
            if st.button("Submit Challenge 4"):
                condition = c4b1.strip().lower().replace(" ", "").replace("'", '"')
                if (
                    condition == 'path["danger"]=="safe"'
                    and c4b2.strip().strip("\"'").lower() == "ancient temple found"
                ):
                    st.session_state.progress[4] = True
                    st.session_state.score += 20
                    update_console(f">>> Correct!\n\n🧩 Map Piece Acquired\nScore +20\n\nCaptain {st.session_state.pirate_name}, the final temple awaits...")
                    st.rerun()
                else:
                    update_console("""Traceback (most recent call last):
File "<challenge4>", line 3
NameError:
Incorrect answer. Try again.
""")
        # ---------------- CHALLENGE 5 ----------------
        elif not st.session_state.progress[5]:
            st.markdown("### 🏛 Challenge 5 – Ancient Temple")
            st.markdown("""
            Ancient records list treasure chests in tuples.
            Use a loop to find the only chest that appears in both records.
            """)
            st.code("""
all_chests = (
    "Wooden Chest",
    "Silver Chest",
    "Golden Chest",
    "Iron Chest"
)
treasure_chests = (
    "Golden Chest",
    "Crystal Chest"
)
for chest in all_chests:
    if chest in treasure_chests:
        final_chest = chest
print(final_chest)
""", language="python")
            c5b1 = st.text_input("Loop line", key="c5b1")
            c5b2 = st.text_input("Condition line", key="c5b2")
            c5b3 = st.text_input("Print output", key="c5b3")
            st.button(
                "💡 Need a Clue (-5 points)",
                key="clue5",
                disabled=st.session_state.clues_used[5],
                on_click=use_clue,
                args=(5, "Use a loop to check each tuple item, then compare it with the other tuple.")
            )
            if st.button("🏛 Unlock Treasure"):
                loop = c5b1.strip().lower().replace(" ", "")
                condition = c5b2.strip().lower().replace(" ", "")
                if (
                    loop == "forchestinall_chests:"
                    and condition == "ifchestintreasure_chests:"
                    and c5b3.strip().lower() == "final_chest"
                ):
                    st.session_state.progress[5] = True
                    st.session_state.score += 20
                    st.session_state.console = f"""\
>>> Correct!
🧩 Final Map Piece Acquired
All five map pieces have been assembled.
Coordinates revealed...
Captain {st.session_state.pirate_name},
the treasure chamber is now unlocked!
"""
                    st.rerun()
                else:
                    st.session_state.console = """Traceback (most recent call last):
File "<challenge5>", line 2
NameError:
Incorrect answer. Try again.
"""
    # ---------------- RIGHT PANEL (CONSOLE) ----------------
    with col3:
        st.markdown("### 🐍 Console")
        st.markdown(f'<div class="console">{st.session_state.console}</div>', unsafe_allow_html=True)
# ---------------- FINAL TREASURE ----------------
if st.session_state.progress[5]:
    if not st.session_state.score_saved:
        st.session_state.console = f"""\
>>> Treasure Located...
Opening Ancient Chest...
Loading...
SUCCESS!
🏆 Treasure Found!
Congratulations Captain {st.session_state.pirate_name}!
"""
        save_score()
        st.session_state.score_saved = True
    st.balloons()
    st.markdown("## 🏆 Final Treasure")
    
    percentage = st.session_state.score
    
    # Rank logic
    if percentage >= 90:
        rank = "🥇 Gold Pirate"
    elif percentage >= 70:
        rank = "🥈 Silver Pirate"
    else:
        rank = "🥉 Bronze Pirate"
    
    # Bonus performance message
    if percentage == 100:
        message = "🏆 Perfect! You solved every challenge without losing points!"
    elif percentage >= 90:
        message = "🌟 Excellent work! You're a true pirate expert."
    elif percentage >= 70:
        message = "⚓ Great job! A little more practice and you'll master Python."
    else:
        message = "📚 Good effort! Try again to improve your score and become a legendary pirate."
    
    st.markdown(f"""
🎉 Congratulations, Captain {st.session_state.pirate_name}!
🧩 You recovered all five pieces of Captain Sparrow's treasure map.
💰 You uncovered the legendary treasure.
⭐ **Final Score: {percentage}/100 ({percentage}%)**
🏅 **Rank:** {rank}
{message}
👑 **You have become the next Pirate Legend!**
""")
    st.markdown("### 🏆 Leaderboard")
    if os.path.exists("scores.csv"):
        leaderboard = pd.read_csv("scores.csv").sort_values(by="Score", ascending=False)
        st.dataframe(leaderboard.head(10), use_container_width=True)
    if st.button("🔄 Play Again"):
        reset_game()
