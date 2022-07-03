import nltk
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')
def tokenize_document(text_file):
    tokens = nltk.word_tokenize(text_file)
    return tokens

def tag_tokens(tokens):
    tagged_tokens = nltk.pos_tag(tokens)
    return tagged_tokens

