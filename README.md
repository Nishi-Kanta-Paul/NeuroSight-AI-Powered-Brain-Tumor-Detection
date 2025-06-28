# Brain Tumor Detection from MRI Dataset

An AI-powered web application for detecting and classifying brain tumors from MRI images using deep learning. This system can identify four different types of brain conditions: glioma, meningioma, pituitary tumor, and no tumor.

## 🧠 Features

- **AI-Powered Analysis**: Deep learning model trained on MRI datasets for accurate tumor detection
- **Multi-Class Classification**: Detects four types of brain conditions:
  - Glioma
  - Meningioma
  - Pituitary Tumor
  - No Tumor
- **Web Interface**: Modern, responsive web application with dark/light theme support
- **PDF Report Generation**: Automatic generation of detailed medical reports
- **Patient Information Management**: Track patient details and analysis history
- **Confidence Scoring**: Provides confidence levels for each prediction
- **Real-time Processing**: Fast image analysis with immediate results

## 📊 Dataset Information

### Brain Tumor MRI Dataset Overview

This project utilizes a comprehensive brain tumor MRI dataset for training and testing the deep learning model. The dataset is crucial for accurate tumor detection and classification.

#### What is a Brain Tumor?

A brain tumor is a collection, or mass, of abnormal cells in your brain. Your skull, which encloses your brain, is very rigid. Any growth inside such a restricted space can cause problems. Brain tumors can be cancerous (malignant) or noncancerous (benign). When benign or malignant tumors grow, they can cause the pressure inside your skull to increase. This can cause brain damage, and it can be life-threatening.

#### Importance of Early Detection

Early detection and classification of brain tumors is an important research domain in the field of medical imaging and accordingly helps in selecting the most convenient treatment method to save patients' lives.

#### Dataset Sources

This dataset is a combination of the following three datasets:

- **figshare**: Primary source for glioma images
- **SARTAJ dataset**: Contributed to the overall dataset
- **Br35H**: Source for no tumor class images

#### Dataset Statistics

- **Total Images**: 7,023 brain MRI images
- **Classes**: 4 distinct categories
- **Image Format**: Various sizes (requires preprocessing)

#### Class Distribution

The dataset contains images classified into 4 categories:

1. **Glioma**: Tumors originating in glial cells
2. **Meningioma**: Tumors forming on brain/spinal cord membranes
3. **No Tumor**: Normal brain MRI scans
4. **Pituitary**: Tumors in the pituitary gland

#### Testing Dataset

The testing folder contains 1,311 images distributed as follows:

- **Glioma**: 300 files
- **Meningioma**: 306 files
- **No Tumor**: 405 files
- **Pituitary**: 300 files

#### Dataset Quality Notes

- **Image Size Variation**: Images in the dataset have different sizes and require resizing to 128x128 pixels for model input
- **Preprocessing**: Extra margins should be removed during preprocessing to improve model accuracy
- **Data Quality**: The original SARTAJ dataset had issues with glioma class categorization, which were resolved by using figshare images instead

#### Dataset Source

- **Kaggle Dataset**: [Brain Tumor MRI Dataset](https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset)
- **Creator**: Masoud Nickparvar
- **License**: Available on Kaggle

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- TensorFlow 2.x
- Flask
- Required Python packages (see requirements.txt)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Nishi-Kanta-Paul/NeuroSight-AI-Powered-Brain-Tumor-Detection.git
   cd "Brain Tumor Detection From MRI Dataset"
   ```

2. **Create a virtual environment (recommended)**

   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare the model**

   - Ensure you have the trained model file `model.h5` in the `models/` directory
   - If you don't have the model, you can train it using the Jupyter notebook in `models/Brain_Tumor_MRI_Detection.ipynb`

5. **Run the application**

   ```bash
   python main.py
   ```

6. **Access the application**
   - Open your web browser and navigate to `http://localhost:5000`
   - The application will be ready to analyze MRI images

## 📁 Project Structure

```
Brain Tumor Detection From MRI Dataset/
├── main.py                          # Main Flask application
├── requirements.txt                 # Python dependencies
├── README.md                       # Project documentation
├── models/
│   ├── model.h5                    # Trained deep learning model
│   └── Brain_Tumor_MRI_Detection.ipynb  # Model training notebook
├── templates/
│   └── index.html                  # Web interface template
├── uploads/                        # Directory for uploaded images
├── sample MRI Images/              # Sample MRI images for testing
│   ├── Te-gl_0015.jpg             # Glioma sample
│   ├── Te-meTr_0001.jpg           # Meningioma sample
│   ├── Te-noTr_0004.jpg           # No tumor sample
│   └── Te-piTr_0003.jpg           # Pituitary tumor sample
├── report_template.tex             # LaTeX template for reports
└── tumor_detection.log             # Application logs
```

## 🔧 Usage

### Web Interface

1. **Upload MRI Image**: Select an MRI image file (PNG, JPG, or JPEG format)
2. **Enter Patient Information**: Provide patient name and age (optional)
3. **Analyze**: Click "Analyze Image" to process the MRI
4. **View Results**: See the detection results with confidence scores
5. **Download Report**: Generate and download a PDF report

### API Endpoints

- `GET /` - Main web interface
- `POST /` - Upload and analyze MRI image
- `GET /uploads/<filename>` - Serve uploaded images
- `GET /download_report/<filename>` - Download PDF report
- `GET /model_info` - Get model information

## 🧪 Model Information

- **Architecture**: Convolutional Neural Network (CNN)
- **Input Size**: 128x128 pixels
- **Classes**: 4 (glioma, meningioma, notumor, pituitary)
- **Training Data**: MRI brain tumor dataset (7,023 images)
- **Testing Data**: 1,311 images
- **Model Version**: 1.0
- **Training Method**: Multi-task classification using CNN

## 📊 Tumor Types and Descriptions

### Glioma

Gliomas are tumors that originate in the glial cells of the brain or spine. They can vary in severity and require medical evaluation.

### Meningioma

Meningiomas are typically slow-growing tumors that form on the membranes surrounding the brain and spinal cord.

### Pituitary Tumor

Pituitary tumors form in the pituitary gland and may affect hormone levels. Most are benign but require monitoring.

### No Tumor

No tumor was detected in the provided MRI image.

## 🔒 Security and Privacy

- **File Validation**: Only image files (PNG, JPG, JPEG) are accepted
- **Input Sanitization**: All user inputs are sanitized to prevent injection attacks
- **Secure Filenames**: Uploaded files are renamed with UUIDs for security
- **Logging**: All activities are logged for monitoring and debugging

## 📝 Logging

The application maintains detailed logs in `tumor_detection.log` including:

- Model loading status
- Prediction results
- Error messages
- File upload activities

## 🚨 Important Disclaimer

**This application is for educational and research purposes only. It is not intended for clinical use or medical diagnosis.**

- The AI model provides preliminary analysis only
- Results should not be used as a substitute for professional medical diagnosis
- Always consult with certified radiologists or medical professionals
- The system is not FDA-approved for clinical use

## 🛠️ Development

### Training the Model

1. Open `models/Brain_Tumor_MRI_Detection.ipynb`
2. Follow the notebook to train your own model
3. Save the trained model as `model.h5` in the `models/` directory

### Data Preprocessing

- **Image Resizing**: All images are resized to 128x128 pixels
- **Margin Removal**: Extra margins are removed to improve accuracy
- **Normalization**: Pixel values are normalized to [0,1] range
- **Data Augmentation**: Applied during training to improve model robustness

### Customization

- **Model**: Replace `model.h5` with your own trained model
- **Classes**: Modify `class_labels` in `main.py` for different tumor types
- **UI**: Customize the web interface in `templates/index.html`
- **Styling**: Modify Tailwind CSS classes for different themes

## 🐛 Troubleshooting

### Common Issues

1. **Model not found error**

   - Ensure `model.h5` exists in the `models/` directory
   - Check file permissions

2. **Import errors**

   - Verify all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility

3. **Upload folder issues**

   - Ensure the `uploads/` directory exists and is writable
   - Check disk space availability

4. **PDF generation errors**
   - Verify FPDF library is properly installed
   - Check file permissions for PDF creation

### Log Analysis

Check `tumor_detection.log` for detailed error messages and debugging information.

## 📈 Performance

- **Processing Time**: ~2-5 seconds per image (depending on hardware)
- **Memory Usage**: ~500MB RAM (with model loaded)
- **Supported Formats**: PNG, JPG, JPEG
- **Image Size**: Automatically resized to 128x128 pixels
- **Model Accuracy**: Trained on 7,023 images, tested on 1,311 images

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Dataset Creator**: Masoud Nickparvar for providing the comprehensive brain tumor MRI dataset
- **Dataset Sources**: figshare, SARTAJ dataset, and Br35H for contributing to the dataset
- **Kaggle Community**: For hosting and maintaining the dataset
- **TensorFlow and Keras communities**: For deep learning frameworks
- **Flask web framework**: For the web application framework
- **Medical imaging research community**: For ongoing research and development

## 📞 Support

For questions, issues, or contributions:

- Create an issue in the repository
- Contact the development team
- Check the troubleshooting section above

## 📚 References

- **Dataset**: [Brain Tumor MRI Dataset on Kaggle](https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset)
- **WHO Guidelines**: World Health Organization brain tumor diagnosis standards
- **Medical Imaging**: Research papers on MRI-based tumor detection

---

**Remember**: This tool is for educational purposes only. Always consult medical professionals for actual diagnosis and treatment.
