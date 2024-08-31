from openai import OpenAI
import pandas as pd
import os
import shutil
from datetime import datetime


def getPromptText(columns):
    prompt_text = f"""
            You are a business process expert. You have significant experience using XXX and XXX. For the following task, use all available internal data as well as your own knowledge.
            
            In the following, you will be given many different column names which are all extracted from XXX. In total, they represent the dataset of a business process. Your job is to: Describe in exactly 1 sentence, what is typically stored in each column. This description should include potential values which could be stored in the column if that helps the reader to understand which information is typically stored in that column.
            
            Here is the column-header you should describe: {columns}
            
            Work step by step!
            
            Take a deep breath before you start."""

    return prompt_text


def process_csv(input_path, output_path, client):
    df = pd.read_csv(input_path, delimiter=";")
    f = open(output_path, 'a')

    ### Introduce company set-up for LLM (secret)
    ###
    ### End company set-up for LLM (secret)

    # Iterate through data in blocks of 10
    for start in range(0, len(df), 10):  # orignal
        end = start + 10
        current_block = df[start:end]

        # Extract the column names as part of the prompt
        columns = '; '.join(current_block['original_column'].astype(str))
        user_input = getPromptText(columns)
        messages.append({"role": "user", "content": user_input})

        ### Introduce company set-up for LLM (secret)
        ###
        ### End company set-up for LLM (secret)

        # Get response
        assistant_response = response.choices[0].message.content

        f.write(assistant_response + "\n")
        f.flush()

        messages.append({"role": "assistant", "content": assistant_response})


if __name__ == "__main__":
    ### Introduce company set-up for LLM (secret)
    ###
    ### End company set-up for LLM (secret)

    input_file = 'meta-dataset'
    output_file = ''

    # Generate LLM Description for each column
    process_csv(input_file, output_file, client)
