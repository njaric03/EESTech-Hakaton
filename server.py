from flask import Flask, jsonify, request
from llama_requests import LlamaResponseParser

llama_response = LlamaResponseParser()
app = Flask(__name__)

@app.route('/api/getEvaluation', methods=['POST'])
def get_evaluation():
    data = request.get_json()
    response = llama_response.post_to_llama(data['q'], data['a'])
    evaluation = llama_response.parse_evaluation_response(response)
    return jsonify(evaluation), 200


# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=2342)
