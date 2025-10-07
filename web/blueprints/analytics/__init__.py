from flask import Blueprint, jsonify, current_app, request
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from githydra.src.utils.git_helper import get_repo

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/weekly-report')
def weekly_report():
    try:
        repo = get_repo(current_app.config.get('REPO_PATH', '.'))
        if not repo:
            return jsonify({'error': 'Not a git repository'}), 400
        
        weeks = int(request.args.get('weeks', 1))
        since_date = datetime.now() - timedelta(weeks=weeks)
        
        commits = list(repo.iter_commits(since=since_date.isoformat()))
        
        total_commits = len(commits)
        authors = {}
        total_additions = 0
        total_deletions = 0
        
        for commit in commits:
            author = commit.author.name
            authors[author] = authors.get(author, 0) + 1
            total_additions += commit.stats.total.get('insertions', 0)
            total_deletions += commit.stats.total.get('deletions', 0)
        
        return jsonify({
            'success': True,
            'data': {
                'total_commits': total_commits,
                'total_additions': total_additions,
                'total_deletions': total_deletions,
                'authors': authors,
                'period': f'{weeks} week(s)'
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@analytics_bp.route('/code-insights')
def code_insights():
    try:
        repo = get_repo(current_app.config.get('REPO_PATH', '.'))
        if not repo:
            return jsonify({'error': 'Not a git repository'}), 400
        
        file_stats = {}
        for item in repo.tree().traverse():
            if item.type == 'blob':
                ext = os.path.splitext(item.name)[1] or 'no-ext'
                file_stats[ext] = file_stats.get(ext, 0) + 1
        
        return jsonify({
            'success': True,
            'data': {
                'file_types': file_stats,
                'total_files': sum(file_stats.values())
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@analytics_bp.route('/team-analytics')
def team_analytics():
    try:
        repo = get_repo(current_app.config.get('REPO_PATH', '.'))
        if not repo:
            return jsonify({'error': 'Not a git repository'}), 400
        
        commits = list(repo.iter_commits(max_count=100))
        
        contributors = {}
        for commit in commits:
            author = commit.author.name
            if author not in contributors:
                contributors[author] = {
                    'commits': 0,
                    'additions': 0,
                    'deletions': 0,
                    'email': commit.author.email
                }
            contributors[author]['commits'] += 1
            contributors[author]['additions'] += commit.stats.total.get('insertions', 0)
            contributors[author]['deletions'] += commit.stats.total.get('deletions', 0)
        
        return jsonify({
            'success': True,
            'data': contributors
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
