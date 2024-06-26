#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
df= pd.read_csv("wind_power_combined.csv")
df


# In[2]:

def predict_power_generation(input_data, model):
    """
    Predict power generation using the trained Random Forest regressor.
    
    Parameters:
        input_data (DataFrame): DataFrame containing features for prediction.
        model: Trained Random Forest regressor model.
    
    Returns:
        predictions (array): Predicted power generation values.
    """
    # Extracting features for prediction
    X_forecasted = input_data[['Air temperature | (°C)', 'Pressure | (atm)', 'Wind speed | (m/s)']]
    
    # Predict power generation
    predictions = model.predict(X_forecasted)
    
    return predictions

def predict_custom_input(air_temp, press, wind_speed):
    # Define custom input data
    custom_input = {
        'Air temperature | (°C)': [air_temp],
        'Pressure | (atm)': [press],
        'Wind speed | (m/s)': [wind_speed]          
    }

    # Create a DataFrame with custom input data
    custom_input_df = pd.DataFrame(custom_input)

    # Get the predictions using custom input data
    custom_predictions = predict_power_generation(custom_input_df, rf_regressor)

    # Print the predictions
    print("Predicted power generation for custom inputs:")
    print(custom_predictions)
    return custom_predictions


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

# Features (X) are 'Air temperature | (°C)', 'Pressure | (atm)', and 'Wind speed | (m/s)'
# Target (y) is 'Power generated by system | (MW)'

# Extracting features (X) and target (y)
X = df[['Air temperature | (°C)', 'Pressure | (atm)', 'Wind speed | (m/s)']]
y = df['Power generated by system | (MW)']

# Splitting the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Initialize the Random Forest regressor
rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)

# Training the Random Forest regressor
rf_regressor.fit(X_train, y_train)

# Predicting on the test set
y_pred = rf_regressor.predict(X_test)

# Evaluating the model using metrics
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Mean Absolute Error:", mae)
print("Mean Squared Error:", mse)
print("R-squared:", r2)


# In[3]:


import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve

# Define a function to plot learning curves
def plot_learning_curve(estimator, X, y):
    train_sizes, train_scores, test_scores = learning_curve(estimator, X, y, cv=5, scoring='neg_mean_squared_error')
    train_scores_mean = -train_scores.mean(axis=1)
    test_scores_mean = -test_scores.mean(axis=1)

    plt.figure(figsize=(10, 6))
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r", label="Training error")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g", label="Cross-validation error")
    plt.xlabel("Training examples")
    plt.ylabel("Mean Squared Error")
    plt.title("Learning Curves")
    plt.legend()
    plt.grid(True)
    plt.show()

# Plot learning curves
plot_learning_curve(rf_regressor, X, y)


# In[4]:


# Load the forecasted data for 2024
forecasted_data_2024 = pd.read_excel("wind_test_data.xlsx")

# Extracting features for prediction
X_forecasted = forecasted_data_2024[['Air temperature | (°C)', 'Pressure | (atm)', 'Wind speed | (m/s)']]

# Predict power generation using the trained Random Forest regressor
predictions = rf_regressor.predict(X_forecasted)

# Print or save the predictions
print("Predicted power generation for 2024:")
print(predictions)



# In[5]:


predictions.sum()


# In[6]:


# Add the predictions to the forecasted data DataFrame
forecasted_data_2024['Predicted Power Generation | (MW)'] = predictions

# Save the DataFrame with predictions to a new Excel file
forecasted_data_2024.to_csv("forecasted_power_generation_2024.csv", index=False)

df_csv = pd.read_csv("forecasted_power_generation_2024.csv")
df_csv.to_excel("forecasted_power_generation_2024.xlsx")

# Optionally, you can also print the DataFrame to see the predictions alongside other data
print("Forecasted data with predictions for 2024:")
print(forecasted_data_2024)


# In[7]:


# Step 1: Load the data
data = pd.read_csv("final_data.csv")

# Step 2: Calculate the total power generated
total_power_generated = data['p1'].sum() + data['p2'].sum() + data['p3'].sum()

# Step 3: Distribute the power to each node based on the specified percentages
power_node1 = total_power_generated * 0.20  # 20% of total power
power_node2 = total_power_generated * 0.45  # 45% of total power
power_node3 = total_power_generated * 0.35  # 35% of total power

# Step 4: Prepare a DataFrame to store the distributed power for each node
node_data = {
    'Node': ['Node 1', 'Node 2', 'Node 3'],
    'Power Generated (MW)': [power_node1, power_node2, power_node3]
}

# Create a DataFrame
power_distribution_df = pd.DataFrame(node_data)

# Calculate the total power generated including P1, P2, and P3
total_power_generated_all = total_power_generated + data['p1'].sum() + data['p2'].sum() + data['p3'].sum()

# Check if generated and distributed powers are equal
equal_powers = total_power_generated == (power_node1 + power_node2 + power_node3)

# Display the DataFrame
print(power_distribution_df)

# Display the total power generated
print("Total Power Generated (including P1, P2, P3):", total_power_generated_all, "MW")

# Display if generated and distributed powers are equal
print("Generated and Distributed Powers are Equal:", equal_powers)


# In[8]:


total_power_generated_all


# In[9]:


# Step 1: Create new columns for each node
data['Power_Node_1'] = data['Power generated by system | (MW)'] * 0.20  # 20% of total power
data['Power_Node_2'] = data['Power generated by system | (MW)'] * 0.45  # 45% of total power
data['Power_Node_3'] = data['Power generated by system | (MW)'] * 0.35  # 35% of total power

# Step 2: Optionally, drop the original columns
data.drop(columns=['Power generated by system | (MW)'], inplace=True)

# Step 3: Display the updated DataFrame
print(data)


# In[10]:


data.head()


# In[11]:


data.to_csv("new_datset")


# In[12]:


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Split the dataset into features and target
X = data.drop(columns=['stability', 'date'])  
y = data['stability']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialize the logistic regression model
logistic_regression_model = LogisticRegression()

# Train the model
logistic_regression_model.fit(X_train_scaled, y_train)

# Predict on the test set
y_pred = logistic_regression_model.predict(X_test_scaled)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Test Accuracy:", accuracy)

# Print classification report
print(classification_report(y_test, y_pred))


# In[13]:

# Load the forecasted data for 2024
forecasted_data_2024 = pd.read_excel("wind_test_data.xlsx")

# Get the predictions
predictions = predict_power_generation(forecasted_data_2024, rf_regressor)

# Print the predictions
print("Predicted power generation for 2024:")
print(predictions)


# In[14]:


from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Generate confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)

# Plot confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, cmap='Blues', fmt='g', cbar=False,
            xticklabels=['Stable', 'Unstable'], yticklabels=['Stable', 'Unstable'])
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.show()


# In[15]:


import pandas as pd


# Step 1: Convert the 'date' column to datetime format
data['date'] = pd.to_datetime(data['date'], format="%d-%m-%Y %H:%M")

# Step 2: Calculate the percentage of 'Stable' and 'Unstable' grid conditions
stability_percentage = data['stability'].value_counts(normalize=True) * 100
print("Percentage of Stable Grid Conditions:", stability_percentage['stable'], "%")
print("Percentage of Unstable Grid Conditions:", stability_percentage['unstable'], "%")

# Step 3: Identify patterns in the hours when the grid is most prone to instability
# Extract hour from the date column
data['Hour'] = data['date'].dt.hour
unstable_hours = data[data['stability'] == 'unstable']['Hour'].value_counts()
most_unstable_hour = unstable_hours.idxmax()
print("Hour when the grid is most prone to instability:", most_unstable_hour)

# Step 4: Analyze the frequency and duration of 'Unstable' conditions throughout the day
unstable_hours_distribution = data[data['stability'] == 'unstable']['Hour'].value_counts(normalize=True) * 100
print("Distribution of Unstable Conditions throughout the day:")
print(unstable_hours_distribution)


# In[16]:


unstable_hour_distribution = unstable_hours.sort_index()
plt.figure(figsize=(10, 6))
plt.bar(unstable_hour_distribution.index, unstable_hour_distribution.values)
plt.xlabel('Hour of Day')
plt.ylabel('Proportion of Unstable Conditions')
plt.title('Distribution of Unstable Conditions Throughout the Day')
plt.xticks(range(24))
plt.grid(True)
plt.show()


# In[17]:


# Step 5: Visualize the trend of stable and unstable conditions over time
data['Date'] = data['date'].dt.date
stability_trend = data.groupby(['Date', 'stability']).size().unstack(fill_value=0)
stability_trend.plot(kind='line', figsize=(12, 6))
plt.title('Stability Trend Over Time')
plt.xlabel('Date')
plt.ylabel('Frequency')
plt.legend(title='Stability', loc='upper left')
plt.grid(True)
plt.show()


# In[ ]:





# In[ ]:





# In[18]:


import pandas as pd
import matplotlib.pyplot as plt

data = {
    'date': ['01-01-2019 01:00', '01-01-2019 02:00', '01-01-2019 03:00', '01-01-2019 04:00', '01-01-2019 05:00',
             '01-04-2019 01:00', '01-04-2019 02:00', '01-04-2019 03:00', '01-04-2019 04:00', '01-04-2019 05:00',
             '01-07-2019 01:00', '01-07-2019 02:00', '01-07-2019 03:00', '01-07-2019 04:00', '01-07-2019 05:00',
             '01-10-2019 01:00', '01-10-2019 02:00', '01-10-2019 03:00', '01-10-2019 04:00', '01-10-2019 05:00'],
    'Power generated by system | (MW)': [33.6881, 37.2619, 30.5029, 28.4192, 27.3703,
                                          30.6881, 27.2619, 32.5029, 35.4192, 31.3703,
                                          34.6881, 36.2619, 33.5029, 30.4192, 29.3703,
                                          32.6881, 35.2619, 31.5029, 29.4192, 28.3703]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Convert 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y %H:%M')

# Extract quarter from the 'date' column
df['Quarter'] = df['date'].dt.to_period('Q')

# Group by quarter and calculate total power generated for each quarter
power_by_quarter = df.groupby('Quarter')['Power generated by system | (MW)'].sum().reset_index()

# Plotting the total power generated for each quarter
plt.figure(figsize=(10, 6))
plt.bar(power_by_quarter['Quarter'].astype(str), power_by_quarter['Power generated by system | (MW)'])
plt.title('Total Power Generated for Each Quarter')
plt.xlabel('Quarter')
plt.ylabel('Total Power Generated (MW)')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.grid(axis='y')
plt.tight_layout()
plt.show()


# In[19]:


import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("final_data.csv")  

# Convert 'date' column to datetime format
data['date'] = pd.to_datetime(data['date'], format='%d-%m-%Y %H:%M')

# Extract year and quarter from the 'date' column
data['Year'] = data['date'].dt.year
data['Quarter'] = data['date'].dt.to_period('Q')

# Group by year and quarter and calculate total power generated for each quarter
power_by_year_quarter = data.groupby(['Year', 'Quarter'])['Power generated by system | (MW)'].sum().reset_index()

# Plotting the total power generated for each quarter over the years
plt.figure(figsize=(12, 8))
for year in range(2019, 2024):
    year_data = power_by_year_quarter[power_by_year_quarter['Year'] == year]
    plt.plot(year_data['Quarter'].astype(str), year_data['Power generated by system | (MW)'],
             label=str(year))

plt.title('Total Power Generated for Each Quarter (2019-2023)')
plt.xlabel('Quarter')
plt.ylabel('Total Power Generated (MW)')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.grid(True)
plt.legend(title='Year')
plt.tight_layout()
plt.show()


# In[20]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
data = pd.read_csv("final_data.csv")

# Select variables for correlation analysis
variables = ['Air temperature | (°C)', 'Pressure | (atm)', 'Wind speed | (m/s)', 'Power generated by system | (MW)']

# Create a pairplot to visualize relationships and distributions
sns.pairplot(data[variables])
plt.show()

# Calculate correlation matrix
correlation_matrix = data[variables].corr()

# Plot the correlation matrix as a heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", annot_kws={"size": 10})
plt.title('Correlation Matrix')
plt.show()

# Print correlation coefficients
print("Correlation coefficients:")
print(correlation_matrix)


# In[ ]:




