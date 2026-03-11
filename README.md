# User Data Analysis Project

## Project Overview

This is a beginner data engineering project that fetches user data from the [DummyJSON Users API](https://dummyjson.com/users?limit=100) and performs exploratory data analysis (EDA) using Python.

The project has two main scripts:

- **`read.py`** – Fetches user data from the DummyJSON API and saves it locally as `users.csv`.
- **`main.py`** – Loads the CSV file and performs data exploration, cleaning, analysis, and visualization using **pandas**, **matplotlib**, and **seaborn**.

---

## Steps Taken

### 1. Data Loading
- Loaded `users.csv` into a pandas DataFrame using `pd.read_csv()`.
- The raw dataset contains 100 users with various nested and complex fields.

### 2. Basic Exploration
- Checked the shape of the DataFrame (rows and columns).
- Listed all column names and their data types.
- Counted missing values per column and duplicate rows.
- Generated summary statistics for numeric columns using `.describe()`.
- Displayed value counts for categorical columns: `gender`, `bloodGroup`, `eyeColor`, and `role`.

### 3. Data Cleaning & Preparation

The data cleaning phase involves 8 detailed steps to normalize and structure the data:

**Step 1: Drop maidenName column**
- Removed the `maidenName` column as it was not needed for analysis.

**Step 2: Standardize birthDate**
- Converted the `birthDate` column to datetime format (YYYY-MM-DD) using `pd.to_datetime()` with error handling set to 'coerce' for robustness.

**Step 3: Parse hair column**
- The `hair` column contained JSON-like strings with nested data (e.g., `{'color': '...', 'type': '...'}`).
- Used `json.loads()` with string replacement to handle single quotes (`'` → `"`).
- Extracted two new columns: `hairColor` and `hairType`.
- Dropped the original `hair` column.

**Step 4: Parse address column**
- The `address` column contained nested JSON-like strings.
- Extracted five new columns: `postalCode`, `street`, `city`, `state`, and `country`.
- After parsing, immediately printed value counts for the `country` column to satisfy reporting requirements.
- Dropped the original `address` column.

**Step 5: Parse bank column**
- The `bank` column contained nested JSON-like strings with banking information.
- Extracted five new columns: `cardExpire`, `cardNumber`, `cardType`, `currency`, and `iban`.
- Dropped the original `bank` column.

**Step 6: Parse company column**
- The `company` column contained nested JSON-like strings with company and location data.
- Extracted six new columns: `company_department`, `company_name`, `company_title`, `company_city`, `company_state`, and `company_country`.
- Note: Company columns use a prefix to distinguish them from personal user data.
- Dropped the original `company` column.

**Step 7: Parse crypto column**
- The `crypto` column contained nested JSON-like strings with cryptocurrency information.
- Extracted three new columns with the `crypto_` prefix to prevent name collisions: `crypto_coin`, `crypto_wallet`, and `crypto_network`.
- Dropped the original `crypto` column.

**Step 8: Handle missing values in numeric columns**
- Checked for missing values in `age`, `height`, and `weight`.
- For any column with missing values, filled them using the column mean using `.fillna()`.
- Printed status messages for each column showing the number of missing values and the mean used for filling (if applicable).

### 4. Analysis
- Calculated the **average age** of all users.
- Calculated the **average age grouped by gender**.
- Counted the **number of users per gender**.
- Found the **Top 10 cities** with the most users and their respective user counts.
- Calculated the **average height** and **average weight** overall.

### 5. Visualizations
Created 5 Seaborn plots to visualize the data:

1. **Top 10 Cities by User Count** – Horizontal bar plot with viridis color palette and gridlines
2. **Number of Users Per Gender** – Count plot with Set2 color palette
3. **Average Age by Gender** – Bar plot with coolwarm color palette
4. **Age vs Height** – Scatter plot colored by gender with deep color palette
5. **Age vs Weight** – Scatter plot colored by gender with deep color palette

### 6. Output
- The cleaned and transformed DataFrame is saved to `users_transformed.csv` for further use or analysis.

---

## Data Transformation Summary

After all cleaning and parsing steps, the dataset is transformed from the original raw columns to a structured, flat format. Here's an overview of the final columns available:

**Personal Information:**
- `id`, `firstName`, `lastName`, `age`, `gender`, `email`, `phone`, `birthDate` (datetime)

**Physical Attributes:**
- `height`, `weight`, `eyeColor`

**Employment & Company:**
- `company_department`, `company_name`, `company_title`, `company_city`, `company_state`, `company_country`

**Address & Location:**
- `city`, `state`, `country`, `street`, `postalCode`

**Professional:**
- `role`, `bloodGroup`

**Appearance:**
- `hairColor`, `hairType`

**Banking:**
- `cardExpire`, `cardNumber`, `cardType`, `currency`, `iban`

**Cryptocurrency:**
- `crypto_coin`, `crypto_wallet`, `crypto_network`

All nested JSON structures have been flattened into a single-level DataFrame, making it easier to query, analyze, and visualize the data.

---

## Key Findings

- The dataset contains 100 users with no duplicate rows.
- The gender split is roughly even between male and female users.
- The average age is around the mid-30s, and it is similar across genders.
- The Top 10 cities each have only a small number of users, showing the data is spread across many cities.
- The scatter plots for Age vs Height and Age vs Weight show **no strong linear relationship** between age and height/weight, meaning these variables are mostly independent in this dataset.

---

## Visualizations

### Plot 1 – Top 10 Cities by User Count
![visuals/Top 10 Cities.png](https://github.com/MazinBakry/ITI_PythonDataAnalyticsLibraries/blob/main/visuals/Top%2010%20Cities.png)

### Plot 2 – Number of Users Per Gender
![visuals/Users Per Gender.png](https://github.com/MazinBakry/ITI_PythonDataAnalyticsLibraries/blob/main/visuals/Users%20Per%20Gender.png)

### Plot 3 – Average Age by Gender
![visuals/Average Age by Gender.png](https://github.com/MazinBakry/ITI_PythonDataAnalyticsLibraries/blob/main/visuals/Average%20Age%20by%20Gender.png)

### Plot 4 – Age vs Height
![visuals/Age vs Height.png](https://github.com/MazinBakry/ITI_PythonDataAnalyticsLibraries/blob/main/visuals/Age%20vs%20Height.png)

### Plot 5 – Age vs Weight
![visuals/Age vs Weight.png](https://github.com/MazinBakry/ITI_PythonDataAnalyticsLibraries/blob/main/visuals/Age%20vs%20Weight.png)

---

## How to Run

1. Run `read.py` first to fetch data from the API and create `users.csv`:
   ```bash
   python read.py
   ```
2. Then run `main.py` to perform the analysis and generate plots:
   ```bash
   python main.py
   ```

## Requirements

- Python 3
- pandas
- matplotlib
- seaborn
- requests (for `read.py`)
