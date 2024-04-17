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
    paragraphs_by_file = {text_name: [] for text_name in text_names}

    # Get context paragraphs for each text
    for text, text_name in zip(texts, text_names):
        context_paragraphs = get_context_paragraphs(text, target_word)
        paragraphs_by_file[text_name] = context_paragraphs

    # Initialize counters for each edition
    counters = {text_name: 0 for text_name in text_names}

    # Iterate through paragraphs and display in groups of three
    max_paragraphs = max(len(paragraphs_by_file[text_name]) for text_name in text_names)
    for i in range(max_paragraphs):
        for text_name in text_names:
            counter = counters[text_name]
            paragraphs = paragraphs_by_file[text_name]
            if counter < len(paragraphs):
                st.write(f"**{text_name}:**")
                highlighted_paragraph = paragraphs[counter]
                
                # Check if the target word is within an HTML tag
                if f">{target_word}<" in highlighted_paragraph:
                    continue  # Skip this paragraph if the target word is within an HTML tag
                
                highlighted_paragraph = highlighted_paragraph.replace(target_word, f"<span style='color: red'>{target_word}</span>")
                
                # Split the paragraph by newline
                lines = highlighted_paragraph.split('\n')
                
                # Iterate through lines
                for j, line in enumerate(lines):
                    # Check if the line contains the target word
                    if target_word in line:
                        # Print the previous line if available
                        if j > 0:
                            st.write(lines[j - 1])
                        # Highlight the line containing the target word
                        st.markdown(line, unsafe_allow_html=True)
                        # Print the next line if available
                        if j < len(lines) - 1:
                            st.write(lines[j + 1])
                            
                        # Add a marker to separate sets
                        st.write("-----")
                st.write("\n")
                
                # Increment the counter for the current edition
                counters[text_name] += 1
                
        # After displaying one instance from each edition, add a separator
        st.write("********")

def main():
    # Displaying heading
    st.title("Concordance Analyzer - Sanskrit Editions (Instance-wise)")

    # URLs of the text files
    file_paths = {
        'BR': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR-Complete.txt', 
        'KK': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KK-Complete.txt', 
        'SV': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/SV-Complete.txt'
    }
    
    texts = []
    text_names = []
    for text_name, file_path in file_paths.items():
        response = requests.get(file_path)
        if response.status_code == 200:
            texts.append(response.text)
            text_names.append(text_name)

    target_word = st.text_input("Enter the Devanagari word for concordance analysis: ")

    if st.button('Perform Concordance Analysis'):
        # Get context paragraphs for the selected text
        perform_concordance(texts, text_names, target_word)


if __name__ == "__main__":
    main()
