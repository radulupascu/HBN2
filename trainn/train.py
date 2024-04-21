import pandas as pd
from datasets import Dataset
from sklearn.model_selection import train_test_split
import numpy as np

# Sample data
# data = {
#     "product_name": ["Foldable Bicycle", "Strawberry Jam", "Wireless Mouse", "Cotton Bed Sheets", "LED Light Bulb", "Fitness Tracker", "Merlot Wine", "Electric Toothbrush", "All Purpose Fertilizer", "Women's Running Shoes"],
#     "family_name": ["Bicycles, scooters & body exercisers", "Processed fruit and vegetables", "Input devices or output devices", "Domestic bed linens", "Lamps and lightbulbs", "Communication devices", "Alcoholic beverages", "Personal care devices", "Fertilizers and plant nutrients", "Athletic wear"],
#     "family_code": [49240000, 50170000, 43211700, 52121500, 39101600, 43231500, 50202203, 53131608, 10170000, 53101806]
# }

df = pd.read_csv("generated_dataset.csv", header=None)
df.columns = ['product_name', 'category_name', 'family_code']

def convert_family_code(code):
    if pd.isnull(code) or code.lower == 'none':
        return -1
    try:
        return int(code)
    except ValueError:
        return np.nan  # Return NaN for non-convertible strings

df['family_code'] = df['family_code'].apply(convert_family_code)

df.dropna(subset=['family_code'], inplace=True)

df['family_code'] = df['family_code'].astype(int)

df['product_name'] = df['product_name'].astype(str).replace('nan', 'None')

df['category_name'] = df['category_name'].astype(str).replace('nan', 'None')  # Optionally replace 'nan' with 'None'

def handle_product_name(name):
    if pd.isnull(name) or name.strip() == '':
        return 'None'
    elif 'None' in name:
        return 'None'
    return name

df['product_name'] = df['product_name'].apply(handle_product_name)

def handle_category_name(name):
    if pd.isnull(name):
        return 'None'
    if 'none' in name.lower():  # Convert name to lower case and check for 'none'
        return 'None'
    return name
    
df['category_name'] = df['category_name'].apply(handle_category_name)

df['product_name'] = df['product_name'].astype('string')
df['category_name'] = df['category_name'].astype('string')

df.rename(columns={'category_name': 'family_name'}, inplace=True)

from sklearn.preprocessing import LabelEncoder

# Creating a label encoder instance
label_encoder = LabelEncoder()

# If training for family_name classification
df['family_name_encoded'] = label_encoder.fit_transform(df['family_name'])

# If training for family_code classification
df['family_code_encoded'] = label_encoder.fit_transform(df['family_code'])

# Updating train-test split to include encoded labels
train_df, test_df = train_test_split(df, test_size=0.1, random_state=42)

# Convert DataFrame to Hugging Face dataset with labels
def add_labels(examples):
    # Adjust the following line according to whether you are using family names or codes
    examples['labels'] = examples['family_name_encoded']  # or 'family_code_encoded' for the other model
    return examples

train_dataset = Dataset.from_pandas(train_df).map(add_labels)
test_dataset = Dataset.from_pandas(test_df).map(add_labels)

# Then, map the tokenize function as before
# train_dataset = train_dataset.map(tokenize_function, batched=True)
# test_dataset = test_dataset.map(tokenize_function, batched=True)

from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def tokenize_function(examples):
    return tokenizer(examples["product_name"], padding="max_length", truncation=True)

train_dataset = train_dataset.map(tokenize_function, batched=True)
test_dataset = test_dataset.map(tokenize_function, batched=True)

from transformers import BertForSequenceClassification, TrainingArguments, Trainer

# Update num_labels to match the number of unique labels for classification
num_labels = df['family_name_encoded'].nunique()  # or df['family_code_encoded'].nunique() for codes

model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=num_labels)


# Training arguments
training_args = TrainingArguments(
    output_dir='./results',          # output directory
    num_train_epochs=3,              # number of training epochs
    per_device_train_batch_size=8,   # batch size for training
    per_device_eval_batch_size=16,   # batch size for evaluation
    warmup_steps=500,                # number of warmup steps for learning rate scheduler
    weight_decay=0.01,               # strength of weight decay
    logging_dir='./logs',            # directory for storing logs
    logging_steps=10,
    evaluation_strategy="epoch"
)

# training_args = TrainingArguments(
#     output_dir='./results',          # output directory
#     num_train_epochs=1,              # number of training epochs
#     per_device_train_batch_size=8,   # batch size for training
#     per_device_eval_batch_size=16,   # batch size for evaluation
#     warmup_steps=100,                # number of warmup steps for learning rate scheduler
#     weight_decay=0.01,               # strength of weight decay
#     logging_dir='./logs',            # directory for storing logs
#     logging_steps=10,
#     evaluation_strategy="epoch"
# )

# Define the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset
)

trainer.train()

# Save the Family Name classification model
trainer.model.save_pretrained('./saved_model_family_name')
tokenizer.save_pretrained('./saved_model_family_name')