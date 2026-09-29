from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
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

# Workspace directory definition
WORKSPACE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'workspace')
os.makedirs(WORKSPACE_DIR, exist_ok=True)


# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


def init_workspace():
    """Ensure essential starter files exist in the workspace directory."""
    main_file = os.path.join(WORKSPACE_DIR, 'main.py')
    if not os.path.exists(main_file):
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(
                '# SmartIDE — Main Application Script\n'
                '# Press "Run Code" or use the Terminal to execute!\n\n'
                'def greet(name: str) -> str:\n'
                '    return f"✨ Welcome to SmartIDE, {name}!"\n\n'
                'def main():\n'
                '    print(greet("Developer"))\n'
                '    print("Desktop-based Python Environment initialized successfully.")\n'
                '    print("-" * 50)\n'
                '    tools = ["AI Assistant", "Smart Editor", "Database Explorer", "Integrated Terminal"]\n'
                '    print("Active Workspace Tools:")\n'
                '    for idx, tool in enumerate(tools, start=1):\n'
                '        print(f"  [{idx}] {tool} — Ready")\n'
                '    print("-" * 50)\n'
                '    print("Tip: Use Ctrl+S to save, or click \'Run\' in the top bar.")\n\n'
                'if __name__ == "__main__":\n'
                '    main()\n'
            )

    calc_file = os.path.join(WORKSPACE_DIR, 'calculator.py')
    if not os.path.exists(calc_file):
        with open(calc_file, 'w', encoding='utf-8') as f:
            f.write(
                '# SmartIDE — Math & Utilities Demo\n\n'
                'class SmartCalculator:\n'
                '    def add(self, a, b):\n'
                '        return a + b\n\n'
                '    def multiply(self, a, b):\n'
                '        return a * b\n\n'
                'if __name__ == "__main__":\n'
                '    calc = SmartCalculator()\n'
                '    print("Calculating in SmartIDE workspace:")\n'
                '    print("  12 + 25 =", calc.add(12, 25))\n'
                '    print("  7 * 8   =", calc.multiply(7, 8))\n'
            )

    welcome_file = os.path.join(WORKSPACE_DIR, 'welcome.txt')
    if not os.path.exists(welcome_file):
        with open(welcome_file, 'w', encoding='utf-8') as f:
            f.write(
                'Welcome to SmartIDE Desktop!\n'
                '==============================\n'
                'Theme: Peach & White Edition\n'
                'Built for speed, clarity, and zero-distraction development.\n'
                'Visit Documentation to explore keyboard shortcuts.\n'
            )


with app.app_context():
    db.create_all()
    init_workspace()


def get_safe_path(filename):
    """Sanitize and return an absolute path inside the workspace."""
    if not filename:
        raise ValueError("Filename is required.")
    clean_name = os.path.basename(filename.strip().replace('\\', '/'))
    if not clean_name or clean_name in ('.', '..'):
        raise ValueError("Invalid filename.")
    target_path = os.path.abspath(os.path.join(WORKSPACE_DIR, clean_name))
    workspace_root = os.path.abspath(WORKSPACE_DIR)
    if not target_path.startswith(workspace_root):
        raise ValueError("Unauthorized path traversal attempt.")
    return target_path


# ---------------- PAGE ROUTES ----------------

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/features')
def features():
    return render_template('features.html')


@app.route('/documentation')
def documentation():
    return render_template('documentation.html')


@app.route('/downloads')
def downloads():
    return render_template('downloads.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/download/<platform>')
def download_platform(platform):
    """Provide desktop release downloads for Windows, macOS, and Linux."""
    platform_key = platform.strip().lower()
    platform_map = {
        'windows': ('SmartIDE-Setup-v2.4.1-x64.exe', 'application/vnd.microsoft.portable-executable'),
        'mac': ('SmartIDE-v2.4.1-Universal.dmg', 'application/x-apple-diskimage'),
        'linux': ('smartide_2.4.1_amd64.deb', 'application/vnd.debian.binary-package'),
    }

    filename, mime = platform_map.get(platform_key, ('SmartIDE-v2.4.1.zip', 'application/zip'))

    installer_payload = (
        f"SmartIDE Desktop Installer — Release v2.4.1\n"
        f"============================================\n"
        f"Target Operating System: {platform.capitalize()}\n"
        f"Theme: Peach & White Desktop Edition\n"
        f"Status: Verified Release Binary\n\n"
        f"Installation instructions:\n"
        f"1. Run this setup package to install SmartIDE.\n"
        f"2. Launch SmartIDE and begin coding with the bundled Python environment.\n"
        f"Or run the online Web IDE anytime at /dashboard.\n"
    ).encode('utf-8')

    bio = io.BytesIO(installer_payload)
    bio.seek(0)
    return send_file(bio, as_attachment=True, download_name=filename, mimetype=mime)


# ---------------- AUTHENTICATION ROUTES ----------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

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
    flash('You have been successfully signed out.', 'success')
    return redirect(url_for('home'))


# ---------------- WORKSPACE FILE APIS ----------------

@app.route('/api/files', methods=['GET'])
def list_workspace_files():
    """List all files in the workspace directory."""
    try:
        files = []
        for entry in os.listdir(WORKSPACE_DIR):
            full_path = os.path.join(WORKSPACE_DIR, entry)
            is_dir = os.path.isdir(full_path)
            size = os.path.getsize(full_path) if not is_dir else 0
            files.append({
                'name': entry,
                'is_dir': is_dir,
                'size': size
            })
        # Sort directories first, then files
        files.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
        return jsonify({'success': True, 'files': files})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/get-file', methods=['POST'])
def get_file():
    """Read and return content of a file in workspace."""
    data = request.get_json(silent=True) or {}
    filename = data.get('filename')
    try:
        filepath = get_safe_path(filename)
        if not os.path.isfile(filepath):
            return jsonify({'success': False, 'error': 'File not found'}), 404
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        return jsonify({'success': True, 'filename': filename, 'content': content})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/save-file', methods=['POST'])
def save_file():
    """Save content to a workspace file."""
    data = request.get_json(silent=True) or {}
    filename = data.get('filename')
    content = data.get('content', '')
    try:
        filepath = get_safe_path(filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return jsonify({'success': True, 'message': f'File {filename} saved successfully.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/new-file', methods=['POST'])
def new_file():
    """Create a new file in workspace."""
    data = request.get_json(silent=True) or {}
    filename = data.get('filename')
    try:
        filepath = get_safe_path(filename)
        if os.path.exists(filepath):
            return jsonify({'success': False, 'error': 'File already exists.'}), 400
        
        default_content = ''
        if filepath.endswith('.py'):
            default_content = f'# {os.path.basename(filepath)}\n# Created with SmartIDE\n\nprint("Hello from {os.path.basename(filepath)}!")\n'
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(default_content)
        return jsonify({'success': True, 'message': f'File {filename} created successfully.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/delete-file', methods=['POST'])
def delete_file():
    """Delete a file from workspace."""
    data = request.get_json(silent=True) or {}
    filename = data.get('filename')
    try:
        filepath = get_safe_path(filename)
        if not os.path.exists(filepath):
            return jsonify({'success': False, 'error': 'File does not exist.'}), 404
        if os.path.isdir(filepath):
            os.rmdir(filepath)
        else:
            os.remove(filepath)
        return jsonify({'success': True, 'message': f'File {filename} deleted successfully.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ---------------- CODE EXECUTION API ----------------

@app.route('/run-code', methods=['POST'])
def run_code():
    """Execute Python code or scripts within workspace and return stdout/stderr."""
    data = request.get_json(silent=True) or {}
    filename = data.get('filename')
    code = data.get('code')

    # If code is supplied with a filename, persist it before running
    if filename and code is not None:
        try:
            filepath = get_safe_path(filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
        except Exception as e:
            return jsonify({'output': f'Error saving file before execution: {str(e)}', 'exit_code': 1})

    cmd = [sys.executable]
    if filename:
        try:
            filepath = get_safe_path(filename)
            if not os.path.exists(filepath):
                return jsonify({'output': f"Error: File '{filename}' not found in workspace.", 'exit_code': 1})
            cmd.append(filepath)
        except ValueError as e:
            return jsonify({'output': str(e), 'exit_code': 1})
    elif code:
        cmd.extend(['-c', code])
    else:
        return jsonify({'output': 'No code or filename provided to execute.', 'exit_code': 1})

    try:
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        proc = subprocess.run(
            cmd,
            cwd=WORKSPACE_DIR,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=15,
            env=env
        )
        output = proc.stdout
        if proc.stderr:
            if output:
                output += '\n' + proc.stderr
            else:
                output = proc.stderr
        return jsonify({
            'output': output if output else '[Program exited with no output]',
            'exit_code': proc.returncode
        })
    except subprocess.TimeoutExpired:
        return jsonify({
            'output': 'Execution timed out (15 second limit reached).',
            'exit_code': -1
        })
    except Exception as e:
        return jsonify({
            'output': f'Execution error: {str(e)}',
            'exit_code': 1
        })


if __name__ == '__main__':
    app.run(debug=True)