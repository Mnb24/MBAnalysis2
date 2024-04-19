import streamlit as st
import requests
import re

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
    for sentence in re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', bori_text):
        for word in input_words:
            if re.search(r'\b' + re.escape(word) + r'\b', sentence, re.IGNORECASE):
                matches.append(sentence)
                break  # If any word is found in the sentence, move to the next sentence
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
                    st.write(match)
            else:
                st.write("No matches found in BORI edition.")

if __name__ == "__main__":
    main()
