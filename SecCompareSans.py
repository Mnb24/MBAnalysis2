import streamlit as st
import requests

# Dictionary containing file URLs
file_urls = {
    'BR': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR-Complete.txt',
    'KK': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KK-Complete.txt',
    'SV': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/SV-Complete.txt'
}

def get_words(text):
    return set(text.split())

def get_common_words(parva_number):
    words_by_edition = {}
    for edition, url in file_urls.items():
        response = requests.get(url)
        if response.status_code == 200:
            text = response.text.split(f"Parva {parva_number}")[1]  # Assuming section 1
            words_by_edition[edition] = get_words(text)
    
    common_words = set.intersection(*words_by_edition.values())
    return common_words, words_by_edition

def get_word_occurrences(word, words_by_edition):
    occurrences = {}
    for edition, words in words_by_edition.items():
        text = requests.get(file_urls[edition]).text.split(f"Parva {parva_number}")[1]
        lines = text.split('\n')
        for line_number, line in enumerate(lines, start=1):
            if word in line.split():
                if word in occurrences:
                    occurrences[word][edition] = line_number
                else:
                    occurrences[word] = {edition: line_number}
    return occurrences

def main():
    st.title("Parva Comparison - Sanskrit Editions")

    # Parva selection
    parva_number = st.select_slider("Select Parva Number", options=list(range(1, 19)), value=1)

    # Button to compare
    if st.button("Compare Parva"):
        common_words, words_by_edition = get_common_words(parva_number)
        total_words = sum(len(words) for words in words_by_edition.values())
        common_word_count = len(common_words)
        similarity_percentage = (common_word_count / total_words) * 100 if total_words > 0 else 0

        st.write(f"Percentage of Similarity: {similarity_percentage:.2f}%")
        st.write("Common Words:")
        for word in common_words:
            occurrences = get_word_occurrences(word, words_by_edition)
            st.write(f"- {word}:")
            for edition, line_number in occurrences[word].items():
                st.write(f"  {edition}: Line {line_number}")

if __name__ == "__main__":
    main()
