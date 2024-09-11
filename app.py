from flask import Flask, jsonify, request, abort
import os
import json

app = Flask(__name__)

# Define the route for fetching Instagram posts based on username
@app.route('/api/posts/<username>', methods=['GET'])
def get_posts(username):
    # Define the directory where JSON files are stored
    json_dir = f"json/{username}"
    json_filename = os.path.join(json_dir, f"{username}_posts.json")

    # Check if the JSON file exists for the given username
    if not os.path.exists(json_filename):
        return abort(404, description="Profile data not found.")
    
    # Load the JSON data from the file
    try:
        with open(json_filename, 'r', encoding='utf-8') as json_file:
            post_data = json.load(json_file)
    except Exception as e:
        return abort(500, description=f"Error loading data: {e}")
    
    # Return the post data as a JSON response
    return jsonify(post_data)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
