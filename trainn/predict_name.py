import pandas as pd
import torch
from transformers import BertForSequenceClassification, BertTokenizer
from sklearn.preprocessing import LabelEncoder

# Load the category labels from a CSV file
labels_df = pd.read_csv('cleaned_dataset_str.csv')
unique_labels = labels_df['family_name'].unique()

# Create a label encoder object
label_encoder = LabelEncoder()
label_encoder.fit(unique_labels)

def prepare_input(text_list, tokenizer):
    # Tokenize a batch of inputs
    return tokenizer(text_list, padding=True, truncation=True, return_tensors="pt", max_length=512)

def predict(df, model, tokenizer, label_encoder):
    model.eval()  # Set model to evaluation mode
    inputs = prepare_input(df['product_name'].tolist(), tokenizer)
    
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.argmax(outputs.logits, dim=1).numpy()  # Get the index of max logit
        predicted_labels = label_encoder.inverse_transform(predictions)  # Decode index to label

    df['predicted_family_name'] = predicted_labels
    return df

# Load the model and tokenizer
model = BertForSequenceClassification.from_pretrained('./saved_model_family_name')
tokenizer = BertTokenizer.from_pretrained('./saved_model_family_name')

# Example DataFrame
pred_files = ["prod.csv", "product_names.csv"]
df = pd.read_csv(pred_files[0], header=None)
df = df.iloc[1:1001]
df.columns = ['product_name']

# Predict and display results
df['product_name'] = df['product_name'].astype(str).replace('nan', 'None')
def handle_product_name(name):
    if pd.isnull(name) or name.strip() == '':
        return 'None'
    elif 'None' in name:
        return 'None'
    return name
df['product_name'] = df['product_name'].apply(handle_product_name)
df['product_name'] = df['product_name'].astype('string')
print(df.info())
print(df.head())

df = predict(df, model, tokenizer, label_encoder)
df.to_csv("prediction_name.csv", mode='a', header=False, index=False)
