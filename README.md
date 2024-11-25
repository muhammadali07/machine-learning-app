# 🌟 **Machine Learning App** 🌟

A **web-based backend application** built with **FastAPI**, designed to:
- Perform **machine learning predictions** using TensorFlow models.
- Manage user authentication via **JWT** and **Google OAuth2**.
- Leverage **Firebase** for secure user management and profile handling.

---

## 🚀 **Features**
- **Prediction API**: Leverages TensorFlow models to predict outcomes based on user input.
- **User Authentication**:
  - Register and login with email/password.
  - **Google OAuth2** for social authentication.
- **JWT Authentication**: Protects API endpoints with JSON Web Tokens.
- **Profile Management**:
  - Retrieve and update user profiles.
- **Firebase Integration**: Securely stores and retrieves user data using Firestore.
- **Configurable**: Easily set up environment variables for deployment.

---

## 📋 **Requirements**

Ensure you have the following installed:
- Python **3.9** or higher.
- [TensorFlow](https://www.tensorflow.org/).
- [FastAPI](https://fastapi.tiangolo.com/).
- Firebase Admin SDK.
- Google OAuth2 credentials.

---

## ⚙️ **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone https://github.com/your-username/machine-learning-app.git
cd machine-learning-app
```

### **2. Create a Virtual Environment**
```bash
pyenv install 3.9.17  # Replace with your Python version
pyenv virtualenv 3.9.17 machine-learning-app-env
pyenv activate machine-learning-app-env
```


### **3. Install Dependencies**
```bash
pip install -r requirements.txt
````
### **4. Configure Firebase**
1. Create a Firebase project via the [Firebase Console].()
2. Download the serviceAccountKey.json and place it in the project root directory.
3. Add your Firebase database URL to the .env file.


