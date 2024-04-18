import streamlit as st
import requests

# Function to fetch text from URL
def fetch_text(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Function to find matches in BORI edition
def find_matches(sanskrit_text, input_text):
    # Implement your matching algorithm here
    # For demonstration purposes, let's just return the input text
    return input_text

def main():
    # Fetch text from URLs
    sv_text = fetch_text("https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/SV-Complete.txt")
    br_text = fetch_text("https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR-Complete.txt")

    # Display side pane with text boxes
    with st.sidebar:
        st.subheader("Sv Text")
        st.text_area("Sv Text", sv_text, height=400)

        st.subheader("Input Text")
        input_text = st.text_area("Input Text", height=200)

    # Display matches in main portion
    st.title("Matches in BORI Edition")
    matches = find_matches(sv_text, input_text)
    st.write(matches)

if __name__ == "__main__":
    main()
