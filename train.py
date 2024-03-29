import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load your dataset into a DataFrame (replace 'your_dataset.csv' with the actual file path)
df = pd.read_csv('Cosmeticsdataset.xlsx')

# Extract features (ingredients and chemical components) and labels (toxicity)
X = df[['Ingredients', 'Dioxane', 'Acrylates', 'Benzophenone', 'Carbon black', 'Carcinogens', 'CoalTar', 'Ethanolamaine', 'Homosalate', 'Hydroquinone', 'Lead', 'Lead Acetate', 'Methylisothiazolinone', 'Methylchloroisothiazolinone', 'Mica', 'Isopropyl acetone', 'methyl ethyl ketone', 'Retinol', 'Parabens', 'arsenic', 'zinc', 'chromium']]
y = df['Toxicity']  # Assuming 'Toxicity' is the column containing toxicity labels (1 for toxic and 0 for non-toxic)

# Initialize a Random Forest classifier with hyperparameters (adjust these as needed)
random_forest = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model on your dataset
random_forest.fit(X, y)

# Save the trained model to disk using joblib
joblib.dump(random_forest, 'toxicity_model.joblib')
