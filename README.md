### Backend Setup:

1. **Install Required Python Packages**: Ensure that all necessary Python packages are installed. This can be done using `pip install` with the `requirements.txt` file (if provided) or by installing each required package individually.

2. **Run the Backend**:  
   Open a terminal and navigate to the `back-end` directory, then run the following command:
   ```bash
   python app.py
   ```

3. **Model Setup**:  
   Ensure the file `model1.h5` is placed in the `back-end` directory. This model can be trained using the `InceptionV3_Model_v1.1.py` script if not already available.

---

### Frontend Setup:

1. **Install Node.js Modules**:  
   In the terminal, navigate to the `front-end` directory and run the following command:
   ```bash
   npm install
   ```
   This will automatically create a `node_modules` folder. Note that errors during this step are common and can often be resolved by retrying or troubleshooting the specific error messages.

2. **Run the Frontend**:  
   After the installation, start the development server by running:
   ```bash
   npm run dev
   ```

---

### Inference:

To perform inference, the input must be a zipped file of the `smalldata_X_Y` dataset. This file will be analyzed using the model.

---

### Python Version:

The backend uses Python version 3.9.*. Ensure compatibility when installing packages and running the application.
