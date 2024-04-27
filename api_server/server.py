from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
data = [
    {'id': 1, 'name': 'John'},
    {'id': 2, 'name': 'Alice'}
]

# Endpoint to get all data
@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(data)

# Endpoint to get data by ID
@app.route('/api/data/<int:id>', methods=['GET'])
def get_data_by_id(id):
    result = next((item for item in data if item['id'] == id), None)
    if result:
        return jsonify(result)
    else:
        return jsonify({'message': 'Data not found'}), 404

# Endpoint to add new data
@app.route('/api/data', methods=['POST'])
def add_data():
    new_data = request.get_json()
    data.append(new_data)
    return jsonify({'message': 'Data added successfully'}), 201

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
