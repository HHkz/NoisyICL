import pandas as pd
from abc import ABCMeta, abstractmethod
import datasets

class DatasetLoader():
    def __init__(self):        
        self.label_space = None
        self.new_label_mapping = None
        self.new_label_space = None
        self.max = None
        self.neutral_label = None
        pass
    
    def get(self, index: int) -> tuple:
        pass

    def get_max(self) -> int:
        return self.max

    def get_label_space(self) -> list:
        if self.new_label_space is None:
            return self.label_space
        return self.new_label_space
    
    def divide(self, begin, end_not_include):
        pass
    
    def default_testing_division(self):
        if self.max >= 512:
            self.divide(0, 512)
        else:
            self.divide(0, self.max // 2)
        return self
    
    def default_training_division(self):
        if self.max >= 1024:
            self.divide(self.max - 512, self.max)
        else:
            self.divide(512, self.max)
        return self
    
    def get_empty_input(self):
        return self.get(None)


class hate_speech18(DatasetLoader):
    def __init__(self):
        super().__init__()
        self.table = datasets.load_dataset("hate_speech18")['train'].shuffle(seed=42)
        self.max = len(self.table)
        self.label_space = ['normal', 'hate', 'skip', 'relation']
        self.dataset_name = 'hate_speech18'

    def get(self, index):
        if index is None:
            return ("", "")
        text = self.table['text'][index]
        label = self.label_space[self.table['label'][index]]
        if self.new_label_mapping != None:
            label = self.new_label_mapping[label]
        return (text, label)
    
    def divide(self, begin, end_not_include):
        self.table = self.table[begin: end_not_include]
        self.max = len(self.table['text'])
        return

    def get_max(self):
        return self.max
    

class poem_sentiment(DatasetLoader):
    def __init__(self):
        super().__init__()
        self.label_space = ['negative', 'neutral', 'positive', 'mix']
        self.label_mapping = {
            0: 'negative',
            1: 'neutral',
            2: 'positive',
            3: 'mix'
        }
        sp_dataset = datasets.load_dataset("poem_sentiment").shuffle(seed=42)
        self.table = datasets.concatenate_datasets([sp_dataset['train'], sp_dataset['validation'], sp_dataset['test']])
        self.max = len(self.table)
        self.dataset_name = 'poem_sentiment'
        self.neutral_label = 1
    
    def get_max(self):
        return self.max
    
    def divide(self, begin, end_not_include):
        self.table = self.table[begin: end_not_include]
        self.max = len(self.table['verse_text'])
        return
    
    def get(self, index):
        if index is None:
            return ("", "")
        return (self.table['verse_text'][index], self.label_mapping[self.table['label'][index]])


class SemEval2014_Restaurants(DatasetLoader):
    def __init__(self):
        super().__init__()
        sp_dataset = datasets.load_dataset("yqzheng/semeval2014_restaurants").shuffle(seed=42)
        self.table = datasets.concatenate_datasets([sp_dataset['train'], sp_dataset['test']])
        self.max = len(self.table)
        self.label_space = ['negative', 'neutral', 'positive']
        self.label_mapping = {
            -1: 'negative',
            0: 'neutral',
            1: 'positive'
        }
        self.dataset_name = 'SemEval 2014-Task 4 Restaurants'
        self.neutral_label = 1
    
    def get_max(self):
        return self.max

    def divide(self, begin, end_not_include):
        self.table = self.table[begin: end_not_include]
        self.max = len(self.table['text'])
        return
    
    def get(self, index):
        if index is None:
            return (", Aspect: ", "")
        text = self.table['text'][index]
        aspect = self.table['aspect'][index]
        label = self.label_mapping[self.table['label'][index]]
        output_text = text + ', Aspect: ' + aspect
        if self.new_label_mapping != None:
            label = self.new_label_mapping[label]
        return (output_text, label)
    

class SemEval2014_Laptops(DatasetLoader):
    def __init__(self):
        super().__init__()
        sp_dataset = datasets.load_dataset("yqzheng/semeval2014_laptops").shuffle(seed=42)
        self.table = datasets.concatenate_datasets([sp_dataset['train'], sp_dataset['test']])
        self.max = len(self.table)
        self.label_space = ['negative', 'neutral', 'positive']
        self.label_mapping = {
            -1: 'negative',
            0: 'neutral',
            1: 'positive'
        }
        self.dataset_name = 'SemEval 2014-Task 4 Laptops'
        self.neutral_label = 1
    
    def get_max(self):
        return self.max
    
    def divide(self, begin, end_not_include):
        self.table = self.table[begin: end_not_include]
        self.max = len(self.table['text'])
        return
    
    def get(self, index):
        if index is None:
            return (", Aspect: ", "")
        text = self.table['text'][index]
        aspect = self.table['aspect'][index]
        label = self.label_mapping[self.table['label'][index]]
        output_text = text + ', Aspect: ' + aspect
        if self.new_label_mapping != None:
            label = self.new_label_mapping[label]
        return (output_text, label)

class glue_rte(DatasetLoader):
    def __init__(self):
        super().__init__()
        sp_dataset = datasets.load_dataset("glue", "rte").shuffle(seed=42)
        self.table = datasets.concatenate_datasets([sp_dataset['train'], sp_dataset['validation']])
        self.max = len(self.table)
        self.label_space = ['include', 'neutral']
        self.label_mapping = {
            0: 'include',
            1: 'neutral'
        }
        self.dataset_name = 'GLUE-RTE'
    
    def get(self, index):
        if index is None:
            return (", Target: ", "")
        text1 = self.table['sentence1'][index]
        text2 = self.table['sentence2'][index]
        label_index = self.table['label'][index]
        label = self.label_mapping[label_index]
        output_text = text1 + ', Target: ' + text2
        if self.new_label_mapping != None:
            label = self.new_label_mapping[label_index]
        return (output_text, label)
    
    def divide(self, begin, end_not_include):
        self.table = self.table[begin: end_not_include]
        self.max = len(self.table['sentence1'])
        return


class glue_mrpc(DatasetLoader):
    def __init__(self):
        super().__init__()
        sp_dataset = datasets.load_dataset("glue", "mrpc").shuffle(seed=42)
        self.table = datasets.concatenate_datasets([sp_dataset['train'], sp_dataset['validation']])
        self.max = len(self.table)
        self.label_space = ['same', 'different']
        self.label_mapping = {
            0: 'different',
            1: 'same'
        }
        self.dataset_name = 'GLUE-MRPC'
    
    def get(self, index):
        if index is None:
            return (", Text 2: ", "")
        text1 = self.table['sentence1'][index]
        text2 = self.table['sentence2'][index]
        label_index = self.table['label'][index]
        label = self.label_mapping[label_index]
        output_text = text1 + ', Text 2: ' + text2
        if self.new_label_mapping != None:
            label = self.new_label_mapping[label_index]
        return (output_text, label)
    
    def divide(self, begin, end_not_include):
        self.table = self.table[begin: end_not_include]
        self.max = len(self.table['sentence1'])
        return


class ethos(DatasetLoader):
    def __init__(self):
        super().__init__()
        self.table = datasets.load_dataset("ethos", "binary")['train'].shuffle(seed=42)
        self.max = len(self.table)
        self.label_space = ['normal', 'hate']
        self.label_mapping = {
            0: 'normal',
            1: 'hate'
        }
        self.dataset_name = 'Ethos'
    
    def cut_by_length(self, max_length = 500):
        # This function is used to cut the dataset by length.
        # Must be called before the divide.
        exclude_list = []
        for i in range(0, len(self.table)):
            if len(self.table['text'][i]) > max_length:
                exclude_list.append(i)
        self.table  = self.table.select(
        (
            i for i in range(len(self.table)) 
            if i not in set(exclude_list)
        ))
        self.max = len(self.table)
    
    def get(self, index):
        if index is None:
            return ("", "")
        text = self.table['text'][index]
        label_index = self.table['label'][index]
        label = self.label_mapping[label_index]
        output_text = text
        if self.new_label_mapping != None:
            label = self.new_label_mapping[label_index]
        return (output_text, label)
    
    def divide(self, begin, end_not_include):
        self.table = self.table[begin: end_not_include]
        self.max = len(self.table['text'])
        return


class financial_phrasebank(DatasetLoader):
    def __init__(self):
        super().__init__()
        self.table = datasets.load_dataset("financial_phrasebank", "sentences_allagree")['train'].shuffle(seed=42)
        self.max = len(self.table)
        self.label_space = ['negative', 'neutral', 'positive']
        self.label_mapping = {
            0: 'negative',
            1: 'neutral',
            2: 'positive'
        }
        self.dataset_name = 'financial_phrasebank'
        self.neutral_label = 1
    
    def get(self, index):
        if index is None:
            return ("", "")
        text = self.table['sentence'][index]
        label_index = self.table['label'][index]
        label = self.label_mapping[label_index]
        output_text = text
        if self.new_label_mapping != None:
            label = self.new_label_mapping[label_index]
        return (output_text, label)
    
    def divide(self, begin, end_not_include):
        self.table = self.table[begin: end_not_include]
        self.max = len(self.table['sentence'])
        return


class glue_sst2(DatasetLoader):
    def __init__(self):
        super().__init__()
        sp_dataset = datasets.load_dataset("glue", "sst2").shuffle(seed=42)
        self.table = datasets.concatenate_datasets([sp_dataset['train'], sp_dataset['validation']])
        self.max = len(self.table)
        self.label_space = ['negative', 'positive']
        self.label_mapping = {
            0: 'negative',
            1: 'positive'
        }
        self.dataset_name = 'GLUE-SST2'
    
    def get(self, index):
        if index is None:
            return ("", "")
        text = self.table['sentence'][index]
        label_index = self.table['label'][index]
        label = self.label_mapping[label_index]
        output_text = text
        if self.new_label_mapping != None:
            label = self.new_label_mapping[label_index]
        return (output_text, label)
    
    def divide(self, begin, end_not_include):
        self.table = self.table[begin: end_not_include]
        self.max = len(self.table['sentence'])
        return


class tweet_eval_emotion(DatasetLoader):
    def __init__(self):
        super().__init__()
        sp_dataset = datasets.load_dataset("tweet_eval", "emotion").shuffle(seed=42)
        self.table = datasets.concatenate_datasets([sp_dataset['train'], sp_dataset['validation'], sp_dataset['test']])
        self.max = len(self.table)
        self.label_space = ['anger', 'joy', 'positive', 'sad']
        self.label_mapping = {
            0: 'anger',
            1: 'joy',
            2: 'positive',
            3: 'sad'
        }
        self.dataset_name = 'Tweet-Emotion'

    def get(self, index):
        if index is None:
            return ("", "")
        text = self.table['text'][index]
        label_index = self.table['label'][index]
        label = self.label_mapping[label_index]
        output_text = text
        if self.new_label_mapping != None:
            label = self.new_label_mapping[label_index]
        return (output_text, label)
    
    def divide(self, begin, end_not_include):
        self.table = self.table[begin: end_not_include]
        self.max = len(self.table['text'])
        return


class tweet_eval_hate(DatasetLoader):
    def __init__(self):
        super().__init__()
        sp_dataset = datasets.load_dataset("tweet_eval", "hate").shuffle(seed=42)
        self.table = datasets.concatenate_datasets([sp_dataset['train'], sp_dataset['validation'], sp_dataset['test']])
        self.max = len(self.table)
        self.label_space = ['normal', 'hate']
        self.label_mapping = {
            0: 'normal',
            1: 'hate'
        }
        self.dataset_name = 'Tweet-Hate'

    def get(self, index):
        if index is None:
            return ("", "")
        text = self.table['text'][index]
        label_index = self.table['label'][index]
        label = self.label_mapping[label_index]
        output_text = text
        if self.new_label_mapping != None:
            label = self.new_label_mapping[label_index]
        return (output_text, label)
    
    def divide(self, begin, end_not_include):
        self.table = self.table[begin: end_not_include]
        self.max = len(self.table['text'])
        return


class tweet_eval_sentiment(DatasetLoader):
    def __init__(self):
        super().__init__()
        sp_dataset = datasets.load_dataset("tweet_eval", "sentiment").shuffle(seed=42)
        self.table = datasets.concatenate_datasets([sp_dataset['train'], sp_dataset['validation'], sp_dataset['test']])
        self.max = len(self.table)
        self.label_space = ['negative', 'neutral', 'positive']
        self.label_mapping = {
            0: 'negative',
            1: 'neutral',
            2: 'positive'
        }
        self.dataset_name = 'Tweet-Sentiment'
        self.neutral_label = 1

    def get(self, index):
        if index is None:
            return ("", "")
        text = self.table['text'][index]
        label_index = self.table['label'][index]
        label = self.label_mapping[label_index]
        output_text = text
        if self.new_label_mapping != None:
            label = self.new_label_mapping[label_index]
        return (output_text, label)
    
    def divide(self, begin, end_not_include):
        self.table = self.table[begin: end_not_include]
        self.max = len(self.table['text'])
        return