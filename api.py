from flask import Flask, request
import os
import torch
import asyncio
import cryptography


app = Flask(__name__)

# Define the folder to store uploaded files
UPLOAD_FOLDER = 'models'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def check_extensoin(filename, extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in extensions
    

@app.route('/upload_model', methods=['POST'])
def upload_model():
    print("files", request.files)
    if 'model_onnx' not in request.files:
        return 'No file part'
    
    model_onnx = request.files['model_onnx']
    if model_onnx.filename == '':
        return 'No ONNX model selected'
    
    if 'id' not in request.form:
        return 'No ID part'
    id = request.form['id']
    if not id.isdigit():
        return 'ID must be a number'
    
    id_folder = os.path.join(app.config['UPLOAD_FOLDER'], id)
    if os.path.exists(id_folder):
        return f'ID {id} already exists'
    else:
        os.makedirs(id_folder)

    if model_onnx and check_extensoin(model_onnx.filename, {'onnx'}):
        model_onnx.save(os.path.join(id_folder, "model.onnx"))
        return f'File successfully uploaded with ID: {id}'
    return 'Invalid file extensions'


@app.route('/list_models', methods=['GET'])
def list_models():
    models = os.listdir(app.config['UPLOAD_FOLDER'])
    return models


@app.route('/compile_prover', methods=['POST'])
def compile_prover():
    if 'id' not in request.form:
        return 'No ID part'
    id = request.form['id']

    x = torch.tensor([[[1., 1., 0., 1., 0., 1., 0., 1., 1.]]])
    res = asyncio.run(cryptography.compile_prover(id, x.shape))
    return res


@app.route('/prove_inference', methods=['POST'])
def prove_inference():
    if 'id' not in request.form:
        return 'No ID part'
    id = request.form['id']

    x = torch.tensor([[[1., 1., 0., 1., 0., 1., 0., 1., 1.]]])
    res = asyncio.run(cryptography.prove_inference(id, x))
    return res


if __name__ == '__main__':
    app.run(debug=True)
