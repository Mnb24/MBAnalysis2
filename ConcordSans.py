import streamlit as st
from nltk.tokenize import sent_tokenize, word_tokenize
import requests
import nltk

# Download nltk resources
nltk.download('punkt')

def get_context_paragraphs(text, target_word):
    sentences = sent_tokenize(text)
    paragraphs = []

    # Find sentences containing the target word
    for i, sentence in enumerate(sentences):
        if target_word in word_tokenize(sentence):
            start_index = max(0, i - 1)
            end_index = min(len(sentences), i + 2)
            context_sentences = sentences[start_index:end_index]
            context_paragraph = " ".join(context_sentences)
            paragraphs.append(context_paragraph)

    return paragraphs

def perform_concordance(texts, text_names, target_word):
    for text, text_name in zip(texts, text_names):
        sentences = sent_tokenize(text)
        st.write(f"**{text_name}:**")
        for i, sentence in enumerate(sentences):
            if target_word in word_tokenize(sentence):
                # Print the previous sentence if available
                if i > 0:
                    st.write(sentences[i - 1])
                # Highlight the target word in the current sentence
                highlighted_sentence = sentence.replace(target_word, f"<span style='color: red'>{target_word}</span>")
                st.markdown(highlighted_sentence, unsafe_allow_html=True)
                # Print the next sentence if available
                if i < len(sentences) - 1:
                    st.write(sentences[i + 1])
                st.write("-----")
        st.write("\n")

def main():
    # Displaying heading
    st.title("Concordance Analyzer - Sanskrit Editions (Sequential)")

    # URLs of the text files
    file_paths = {
        'BR': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR-Complete.txt', 
        'KK': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KK-Complete.txt', 
        'SV': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/SV-Complete.txt',
        'MBTN': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/MBTN.txt'
    }
    
    # Dropdown to select the edition
    selected_edition = st.selectbox("Select Edition", list(file_paths.keys()))

    # Function to fetch text data from URL
    def fetch_text(url):
        response = requests.get(url)
        return response.text
    
    # Fetching text for the selected edition
    text = fetch_text(file_paths[selected_edition])

    target_word = st.text_input("Enter the Devanagari word for concordance analysis: ")

    if st.button('Perform Concordance Analysis'):
    # Get context paragraphs for the selected text
        perform_concordance([text], [selected_edition], target_word)


if __name__ == "__main__":
    main()
