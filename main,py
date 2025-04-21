import pandas as pd
import json
from pathlib import Path
from utils import Traducteur, Evaluator, Data, Formatter
import typer
from itertools import product
from tqdm import tqdm
import os
from pprint import pprint
from time import sleep
import random
import litellm
litellm.suppress_debug_info = True
import logging
import glob
import math
logging.getLogger().setLevel(logging.CRITICAL)

app = typer.Typer()

dialect_keys = {
    "lebanon_north": ["LB_EN", "LB_AR"],
    "lebanon_south": ["LB_EN", "LB_AR"],
    "algeria_algiers": ["ALG_EN", "ALG_AR"],
    "algeria_constantine": ["ALG_EN", "ALG_AR"],
    "egypt_cairo": ["EG_EN", "EG_AR"],
    "egypt_louxour": ["EG_EN", "EG_AR"]
}

def clean_string(s):
    """
    Cleans a string by handling NaN values and preprocessing text.

    This function checks if the input is a NaN value and returns "NaN" if true.
    Otherwise, it performs the following preprocessing steps:
    1. Replaces newlines with spaces
    2. Attempts to extract the substring after the first colon (if present)
    3. Removes trailing whitespace

    Parameters:
    ----------
    s : str or numeric
        The input to clean, which can be a string or a value that might be NaN

    Returns:
    -------
    str
        The cleaned string or "NaN" if the input is NaN

    Raises:
    ------
    TypeError may be caught internally when attempting to check if a non-numeric value is NaN
    """
    try:
        if math.isnan(s):
            return "NaN"
    except TypeError:
        s = s.replace("\n", " ")
        try:
            s = s.split(":")[1]
        except:
            s = s
        s = s.rstrip()
        return s

@app.command()
def processdata():
    print(f"Processing data...")
    pipeline = Data()
    corpus = pipeline.processdata()
    print(f"Checking corpus is correct...")
    for dialect in corpus.keys():
        l = [len(v) for v in corpus[dialect].values()]
        assert len(set(l)) == 1, f"Error in {dialect} corpus."
        
    with open("corpus/corpus.json", "w") as f:
        json.dump(corpus, f, indent=4, ensure_ascii=False)
    print(f"Data processed and saved to 'corpus/corpus.json'.")

@app.command()
def createtranscorpora(target_lang: str = "EN"):
    MODELS = ["gpt4o", "claude3", "llama3", "gemma2", "mistrallarge", "jais", "gemini"]
    dialects = ['lebanon_north', 'lebanon_south', 'algeria_algiers', 'algeria_constantine', 'egypt_cairo', 'egypt_louxour']
    countries = ["lebanon", "algeria", "egypt"]
    prompt_tech = ["no-shot", "one-shot", "two-shot"]
    prompt_langs = ["EN", "AR"]

    for prompt_lang in prompt_langs:
        print(f"Creating translation corpora with prompt_lang {prompt_lang}...")
    
        root_in = f"translations/{prompt_lang}"
        root_out = f"translation_corpora/{prompt_lang}"
        if not os.path.exists(root_out):
            os.makedirs(root_out)

        target_langs = ["EN", "AR"]
        if target_lang not in target_langs:
            print(f"Error: {target_lang} not supported.")
            return
            
        filepaths = [f for f in glob.glob(f"{root_in}/**/*", recursive=True) if f.endswith(f"{target_lang}.json")]

        # by "country"
        for country in countries:
            formatter = Formatter()
            file_out_s = f"{root_out}/{country}_{target_lang}_source.txt"
            file_out_t = f"{root_out}/{country}_{target_lang}_target.txt"
            for country in countries:
                country_files = [f for f in filepaths if country in f]
                data = formatter.format(country_files)
                with open(file_out_s, "a") as f:
                    for d in data:
                        f.write(f"{clean_string(d['arabizi'])}\n")
                    f.close()
                with open(file_out_t, "a") as f:
                    for d in data:
                        f.write(f"{clean_string(d['traduction'])}\n")
                    f.close()
        
        # by country and model
        for country in countries:
            for model in MODELS:
                formatter = Formatter()
                file_out_s = f"{root_out}/{country}_{model}_{target_lang}_source.txt"
                file_out_t = f"{root_out}/{country}_{model}_{target_lang}_target.txt"
                country_files = [f for f in filepaths if country in f and model in f]
                data = formatter.format(country_files)
                with open(file_out_s, "a") as f:
                    for d in data:
                        f.write(f"{clean_string(d['arabizi'])}\n")
                    f.close()
                with open(file_out_t, "a") as f:
                    for d in data:
                        f.write(f"{clean_string(d['traduction'])}\n")
                    f.close()
        
        # by prompt technique:
        for prompt in prompt_tech:
            formatter = Formatter()
            file_out_s = f"{root_out}/{prompt}_{target_lang}_source.txt"
            file_out_t = f"{root_out}/{prompt}_{target_lang}_target.txt"
            prompt_files = [f for f in filepaths]
            data = formatter.format(prompt_files)
            with open(file_out_s, "a") as f:
                for d in data:
                    if d['prompt'] == prompt:
                        f.write(f"{clean_string(d['arabizi'])}\n")
                f.close()
            with open(file_out_t, "a") as f:
                for d in data:
                    if d['prompt'] == prompt:
                        f.write(f"{clean_string(d['traduction'])}\n")
                f.close()
        # by model:
        for model in MODELS:
            formatter = Formatter()
            file_out_s = f"{root_out}/{model}_{target_lang}_source.txt"
            file_out_t = f"{root_out}/{model}_{target_lang}_target.txt"
            model_files = [f for f in filepaths if model in f]
            data = formatter.format(model_files)
            with open(file_out_s, "a") as f:
                for d in data:
                    f.write(f"{clean_string(d['arabizi'])}\n")
                f.close()
            with open(file_out_t, "a") as f:
                for d in data:
                    f.write(f"{clean_string(d['traduction'])}\n")
                f.close()
        
        # by model and prompt technique:
        for model in MODELS:
            for prompt in prompt_tech:
                formatter = Formatter()
                file_out_s = f"{root_out}/{model}_{prompt}_{target_lang}_source.txt"
                file_out_t = f"{root_out}/{model}_{prompt}_{target_lang}_target.txt"
                model_files = [f for f in filepaths if model in f]
                data = formatter.format(model_files)
                with open(file_out_s, "a") as f:
                    for d in data:
                        if d['prompt'] == prompt:
                            f.write(f"{clean_string(d['arabizi'])}\n")
                    f.close()
                with open(file_out_t, "a") as f:
                    for d in data:
                        if d['prompt'] == prompt:
                            f.write(f"{clean_string(d['traduction'])}\n")
                    f.close()
        # by model and country:
        for model in MODELS:
            for country in countries:
                formatter = Formatter()
                file_out_s = f"{root_out}/{model}_{country}_{target_lang}_source.txt"
                file_out_t = f"{root_out}/{model}_{country}_{target_lang}_target.txt"
                model_files = [f for f in filepaths if model in f and country in f]
                data = formatter.format(model_files)
                with open(file_out_s, "a") as f:
                    for d in data:
                        f.write(f"{clean_string(d['arabizi'])}\n")
                    f.close()
                with open(file_out_t, "a") as f:
                    for d in data:
                        f.write(f"{clean_string(d['traduction'])}\n")
                    f.close()






@app.command()
def translate(dialect: str = "lebanon_north", model: str = "all", promptlang: str = "AR"):
    MODELS = ["gpt4o", "claude3", "llama3q", "llama3", "gemma2", "mistrallarge", "jais", "gemini"]
    outdir = f"translations/{promptlang}"
    try:
        os.makedirs(outdir, exist_ok=True)
    except FileExistsError:
        print(f"Directory {outdir} already exists.")
    
    """
    if dialect == "all":
        dialects = ['lebanon_north', 'lebanon_south', 'algeria_algiers', 'algeria_constantine', 'egypt_cairo', 'egypt_louxour']
    elif dialect not in ['lebanon_north', 'lebanon_south', 'algeria_algiers', 'algeria_constantine', 'egypt_cairo', 'egypt_louxour']:
        print(f"Error: {dialect} not in corpus.")
        return
    """
    if dialect not in ['lebanon_north', 'lebanon_south', 'algeria_algiers', 'algeria_constantine', 'egypt_cairo', 'egypt_louxour']:
        print(f"Error: {dialect} not in corpus.")


    with open(f"corpus/corpus.json", "r") as f:
        corpus = json.load(f)

    if model == "all":
        models = MODELS
    elif model not in MODELS:
        print(f"Error: {model} not supported.")    
    else: 
        models = [model]
    
    # generate prompts
    
    with open(f"prompts/prompts_{promptlang}.json", "r") as f:
        prompts_r = json.load(f)
    
    prompts_target = {}
    for target in dialect_keys[dialect]: # lb_en, lb_ar
        prompts_target[target] = prompts_r[target]
    
    corpus = corpus[dialect]
    for target in prompts_target.keys():
        print(f"Translating {dialect} with {model}, target is {target}...")
        prompts = prompts_target[target]
        combinations = list(product(models, prompts))
        #print(f"All possible unique combinations: {combinations}")
        
        arabizi = corpus['arabizi']
        ref_arabic = corpus['ref_arabic']
        ref_english = corpus['ref_english']
        ids = corpus['ids']
        
        traductions = []
        sysprompt = f"You are a translator. Only return the translation, nothing else."
        
        for sentence, identifier in tqdm(zip(arabizi, ids), total=len(arabizi)):
            for model, prompt in combinations:
        
                real_prompt = prompts[prompt]
                
                traducteur = Traducteur(model)
            
                traduction, usage = traducteur.traduire(sysprompt, real_prompt, sentence)
                traductions.append({ 
                        "sentence_id": identifier,
                        "arabizi": sentence,
                        "ref_arabic": ref_arabic[identifier-1],
                        "ref_english": ref_english[identifier-1],
                        "traduction": traduction,
                        "usage": usage,
                        "model": model,
                        "prompt": prompt
                    })
                
            if model == "mistrallarge":
                #sleep(random.randint(0, 2))
                # mistral is ratelimiting like crazy 
                sleep(1)

        with open(f"{outdir}/{dialect}_{model}_{target}.json", "w") as f:
            json.dump(traductions, f, indent=4, ensure_ascii=False)
        print(f"Translations saved to '{outdir}/{dialect}_{model}_{target}.json'.")
    

if __name__ == "__main__":
    app()