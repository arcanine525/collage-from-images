from flask import Flask, render_template, request, jsonify, send_from_directory
from image_collage_maker import CollageGenerator
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['COLLAGE_FOLDER'] = 'collages'

@app.route('/')
def index():
    """Renders the main page of the web application.

    Returns:
        flask.Response: The rendered HTML of the index page.
    """
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    """Handles file uploads from the user.

    Saves uploaded files to the UPLOAD_FOLDER and returns their paths.

    Returns:
        flask.Response: A JSON response containing the filepaths of the uploaded files,
                        or an error message if no files were uploaded.
    """
    if 'files' not in request.files:
        return jsonify({'error': 'No files part'}), 400
    files = request.files.getlist('files')
    if not files:
        return jsonify({'error': 'No selected files'}), 400

    filepaths = []
    for file in files:
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            filepaths.append(filepath)

    return jsonify({'filepaths': filepaths})

@app.route('/generate_collage', methods=['POST'])
def generate_collage():
    """Generates a collage from the uploaded files.

    Takes a list of filepaths, creates a collage using CollageGenerator,
    and returns the URL of the generated collage.

    Returns:
        flask.Response: A JSON response containing the URL of the generated collage.
    """
    data = request.get_json()
    filepaths = data.get('filepaths', [])

    generator = CollageGenerator(images_dir=None, output_dir=app.config['COLLAGE_FOLDER'])
    collage_path = generator.create_single_collage(filepaths, (1200, 1200))

    return jsonify({'collage_url': os.path.basename(collage_path)})

@app.route('/collages/<filename>')
def serve_collage(filename):
    """Serves a generated collage file.

    Args:
        filename (str): The name of the collage file to serve.

    Returns:
        flask.Response: The requested collage file.
    """
    return send_from_directory(app.config['COLLAGE_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['COLLAGE_FOLDER']):
        os.makedirs(app.config['COLLAGE_FOLDER'])
    app.run(debug=True)
