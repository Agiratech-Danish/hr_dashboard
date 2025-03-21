from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Static username and password 
VALID_USERNAME = "Agira"
VALID_PASSWORD = "12345"

@app.route('/')
def index():
    # Show dashboard as the home page (no login required)
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            # Store username in session to keep user logged in
            session['username'] = username
            
            # If user was trying to access PowerBI, redirect there
            if 'next' in session:
                next_page = session.pop('next')
                return redirect(next_page)
            
            # Otherwise go back to home page
            return redirect(url_for('index'))
        else:
            # Show error message
            return render_template('login.html', error="Invalid username or password. Please try again.")
    
    # GET request - show login page
    return render_template('login.html')

@app.route('/powerbi')
def powerbi():
    # Check if user is logged in
    if 'username' not in session:
        # Store the intended destination
        session['next'] = url_for('powerbi')
        # Redirect to login
        return redirect(url_for('login'))
    
    # User is logged in, show PowerBI dashboard
    return render_template('powerbi.html')

@app.route('/logout')
def logout():
    # Remove username from session
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)

