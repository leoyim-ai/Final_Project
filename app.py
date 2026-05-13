import streamlit as st
from openai import OpenAI as CLANKER
import json

st.title("Lie Detection App")

# Word lists
lying_words = [
    "Maybe","Probably","I think","Kind of","Sort of",
    "Essentially","Basically","As far as I know",
    "That person","The phone","It happened","Left",
    "Someone","Actually","Just","Literally","Well"
]

honesty_words = [
    "Honestly","Truthfully","To be real","I swear",
    "Believe me","Why would I lie",
    "Hand on my heart","To be 100% real"
]

if "APIKEY" not in st.secrets:
    st.error("API key not found")
    st.stop()

client = CLANKER(api_key=st.secrets["APIKEY"])

if "done" not in st.session_state:
    st.session_state.done = False

if "thinking" not in st.session_state:
    st.session_state.thinking = False

if "text" not in st.session_state:
    st.session_state.text = ""

if "reset" not in st.session_state:
    st.session_state.reset = False

if st.session_state.reset:
    st.session_state.text = ""
    st.session_state.reset = False

user_input = st.text_input(
    "Enter text here",
    key="text",
    disabled=st.session_state.done or st.session_state.thinking
)

if st.button("Submit", disabled=st.session_state.done or st.session_state.thinking):
    if user_input.strip():
        st.session_state.thinking = True
        st.rerun()

if st.session_state.thinking:
    with st.spinner("Analyzing your text"):
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a lie detection assistant.\n\n"
                        "You will analyze the user's text and determine the likelihood of it being a lie.\n\n"
                        "use context to make your decision to see if an word is lie word or not.\n\n"
                        "If there is bad words then just put in explanation cant do bad words.\n\n"
                        "Return ONLY valid JSON OR ELSE U WILL BE PUNISHED.\n\n"
                        "NOTHING ELSE ONLY VALID JSON NO BEGINING WORDS OR ENDING WORDS ONLY JSON\n\n"
                        "Format exactly like this:\n"
                        "{\n"
                        '  "percentage": number,\n'
                        '  "lying_words": [list],\n'
                        '  "explanation": "short text"\n'
                        "}\n\n"
                        f"Lying words list: {', '.join(lying_words)}\n"
                        f"Honesty words list: {', '.join(honesty_words)}"
                    )
                },
                {"role": "user", "content": st.session_state.text}
            ]
        )
        result_text = completion.choices[0].message.content

        try:
            data = json.loads(result_text)
            st.subheader("Results")
            st.slider(
                f"Lie chance: {data['percentage']}%",
                0, 100, data['percentage'], disabled=True
            )
            st.write(f"Lying Words Found: {data['lying_words']}")
            st.write(f"Explanation: {data['explanation']}")
            st.session_state.done = True
            st.session_state.thinking = False

        except:
            st.error("Did not return valid JSON")
            st.session_state.thinking = False
if st.session_state.done:
    if st.button("Reset"):
        st.session_state.done=False
        st.session_state.thinking=False
        st.session_state.reset=True
        st.rerun()