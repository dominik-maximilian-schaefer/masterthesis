from openai import OpenAI
import pandas as pd
import os
import shutil
from datetime import datetime
from PyPDF2 import PdfReader
import itertools
import re


def save_dictionary_to_csv(dictionary, output_file):
    flattened_data = []

    for keyword, data in dictionary.items():
        unique_primary_keys = set(data['primary_keys'])
        count = len(unique_primary_keys)
        primary_keys = '; '.join(unique_primary_keys)
        flattened_data.append({
            'Keyword': keyword,
            'Count': count,
            'Primary Keys': primary_keys
        })
        print(f"{keyword}: {count}, {primary_keys}")

    df = pd.DataFrame(flattened_data)
    df.to_csv(output_file, sep=';', index=False)


def search_combinations_in_csv(file_path, columns):

    # Dynamic Script: Comment out/in the snippets needed!

    ## ENERGY CONSUMPTION
    """
    set1 = ["Energy","dynamism", "electricity", "heat", "potential", "service", "strength","Power"]
    set2 = ["Consumption","drinking", "expenditure", "utilization","using up", "use", "loss", "waste", "drain", "consuming", "expenditure", "exhaustion", "depletion", "utilization", "dissipation"]
    combinations = [' '.join(combo) for combo in itertools.product(set1, set2)]
    #combinations = set2
    #print(len(combinations))
    print(combinations)
    """

    ## EMISSIONS
    """
    set1 = ["Greenhouse", "arboretum", "conservatory", "nursery", "glasshouse", "conservatory", "hothouse"]
    set2 = ["Gas", "smoke", "vapor", "fumes", "vapour", "mist", "fog", "haze", "smoke", "breath", "steam", "fumes", "dampness", "miasma", "exhalation"]
    set3 = ["Emission","discharge", "radiation", "giving off", "giving out", "release", "shedding", "leak", "radiation", "discharge", "transmission", "venting", "issue", "diffusion", "utterance", "ejaculation", "outflow", "issuance", "ejection", "exhalation", "emanation", "exudation"]
    set4 = ["Carbon", "graphite", "soot"]
    set5 = ["Dioxide"]
    set6 = ["Footprint"]
    #combinations = [' '.join(combo) for combo in itertools.product(set4, set5)]
    combinations = set3
    #print(len(combinations))
    print(combinations)
    """

    ## MATERIAL USE and WASTE GENERATION
    # """
    set1 = ["Material", "cloth", "component", "element", "equipment", "goods", "ingredient", "machinery", "object",
            "stuff", "substance", "supply", "textile", "substance", "body", "matter", "stuff", "elements",
            "constituents"]
    set2 = ["Use", "adopt", "apply", "employ", "handle", "manage", "operate", "practice", "run", "spend", "utilize",
            "wield", "work", "consume", "go through", "exhaust", "spend", "waste", "get through", "run through",
            "deplete", "squander", "dissipate", "expend", "fritter away"]
    set3 = ["Waste", "debris", "rubbish", "scrap", "trash", "rubbish", "refuse", "debris", "sweepings", "scrap",
            "litter", "garbage", "trash", "leftovers", "offal", "dross", "dregs", "leavings", "offscourings"]
    set4 = ["Generation", "bearing", "breeding", "formation", "genesis", "origination", "procreation", "propagation",
            "reproduction", "production", "manufacture", "manufacturing", "creation", "formation", "origination",
            "production", "breeding", "creation", "formation", "reproduction", "genesis", "propagation", "begetting",
            "procreation", "origination", "engenderment"]
    combinations = [' '.join(combo) for combo in itertools.product(set1, set2)]
    # combinations = set4
    print(combinations)
    # """

    ## Compound terms
    """
    set1 = ["Energy Consumption"]
    set2 = ["Greenhouse Gas"]
    set3 = ["Greenhouse Gas Emission"]
    set4 = ["GHG Emission"]
    set5 = ["Carbon Dioxide", "carbonic acid", "carbonic acid gas", "CO2"]
    set6 = ["Carbon Dioxide Footprint"]
    set7 = ["CO2 Footprint"]
    set8 = ["Material Use"]
    set9 = ["Waste Generation"]
    combinations = set8
    print(combinations)
    """

    df = pd.read_csv(file_path)

    combination_counts = {combo: {"count": 0, "primary_keys": []} for combo in combinations}

    for col in columns:
        if col in df.columns:
            for idx, row in df.iterrows():
                primary_key = row['original_column']
                for combo in combinations:
                    if pd.notna(row[col]) and re.search(re.escape(combo), row[col], re.IGNORECASE):
                        combination_counts[combo]["count"] += 1
                        combination_counts[combo]["primary_keys"].append(primary_key)

    filtered_counts = {k: v for k, v in combination_counts.items() if v["count"] > 0}
    sorted_counts = dict(sorted(filtered_counts.items(), key=lambda item: item[1]["count"], reverse=True))
    if not sorted_counts:
        print("No combinations are found with occurrences greater than zero.")
        return "No combinations are found with occurrences greater than zero."

    (sorted_counts, output_file)
    return sorted_counts


if __name__ == "__msave_dictionary_to_csvain__":
    input_file = 'meta-dataset'
    output_file = ''
    columns = ["original_column", "demo_values", "LLM"]

    # Find matches for keywords in meta-dataset
    search_combinations_in_csv(input_file, columns)