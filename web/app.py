from flask import Flask, render_template
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from web.blueprints.core import core_bp
from web.blueprints.git_ops import git_ops_bp
from web.blueprints.analytics import analytics_bp
from web.blueprints.ai import ai_bp

def create_app(repo_path='.'):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['REPO_PATH'] = repo_path
    
    app.register_blueprint(core_bp, url_prefix='/')
    app.register_blueprint(git_ops_bp, url_prefix='/api/git')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    
    return app

def run_web_server(repo_path='.', port=5000, debug=True):
    app = create_app(repo_path)
    print(f"🚀 GitHydra Web Dashboard starting...")
    print(f"📁 Repository: {os.path.abspath(repo_path)}")
    print(f"🌐 Server: http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=debug)

if __name__ == '__main__':
    run_web_server()
