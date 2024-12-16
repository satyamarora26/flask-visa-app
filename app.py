from flask import Flask, request, jsonify
from pymongo import MongoClient
from llm_helper import refine_answer_with_llm

# Flask app setup
app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["visa_db"]
collection = db["visitor_600_data"]

def interpret_query(user_input):
    query_lower = user_input.lower()
    if "stream" in query_lower:
        return {"type": "streams"}
    elif "duration" in query_lower or "how long" in query_lower:
        return {"type": "duration"}
    elif "work" in query_lower:
        return {"type": "work"}
    else:
        return {"type": "general"}

def query_database(intent):
    doc = collection.find_one({"visa_name": "Visitor visa (subclass 600)"})
    if not doc:
        return "No data found."

    if intent["type"] == "streams":
        streams = [stream["name"] for stream in doc["streams"]]
        return "The following streams are available under the Visitor Visa (Subclass 600): " + ", ".join(streams)
    elif intent["type"] == "duration":
        tourist_stream = next((s for s in doc["streams"] if "Tourist" in s["name"]), None)
        if tourist_stream:
            return "Under the Tourist Stream, you can generally stay up to 12 months. Check the official grant letter for specific conditions."
        else:
            return "Duration details not found."
    elif intent["type"] == "work":
        return "No, you cannot work on a Visitor Visa (Subclass 600)."
    else:
        return "You can apply for a Visitor Visa (Subclass 600) for tourism, family visits, or business visitor activities. Check the official website for more details."

@app.route("/ask", methods=["GET"])
def ask():
    user_query = request.args.get("q", "")
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    # Interpret user query
    intent = interpret_query(user_query)

    # Query the database
    raw_answer = query_database(intent)

    # Refine the answer with LLM
    refined_answer = refine_answer_with_llm(user_query, raw_answer)

    # Return both raw and refined answers
    return jsonify({
        "question": user_query,
        "raw_answer": raw_answer,
        "refined_answer": refined_answer
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)