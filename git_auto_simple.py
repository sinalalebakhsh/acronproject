import subprocess
import time
import datetime
import os
import sys
import requests
from pathlib import Path

# Configuration
CONFIG = {
    'initial_interval': 60,      # 1 minute in seconds
    'normal_interval': 300,      # 5 minutes in seconds
    'initial_checks': 3,         # Number of initial checks
    'max_retries': 3,            # Maximum retries for failed operations
    'error_log_dir': 'git_auto_errors',
    'timeout': 10,               # Timeout for internet checks in seconds
    'branch': 'main',            # Default branch (change to 'master' if needed)
    'log_file': 'git_auto_log.txt',  # Log file name
    'max_log_lines': 2000,       # Maximum lines in log file
    'log_rotation_size': 1000,   # Keep last 1000 lines when rotating
}

def check_internet_connection():
    """Check internet connection using multiple methods"""
    try:
        # روش ساده‌تر برای ویندوز
        if sys.platform == 'win32':
            result = subprocess.run(['ping', '-n', '1', 'google.com'], 
                                  timeout=CONFIG['timeout'], 
                                  capture_output=True)
        else:
            result = subprocess.run(['ping', '-c', '1', 'google.com'], 
                                  timeout=CONFIG['timeout'], 
                                  capture_output=True)
        return result.returncode == 0
    except:
        return False

def get_django_changes():
    """Check Django project changes and generate appropriate message"""
    try:
        # Get git status
        status_result = subprocess.run(['git', 'status', '--porcelain'], 
                                      capture_output=True, 
                                      text=True)
        
        if not status_result.stdout.strip():
            return "No changes found"
        
        changes = status_result.stdout.strip().split('\n')
        
        # Analyze changes
        added = []
        modified = []
        deleted = []
        
        for change in changes:
            status = change[:2].strip()
            file_path = change[3:]
            
            if status == 'A' or status == '??':
                added.append(file_path)
            elif status == 'M':
                modified.append(file_path)
            elif status == 'D':
                deleted.append(file_path)
        
        # Generate commit message
        commit_message = "Django project changes:\n\n"
        
        if added:
            commit_message += "Added files:\n"
            for file in added[:5]:
                commit_message += f"- {file}\n"
            if len(added) > 5:
                commit_message += f"... and {len(added) - 5} more files\n"
            commit_message += "\n"
        
        if modified:
            commit_message += "Modified files:\n"
            for file in modified[:5]:
                commit_message += f"- {file}\n"
            if len(modified) > 5:
                commit_message += f"... and {len(modified) - 5} more files\n"
            commit_message += "\n"
        
        if deleted:
            commit_message += "Deleted files:\n"
            for file in deleted[:5]:
                commit_message += f"- {file}\n"
            if len(deleted) > 5:
                commit_message += f"... and {len(deleted) - 5} more files\n"
        
        return commit_message.strip()
        
    except Exception as e:
        return f"Error checking changes: {str(e)}"

def rotate_log_file_if_needed():
    """Rotate log file if it exceeds maximum lines"""
    log_file = CONFIG['log_file']
    
    if not os.path.exists(log_file):
        return
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        total_lines = len(lines)
        
        if total_lines >= CONFIG['max_log_lines']:
            print(f"⚠ Log file has {total_lines} lines (max: {CONFIG['max_log_lines']}). Rotating...")
            
            keep_lines = CONFIG['log_rotation_size']
            if keep_lines < total_lines:
                lines_to_keep = lines[-keep_lines:]
                
                with open(log_file, 'w', encoding='utf-8') as f:
                    f.writelines(lines_to_keep)
                
                print(f"✓ Log file rotated. Kept last {keep_lines} lines.")
                
                rotation_marker = [
                    f"\n{'='*80}\n",
                    f"LOG FILE ROTATED\n",
                    f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
                    f"Previous size: {total_lines} lines\n",
                    f"New size: {len(lines_to_keep)} lines\n",
                    f"Rotation threshold: {CONFIG['max_log_lines']} lines\n",
                    f"{'='*80}\n\n"
                ]
                
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.writelines(rotation_marker)
    
    except Exception as e:
        print(f"✗ Error rotating log file: {str(e)}")

def save_to_log_file(message, separator="="*60):
    """Save message to log file with timestamp and auto-rotation"""
    try:
        rotate_log_file_if_needed()
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(CONFIG['log_file'], 'a', encoding='utf-8') as f:
            f.write(f"\n{separator}\n")
            f.write(f"[{timestamp}]\n")
            f.write(f"{separator}\n")
            f.write(f"{message}\n")
        
        print(f"✓ Log saved to {CONFIG['log_file']}")
            
    except Exception as e:
        print(f"✗ Error saving to log file: {str(e)}")

def save_error_to_file(error_message):
    """Save error to txt file"""
    error_dir = CONFIG['error_log_dir']
    os.makedirs(error_dir, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{error_dir}/error_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Error time: {datetime.datetime.now()}\n")
        f.write(f"Error: {error_message}\n")
        f.write(f"Config: {CONFIG}\n")
        f.write(f"Platform: {sys.platform}\n")
    
    print(f"Error saved to file: {filename}")
    
    save_to_log_file(f"ERROR: {error_message}")

def get_git_info():
    """Get comprehensive git information"""
    git_info = {}
    
    try:
        branch_result = subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True,
            text=True
        )
        git_info['branch'] = branch_result.stdout.strip()
        
        remote_result = subprocess.run(
            ['git', 'remote', '-v'],
            capture_output=True,
            text=True
        )
        git_info['remote'] = remote_result.stdout.strip()
        
        log_result = subprocess.run(
            ['git', 'log', '--oneline', '-5'],
            capture_output=True,
            text=True
        )
        git_info['recent_commits'] = log_result.stdout.strip()
        
        user_name = subprocess.run(
            ['git', 'config', 'user.name'],
            capture_output=True,
            text=True
        ).stdout.strip()
        
        user_email = subprocess.run(
            ['git', 'config', 'user.email'],
            capture_output=True,
            text=True
        ).stdout.strip()
        
        git_info['user'] = f"{user_name} <{user_email}>"
        
        return git_info
        
    except Exception as e:
        git_info['error'] = f"Error getting git info: {str(e)}"
        return git_info

def run_git_commands():
    """Execute git commands immediately"""
    try:
        current_time = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")
        full_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_content = []
        log_content.append(f"IMMEDIATE GIT OPERATION STARTED")
        log_content.append(f"Time: {full_timestamp}")
        log_content.append("")
        
        changes_message = get_django_changes()
        
        if changes_message == "No changes found":
            message = f"{current_time} - No changes to commit"
            print(message)
            log_content.append(message)
            save_to_log_file("\n".join(log_content))
            return True
        
        log_content.append("1. GIT ADD")
        log_content.append("-" * 40)
        
        print("\n1. Running git add ...")
        add_result = subprocess.run(['git', 'add', '.'], 
                                   capture_output=True, 
                                   text=True)
        
        if add_result.returncode != 0:
            raise Exception(f"Error in git add: {add_result.stderr}")
        
        log_content.append(f"✓ git add completed")
        log_content.append(f"Output: {add_result.stdout.strip()}")
        log_content.append("")
        print("   ✓ git add completed")
        
        log_content.append("2. GIT COMMIT")
        log_content.append("-" * 40)
        
        commit_msg = f"{current_time}\n{changes_message}"
        
        print("\n2. Running git commit ...")
        commit_result = subprocess.run(['git', 'commit', '-m', commit_msg], 
                                      capture_output=True, 
                                      text=True)
        
        if commit_result.returncode != 0:
            raise Exception(f"Error in git commit: {commit_result.stderr}")
        
        commit_hash = subprocess.run(
            ['git', 'rev-parse', '--short', 'HEAD'],
            capture_output=True,
            text=True
        ).stdout.strip()
        
        log_content.append(f"✓ git commit completed")
        log_content.append(f"Commit Hash: {commit_hash}")
        log_content.append(f"Commit Message:\n{commit_msg}")
        log_content.append(f"Output: {commit_result.stdout.strip()}")
        log_content.append("")
        print(f"   ✓ git commit completed (commit: {commit_hash})")
        
        log_content.append("3. GIT PUSH")
        log_content.append("-" * 40)
        
        print(f"\n3. Running git push to {CONFIG['branch']} branch...")
        push_result = subprocess.run(['git', 'push', '-u', 'origin', CONFIG['branch']], 
                                    capture_output=True, 
                                    text=True)
        
        if push_result.returncode != 0:
            raise Exception(f"Error in git push: {push_result.stderr}")
        
        log_content.append(f"✓ git push completed")
        log_content.append(f"Branch: {CONFIG['branch']}")
        log_content.append(f"Output: {push_result.stdout.strip()}")
        log_content.append("")
        print(f"   ✓ git push completed")
        
        log_content.append("4. GIT INFORMATION")
        log_content.append("-" * 40)
        
        git_info = get_git_info()
        
        if 'error' in git_info:
            log_content.append(f"Error getting git info: {git_info['error']}")
        else:
            log_content.append(f"Current Branch: {git_info.get('branch', 'N/A')}")
            log_content.append(f"Git User: {git_info.get('user', 'N/A')}")
            log_content.append("")
            log_content.append("Remote URLs:")
            log_content.append(git_info.get('remote', 'N/A'))
            log_content.append("")
            log_content.append("Recent Commits (last 5):")
            log_content.append(git_info.get('recent_commits', 'N/A'))
        
        log_content.append("")
        log_content.append("OPERATION COMPLETED SUCCESSFULLY")
        log_content.append(f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        log_content.append(f"Commit: {commit_hash}")
        
        save_to_log_file("\n".join(log_content))
        
        print(f"\n{current_time} - Operation completed successfully")
        print(f"Commit: {commit_hash}")
        print(f"Message preview: {commit_msg[:100]}...")
        print(f"✓ All logs saved to {CONFIG['log_file']}")
        
        return True
        
    except Exception as e:
        error_msg = f"Error executing git commands: {str(e)}"
        print(f"\n✗ {error_msg}")
        
        error_log = [
            f"GIT OPERATION FAILED",
            f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Error: {error_msg}",
            "",
            "Last Git Status:",
            get_django_changes()
        ]
        save_to_log_file("\n".join(error_log))
        
        save_error_to_file(error_msg)
        return False

def main():
    """Main function - Immediate execution only"""
    print("=== Immediate Git Auto Push Script ===\n")
    print(f"Configuration:")
    print(f"  - Target branch: {CONFIG['branch']}")
    print(f"  - Log file: {CONFIG['log_file']}")
    print(f"  - Max log lines: {CONFIG['max_log_lines']}")
    
    # Check log file status
    log_file = CONFIG['log_file']
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            print(f"  - Current log lines: {len(lines)}")
        except:
            pass
    
    try:
        rotate_log_file_if_needed()
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"IMMEDIATE GIT PUSH STARTED\n")
            f.write(f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Script: push.sh trigger\n")
            f.write(f"{'='*80}\n")
        print(f"✓ Log file initialized: {log_file}")
    except Exception as e:
        print(f"✗ Error initializing log file: {str(e)}")
    
    # Check internet
    print("\nChecking internet connection...")
    if check_internet_connection():
        print("✓ Internet connection: CONNECTED")
        
        # Execute git commands immediately
        success = run_git_commands()
        
        if success:
            print("\n✅ Git operations completed successfully!")
        else:
            print("\n❌ Git operations failed. Check error logs.")
            return 1
    else:
        print("✗ Internet connection: DISCONNECTED")
        print("❌ Cannot proceed without internet connection.")
        return 1
    
    return 0

if __name__ == "__main__":
    # Check if git exists in project
    if not os.path.exists(".git"):
        print("Error: Git directory not found! Please run in Django project directory.")
        sys.exit(1)
    
    # Check git configuration
    try:
        branch_result = subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True,
            text=True
        )
        if branch_result.stdout.strip():
            CONFIG['branch'] = branch_result.stdout.strip()
    except:
        pass
    
    sys.exit(main())

