import re
class Connectives:
    # TO INDICATE AN EFFECT, RESULT, OR CONSEQUENCE
    list_1 =  ['accordingly', 'consequently', 'henceforth', 'thereupon', 'as a result', 'for this reason', 'in that case', 'thus', 'because', 'forthwith', 'therefore', 'hence']
    
    # TO INDICATE CAUSE, CONDITION, OR PURPOSE 
    list_2 = ['as long as,' 'so long as', 'in order to', 'only if', 'even if', 'to the end that', 'because of', 'in the event that', 'owing to', 'unless', 'due to', 'in the hope that', 'provided that', 'when', 'for fear that', 'in view of', 'seeing that', 'being that', 'whenever', 'for the purpose of', 'inasmuch as', 'since', 'while', 'given that', 'lest', 'so as to', 'with this in mind', 'granted', 'granted that', 'on condition', 'on the condition that', 'so that', 'with this intention']
    
    # TO INDICATE TIME, CHRONOLOGY, OR SEQUENCE 
    list_3 = ['after', 'formerly', 'last', 'sooner', 'later', 'sooner or later', 'all of a sudden', 'forthwith', 'later', 'straightaway', 'as long as', 'from time to time', 'meanwhile', 'suddenly', 'as soon as', 'further', 'next', 'then', 'at the present time', 'at present', 'hence', 'now', 'till', 'at the same time', 'henceforth', 'now that', 'to begin with', 'at this instant', 'immediately', 'occasionally', 'until', 'before', 'in a moment', 'once', 'until now', 'by the time', 'in due time', 'presently', 'up to the present time', 'during', 'in the first place', 'prior to', 'when', 'eventually', 'in the meantime', 'quickly', 'whenever', 'finally', 'in time', 'shortly', 'whenever', 'first', 'second', 'instantly', 'since', 'without delay'] 
    
    # List of Interclausal Connectives 
    # Link : https://mrswarnerarlington.weebly.com/uploads/6/9/0/0/6900648/conjunctions_master_list_alternate_version.pdf
    list_4 = ['And', 'Or', 'But', 'Nor', 'So', 'For', 'Yet' ]
    list_5 = ['After', 'Although', 'As', 'As If', 'As Long As', 'Because', 'Before', 'Even If', 'Even Though', 'If', 'Once', 'Provided', 'Since', 'So That', 'That', 'Though', 'Till', 'Unless', 'Until', 'What', 'When', 'Whenever', 'Wherever', 'Whether', 'While']

    # THESE DO NOT JOIN TWO SENTENCES
    list_6 = ['Accordingly', 'Also', 'Anyway', 'Besides', 'Consequently', 'Finally', 'For Example', 'For Instance', 'Further', 'Furthermore', 'Hence', 'However', 'Incidentally', 'Indeed', 'In Fact', 'Instead', 'Likewise', 'Meanwhile', 'Moreover', 'Namely', 'Now', 'Of Course', 'On the Contrary', 'On the Other Hand', 'Otherwise', 'Nevertheless', 'Next', 'Nonetheless', 'Similarly', 'So Far', 'Until Now', 'Still', 'Then', 'Therefore', 'Thus'] 
    
    list_causal = list_1 + list_2
    list_temporal = list_3
    list_interclausal = list_4 + list_5
    
    def __init__(self, connectives = None):
        
        self.connectives = connectives
        
        if not self.connectives:
            raise ValueError("You must define a type of Connectives to search for. Options are 'interclausal', 'causal' and 'temporal'")
        else:
            if self.connectives == 'interclausal':
                self.connectives_list = Connectives.list_interclausal
            elif self.connectives == 'causal':
                self.connectives_list = Connectives.list_causal
            elif self.connectives == 'temporal':
                self.connectives_list = Connectives.list_temporal
            else:
                raise ValueError("Chosen value of connectives not implemented. Options are 'interclausal', 'causal' and 'temporal'")

        self.pat_to_find = self._generate_pattern()

    def _generate_pattern(self):
        # lowercase
        self.connectives_list = [i for i in self.connectives_list]
        # sort in descending order to account for greedy search 
        self.connectives_list = list(sorted(self.connectives_list, key = lambda x: len(x), reverse = True))
        # join to make the pattern
        _connectives_list = "|".join(self.connectives_list)
        # compile this pattern
        pat = re.compile(_connectives_list)
        # return 
        return pat

    def findall_connectives(self, sentence):
        _found = re.findall(self.pat_to_find, sentence)
        
        # implement : If the word starts the sentence in interclausal connectives, remove from list 
        if self.connectives == 'interclausal':
            return len(_found)
        else:
            return len(_found)