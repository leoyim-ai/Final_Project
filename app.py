import streamlit as st
from openai import OpenAI as CLANKER
import json

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

user_input = st.text_input("Enter text here", disabled=st.session_state.done)

if st.button("Submit") and user_input.strip():

    st.session_state.done = True

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a lie detection assistant.\n"
                    "Return ONLY valid JSON.\n\n"
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
            {"role": "user", "content": user_input}
        ]
    )

    result_text = completion.choices[0].message.content

    st.write("Raw output:")
    st.code(result_text)

    try:
        data = json.loads(result_text)

        st.subheader("Results")
        st.write(f"**Lie chance:** {data['percentage']}%")
        st.write(f"**Lying Words Found:** {data['lying_words']}")
        st.write(f"**Explanation:** {data['explanation']}")

    except:
        st.error("Model did not return valid JSON")