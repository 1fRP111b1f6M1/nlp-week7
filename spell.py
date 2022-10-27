# %%
import re
from collections import Counter
import streamlit as st


# %%
def words(text):
    return re.findall(r"\w+", text.lower())


word_count: Counter = Counter(words(open("big.txt").read()))
N = sum(word_count.values())


def P(word):
    return word_count[word] / N  # float


# Run the function:

# print(list(map(lambda x: (x, P(x)), words("speling spelling speeling"))))

letters = "abcdefghijklmnopqrstuvwxyz"


def edits1(word):
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


# Run the function:
# pprint(list(edits1("speling"))[:3])
# pprint(list(map(lambda x: (x, P(x)), edits1("speling"))))
# print(list(filter(lambda x: P(x) != 0.0, edits1("speling"))))
# print(max(edits1("speling"), key=P))


def correction(word):
    return max(candidates(word), key=P)


def candidates(word):
    return known([word]) or known(edits1(word)) or known(edits2(word)) or [word]


def known(words):
    return set(w for w in words if w in word_count)


def edits2(word):
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


def init_state(key: str, default: str):
    if key not in st.session_state:
        st.session_state[key] = default


# %%
state = st.session_state
init_state("is-select", "true")
init_state("selected-word", "")
init_state("typed-word", "")

is_select = state["is-select"]
is_select = (
    "false"
    if is_select == "true" and state["typed-word"] != ""
    else "true"
    if is_select == "false" and state["selected-word"] != ""
    else is_select
)

if is_select == "true":
    state["typed-word"] = ""
else:
    state["selected-word"] = ""

word = state["selected-word"] if is_select == "true" else state["typed-word"]
# print(is_select)
# print(state["selected-word"])
# print(state["typed-word"])
# print(word)

state["is-select"] = is_select

st.title("Spell Checker")
st.selectbox(
    "Choose a word or...",
    [
        "",
        "initials",
        "inistals",
        "remember",
        "rememmer",
        "opposite",
        "oppossitte",
        "supersede",
        "superceed",
    ],
    key="selected-word",
)
st.text_input("Type a word", key="typed-word")

corrected = correction(word)
if st.sidebar.checkbox("Show original word"):
    st.text(f"Original word is: {corrected if word != '' else ''}")

if corrected == word:
    st.success(f"{word} is the correct spelling")
elif word != "":
    st.error(f"Correction: {corrected}")


# print("speling -->", correction("speling"))
# speling spelling
