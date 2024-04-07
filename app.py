import streamlit as st
import pandas as pd
from joblib import dump, load

# Load the trained model
model = load('gradient_boosting_model.joblib')



# Define Streamlit app
def main():
    st.title("Power Generation Prediction")

    # Sidebar section for user input
    st.sidebar.header("User Input")

    # Dropdown for selecting stability
    stability_options = ["All", "Stable", "Unstable"]
    selected_stability = st.sidebar.selectbox("Select Stability:", stability_options)

    # Load the dataset
    data = load_data()

    # Filter data based on selected stability
    if selected_stability == "All":
        filtered_data = data
    elif selected_stability == "Stable":
        filtered_data = data[data['stability'] == 'stable']
    else:
        filtered_data = data[data['stability'] == 'unstable']

    # Display filtered data
    st.subheader("Filtered Data")
    st.write(filtered_data)

    # Main content section for power generation prediction
    st.subheader("Power Generation Prediction")

    # User input for pressure, wind, and air temperature
    pressure = st.number_input("Enter Pressure (atm):", step=0.01)
    wind_speed = st.number_input("Enter Wind Speed (m/s):", step=0.01)
    air_temperature = st.number_input("Enter Air Temperature (°C):", step=0.01)

    # User input for date (optional)
    selected_date = st.date_input("Select Date (optional):")
    selected_date = selected_date.strftime("%d-%m-%Y")
    selected_time = st.time_input("Select Time (optional):")

    # Perform prediction based on user input (if all inputs are provided)
    if st.button("Predict Power Generation"):
        power_prediction = predict_power_generation(air_temperature, pressure, wind_speed, filtered_data, selected_date, selected_time)
        st.write(f"Predicted Power Generation: {power_prediction:.6f} MW")  # Format prediction to 6 decimal places

    # # Perform prediction for stability based on user input
    if st.button("Predict Stability"):
        stability_prediction = predict_stability(pressure, wind_speed, air_temperature, filtered_data, selected_date, selected_time)
        st.write(f"Predicted Stability: {stability_prediction}")

    if st.button("Predict Power Generation from Parameter"):
        power_prediction_param = predict_power_generation_param(air_temperature, pressure, wind_speed, filtered_data )
        st.write(f"Predicted Power Generation: {power_prediction_param[0]}")  # Format prediction to 6 decimal places

    # Add section for Power BI dashboard
    st.subheader("Power BI Dashboard")
    power_bi_dashboard = """
    <iframe width="800" height="506" src="https://app.powerbi.com/view?r=eyJrIjoiNjE3N2IzNTUtNzlhZi00NGVmLWI3MzUtODY1YjJiZmJhYzZiIiwidCI6IjNkNmVhYjlkLTc5MmMtNGFmOS05NDYwLTc5MzljYTkwYjZhYiJ9&pageName=ReportSection" frameborder="0" allowFullScreen="true"></iframe>
    """
    st.markdown(power_bi_dashboard, unsafe_allow_html=True)

# Function to load the dataset
def load_data():
    # Implement this function to load your dataset
    return pd.read_csv("C:\\Users\\admin\\Downloads\\Hackwave-vs\\9_Sustainability_and_Environment\\gbr_updated_dataset.csv")  # Update with your dataset path

# Function to perform power generation prediction
def predict_power_generation(air_temperature, pressure, wind_speed, filtered_data, selected_date, selected_time):
    hour = selected_time.hour
    minute = selected_time.minute
    
    date_time = str(selected_date) + " " + str(hour) + ":" + str(minute)
    # Convert selected_date to datetime object
    selected_datetime = pd.to_datetime(date_time)
    print(selected_datetime)
    # Filter the data based on the selected date and time
    filtered_data['date'] = pd.to_datetime(filtered_data['date'], format='%d-%m-%Y %H:%M')
    filtered_data = filtered_data.set_index('date')
    filtered_data = filtered_data.loc[selected_datetime]

    # Extract the relevant power generation value
    power_generation = filtered_data['Power generated by system | (MW)']
    
    return power_generation

# Function to predict stability based on user input
def predict_stability(pressure, wind_speed, air_temperature, filtered_data, selected_date, selected_time):
    # Extract hour and minute from selected_time
    hour = selected_time.hour
    minute = selected_time.minute

    # Combine selected_date and time components into a single datetime object
    date_time = pd.to_datetime(selected_date) + pd.DateOffset(hours=hour, minutes=minute)

    # Filter the data based on the selected date and time
    filtered_data['date'] = pd.to_datetime(filtered_data['date'], format='%d-%m-%Y %H:%M')
    filtered_data = filtered_data.set_index('date')
    filtered_data = filtered_data.loc[date_time]

    # Extract the stability value
    stability = filtered_data['stability']
    
    return stability

def predict_power_generation_param(air_temperature, pressure, wind_speed, filtered_data):
    # Prepare the input data for prediction
    new_data = [[air_temperature, pressure, wind_speed]]  # Replace feature1, feature2, ... with actual values

    # Make predictions
    predictions = model.predict(new_data)

    # Display predictions
    print("Predicted power generation:", predictions)
    
    return predictions

# Load the dataset
data = pd.read_csv("C:\\Users\\admin\\Downloads\\Hackwave-vs\\9_Sustainability_and_Environment\\final_data.csv")  # Update with your dataset path

# Run the Streamlit app
if __name__ == "__main__":
    main()
