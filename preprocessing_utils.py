import nltk
import stanza
from flair.data import Sentence
from flair.models import SequenceTagger
from tqdm import tqdm
tqdm.pandas()

## NER OPTIONS :: CoNLL03 92.1 , OntoNotes 88.8 (18 Categories)
# stanza_tagger_4 = stanza.Pipeline(lang='en', processors={'ner': 'OntoNotes'}, device='cuda:1')
# stanza_tagger_18 = stanza.Pipeline(lang='en', processors={'ner': 'CoNLL03'}, device='cuda:1')

# flair_tagger_4 = SequenceTagger.load("flair/ner-english-large")
# flair_tagger_18 = SequenceTagger.load("flair/ner-english-ontonotes-large")

class preprocessing_utils:
    def __init__(self, ner_categories = 4, ner_library = 'stanza', enable_ner = False):
        
        self.ner_library = ner_library
        self.ner_categories = ner_categories
        
        if ner_categories not in {4,18}:
            raise ValueError(f"No Tagger implemented for {categories = }!!!")
        if ner_library not in {'stanza', 'flair'}:
            raise ValueError(f"No Tagger implemented for {ner_library = }!!!")
        
        if enable_ner:
            if ner_categories == 4:
                if ner_library == 'stanza':
                    self.tagger = stanza.Pipeline(lang='en', processors={'ner': 'CoNLL03'}, device='cuda:1')
                if ner_library == 'flair':
                    self.tagger = SequenceTagger.load("flair/ner-english-large")
            if ner_categories == 18:
                if ner_library == 'stanza':
                    self.tagger = stanza.Pipeline(lang='en', processors={'ner': 'OntoNotes'}, device='cuda:1')
                if ner_library == 'flair':
                    self.tagger = SequenceTagger.load("flair/ner-english-ontonotes-large")
        else:
            self.tagger = None
        
    
    def calculate_word_length(self, text):
        return len(nltk.word_tokenize(text))
    
    def stanza_ner(self, text):
        if self.ner_library == 'flair':
            raise Exception('class was initialized with flair but you are using stanza ner function.')
        
        doc = self.tagger(text)
        return [(ent.text,ent.type) for sent in doc.sentences for ent in sent.ents]
   
    def flair_ner(self, text):
        if self.ner_library == 'stanza':
            raise Exception('class was initialized with stanza but you are using flair ner function.')
        
        # make example sentence
        sentence = Sentence(text)

        # predict NER tags
        self.tagger.predict(sentence)
        
        return sentence.to_dict()['entities']
    
    def calculate_num_sentences(self, text):
        return len(nltk.sent_tokenize(text))