import streamlit as st
from pint import UnitRegistry
import requests
import json
# Initialize Unit Registry
ureg = UnitRegistry()

# Function to fetch real-time exchange rates
def get_currency_conversion(from_currency, to_currency, amount):
    try:
        api_url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(api_url)
        data = response.json()
        rate = data["rates"].get(to_currency, None)
        if rate:
            return amount * rate
        else:
            return "Currency not supported"
    except Exception as e:
        return f"Error: {e}"

# Function to store conversion history
def save_conversion(history, category, value, from_unit, to_unit, result):
    history.append(f"{category}:\n{value} {from_unit} = {result} {to_unit}")
    if len(history) > 10:
        history.pop(0)  # Keep only the last 10 conversions
    st.session_state["history"] = history

# Function to display unit definitions
def show_unit_definitions():
    st.sidebar.subheader("Unit Definitions")
    st.sidebar.text("Meter: SI unit of length")
    st.sidebar.text("Kilogram: SI unit of mass")
    st.sidebar.text("Joule: SI unit of energy")
    st.sidebar.text("Kelvin: SI unit of temperature")
    st.sidebar.text("Second: SI unit of time")
    st.sidebar.text("Pascal: SI unit of pressure")
    st.sidebar.text("Celsius: SI unit of temperature")
def convert_units(category, value, from_unit, to_unit):
    try:
        result = (value * ureg(from_unit)).to(to_unit)
        return result.magnitude
    except Exception as e:
        return f"Error: {e}"

def main():
    st.set_page_config(page_title="📃Umar's Unit Converter", layout="wide")
    history = st.session_state.get("history", [])
    st.title("📃Umar's Unit Converter")
    
    categories = {
        "Currency" : ["PKR","USD", "EUR", "GBP", "JPY", "BTC", "ETH", "XRP", "LTC", "DOGE", "SOL", "BTC",],

        "Length": ["meter", "kilometer", "mile", "yard", "centimeter" , "millimeter",
                    "nautical_mile", "nanometer", "micrometer" ,"foot", "inch"],

        "Area": ["square meter", "square kilometer", "square mile", "square_yard", "square_foot","square_inch",
                 "hectare","acre"],

        "Data Transfer Rate": ["bit/second", "kilobit/second", "megabit/second", "kibibit/second","kilobyte/second",
                               "megabyte/second","gigabit/second", "gigabyte/second","terabit/second", "terabyte/second",
                               "tibit/second","tibibyte/second", "mebibit/second", "mebibyte/second"],
        
        "Digital Storage": ["bit", "kilobit","kibibit", "megabit","mibibit", "gigabit","gibibit", "terabit","tibibit",
                            "petabit","pebibit", "byte", "kilobyte", "kibibyte", "megabyte", "mibibyte", "gigabyte",
                            "gibibyte", "terabyte", "tibibyte", "petabyte", "pebibyte"],
        
        "Energy": ["joule","kilojoule","gram_calorie","kilocalorie","watt_hour", "kilowatt_hour","electronvolt",
                    "british_thermal_unit","Us_therm","foot_pound"],

        "Frequency": ["hertz", "kilohertz", "megahertz", "gigahertz"],

        "Fuel Economy": ["kilometer/liter","mile/us_gallon", "mile/gallon","liter/100kilometer"],

        "Mass": ["gram", "kilogram", "pound", "ounce", "tonne", "us_ton", "stone", "milligram", "microgram", "imperial_ton", "tonne_metric"],

        "Plane Angle": ["degree", "radian", "gradian","Minute of arc","Arc_second", "milliradian"],

        "Pressure": ["pascal", "bar", "pound/square_inch", "standard_atmosphere", "torr"],

        "Speed": ["meter/second", "kilometer/hour", "mile/hour", "foot/second", "mile/second", "knot"],

        "Temperature": ["celsius", "fahrenheit", "kelvin"],

        "Time": ["second", "millisecond","microsecond", "nanosecond", "minute", "hour", "day", "week",
                 "month", "year", "decade", "century"],

        "Volume": ["liter", "milliliter", "gallon","us_liquid_gallon", "us_liquid_pint", "us_liquid_quart",
                    "us_legal_cup" ,"us_fluid_ounce", "us_tablespoon", "us_teaspoon", "cubic meter",
                     "imperial_gallon", "imperial_pint", "imperial_quart", "imperial_cup", "imperial_fluid_ounce",
                     "imperial_tablespoon", "imperial_teaspoon", "cubic foot", "cubic inch", "cubic yard"],

    }
    
    selected_category = st.selectbox("Select Category", list(categories.keys()))
    from_unit = st.selectbox("From Unit", categories[selected_category])
    to_unit = st.selectbox("To Unit", categories[selected_category])
    value = st.number_input("Enter Value", min_value=0.0, step=1.00)
    
    if st.button("Convert"):
        if selected_category == "Currency":
            result = get_currency_conversion(from_unit, to_unit, value)
        else:
            result = convert_units(selected_category, value, from_unit, to_unit)
        
        st.success(f"Converted Value: {result} {to_unit}")
        
        # Save conversion to history
        if "history" not in st.session_state:
            st.session_state["history"] = []
        save_conversion(st.session_state["history"], selected_category, value, from_unit, to_unit, result)
    
    # Display conversion history
    st.sidebar.subheader("Conversion History")
    if "history" in st.session_state:
        for entry in st.session_state["history"]:
            st.sidebar.text(entry)
    
    # Show unit definitions
    show_unit_definitions()

if __name__ == "__main__":
    main()
