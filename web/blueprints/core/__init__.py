from flask import Blueprint, render_template, current_app
import os

core_bp = Blueprint('core', __name__, template_folder='../../templates')

@core_bp.route('/')
def index():
    return render_template('dashboard.html')

@core_bp.route('/branches')
def branches():
    return render_template('branches.html')

@core_bp.route('/commits')
def commits():
    return render_template('commits.html')

@core_bp.route('/stage')
def stage():
    return render_template('stage.html')

@core_bp.route('/stash')
def stash():
    return render_template('stash.html')

@core_bp.route('/remotes')
def remotes():
    return render_template('remotes.html')

@core_bp.route('/tags')
def tags():
    return render_template('tags.html')

@core_bp.route('/analytics')
def analytics_page():
    return render_template('analytics.html')

@core_bp.route('/ai-tools')
def ai_tools():
    return render_template('ai_tools.html')

@core_bp.route('/settings')
def settings():
    return render_template('settings.html')
