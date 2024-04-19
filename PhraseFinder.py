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

# Function to find matches in the text and return lines with matched phrases highlighted
def find_matches(text, input_text, delimiter):
    # Find matches in the text
    lines = text.split(delimiter)
    matched_lines = []
    for line in lines:
        if re.search(r'\b' + re.escape(input_text) + r'\b', line):
            line = re.sub(r'\b' + re.escape(input_text) + r'\b', f'<span style="color:red">{input_text}</span>', line)
            matched_lines.append(delimiter + line)
    return matched_lines

def main():
    # Fetch text from URLs
    sv_text = fetch_text("https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/SV-Complete.txt")
    br_text = fetch_text("https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR-Complete.txt")
    kk_text = fetch_text("https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KK-Complete.txt")

    # Display side pane with text boxes
    st.sidebar.subheader("SV Text")
    sv_text_input = st.sidebar.text_area("SV Text", sv_text, height=400)

    st.sidebar.subheader("Input Text")
    input_text = st.sidebar.text_area("Input Text", height=200)

    find_matches_button = st.sidebar.button("Find Matches")

    # Display matches in main portion
    st.title("Matches in BORI and KK Editions")
    if find_matches_button:
        if br_text and input_text:
            matched_lines = find_matches(br_text, input_text, ' BR')
            if matched_lines:
                st.write("Matches found in BORI edition:")
                for line in matched_lines:
                    st.markdown(line, unsafe_allow_html=True)
            else:
                st.write("No matches found in BORI edition.")
        
        if kk_text and input_text:
            matched_lines = find_matches(kk_text, input_text, ' KK')
            if matched_lines:
                st.write("Matches found in KK edition:")
                for line in matched_lines:
                    st.markdown(line, unsafe_allow_html=True)
            else:
                st.write("No matches found in KK edition.")

if __name__ == "__main__":
    main()
