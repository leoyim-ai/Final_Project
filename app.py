import streamlit as st
from openai import OpenAI as CLANKER

lying_words = [
    "Maybe",
    "Probably",
    "I think",
    "Kind of",
    "Sort of",
    "Essentially",
    "Basically",
    "As far as I know",
    "That person",
    "The phone",
    "It happened",
    "Left",
    "Someone",
    "Actually",
    "Just",
    "Literally",
    "Well"
]

honesty_words = [
    "Honestly",
    "Truthfully",
    "To be real",
    "I swear",
    "Believe me",
    "Why would I lie",
    "Hand on my heart",
    "To be 100% real"
]

client = CLANKER(api_key=st.secrets["APIKEY"])

user_input = st.text_input("Enter text here")

is_empty = not user_input.strip()

if st.button("Submit", disabled=is_empty):
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": user_input, "These are words that might show they are lying.": lying_words, "honesty_words": honesty_words}
    ]
)


