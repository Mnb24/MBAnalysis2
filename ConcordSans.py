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

    # Print concordance results in groups of three
    num_paragraphs = max(len(paragraphs_by_file[text_name]) for text_name in text_names)
    for i in range(num_paragraphs):
        for text_name in text_names:
            if i < len(paragraphs_by_file[text_name]):
                st.write(f"**{text_name}:**")
                highlighted_paragraph = paragraphs_by_file[text_name][i].replace(target_word, f"<span style='color: red'>{target_word}</span>")
                
                # Split the paragraph by newline
                lines = highlighted_paragraph.split('\n')
                
                # Iterate through lines
                for j, line in enumerate(lines):
                    # Print the previous line if available
                    if j > 0:
                        st.write(lines[j - 1])
                    # Highlight the line containing the target word
                    st.markdown(line, unsafe_allow_html=True)
                    # Print the next line if available
                    if j < len(lines) - 1:
                        st.write(lines[j + 1])
                    
                    # Add a marker to separate sets
                    if j < len(lines) - 1:
                        st.write("-----")
                st.write("\n")
        st.write("********")  # Inserting special characters after each group of three instances


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
        context_paragraphs = get_context_paragraphs(text, target_word)
        
        # Print concordance results in sets of three lines
        for paragraph in context_paragraphs:
            lines = paragraph.split('\n')
            for i, line in enumerate(lines):
                # Add a newline before BR, KK, SV, and MB
                if line.startswith(('BR', 'KK', 'SV', 'MBTN')):
                    st.write("")
                # Highlight the line containing the target word
                if target_word in line:
                    st.markdown(line.replace(target_word, f"<span style='color: red'>{target_word}</span>"), unsafe_allow_html=True)
                else:
                    st.write(line)
                    
                # Print the next line if available
                if i < len(lines) - 1:
                    st.write(lines[i + 1])
                    
                # Add a marker to separate sets
                st.write("-----")
            st.write("********")


if __name__ == "__main__":
    main()
