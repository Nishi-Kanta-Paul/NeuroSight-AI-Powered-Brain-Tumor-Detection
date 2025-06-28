from flask import Flask, render_template, request, send_from_directory, send_file
from tensorflow.keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os
import logging
from datetime import datetime
import uuid
from werkzeug.utils import secure_filename
from fpdf import FPDF

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='tumor_detection.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load the trained model
try:
    model = load_model(os.path.join('models', 'model.h5'))
    logging.info("Model loaded successfully")
except Exception as e:
    logging.error(f"Failed to load model: {str(e)}")
    raise

# Class labels and tumor descriptions
class_labels = ['glioma', 'meningioma', 'notumor', 'pituitary']
tumor_info = {
    'glioma': 'Gliomas are tumors that originate in the glial cells of the brain or spine. They can vary in severity and require medical evaluation.',
    'meningioma': 'Meningiomas are typically slow-growing tumors that form on the membranes surrounding the brain and spinal cord.',
    'notumor': 'No tumor was detected in the provided MRI image.',
    'pituitary': 'Pituitary tumors form in the pituitary gland and may affect hormone levels. Most are benign but require monitoring.'
}

# Define folders
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Helper function to check allowed file extensions


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Helper function to sanitize text input


def sanitize_text(text):
    if not text:
        return "Not provided"
    return ''.join(c for c in text if ord(c) >= 32 or c == '\n')

# Helper function to predict tumor type


def predict_tumor(image_path):
    try:
        IMAGE_SIZE = 128
        img = load_img(image_path, target_size=(IMAGE_SIZE, IMAGE_SIZE))
        img_array = img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_array)
        predicted_class_index = np.argmax(predictions, axis=1)[0]
        confidence_score = np.max(predictions, axis=1)[0]

        predicted_label = class_labels[predicted_class_index]
        logging.info(
            f"Prediction made: {predicted_label}, Confidence: {confidence_score}")

        if predicted_label == 'notumor':
            return "No Tumor", confidence_score, predicted_label
        else:
            return f"Tumor: {predicted_label}", confidence_score, predicted_label
    except Exception as e:
        logging.error(f"Prediction failed: {str(e)}")
        return None, None, None

# Route for the main page


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            logging.warning("No file part in request")
            return render_template('index.html', result=None, error="No file selected.")

        file = request.files['file']
        if file.filename == '':
            logging.warning("No file selected")
            return render_template('index.html', result=None, error="No file selected.")

        patient_name = request.form.get('patientName', '')
        patient_age = request.form.get('patientAge', '')

        if file and allowed_file(file.filename):
            filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            result, confidence, predicted_label = predict_tumor(file_path)
            if result is None:
                return render_template('index.html', result=None, error="Error processing image. Please try again.")

            return render_template('index.html',
                                   result=result,
                                   confidence=f"{confidence*100:.2f}",
                                   file_path=f'/uploads/{filename}',
                                   tumor_info=tumor_info.get(
                                       predicted_label, ''),
                                   filename=filename,
                                   patientName=patient_name,
                                   patientAge=patient_age)
        else:
            logging.warning(f"Invalid file type: {file.filename}")
            return render_template('index.html', result=None, error="Invalid file type. Please upload a PNG, JPG, or JPEG image.")

    return render_template('index.html', result=None)

# Route to serve uploaded files


@app.route('/uploads/<filename>')
def get_uploaded_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        logging.error(f"Error serving file {filename}: {str(e)}")
        return "File not found", 404

# Route to download PDF report


@app.route('/download_report/<filename>')
def download_report(filename):
    try:
        result = request.args.get('result', 'Unknown')
        confidence = request.args.get('confidence', 'Unknown')
        patient_name = request.args.get('patientName', 'Not provided')
        patient_age = request.args.get('patientAge', 'Not provided')
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Sanitize inputs
        patient_name = sanitize_text(patient_name)
        patient_age = sanitize_text(patient_age)
        result = sanitize_text(result)
        confidence = sanitize_text(confidence)
        # Determine the tumor label for description lookup
        tumor_label = result.lower().replace('tumor: ', '').replace('no tumor', 'notumor').strip()
        tumor_info_text = sanitize_text(tumor_info.get(tumor_label, 'No additional information available.'))
        report_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Generate PDF using FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=5)
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, 'MRI Tumor Detection Report', 0, 1, 'C')
        pdf.set_font("Arial", '', 10)

        # Patient Information
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, 'Patient Information', 0, 1)
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 10, f'Name: {patient_name}', 0, 1)
        pdf.cell(0, 10, f'Age: {patient_age}', 0, 1)
        pdf.cell(0, 10, f'Report Date: {report_date}', 0, 1)

        # Analysis Results
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, 'Analysis Results', 0, 1)
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 10, f'Result: {result}', 0, 1)
        pdf.cell(0, 10, f'Confidence: {confidence}%', 0, 1)
        pdf.cell(0, 10, f'Description: {tumor_info_text}', 0, 1)

        # Disclaimer
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, 'Disclaimer', 0, 1)
        pdf.set_font("Arial", '', 10)
        pdf.multi_cell(0, 10, 'This report is generated by an AI-based system for preliminary analysis. It is not a substitute for professional medical diagnosis. Please consult a certified radiologist or medical professional for an accurate diagnosis and treatment plan.')

        # MRI Image
        if os.path.exists(image_path):
            # Add MRI Image section title
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, 'MRI Image', 0, 1, 'L')
            pdf.set_font("Arial", '', 10)
            # Calculate center position for the image
            image_width = 120
            page_width = pdf.w - 2 * pdf.l_margin
            x_center = (page_width - image_width) / 2 + pdf.l_margin
            y_pos = pdf.get_y() + 5
            pdf.image(image_path, x=x_center, y=y_pos, w=image_width)
            pdf.ln(image_width * 0.7)  # Add some space after image
        else:
            logging.error(f"Image not found at {image_path}")
            pdf.set_font("Arial", '', 10)
            pdf.cell(0, 10, 'MRI Image unavailable.', 0, 1)
        # Save PDF
        pdf_path = os.path.join(
            app.config['UPLOAD_FOLDER'], f"MRI_Report_{filename}.pdf")
        pdf.output(pdf_path)

        return send_file(pdf_path, as_attachment=True, download_name=f"MRI_Report_{filename}.pdf")
    except Exception as e:
        logging.error(f"Error generating report: {str(e)}")
        return f"Error generating report. Check logs for details: {str(e)}", 500
    # Removed finally block to avoid permission error
    # Cleanup can be done manually or via a separate script if needed
    # logging.info(f"PDF generated at {pdf_path}. Manual cleanup recommended if space is a concern.")

# Route for model information


@app.route('/model_info')
def model_info():
    return {
        "model_version": "1.0",
        "last_trained": "2025-06-01",
        "classes": class_labels,
        "image_size": 128
    }


if __name__ == '__main__':
    app.run(debug=True)
