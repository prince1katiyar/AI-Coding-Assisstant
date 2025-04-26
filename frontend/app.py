import streamlit as st
import requests

st.title("🤖 AI-Based Coding Assistant for Students")

language = st.selectbox("Select Language", ["Python", "Java", "C++"])
topic = st.text_input("Enter Topic")
level = st.selectbox("Select Level", ["Beginner", "Intermediate", "Advanced"])

API_URL = "http://127.0.0.1:8000"

# Function to send requests safely
def fetch_response(endpoint, payload):
    try:
        response = requests.post(f"{API_URL}/{endpoint}", json=payload)
        
        # Print API response (for debugging)
        st.write(f"DEBUG: API Response - {response.status_code}")
        st.write(response.text)  # Show raw response

        # Check if response is valid JSON
        response_data = response.json()

        if "response" in response_data:
            return response_data["response"]
        else:
            st.error("⚠️ Unexpected API Response Format!")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"🚨 API Request Failed: {e}")
        return None
    except requests.exceptions.JSONDecodeError:
        st.error("⚠️ Error: Backend did not return JSON. Check if FastAPI is running.")
        return None

# Button to explain code
if st.button("Explain Code"):
    explanation = fetch_response("explain", {"language": language, "topic": topic, "level": level})
    if explanation:
        st.write("### 📖 Explanation:")
        st.write(explanation)

# Button to debug code
if st.button("Debug Code"):
    response = requests.post(
        "http://127.0.0.1:8000/debug",
        json={"language": language, "topic": topic, "level": level},  # Added "level"
    )
    
    st.write(f"ℹ️ **Debug API Raw Response:** `{response.text}`")  # Print raw response

    if response.status_code == 200:
        result = response.json()
        st.write("### 🛠 Debugging:")
        st.write(result.get("response", "⚠️ No valid response received."))
    else:
        st.error(f"⚠️ Error {response.status_code}: {response.text}")



# Button to generate code
if st.button("Generate Code"):
    generated_code = fetch_response("generate", {"language": language, "topic": topic, "level": level})
    if generated_code:
        st.write("### 💡 Code Example:")
        st.code(generated_code, language=language.lower())
