from flask import Flask, jsonify, request
from llama_requests import LlamaResponseParser
import json
from flask_cors import CORS

llama_response = LlamaResponseParser()
app = Flask(__name__)
CORS(app)

@app.route('/api/getEvaluation', methods=['POST'])
def get_evaluation():
    data = request.get_json()
    response = llama_response.post_to_llama(data['q'], data['a'])
    evaluation = llama_response.parse_evaluation_response(response)
    return jsonify(evaluation), 200

@app.route('/api/getAverageScore', methods=['POST'])
def get_average_score():
    data = request.get_json()
    scenario_id = int(data['id'])
    return jsonify({'average_score': llama_response.get_average_score(scenario_id)}), 200

@app.route('/api/getQuestions', methods=['GET'])
def get_questions():
    with open('interview_questions.json', 'r') as file:
        data = json.load(file)
    reformatted_data = {
        1: [],
        2: []
    }
    for category in data['categories']:
        reformatted_data[1].append({
            'category': category['category'],
            'question': category['questions']['Entry-level Software Engineer']
        })
        reformatted_data[2].append({
            'category': category['category'],
            'question': category['questions']['Team Lead']
        })
    return jsonify(reformatted_data), 200

@app.route('/api/getScenarios', methods=['GET'])
def get_scenarios():
    with open('scenarios.json', 'r') as file:
        data = json.load(file)
    return jsonify(data), 200


# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=2342)
