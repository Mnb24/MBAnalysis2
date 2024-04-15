import streamlit as st
from collections import Counter
import re
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import requests

def count_words_in_text(text, words):
    words_text = re.findall(r'\w+', text.lower())
    return [words_text.count(word.lower()) for word in words]

st.title('Multi-Entity Frequency Analyzer - Adi Parva')

words_to_search = st.text_input("Enter words to analyze (comma separated):")

# Define the file paths
file_paths = ['https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR-Complete.txt', 
              'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KK-Complete.txt', 
              'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/SV-Complete.txt',
              'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/MBTN.txt']

# Define the file names
file_names = ['BD', 'KMG', 'MND']

if st.button('Analyze'):
    if words_to_search:
        words_to_search = [word.strip() for word in words_to_search.split(',')]
        data = []
        for file_path, file_name in zip(file_paths, file_names):
            response = requests.get(file_path)
            text = response.text
            counts = count_words_in_text(text, words_to_search)
            for word, count in zip(words_to_search, counts):
                data.append([file_name, word, count])

        # Create a DataFrame
        df = pd.DataFrame(data, columns=['File', 'Word', 'Frequency'])

        # Create a bar plot
        sns.barplot(x='Word', y='Frequency', hue='File', data=df)
        plt.title('Frequency of each word in each file')
        st.pyplot(plt)
    else:
        st.write("Please input words (comma separated).")
