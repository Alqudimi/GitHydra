from flask import Blueprint, jsonify, request, current_app
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from githydra.src.utils.git_helper import get_repo
from githydra.src.ai_service import generate_commit_message, review_code, detect_bugs

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/commit-message', methods=['POST'])
def commit_message():
    try:
        repo = get_repo(current_app.config.get('REPO_PATH', '.'))
        if not repo:
            return jsonify({'error': 'Not a git repository'}), 400
        
        diff = repo.git.diff('--cached')
        if not diff:
            return jsonify({'success': False, 'error': 'No staged changes'}), 400
        
        message = generate_commit_message(diff)
        
        return jsonify({'success': True, 'data': {'message': message}})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@ai_bp.route('/review-code', methods=['POST'])
def review_code_api():
    try:
        data = request.json
        code = data.get('code', '')
        
        if not code:
            return jsonify({'success': False, 'error': 'No code provided'}), 400
        
        review = review_code(code)
        
        return jsonify({'success': True, 'data': review})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@ai_bp.route('/detect-bugs', methods=['POST'])
def detect_bugs_api():
    try:
        data = request.json
        code = data.get('code', '')
        
        if not code:
            return jsonify({'success': False, 'error': 'No code provided'}), 400
        
        bugs = detect_bugs(code)
        
        return jsonify({'success': True, 'data': bugs})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
