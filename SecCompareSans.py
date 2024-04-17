import streamlit as st
import requests

# Dictionary containing file URLs
file_urls = {
    'BR': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR-Complete.txt',
    'KK': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KK-Complete.txt',
    'SV': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/SV-Complete.txt'
}

def get_common_words(parva_number):
    common_words_with_line_numbers = {}
    for key, url in file_urls.items():
        response = requests.get(url)
        if response.status_code == 200:
            text = response.text.split(f"Parva {parva_number}")[1]  # Assuming section 1
            lines = text.split('\n')
            for line_number, line in enumerate(lines, start=1):
                words = line.split()
                for word in words:
                    if word in common_words_with_line_numbers:
                        common_words_with_line_numbers[word].append((key, line_number))
                    else:
                        common_words_with_line_numbers[word] = [(key, line_number)]
    common_words = set(common_words_with_line_numbers.keys())
    return common_words, common_words_with_line_numbers

def main():
    st.title("Parva Comparison - Sanskrit Editions")

    # Parva selection
    parva_number = st.select_slider("Select Parva Number", options=list(range(1, 19)), value=1)

    # Button to compare
    if st.button("Compare Parva"):
        common_words, common_words_with_line_numbers = get_common_words(parva_number)
        st.write("Common Words:")
        for word in common_words:
            line_info = '\n'.join([f'{edition}-{line}' for edition, line in common_words_with_line_numbers[word]])
            st.write(f"- {word}:\n{line_info}\n")

if __name__ == "__main__":
    main()
