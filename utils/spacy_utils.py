import spacy

class TextStats:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def __preprocess(self, text):
        # Perform any necessary preprocessing steps
        text = text.lower()
        doc = self.nlp(text)
        return doc

    def count_adjectives(self, text):
        doc = self.__preprocess(text)
        adjectives = [token for token in doc if token.pos_ == "ADJ"]
        return len(adjectives)

    def count_unique_attributes(self, text):
        """
        Assumption : Unique Attributes are Adjectives
        """
        doc = self.__preprocess(text)
        adjectives = [token for token in doc if token.pos_ == "ADJ"]
        return len(set(adjectives))
    
    def count_adverbs(self, text):
        doc = self.__preprocess(text)
        adverbs = [token for token in doc if token.pos_ == "ADV"]
        return len(adverbs)
    
    def count_unique_activites(self, text):
        """
        Assumption : Unique Activities are Adverbs
        """
        doc = self.__preprocess(text)
        adverbs = [token for token in doc if token.pos_ == "ADV"]
        return len(set(adverbs))