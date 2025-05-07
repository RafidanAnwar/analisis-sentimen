from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Used for session management

# Expanded positive and negative words for Lexicon-based Sentiment Analysis
positive_words = {
    "baik", "cepat", "keren", "bantu", "ngebantu", "user", "friendly", "simpel",
    "recomended", "top", "markotop", "oke", "bagus", "lumayan", "istimewa", "lengkap"
}
negative_words = {
    "error", "bug", "lambat", "lemot", "stress", "frustasi", "ganggu", "bingung",
    "jelek", "lemot", "masalah", "gagal", "terlambat", "kurang", "ribet"
}

# Staff credentials
staff_credentials = {
    'username': 'indah',
    'password': generate_password_hash('123')  # Store hashed password
}

# Function to analyze sentiment based on Lexicon-based approach
def analyze_sentiment(feedback):
    words = feedback.lower().split()
    sentiment_score = 0
    for word in words:
        if word in positive_words:
            sentiment_score += 1
        elif word in negative_words:
            sentiment_score -= 1
    if sentiment_score > 0:
        return "Positive"
    elif sentiment_score < 0:
        return "Negative"
    else:
        return "Neutral"

# Feedback data (hardcoded based on the dataset provided by the user)
feedback_data = [
    {'feedback': 'Aku sukaaa banget sama SIAK karena bikin urusan akademik jadi gak ribet. Tapi kadang agak lemot kalo jam sibuk, tapi overall sih TOP MARKOTOP! 👏👏', 'sentiment': 'Positive'},
    {'feedback': 'Ini sistem keren parah, apalagi buat liat jadwal kuliah sama nilai. Cuma kadang-kadang error dikit, tapi masih bisa dimaklumin lah ya. 😌✨', 'sentiment': 'Positive'},
    {'feedback': 'SIAK tuh simpel banget dipake, gak ribet, dan navigasi antarmukanya juga cukup friendly. Recomended deh buat mahasiswa yang mau urus administrasi tanpa ribet! 🤩🙌', 'sentiment': 'Positive'},
    {'feedback': 'SIAK sering banget error pas lagi penting-pentingnya! 😤 Pas mau daftar mata kuliah tuh auto stress, kadang sampe harus nunggu lama baru bisa masuk. Please diperbaiki dong, admin! 🥺💔', 'sentiment': 'Negative'},
    {'feedback': 'UI-nya tuh kurang kece sih menurutku. Kadang bingung mau klik mana dulu, trus kecepatannya juga lambat banget pas jam sibuk. Fix butuh upgrade nih! 🚀😤', 'sentiment': 'Negative'},
    {'feedback': 'Gak jarang aku nemu bug pas lagi pake SIAK. Kayak kemarin, nilai aku gak muncul padahal udah keluar di dosen. Auto panik mode: ON! 😱😭', 'sentiment': 'Negative'},
    {'feedback': 'Jujur ya, SIAK tuh lumayan ngebantu, tapi masalah teknisnya bikin frustasi. Kadang login aja susah, trus error mulu pas mau liat jadwal. Mohon diperhatikan lagi deh performanya! 🙏😢', 'sentiment': 'Negative'},
    {'feedback': 'SIAK tuh standar aja sih buat aku. Ada bagusnya, ada jeleknya juga. Kayak gampang dipake, tapi kadang lemot atau error. Semoga ke depannya bisa lebih stabil ya! 😊🙏', 'sentiment': 'Neutral'},
    {'feedback': 'Secara keseluruhan sih oke, cuma kadang ada masalah teknis yang bikin ganggu aktivitas kuliah. Tapi tetep worth it buat ngecek nilai sama jadwal kuliah! 📅💻', 'sentiment': 'Neutral'},
    {'feedback': 'Sistemnya cukup membantu, tapi gak istimewa-istimewa banget. Mungkin kalau tampilan antarmukanya lebih modern, bakal lebih nyaman dipake. Keep improving, guys! ✨💡', 'sentiment': 'Neutral'},
    {'feedback': 'Aku pake SIAK biasa aja sih, gak ada masalah besar. Tapi yaaa, kalau bisa dipercepat aksesnya sama diperbaiki fitur-fiturnya biar lebih maksimal, pasti lebih keren! 🚀👍', 'sentiment': 'Neutral'},
    {'feedback': 'SIAK tuh sistem yang bener-bener ngebantu, tapi sayangnya sering error pas lagi penting-pentingnya. Misalnya pas mau daftar mata kuliah, auto stuck mulu. Plisss diperbaiki ya, admin! 😤🙏', 'sentiment': 'Negative'},
    {'feedback': 'Antarmuka SIAK tuh lumayan user-friendly, tapi kecepatannya kadang bikin emosi. Pas jam sibuk tuh auto loading lama, bikin males pakenya. Fix perlu upgrade performa nih! 🚀💔', 'sentiment': 'Negative'},
    {'feedback': 'Fitur SIAK udah lengkap sih, tapi kadang ada bug yang bikin ganggu. Contohnya pas pencarian mata kuliah tuh suka error. Semoga ke depannya bisa lebih reliable ya! 💪✨', 'sentiment': 'Neutral'},
    {'feedback': 'SIAK tuh lumayan membantu sih, tapi kadang error pas lagi penting-pentingnya. Semoga bisa diperbaiki ya, admin! 😊🙏', 'sentiment': 'Neutral'}
]

# Route for home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for student feedback submission
@app.route('/mahasiswa', methods=['POST', 'GET'])
def mahasiswa():
    if request.method == 'POST':
        feedback = request.form['feedback']
        sentiment = analyze_sentiment(feedback)
        # Store user feedback
        user_feedback_data = {'feedback': feedback, 'sentiment': sentiment}
        feedback_data.append(user_feedback_data)  # Add the user feedback to the main dataset
        return render_template('mahasiswa_result.html', feedback=feedback, sentiment=sentiment)
    return render_template('mahasiswa_feedback.html')

# Route for staff to view all feedback results (requires login)
@app.route('/staff')
def staff():
    if 'staff_logged_in' not in session:
        return redirect(url_for('login'))

    return render_template('staff_dashboard.html', feedback_data=feedback_data)

# Login page for staff
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if credentials are correct
        if username == staff_credentials['username'] and check_password_hash(staff_credentials['password'], password):
            session['staff_logged_in'] = True  # Create session for staff
            return redirect(url_for('staff'))
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

# Logout functionality
@app.route('/logout')
def logout():
    session.pop('staff_logged_in', None)  # Remove session
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
