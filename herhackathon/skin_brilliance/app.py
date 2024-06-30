import time
from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import os
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw, ImageFont
from transformers import AutoImageProcessor, AutoModelForImageClassification
import torch
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

processor = AutoImageProcessor.from_pretrained("tuphamdf/skincare-detection")
model = AutoModelForImageClassification.from_pretrained("tuphamdf/skincare-detection")

skincare_products = [
    {"name": "Product 1", "description": "Description of Product 1", "image": "product1.jpg"},
    {"name": "Product 2", "description": "Description of Product 2", "image": "product2.jpg"},
    {"name": "Product 3", "description": "Description of Product 3", "image": "product3.jpg"},
]

users = {
    "user1": generate_password_hash("password1"),
    "user2": generate_password_hash("password2")
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def splash_screen():
    # Simulate a splash screen delay (adjust as needed)
    delay_seconds = 2
    return render_template('splash.html', delay_seconds=delay_seconds)

@app.route('/loginnew')
def login_screen():
    return render_template('loginnew.html')    

@app.route('/termscondition', methods=['GET', 'POST'])
def termscondition():
    return render_template('termscondition.html')


@app.route('/index')
def index():
    if 'username' in session:
        username = session['username']
        products = [
        {"name": "Product 1", "description": "Description of Product 1"},
        {"name": "Product 2", "description": "Description of Product 2"},
        {"name": "Product 3", "description": "Description of Product 3"}]
        return render_template('index.html', username=username, products=products)
    return render_template('index.html', guest=True)

@app.route('/guest_access')
def guest_access():
    return render_template('index.html', guest=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error = 'Invalid username or password'
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users.push(username,generate_password_hash(password))
        return render_template('index.html', username=username)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return redirect(url_for('analyze_image', filename=filename))
    return redirect(url_for('index'))

@app.route('/analyze/<filename>')
def analyze_image(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image = Image.open(file_path).convert("RGB")
    
    # Process the image
    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1).detach().numpy().flatten()
    
    labels = ['normal', 'dry', 'oily', 'acne', 'hidradenitis_suppurativa']
    
    # Create results with probabilities
    results = [{"label": label, "probability": float(probabilities[i])} for i, label in enumerate(labels)]
    results.sort(key=lambda x: x["probability"], reverse=True)
    
    # Annotate the image for visualization
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    annotations = []

    # Example detection logic for 'acne' (Adjust according to your detection mechanism)
    if probabilities[labels.index('acne')] > 0.001:
        annotations.append((50, 50, 150, 150, "Acne"))  # Example coordinates and label

    if probabilities[labels.index('dry')] > 0.110:
        annotations.append((200, 50, 300, 150, "Dry"))  # Example coordinates and label

    if probabilities[labels.index('hidradenitis_suppurativa')] > 0.830:
        annotations.append((50, 200, 150, 300, "Hidradenitis Suppurativa"))  # Example coordinates and label    

    if probabilities[labels.index('oily')] > 0.001:
        annotations.append((200, 200, 300, 300, "Oily"))  # Example coordinates and label   

    if probabilities[labels.index('normal')] > 0.002:
        annotations.append((50, 350, 150, 450, "Normal"))  # Example coordinates and label  

    # Annotate the image with bounding boxes and labels
    for annotation in annotations:
        x1, y1, x2, y2, text = annotation
        draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
        draw.text((x1, y1 - 10), text, fill="red", font=font)
    
    # Save the annotated image
    annotated_image_path = f"annotated_{filename}"
    annotated_image_full_path = os.path.join(app.config['UPLOAD_FOLDER'], annotated_image_path)
    image.save(annotated_image_full_path)
    
    return render_template('result.html', results=results, filename=filename, annotated_image_path=annotated_image_path, products=skincare_products)

@app.route('/routine')
def skin_routine():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('routine.html')

@app.route('/buy')
def buy_product():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('buy.html')

@app.route('/capture', methods=['POST'])
def capture_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({'redirect': url_for('analyze_image', filename=filename)})
    return jsonify({'error': 'Invalid file'}), 400

if __name__ == '__main__':
    app.run(debug=True)
