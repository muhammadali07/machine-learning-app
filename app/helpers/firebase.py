import firebase_admin

from firebase_admin import credentials, firestore, initialize_app

def firebaseconfig(username):
    # Inisialisasi Firebase
    cred = credentials.Certificate("serviceAccountKey.json")


    initialize_app(cred)
    db = firestore.client()
    user_ref = db.collection('users')
    return user_ref.document

def configure_firebase(service_account_path: str):
    """
    Konfigurasi Firebase menggunakan service account JSON.

    Parameters:
        service_account_path (str): Path ke file serviceAccountKey.json.

    Returns:
        firestore.Client: Instance Firestore yang dikonfigurasi.
    """
    try:
        # Periksa apakah Firebase sudah diinisialisasi
        if not firebase_admin._apps:
            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred)
        else:
            print("Firebase sudah diinisialisasi.")

        # Inisialisasi Firestore
        db = firestore.client()
        print("Firebase Firestore berhasil dikonfigurasi.")
        return db

    except Exception as e:
        print(f"Terjadi kesalahan saat konfigurasi Firebase: {e}")
        raise e