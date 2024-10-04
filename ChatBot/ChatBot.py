

from pyuac import main_requires_admin
import random
from transformers import pipeline, GPT2LMHeadModel, GPT2Tokenizer

import random
from transformers import pipeline, GPT2LMHeadModel, GPT2Tokenizer

# Load pre-trained GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Initialize chatbot pipeline using GPT-2
generator = pipeline('text-generation', model=model, tokenizer=tokenizer)


# Simulate sensor data (replace with actual sensor API if available)
def get_temperature():
    return random.uniform(18.0, 35.0)  # Simulate temperature (Celsius)


def get_humidity():
    return random.uniform(30.0, 80.0)  # Simulate humidity (percentage)


def get_gas_level():
    return random.choice(["normal", "elevated", "high"])  # Simulate gas level


# Get all sensor data as a dictionary
def get_sensor_data():
    return {
        "temperature": get_temperature(),
        "humidity": get_humidity(),
        "gas_level": get_gas_level()
    }


# Generate chatbot response based on user input and sensor data

def chatbot_response(user_input, sensor_data):
    # Basic prompt structure focusing on house-specific insights
    prompt = f"User: {user_input}\nThis house currently has the following conditions:\nTemperature: {sensor_data['temperature']:.2f}°C, Humidity: {sensor_data['humidity']:.2f}%, Gas Level: {sensor_data['gas_level']}."

    # Generate response using the GPT-2 model
    generated_text = generator(
        prompt,
        max_length=50,  # Limit the length of the generated text
        num_return_sequences=1,
        temperature=0.7,  # Control randomness
        top_p=0.9,  # Use nucleus (top-p) sampling
        top_k=50  # Consider only the top 50 words for each generation step
    )[0]['generated_text']

    # Extract bot's reply
    bot_reply = generated_text.split("House Bot:")[-1].strip()

    # Add custom insights specific to house conditions
    if sensor_data["temperature"] > 30:
        bot_reply += " The house feels quite warm. You might want to turn on the AC or fans to cool it down."
    elif sensor_data["temperature"] < 20:
        bot_reply += " The house feels cold. Consider increasing the heating or using a heater."

    if sensor_data["humidity"] > 60:
        bot_reply += " The humidity level in the house is high, which might feel uncomfortable. A dehumidifier could help."
    elif sensor_data["humidity"] < 40:
        bot_reply += " The air in the house is dry. Using a humidifier would improve comfort."

    if sensor_data["gas_level"] == "elevated":
        bot_reply += " Caution: The gas levels are slightly elevated in the house. Ensure windows are open for proper ventilation."
    elif sensor_data["gas_level"] == "high":
        bot_reply += " WARNING: High gas levels detected! Take immediate action, ventilate the house, and ensure gas appliances are checked."

    return bot_reply


# Main chat loop for interacting with the chatbot
def chat_with_bot():
    print(
        "House Insight Bot: Hi! I am here to provide insights about the conditions in your house. How can I assist you today?")

    while True:
        user_input = input("User: ")
        if user_input.lower() in ['exit', 'quit']:
            print("House Insight Bot: Goodbye! Stay safe.")
            break

        # Fetch sensor data
        sensor_data = get_sensor_data()

        # Generate response based on user input and sensor readings
        response = chatbot_response(user_input, sensor_data)

        print(f"House Insight Bot: {response}\n")


# Run the chatbot
if __name__ == "__main__":
    chat_with_bot()


