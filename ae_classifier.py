import os
import pandas as pd
import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification
from torch.utils.data import DataLoader, TensorDataset
from tqdm import tqdm
import argparse

# Define the device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load the model from Hugging Face
model = RobertaForSequenceClassification.from_pretrained('vtiyyal1/AE-classification-RoBerta').to(device)
model.eval()

# Load the tokenizer
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')

# Function to prepare data loader
def prepare_data_loader(texts, batch_size=16):
    input_ids = []
    attention_masks = []
    for text in texts:
        encoded_dict = tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=512,  # Limit the length to 512 tokens
            padding='max_length',  # Pad to max length
            truncation=True,  # Truncate longer sequences
            return_attention_mask=True,
            return_tensors='pt'
        )
        input_ids.append(encoded_dict['input_ids'])
        attention_masks.append(encoded_dict['attention_mask'])

    input_ids = torch.cat(input_ids, dim=0)
    attention_masks = torch.cat(attention_masks, dim=0)

    dataset = TensorDataset(input_ids, attention_masks)
    data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=False)
    return data_loader

# Function to get predictions
def get_predictions(data_loader):
    all_preds = []
    model.eval()
    with torch.no_grad():
        for batch in tqdm(data_loader, desc="Predicting"):
            input_ids, attention_mask = [b.to(device) for b in batch]
            outputs = model(input_ids, attention_mask=attention_mask)
            preds = torch.argmax(outputs.logits, dim=1)
            all_preds.extend(preds.cpu().numpy())
    return all_preds

def main(input_file, output_file):
    # Load the input CSV file
    df = pd.read_csv(input_file)
    
    # Ensure the required columns exist
    if 'id' not in df.columns or 'comment' not in df.columns:
        raise ValueError("Input CSV must contain 'id' and 'comment' columns")
    
    # Prepare the data loader
    texts = df['comment'].astype(str).tolist()
    data_loader = prepare_data_loader(texts)

    # Get predictions
    predictions = get_predictions(data_loader)
    
    # Add predictions to the DataFrame
    df['ae_label'] = ['yes' if pred == 1 else 'no' for pred in predictions]

    # Save the output CSV file
    df[['id', 'comment', 'ae_label']].to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Adverse Event Classification Tool")
    parser.add_argument("--input", type=str, required=True, help="Path to the input CSV file")
    parser.add_argument("--output", type=str, required=True, help="Path to save the output CSV file")

    args = parser.parse_args()
    main(args.input, args.output)
