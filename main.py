import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import json


# 1. LOAD DATA
df = pd.read_csv('users.csv')


# 2. BASIC DATA EXPLORATION
print("=" * 50)
print("BASIC DATA EXPLORATION")
print("=" * 50)

# Shape
print(f"\nShape of DataFrame: {df.shape}")

# Column names
print(f"\nColumn Names:\n{list(df.columns)}")

# Data types
print(f"\nData Types:\n{df.dtypes}")

# Missing values
print("\nMissing Values Per Column:")
print(df.isnull().sum())

# Duplicate rows
duplicates = df.duplicated().sum()
print(f"\nNumber of Duplicate Rows: {duplicates}")

# Summary statistics for numeric columns
print("\nSummary Statistics (Numeric Columns):")
print(df.describe())

# Value counts for categorical columns
print("\nValue Counts - Gender:")
print(df['gender'].value_counts())

print("\nValue Counts - Blood Group:")
print(df['bloodGroup'].value_counts())

print("\nValue Counts - Eye Color:")
print(df['eyeColor'].value_counts())

print("\nValue Counts - Role:")
print(df['role'].value_counts())



# 3. DATA CLEANING / PREPARATION
print("\n" + "=" * 50)
print("DATA CLEANING")
print("=" * 50)

# --- Step 1: Drop maidenName column ---
df = df.drop(columns=['maidenName'])
print("\nDropped 'maidenName' column.")

# --- Step 2: Standardize birthDate to YYYY-MM-DD ---
df['birthDate'] = pd.to_datetime(df['birthDate'], errors='coerce')
print("Converted 'birthDate' to datetime format.")

# --- Step 3: Parse hair column ---
def parse_hair(val):
    try:
        d = json.loads(val.replace("'", '"'))
        return d.get('color', 'Unknown'), d.get('type', 'Unknown')
    except:
        return 'Unknown', 'Unknown'

df[['hairColor', 'hairType']] = df['hair'].apply(parse_hair).apply(pd.Series)
df = df.drop(columns=['hair'])
print("Parsed 'hair' into 'hairColor' and 'hairType', dropped original column.")

# --- Step 4: Parse address column ---
def parse_address(val):
    try:
        d = json.loads(val.replace("'", '"'))
        return (
            d.get('postalCode', 'Unknown'),
            d.get('address', 'Unknown'),
            d.get('city', 'Unknown'),
            d.get('state', 'Unknown'),
            d.get('country', 'Unknown')
        )
    except:
        return 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown'

df[['postalCode', 'street', 'city', 'state', 'country']] = df['address'].apply(parse_address).apply(pd.Series)
df = df.drop(columns=['address'])
print("Parsed 'address' into 'postalCode', 'street', 'city', 'state', 'country', dropped original column.")

# output country value counts immediately after parsing address
print("\nValue Counts - Country:")
print(df['country'].value_counts())

# --- Step 5: Parse bank column ---
def parse_bank(val):
    try:
        d = json.loads(val.replace("'", '"'))
        return (
            d.get('cardExpire', 'Unknown'),
            d.get('cardNumber', 'Unknown'),
            d.get('cardType', 'Unknown'),
            d.get('currency', 'Unknown'),
            d.get('iban', 'Unknown')
        )
    except:
        return 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown'

df[['cardExpire', 'cardNumber', 'cardType', 'currency', 'iban']] = df['bank'].apply(parse_bank).apply(pd.Series)
df = df.drop(columns=['bank'])
print("Parsed 'bank' into 'cardExpire', 'cardNumber', 'cardType', 'currency', 'iban', dropped original column.")

# --- Step 6: Parse company column ---
def parse_company(val):
    try:
        d = json.loads(val.replace("'", '"'))
        addr = d.get('address', {})
        return (
            d.get('department', 'Unknown'),
            d.get('name', 'Unknown'),
            d.get('title', 'Unknown'),
            addr.get('city', 'Unknown'),
            addr.get('state', 'Unknown'),
            addr.get('country', 'Unknown')
        )
    except:
        return 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown'

df[['company_department', 'company_name', 'company_title',
    'company_city', 'company_state', 'company_country']] = df['company'].apply(parse_company).apply(pd.Series)
df = df.drop(columns=['company'])
print("Parsed 'company' into 'company_department', 'company_name', 'company_title', 'company_city', 'company_state', 'company_country', dropped original column.")

# --- Step 7: Parse crypto column ---
def parse_crypto(val):
    try:
        d = json.loads(val.replace("'", '"'))
        return d.get('coin', 'Unknown'), d.get('wallet', 'Unknown'), d.get('network', 'Unknown')
    except:
        return 'Unknown', 'Unknown', 'Unknown'

df[['crypto_coin', 'crypto_wallet', 'crypto_network']] = df['crypto'].apply(parse_crypto).apply(pd.Series)
df = df.drop(columns=['crypto'])
print("Parsed 'crypto' into 'crypto_coin', 'crypto_wallet', 'crypto_network', dropped original column.")

# --- Step 8: Handle missing values in age, height, weight ---
for col in ['age', 'height', 'weight']:
    missing = df[col].isnull().sum()
    print(f"\nMissing values in '{col}': {missing}")
    if missing > 0:
        mean_val = df[col].mean()
        df[col] = df[col].fillna(mean_val)
        print(f"  -> Filled with mean: {mean_val:.2f}")
    else:
        print(f"  -> No missing values, no filling needed.")



# 4. ANALYSIS
print("\n" + "=" * 50)
print("ANALYSIS")
print("=" * 50)

# Average age
avg_age = df['age'].mean()
print(f"\nAverage Age of Users: {avg_age:.2f}")

# Average age by gender
avg_age_gender = df.groupby('gender')['age'].mean()
print(f"\nAverage Age by Gender:\n{avg_age_gender}")

# Number of users per gender
users_per_gender = df['gender'].value_counts()
print(f"\nNumber of Users Per Gender:\n{users_per_gender}")

# Top 10 cities by user count
top_cities = df.groupby('city').size().reset_index(name='User_Count')
top_cities = top_cities.sort_values('User_Count', ascending=False).head(10)
print(f"\nTop 10 Cities by User Count:\n{top_cities.to_string(index=False)}")

# Average height and weight overall
avg_height = df['height'].mean()
avg_weight = df['weight'].mean()
print(f"\nAverage Height: {avg_height:.2f}")
print(f"Average Weight: {avg_weight:.2f}")



# 5. VISUALIZATIONS
print("\n" + "=" * 50)
print("GENERATING VISUALIZATIONS...")
print("=" * 50)

# --- Plot 1: Top 10 Cities Bar Plot ---
plt.figure(figsize=(10, 6))
sns.barplot(data=top_cities, x='User_Count', y='city', palette='viridis')
plt.title('Top 10 Cities by User Count', fontsize=16)
plt.xlabel('Number of Users', fontsize=12)
plt.ylabel('City', fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# --- Plot 2: Users Per Gender Count Plot ---
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x='gender', palette='Set2')
plt.title('Number of Users Per Gender', fontsize=16)
plt.xlabel('Gender', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.tight_layout()
plt.show()

# --- Plot 3: Average Age by Gender Bar Plot ---
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x='gender', y='age', estimator='mean', palette='coolwarm', errorbar=None)
plt.title('Average Age by Gender', fontsize=16)
plt.xlabel('Gender', fontsize=12)
plt.ylabel('Average Age', fontsize=12)
plt.tight_layout()
plt.show()

# --- Plot 4: Age vs Height Scatter Plot ---
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x='age', y='height', hue='gender', palette='deep')
plt.title('Age vs Height', fontsize=16)
plt.xlabel('Age', fontsize=12)
plt.ylabel('Height (cm)', fontsize=12)
plt.tight_layout()
plt.show()

# --- Plot 5: Age vs Weight Scatter Plot ---
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x='age', y='weight', hue='gender', palette='deep')
plt.title('Age vs Weight', fontsize=16)
plt.xlabel('Age', fontsize=12)
plt.ylabel('Weight (kg)', fontsize=12)
plt.tight_layout()
plt.show()

df.to_csv("users_transformed.csv")