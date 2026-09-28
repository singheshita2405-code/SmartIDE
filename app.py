from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, Response, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sys
import subprocess
import io

app = Flask(__name__)
app.secret_key = 'smartide-peach-secretkey'  # secret key for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

with app.app_context():
    db.create_all()

WORKSPACE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workspace")
os.makedirs(WORKSPACE, exist_ok=True)

# Seed default workspace files if empty
default_main = '''# SmartIDE — Main Application Script
# Click "Run Code" or use the Terminal to execute!

def greet(name: str) -> str:
    return f"✨ Welcome to SmartIDE, {name}!"

def main():
    print(greet("Developer"))
    print("Desktop-based Python Environment initialized successfully.")
    print("--------------------------------------------------")
    
    tools = ["AI Assistant", "Smart Editor", "Database Explorer", "Integrated Terminal"]
    print("Active Workspace Tools:")
    for idx, tool in enumerate(tools, start=1):
        print(f"  [{idx}] {tool} — Ready")
        
    print("--------------------------------------------------")
    print("Tip: Use Ctrl+S to save, or click 'Run' in the top bar.")

if __name__ == "__main__":
    main()
'''

if not os.path.exists(os.path.join(WORKSPACE, "main.py")):
    with open(os.path.join(WORKSPACE, "main.py"), "w", encoding="utf-8") as f:
        f.write(default_main)


# ==========================
# PAGE ROUTES
# ==========================

@app.route('/')
def home():
    """Launching page with 3 download buttons and desktop IDE preview."""
    return render_template('home.html')

@app.route('/features')
def features():
    """SmartIDE feature highlights."""
    return render_template('features.html')

@app.route('/documentation')
def documentation():
    """Complete SmartIDE user documentation, shortcuts, and setup guide."""
    return render_template('documentation.html')

@app.route('/downloads')
def downloads():
    """Dedicated downloads page for Windows, macOS, and Linux."""
    return render_template('downloads.html')

@app.route('/ide')
@app.route('/dashboard')
def dashboard():
    """Full-featured Desktop-style IDE application in Peach & White theme."""
    return render_template('dashboard.html')

# Graceful redirects for consolidated/streamlined pages
@app.route('/about')
def about():
    return redirect(url_for('home'))

@app.route('/contact')
def contact():
    return redirect(url_for('documentation'))


# ==========================
# AUTHENTICATION ROUTES
# ==========================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validations
        if not name or len(name) < 2:
            flash('Name must be at least 2 characters long.', 'error')
            return redirect(url_for('register'))
        
        if not email or '@' not in email:
            flash('Please enter a valid email address.', 'error')
            return redirect(url_for('register'))

        if len(password) < 8 or not any(c.isdigit() for c in password) or not any(c.isalpha() for c in password):
            flash('Password must be at least 8 characters long and contain letters and numbers.', 'error')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please sign in.', 'error')
            return redirect(url_for('login'))

        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! Please sign in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('register'))
        
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash('Welcome back!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('home'))


# ==========================
# WORKSPACE & FILE APIs
# ==========================

@app.route('/api/files', methods=['GET'])
def list_workspace_files():
    """List all files in the workspace directory."""
    try:
        items = []
        for entry in os.listdir(WORKSPACE):
            full_path = os.path.join(WORKSPACE, entry)
            is_dir = os.path.isdir(full_path)
            size = os.path.getsize(full_path) if not is_dir else 0
            items.append({
                "name": entry,
                "is_dir": is_dir,
                "size": size
            })
        items.sort(key=lambda x: (not x['is_dir'], x['name']))
        return jsonify({"success": True, "files": items})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/get-file', methods=['POST'])
def get_file_content():
    """Retrieve content of a specific workspace file."""
    data = request.get_json() or {}
    filename = data.get('filename')
    if not filename:
        return jsonify({"success": False, "message": "Filename is required"}), 400

    # Sanitize filename
    safe_name = os.path.basename(filename)
    filepath = os.path.join(WORKSPACE, safe_name)

    if not os.path.exists(filepath) or not os.path.isfile(filepath):
        return jsonify({"success": False, "message": "File not found"}), 404

    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        return jsonify({"success": True, "filename": safe_name, "content": content})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/save-file', methods=['POST'])
def save_file_content():
    """Save content to a workspace file."""
    data = request.get_json() or {}
    filename = data.get('filename')
    content = data.get('content', '')

    if not filename:
        return jsonify({"success": False, "message": "Filename is required"}), 400

    safe_name = os.path.basename(filename)
    filepath = os.path.join(WORKSPACE, safe_name)

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return jsonify({"success": True, "filename": safe_name, "message": "Saved successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/new-file', methods=['POST'])
@app.route('/new-file', methods=['POST'])
def new_file():
    """Create a new file in workspace."""
    data = request.get_json() or {}
    filename = data.get('filename', '').strip()

    if not filename:
        return jsonify({"success": False, "message": "Filename required"}), 400

    safe_name = os.path.basename(filename)
    filepath = os.path.join(WORKSPACE, safe_name)

    try:
        if not os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# {safe_name}\n# Created in SmartIDE\n")
        return jsonify({"success": True, "filename": safe_name, "message": "File created"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/delete-file', methods=['POST'])
def delete_file():
    """Delete a file from workspace."""
    data = request.get_json() or {}
    filename = data.get('filename', '').strip()

    if not filename:
        return jsonify({"success": False, "message": "Filename required"}), 400

    safe_name = os.path.basename(filename)
    filepath = os.path.join(WORKSPACE, safe_name)

    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return jsonify({"success": True, "filename": safe_name, "message": "File deleted"})
        return jsonify({"success": False, "message": "File not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ==========================
# CODE EXECUTION ENGINE
# ==========================

@app.route('/run-code', methods=['POST'])
def run_code():
    """Safely execute Python code from the Desktop IDE and return stdout/stderr."""
    data = request.get_json() or {}
    code = data.get('code')
    filename = data.get('filename', 'main.py')

    if code is None:
        safe_name = os.path.basename(filename)
        filepath = os.path.join(WORKSPACE, safe_name)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
        else:
            return jsonify({"success": False, "output": f"Error: File '{safe_name}' not found."})

    try:
        # Run in temporary execution process with timeout
        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=WORKSPACE,
            capture_output=True,
            text=True,
            timeout=8
        )
        output = result.stdout
        if result.stderr:
            output += ("\n--- Errors / Traceback ---\n" if output else "") + result.stderr

        if not output:
            output = "[Program executed cleanly with no standard output]"

        return jsonify({
            "success": True,
            "exit_code": result.returncode,
            "output": output
        })
    except subprocess.TimeoutExpired:
        return jsonify({
            "success": False,
            "exit_code": -1,
            "output": "Execution timed out (maximum 8 seconds exceeded)."
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "exit_code": 1,
            "output": f"Execution error: {str(e)}"
        })


# ==========================
# DOWNLOADS SIMULATION ENDPOINT
# ==========================

@app.route('/download/<platform>')
def download_platform(platform):
    """Direct package downloader for Windows, Mac, and Linux packages."""
    platform = platform.lower()
    filenames = {
        'windows': ('SmartIDE-Setup-v2.4.1-x64.exe', 'application/octet-stream'),
        'win': ('SmartIDE-Setup-v2.4.1-x64.exe', 'application/octet-stream'),
        'mac': ('SmartIDE-v2.4.1-Universal.dmg', 'application/x-apple-diskimage'),
        'macos': ('SmartIDE-v2.4.1-Universal.dmg', 'application/x-apple-diskimage'),
        'linux': ('smartide_2.4.1_amd64.deb', 'application/vnd.debian.binary-package')
    }

    if platform not in filenames:
        return redirect(url_for('downloads'))

    target_name, mime_type = filenames[platform]
    
    # Generate an authentic installer package stub
    stub_content = f"""SmartIDE Desktop Release Package v2.4.1
Target Platform: {platform.upper()}
Package Name: {target_name}
Checksum (SHA-256): e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

Installation Instructions:
1. Double-click or run {target_name} on your {platform.capitalize()} system.
2. Follow the on-screen installer prompts.
3. Launch SmartIDE and start coding!

Thank you for downloading SmartIDE Peach Edition!
"""
    return Response(
        stub_content,
        mimetype=mime_type,
        headers={"Content-Disposition": f"attachment;filename={target_name}"}
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)