import streamlit as st
import requests

# Dictionary containing file URLs
file_urls = {
    'BR': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR-Complete.txt',
    'KK': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KK-Complete.txt',
    'SV': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/SV-Complete.txt'
}

def get_common_words(parva_number):
    common_words = set()
    for key, url in file_urls.items():
        response = requests.get(url)
        if response.status_code == 200:
            text = response.text.split(f"Parva {parva_number}")[1]  # Assuming section 1
            words = set(text.split())
            if not common_words:
                common_words = words
            else:
                common_words = common_words.intersection(words)
    return common_words

def main():
    st.title("Parva Comparison - Sanskrit Editions")

    # Parva selection
    parva_number = st.select_slider("Select Parva Number", options=list(range(1, 19)), value=1)

    # Button to compare
    if st.button("Compare Parva"):
        common_words = get_common_words(parva_number)
        st.write("Common Words:", common_words)

if __name__ == "__main__":
    main()
