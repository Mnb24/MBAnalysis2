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
    for word in input_words:
        if re.search(r'\b' + re.escape(word) + r'\b', bori_text, re.IGNORECASE):
            matches.append(word)
    return matches

def main():
    # Fetch text from URLs
    sv_text = fetch_text("https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/SV-Complete.txt")
    br_text = fetch_text("https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR-Complete.txt")

    # Display side pane with text boxes
    with st.sidebar:
        st.subheader("SV Text")
        st.text_area("SV Text", sv_text, height=400)

        st.subheader("Input Text")
        input_text = st.text_area("Input Text", height=200)
        
        if st.button("Find Matches"):
            if br_text and input_text:
                matches = find_matches(br_text, input_text)
                if matches:
                    st.write("Matches found in BORI edition:")
                    st.write(matches)
                else:
                    st.write("No matches found in BORI edition.")

    # Display matches in main portion
    st.title("Matches in BORI Edition")
    if br_text and input_text:
        matches = find_matches(br_text, input_text)
        if matches:
            st.write("Matches found in BORI edition:")
            st.write(matches)
        else:
            st.write("No matches found in BORI edition.")

if __name__ == "__main__":
    main()
