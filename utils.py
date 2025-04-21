import openai
import os
from dotenv import load_dotenv
from sacrebleu.metrics import BLEU, CHRF, TER
from comet import download_model, load_from_checkpoint
#from litellm import completion
import pandas as pd
import json


load_dotenv()

##### local litellm deployment #####
API_KEY = "sk-1234" 
URL = "http://192.168.0.18:4000" 

client = openai.Client(
    api_key = API_KEY,
    base_url = URL
)

class Data:
    def __init__(self):
        excel_file = pd.ExcelFile("MT for Arabizi.xlsx")
        self.sheet_names = excel_file.sheet_names
        return
    
    def processdata(self):
        if not os.path.exists("corpus"):
            os.makedirs("corpus")
        corpus = {}
        for sheet in self.sheet_names:
            dialect = sheet.replace("Corpus ", "").replace(" ", "_").lower() 
            df_sheet = pd.read_excel("MT for Arabizi.xlsx", sheet_name=sheet, index_col=0)
            data = {
                "ids": [],
                "arabizi": [],
                "ref_arabic": [],
                "ref_english": []
                    }
            for index, row in df_sheet.iterrows():
                # check if not nan
                if pd.isna(index):
                    continue
                data['ids'].append(int(index))
                try:
                    arabizi = str(row['Corpus en arabe romanisé'])
                    arabizi = arabizi.split(": ")[1]
                    #print(arabizi)
                except:
                    arabizi = row['Corpus en arabe romanisé']
                data['arabizi'].append(arabizi)
                data['ref_arabic'].append(str(row["Traduction humaine vers l'arabe classique"]))
                data['ref_english'].append(str(row["Traduction humaine vers l'anglais"]))
            corpus[dialect] = data
        return corpus



class Traducteur:
    def __init__(self, model_id):
        self.model_id = model_id
        self.client = openai.Client(
            api_key = API_KEY,
            base_url = URL
        )
        return
    
    def traduire(self, sysprompt, prompt, sentence):
        input_text = f"{prompt}\n{sentence}"
        completion = self.client.chat.completions.create(
            model=self.model_id,
            #seed=1830,
            temperature=0.5,
            messages=[

                {"role": "system", "content": sysprompt},
                {"role": "user", "content": input_text}

                    ]
            ) 
        #print(completion.usage.total_tokens)
        return completion.choices[0].message.content, completion.usage.total_tokens

class Formatter:
    def __init__(self):
        return
    def format(self, filepaths):
        formatted_data = []
        for filepath in filepaths:
            with open(filepath, "r") as f:
                data = json.load(f)
            
            for d in data:
                formatted_data.append({
                    "sentence_id": d["sentence_id"],
                    "arabizi": d["arabizi"],
                    "ref_arabic": d["ref_arabic"],
                    "ref_english": d["ref_english"],
                    "traduction": d["traduction"],
                    "usage": d["usage"],
                    "model": d["model"],
                    "prompt": d["prompt"]
                })
        return formatted_data

class Evaluator:
    def __init__(self):
        #with open(".env") as f:
        #    t = f.read().rstrip().split("=")[1]
        #model_path = download_model("Unbabel/XCOMET-XL")
        #self.model = load_from_checkpoint(model_path)
        return
    
    def evaluate(self, reference_translations, translated_texts, source_texts = []):
        """
        One catch-all function to evaluate translations
        COMET in another script
        """
        data = {
            "src": source_texts,
            "mt": translated_texts,
            "ref": reference_translations
        }

        bleu = BLEU()
        chrf = CHRF()
        ter = TER()
        
        bleu_score = bleu.corpus_score(reference_translations, translated_texts)
        chrf_score = chrf.corpus_score(reference_translations, translated_texts)
        ter_score = ter.corpus_score(reference_translations, translated_texts)
        #comet_score = self.model.predict(data, batch_size=8, gpus=1).system_score

        return bleu_score, chrf_score, ter_score#, comet_score