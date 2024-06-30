# HERHACKATHON2024
DermaFilos-your Skins Best friend

# Skincare Analysis and Product Recommendation

This project is a web application that analyzes realtime scanned or uploaded images for various skin conditions and provides product recommendations based on the analysis. The project utilizes machine learning models from the Hugging Face Transformers library for image classification.

## Features

- Upload an image for skin analysis.
- Detects skin conditions such as acne, dry skin, oily skin, hidradenitis suppurativa, etc.
- Provides probabilities for each detected condition.
- Annotates the uploaded image with detected skin conditions.
- Displays recommended skincare products based on the analysis.
- Secure login system to view detailed recommendations.
- Integrated Skincare specialist bot

<p align="center">
<img width="206" alt="login" src="https://github.com/latika123/herhackathon2024/assets/5699249/67229300-e242-4066-9822-239e48c80059">
&nbsp;&nbsp;&nbsp;&nbsp;
<img width="210" alt="skinan" src="https://github.com/latika123/herhackathon2024/assets/5699249/014d538d-e7a3-4b9f-9234-bef18f494596">
&nbsp;&nbsp;&nbsp;&nbsp;
<img width="209" alt="skinchatbotintegeration" src="https://github.com/latika123/herhackathon2024/assets/5699249/c19738a7-8122-4c37-911d-f6e1889bab70">
</p>

## Tools and Libraries Used

- Flask: Web framework for Python.
- Transformers: For the image classification model.
- PIL (Pillow): Python Imaging Library for image processing.
- Jinja2: Templating engine for rendering HTML.
- OpenCV: Computer Vision library (optional, depending on additional image processing needs).
- Hugging face pretrained skin care detection model https://huggingface.co/tuphamdf/skincare-detection
  This model is a fine-tuned version of google/vit-base-patch16-224-in21k

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   
2. **Create a virtual environment:**
   ```bash  
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt

4. **Set up environment variables:**
   ```bash
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key
   UPLOAD_FOLDER=uploads

6. **Run the Flask application:**
   ```bash
   flask run

Usage
Upload an Image:

Visit the home page of the application.
Use the upload form to select and upload an image for analysis.

View Analysis Results:

After uploading, you will be redirected to a page showing the analysis results.
The results include probabilities for various skin conditions and an annotated image highlighting detected conditions.

Product Recommendations:

Logged-in users will see recommended skincare products based on the analysis.

**Contributing**
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch

3. Make your changes and commit them
   ```bash
   git commit -m "Description of the feature"

4. Push to the branch:
   ```bash
   git push origin feature-branch

5. Open a pull request on GitHub.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgements
Hugging Face for providing the Transformers library.
Flask for the web framework.
Pillow for image processing.
Contact
For any inquiries or support, please contact latikasoni13@gmail.com.









