from flask import Blueprint, jsonify, request, current_app
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from githydra.src.utils.git_helper import get_repo, get_branch_list, get_commit_history, get_staged_files

git_ops_bp = Blueprint('git_ops', __name__)

@git_ops_bp.route('/status')
def status():
    try:
        repo = get_repo(current_app.config.get('REPO_PATH', '.'))
        if not repo:
            return jsonify({'error': 'Not a git repository'}), 400
        
        return jsonify({
            'success': True,
            'data': {
                'branch': repo.active_branch.name if not repo.head.is_detached else 'HEAD detached',
                'staged': get_staged_files(repo),
                'unstaged': [item.a_path for item in repo.index.diff(None)],
                'untracked': repo.untracked_files
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@git_ops_bp.route('/branches')
def branches():
    try:
        repo = get_repo(current_app.config.get('REPO_PATH', '.'))
        if not repo:
            return jsonify({'error': 'Not a git repository'}), 400
        
        branches_list = get_branch_list(repo)
        current_branch = repo.active_branch.name if not repo.head.is_detached else None
        
        return jsonify({
            'success': True,
            'data': {
                'current': current_branch,
                'branches': [{'name': b[0], 'current': b[1]} for b in branches_list]
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@git_ops_bp.route('/branches/create', methods=['POST'])
def create_branch():
    try:
        repo = get_repo(current_app.config.get('REPO_PATH', '.'))
        if not repo:
            return jsonify({'error': 'Not a git repository'}), 400
        
        data = request.json
        branch_name = data.get('name')
        checkout = data.get('checkout', False)
        
        new_branch = repo.create_head(branch_name)
        if checkout:
            new_branch.checkout()
        
        return jsonify({'success': True, 'message': f'Branch {branch_name} created successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@git_ops_bp.route('/branches/switch', methods=['POST'])
def switch_branch():
    try:
        repo = get_repo(current_app.config.get('REPO_PATH', '.'))
        if not repo:
            return jsonify({'error': 'Not a git repository'}), 400
        
        data = request.json
        branch_name = data.get('name')
        
        repo.heads[branch_name].checkout()
        
        return jsonify({'success': True, 'message': f'Switched to branch {branch_name}'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@git_ops_bp.route('/branches/delete', methods=['POST'])
def delete_branch():
    try:
        repo = get_repo(current_app.config.get('REPO_PATH', '.'))
        if not repo:
            return jsonify({'error': 'Not a git repository'}), 400
        
        data = request.json
        branch_name = data.get('name')
        force = data.get('force', False)
        
        repo.delete_head(branch_name, force=force)
        
        return jsonify({'success': True, 'message': f'Branch {branch_name} deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@git_ops_bp.route('/commits')
def commits():
    try:
        repo = get_repo(current_app.config.get('REPO_PATH', '.'))
        if not repo:
            return jsonify({'error': 'Not a git repository'}), 400
        
        limit = int(request.args.get('limit', 20))
        commits_data = get_commit_history(repo, limit)
        
        return jsonify({'success': True, 'data': commits_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@git_ops_bp.route('/commit', methods=['POST'])
def commit():
    try:
        repo = get_repo(current_app.config.get('REPO_PATH', '.'))
        if not repo:
            return jsonify({'error': 'Not a git repository'}), 400
        
        data = request.json
        message = data.get('message')
        
        if not message:
            return jsonify({'success': False, 'error': 'Commit message is required'}), 400
        
        repo.index.commit(message)
        
        return jsonify({'success': True, 'message': 'Changes committed successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@git_ops_bp.route('/stage/files')
def stage_files():
    try:
        repo = get_repo(current_app.config.get('REPO_PATH', '.'))
        if not repo:
            return jsonify({'error': 'Not a git repository'}), 400
        
        staged = get_staged_files(repo)
        unstaged = [item.a_path for item in repo.index.diff(None)]
        untracked = repo.untracked_files
        
        return jsonify({
            'success': True,
            'data': {
                'staged': staged,
                'unstaged': unstaged,
                'untracked': untracked
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@git_ops_bp.route('/stage/add', methods=['POST'])
def stage_add():
    try:
        repo = get_repo(current_app.config.get('REPO_PATH', '.'))
        if not repo:
            return jsonify({'error': 'Not a git repository'}), 400
        
        data = request.json
        files = data.get('files', [])
        
        if not files:
            repo.git.add(A=True)
        else:
            repo.index.add(files)
        
        return jsonify({'success': True, 'message': 'Files staged successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@git_ops_bp.route('/stage/reset', methods=['POST'])
def stage_reset():
    try:
        repo = get_repo(current_app.config.get('REPO_PATH', '.'))
        if not repo:
            return jsonify({'error': 'Not a git repository'}), 400
        
        data = request.json
        files = data.get('files', [])
        
        if not files:
            repo.index.reset()
        else:
            repo.index.reset(paths=files)
        
        return jsonify({'success': True, 'message': 'Files unstaged successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@git_ops_bp.route('/stash')
def stash_list():
    try:
        repo = get_repo(current_app.config.get('REPO_PATH', '.'))
        if not repo:
            return jsonify({'error': 'Not a git repository'}), 400
        
        stash_output = repo.git.stash('list')
        stashes = []
        
        if stash_output:
            for i, line in enumerate(stash_output.split('\n')):
                if line.strip():
                    # Parse format: "stash@{0}: WIP on main: abc1234 commit message"
                    parts = line.split(':', 2)
                    if len(parts) >= 3:
                        stashes.append({
                            'index': i,
                            'message': parts[2].strip(),
                            'date': ''  # Date not easily available from list command
                        })
                    else:
                        stashes.append({
                            'index': i,
                            'message': line.strip(),
                            'date': ''
                        })
        
        return jsonify({'success': True, 'data': stashes})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@git_ops_bp.route('/stash/save', methods=['POST'])
def stash_save():
    try:
        repo = get_repo(current_app.config.get('REPO_PATH', '.'))
        if not repo:
            return jsonify({'error': 'Not a git repository'}), 400
        
        data = request.json
        message = data.get('message', 'WIP')
        
        repo.git.stash('save', message)
        
        return jsonify({'success': True, 'message': 'Changes stashed successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@git_ops_bp.route('/remotes')
def remotes():
    try:
        repo = get_repo(current_app.config.get('REPO_PATH', '.'))
        if not repo:
            return jsonify({'error': 'Not a git repository'}), 400
        
        remotes_list = [{
            'name': remote.name,
            'url': list(remote.urls)[0] if remote.urls else ''
        } for remote in repo.remotes]
        
        return jsonify({'success': True, 'data': remotes_list})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@git_ops_bp.route('/tags')
def tags():
    try:
        repo = get_repo(current_app.config.get('REPO_PATH', '.'))
        if not repo:
            return jsonify({'error': 'Not a git repository'}), 400
        
        tags_list = [{'name': tag.name, 'commit': tag.commit.hexsha[:7]} for tag in repo.tags]
        
        return jsonify({'success': True, 'data': tags_list})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
