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

placeholder = st.empty()
if placeholder.button("Submit", disabled=st.session_state.done) and user_input.strip():

   
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
    
    try:
        data = json.loads(result_text)
        placeholder.empty()

        st.subheader("Results")
        st.slider(f"**Lie chance:** {data['percentage']}%", 0, 100, data['percentage'],disabled=True)
        st.write(f"**Lying Words Found:** {data['lying_words']}")
        st.write(f"**Explanation:** {data['explanation']}")
        st.session_state.done = True


    except:
        st.error("did not return valid JSON")
