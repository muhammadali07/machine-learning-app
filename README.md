#Machine Learning App
A web-based backend application built with FastAPI, designed to facilitate machine learning predictions and user authentication using JWT and Google OAuth2. The app supports Firebase for user management and offers endpoints for prediction, user profile management, and authentication.

#Features
Prediction API: Utilize TensorFlow models for predictions based on user input.
User Management:
Register, login, and manage user profiles.
Authenticate via Google OAuth2.
JWT Authentication: Secure endpoints with JSON Web Tokens.
Firebase Integration: Leverages Firebase Firestore for user data storage.
Flexible Configurations: Supports environment variables for easy deployment.

#Requirements :
Before running this application, ensure you have the following installed:

Python 3.9 or higher
TensorFlow
FastAPI
Firebase Admin SDK
Google Cloud OAuth2 credentials
Setup Instructions
1. Clone the Repository
bash
Copy code
git clone https://github.com/your-username/machine-learning-app.git
cd machine-learning-app
2. Create a Virtual Environment
Using pyenv:

bash
Copy code
pyenv install 3.9.17  # Replace with the desired version
pyenv virtualenv 3.9.17 machine-learning-app-env
pyenv activate machine-learning-app-env
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Set Up Firebase
Create a Firebase project in the Firebase Console.
Download the serviceAccountKey.json file and place it in the project root directory.
Add your Firebase database URL to the .env file.
5. Configure Google OAuth2
Go to the Google Cloud Console.
Create a new project and enable Google OAuth2 API.
Download your client_secret.json and configure the .env file:
makefile
Copy code
GOOGLE_CLIENT_ID=<your-client-id>
GOOGLE_CLIENT_SECRET=<your-client-secret>
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
6. Environment Variables
Create a .env file in the project root:

env
Copy code
SECRET_KEY=<your-secret-key>
FIREBASE_DATABASE_URL=https://<your-firebase-database>.firebaseio.com
GOOGLE_CLIENT_ID=<your-google-client-id>
GOOGLE_CLIENT_SECRET=<your-google-client-secret>
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
7. Run the Application
Start the development server:

bash
Copy code
uvicorn main:app --reload
Usage
Endpoints
Authentication
/auth/register: Register a new user.
/auth/login: Login with email and password.
/auth/login/google: Redirect to Google OAuth2 login.
/auth/callback: Handle Google OAuth2 callback.
Prediction
/predict: Send a POST request with user data for prediction.
User Management
/profile: Get user profile.
/profile/update: Update user profile.
Example Payload for /predict
json
Copy code
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
Project Structure
bash
Copy code
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
Contributing
Contributions are welcome! Please follow these steps:

Fork this repository.
Create a new branch: git checkout -b feature-name.
Commit your changes: git commit -m 'Add some feature'.
Push to the branch: git push origin feature-name.
Submit a pull request.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
For questions or support, feel free to reach out:

Email: muhalibakhtiar@gmail.com
GitHub: muhammadali07
