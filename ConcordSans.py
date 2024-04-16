import streamlit as st
from nltk.tokenize import sent_tokenize, word_tokenize
import requests
import nltk

# Download nltk resources
nltk.download('punkt')

def get_context_paragraphs(text, target_word, context_lines=2):
    sentences = sent_tokenize(text)
    paragraphs = []

    # Find sentences containing the target word
    for i, sentence in enumerate(sentences):
        if target_word in word_tokenize(sentence):
            start_index = max(0, i - context_lines)
            end_index = min(len(sentences), i + context_lines + 1)
            context_sentences = sentences[start_index:end_index]
            context_paragraph = " ".join(context_sentences)
            paragraphs.append(context_paragraph)

    return paragraphs

def perform_concordance(texts, text_names, target_word):
    paragraphs_by_file = {text_name: [] for text_name in text_names}

    # Get context paragraphs for each text
    for text, text_name in zip(texts, text_names):
        context_paragraphs = get_context_paragraphs(text, target_word)
        paragraphs_by_file[text_name] = context_paragraphs

    # Print concordance results in groups of three
    num_paragraphs = max(len(paragraphs_by_file[text_name]) for text_name in text_names)
    for i in range(0, num_paragraphs, 3):
        for text_name in text_names:
            if i < len(paragraphs_by_file[text_name]):
                st.write(f"**{text_name}:**")
                highlighted_paragraph = paragraphs_by_file[text_name][i].replace(target_word, f"<span style='color: red'>{target_word}</span>")
                st.write(highlighted_paragraph, unsafe_allow_html=True)
                st.write("\n")
        st.write("********")  # Inserting special characters after each group of three instances

def main():
    # Displaying heading
    st.title("Concordance Analyzer - Adi Parva (Instance-wise)")

    # URLs of the text files
    file_paths = [
        'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BD1.txt', 
        'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KMG1.txt', 
        'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/MND1.txt'
    ]
    text_names = ['BD1', 'KMG1', 'MND1']
    
    texts = []
    for file_path in file_paths:
        response = requests.get(file_path)
        text = response.text
        texts.append(text)

    target_word = st.text_input("Enter the word for concordance analysis: ")

    if st.button('Perform Concordance Analysis'):
        perform_concordance(texts, text_names, target_word)

if __name__ == "__main__":
    main()
