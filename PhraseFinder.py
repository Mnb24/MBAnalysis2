import streamlit as st
import requests
import re
from bs4 import BeautifulSoup

# Function to fetch text from URL
def fetch_text(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Function to find matches in BORI edition
def find_matches(bori_text, input_text):
    # Split input text into words
    input_words = re.findall(r'\b\w+\b', input_text)

    # Find matches in BORI edition
    matches = []
    sentences = bori_text.split('.')
    for sentence in sentences:
        for word in input_words:
            if re.search(r'\b' + re.escape(word) + r'\b', sentence, re.IGNORECASE):
                sentence = sentence.replace(word, f"<span style='color:red'>{word}</span>")
                matches.append(sentence.strip())
    return matches

def main():
    # Fetch text from URLs
    sv_text = fetch_text("https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/SV-Complete.txt")
    br_text = fetch_text("https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR-Complete.txt")

    # Display side pane with text boxes
    st.sidebar.subheader("SV Text")
    sv_text_input = st.sidebar.text_area("SV Text", sv_text, height=400)

    st.sidebar.subheader("Input Text")
    input_text = st.sidebar.text_area("Input Text", height=200)

    find_matches_button = st.sidebar.button("Find Matches")

    # Display matches in main portion
    st.title("Matches in BORI Edition")
    if find_matches_button:
        if br_text and input_text:
            matches = find_matches(br_text, input_text)
            if matches:
                st.write("Matches found in BORI edition:")
                for match in matches:
                    st.markdown(match, unsafe_allow_html=True)
            else:
                st.write("No matches found in BORI edition.")

if __name__ == "__main__":
    main()
