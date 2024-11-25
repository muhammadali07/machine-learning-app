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


### **2. Create a Virtual Environment**
```bash
pyenv install 3.9.17  # Replace with your Python version
pyenv virtualenv 3.9.17 machine-learning-app-env
pyenv activate machine-learning-app-env
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```
### **4. Configure Firebase**
1. Create a Firebase project via the [Firebase Console](https://console.firebase.google.com/u/0/).
2. Download the serviceAccountKey.json and place it in the project root directory.
3. Add your Firebase database URL to the .env file.

### **5. Configure Google OAuth2**
1. Create a project in the Google Cloud Console.
2. Enable the Google OAuth2 API.
3. Download the client_secret.json and set the following in .env:
```bash
GOOGLE_CLIENT_ID=<your-client-id>
GOOGLE_CLIENT_SECRET=<your-client-secret>
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
```

### **6. Create a .env File**
Set environment variables in .env:
```bash
GOOGLE_CLIENT_ID = <your-google-client-id>
GOOGLE_CLIENT_SECRET = <your-google-client-secret>
GOOGLE_REDIRECT_URI = "http://localhost:8000" -> or your preference host another app

# Constants for Google OAuth
GOOGLE_AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URI = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URI = "https://www.googleapis.com/oauth2/v1/userinfo"

```

### **7. Run the Application**
Start the FastAPI development server:
```bash
uvicorn main:app --reload
```

## 📊 **Usage**
Available Endpoints
### 🔐 **Authentication**
- POST /auth/register: Register a new user.
- POST /auth/login: Login with email and password.
- GET /auth/login/google: Redirect to Google OAuth2 login.
- GET /auth/callback: Handle Google OAuth2 callback.
### 🤖 **Prediction**
- POST /predict: Predict outcomes using TensorFlow.
Sample Payload:
```json
{
  "gender": "Male",
  "age": 25.0,
  "height": 175.0,
  "weight": 70.0,
  "family_history": 1,
  "high_calorie_food": 0,
  "vegetable_freq": 5,
  "meals_per_day": 3.0,
  "food_between_meals": "Rarely",
  "smoking": 0,
  "water_consumption": 2.5,
  "calorie_monitoring": 1,
  "physical_activity": 3.5,
  "tech_usage": 4,
  "alcohol_consumption": "Occasionally",
  "transportation": "Car"
}
```

###🧑‍💼 **User Profile**
- GET /profile: Retrieve user profiles.
- PUT /profile/update: Update a user profile.

### 🛠️ **Project Structure**
```bash
machine-learning-app/
│
├── main.py                # Entry point of the application
├── requirements.txt       # Python dependencies
├── serviceAccountKey.json # Firebase credentials
├── .env                   # Environment variables
├── models/                # TensorFlow models
├── utils/                 # Utility functions
├── routers/               # API endpoint routers
└── README.md              # Documentation
```

### 🤝 **Contributing**
We welcome contributions! To contribute:

Fork this repository.
1. Create a new branch: git checkout -b feature-name.
2. Commit your changes: git commit -m 'Add some feature'.
3. Push to the branch: git push origin feature-name.
4. Submit a pull request.
## 🧾 **License**
This project is licensed under the MIT License. See the [LICENSE] file for details.

## 📞 **Contact**
For questions or support:

Email: [muhalibakhtiar@gmail.com]
GitHub: [Muhammad Ali](https://github.com/muhammadali07)





