# DPIRD AgriVision Development Documentation

## Project Overview

DPIRD AgriVision is a robust and integrated system designed to process multi-spectral image data and perform predictive analysis using advanced deep learning techniques. The system helps differentiate between crops and weeds, assess the extent of crop damage, and provide recommendations for effective farm management. The project is composed of front-end and back-end components, with seamless integration to provide users with real-time processing, data analysis, and weed removal suggestions.

### Key Features:
- **Image Upload**: Users can upload ZIP files containing multi-spectral TIF images.
- **AI Prediction**: The system processes the images using a deep learning model to detect crops, weeds, and other elements.
- **Analysis**: Provides detailed results and weed removal suggestions based on the prediction.
- **Password Management**: Users can change their account password securely.
- **Interactive Timeline**: Shows historical data on weed management for different regions.

---

## Back-End Documentation

### 1. **Flask Application (app.py)**

This script initializes the Flask application, sets up routing, and connects the different components of the system. It includes security features, logging, database initialization, and model loading.

- **Components**:
  - **Flask Initialization**: Configures the application with CORS, security, and session settings.
  - **Blueprints**: Registers three main blueprints (`main_bp`, `auth_bp`, `file_ops_bp`) for routing.
  - **TensorFlow Model**: Loads a pre-trained model for performing AI predictions on uploaded image data.
  - **Database Setup**: Initializes a SQLite database to store user data.

- **Key Functions**:
  - `create_app()`: Configures the Flask app, including CORS, security, and blueprint registration.
  - `init_db()`: Initializes the SQLite database with a `user` table for storing user credentials.

### 2. **User Authentication (auth.py)**

This module handles user authentication, registration, and password management.

- **Components**:
  - **Login**: Verifies the user’s credentials and returns success or failure.
  - **Registration**: Registers new users with hashed passwords and checks for existing usernames.
  - **Password Update**: Allows users to update their passwords securely.

- **Key Routes**:
  - `/login`: Handles user login via POST request.
  - `/regi`: Registers a new user.
  - `/update_password`: Updates the user’s password after verifying the current password.

### 3. **File Operations (file_operations.py)**

This module manages the upload, extraction, and processing of ZIP files containing multi-spectral images.

- **Components**:
  - **File Upload**: Accepts ZIP files, extracts TIF images, and processes them for spectral analysis.
  - **Image Processing**: Calculates multiple vegetation indices from the uploaded images (GNDVI, SAVI, NDVI, etc.).

- **Key Routes**:
  - `/upload`: Uploads a ZIP file and processes the images.
  - `/download`: Handles file downloads.

- **Functions**:
  - `process_zip_and_calculate_indices()`: Processes the ZIP file, extracts TIF images, and calculates vegetation indices.
  - `calculate_indices()`: Calculates vegetation indices such as NDVI, GNDVI, and SAVI from the multi-spectral image bands.

---

## Front-End Documentation

### 1. **Main Page (mainPage.vue)**

The main landing page of the application that introduces the project and its objectives.

- **Key Features**:
  - Displays an overview of the DPIRD AgriVision project.
  - Provides information on how the system will assist farmers using precision agriculture techniques.

### 2. **Login Page (frontPage.vue)**

This page allows users to log in to their accounts.

- **Key Features**:
  - Form to input the username and password.
  - Provides a link to the registration page for new users.
  - Handles form submission and interacts with the backend to authenticate users.

### 3. **Registration Page (regiPage.vue)**

Allows users to create an account by providing a username and password.

- **Key Features**:
  - Form to enter and confirm new passwords.
  - Validates the input to ensure passwords match and meet length requirements.
  - Interacts with the back-end to register new users.

### 4. **Header Component (Header.vue)**

Displays the main navigation header with user information and links to different parts of the application.

- **Key Features**:
  - Dropdown menu with options to change the password or log out.
  - Navigation links to upload page and time capsule.
  - Integration with Vuex to display the logged-in user’s name.

### 5. **Content Page (Content.vue)**

The core component that handles image upload, AI prediction, and analysis results.

- **Key Features**:
  - File upload functionality for ZIP files containing TIF images.
  - Displays AI-predicted results (crops, weeds, others).
  - Provides detailed analysis and weed removal suggestions based on AI predictions.

- **Methods**:
  - `update()`: Handles file uploads and initiates the AI prediction process.
  - `drawChart()`: Placeholder for charting functionality.

### 6. **Time Capsule Page (TimeCapsule.vue)**

Displays historical data for different regions using a timeline format.

- **Key Features**:
  - Allows users to select a region and plot to view historical data on weed management.
  - Shows a vertical timeline with year-by-year data.

### 7. **User Page (userPage.vue)**

Allows users to change their password after logging in.

- **Key Features**:
  - Form to input the current password and a new password.
  - Validates that the new password meets the required criteria.
  - Submits the password change request to the backend.

---

## Technical Details

### 1. **Multi-Spectral Image Processing**

The back-end processes multi-spectral images using the following vegetation indices:

- **NDVI (Normalized Difference Vegetation Index)**: Measures the difference between near-infrared (NIR) and red bands to monitor vegetation health.
- **GNDVI (Green Normalized Difference Vegetation Index)**: Uses green and NIR bands for vegetation assessment.
- **SAVI (Soil Adjusted Vegetation Index)**: An improvement of NDVI that reduces the influence of soil brightness.
- **MSAVI (Modified SAVI)**: A refinement of SAVI, especially for areas with low vegetation cover.
- **ExG (Excess Green Index)**: Detects green vegetation by enhancing the green band relative to red and blue.

### 2. **Model Integration**

The TensorFlow deep learning model is used to analyze multi-spectral image data for crop and weed identification. The model is pre-trained and loaded during application initialization (`app.py`), and is used to predict vegetation types from the uploaded images.

### 3. **Database and User Management**

The user authentication system uses a SQLite database to store user credentials securely, with hashed passwords. It supports user registration, login, and password management functionalities.

### 4. **Front-End Framework**

The front-end is built using Vue.js, with Element UI as the primary UI component library. It features a responsive design and user-friendly interfaces for image uploads, viewing results, and managing user accounts.

---

## Future Enhancements

- **Expanded Spectral Analysis**: Add support for more vegetation indices and spectral bands.
- **Mobile Support**: Improve responsiveness for mobile and tablet devices.
- **Report Generation**: Automatically generate detailed reports based on analysis results.
- **Multi-Language Support**: Add multi-language support for a broader user base.

---

