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
    'version_file': '.git_auto_version',  # File to store current version
}

# Version management
CURRENT_VERSION = "1.1.3"  # Starting version

def load_version():
    """Load current version from file or use default"""
    global CURRENT_VERSION
    version_file = CONFIG['version_file']
    
    if os.path.exists(version_file):
        try:
            with open(version_file, 'r') as f:
                version = f.read().strip()
                if version:
                    CURRENT_VERSION = version
                    print(f"📦 Loaded version: {CURRENT_VERSION}")
                else:
                    print(f"⚠ Version file empty, using default: {CURRENT_VERSION}")
        except Exception as e:
            print(f"⚠ Error loading version file: {str(e)}")
            print(f"  Using default version: {CURRENT_VERSION}")
    else:
        print(f"📦 Version file not found, starting with: {CURRENT_VERSION}")
    
    return CURRENT_VERSION

def save_version(version):
    """Save version to file"""
    try:
        with open(CONFIG['version_file'], 'w') as f:
            f.write(version)
        print(f"💾 Version saved: {version}")
        return True
    except Exception as e:
        print(f"✗ Error saving version: {str(e)}")
        return False

def increment_version(current_version):
    """
    Increment version according to semantic versioning rules:
    1.1.3 -> 1.1.4 -> ... -> 1.1.99 -> 1.2.0 -> ... -> 1.99.0 -> 2.0.0
    """
    try:
        # Split version into parts
        parts = current_version.split('.')
        if len(parts) != 3:
            print(f"⚠ Invalid version format: {current_version}, using default increment")
            return "1.1.4"
        
        major = int(parts[0])
        minor = int(parts[1])
        patch = int(parts[2])
        
        # Increment logic
        if patch < 99:
            # Increment patch: 1.1.3 -> 1.1.4
            patch += 1
        elif minor < 99:
            # Increment minor, reset patch: 1.1.99 -> 1.2.0
            minor += 1
            patch = 0
        else:
            # Increment major, reset minor and patch: 1.99.99 -> 2.0.0
            major += 1
            minor = 0
            patch = 0
        
        new_version = f"{major}.{minor}.{patch}"
        print(f"🔄 Version incremented: {current_version} -> {new_version}")
        return new_version
        
    except ValueError as e:
        print(f"✗ Error parsing version {current_version}: {str(e)}")
        # Fallback: simple increment
        return "1.1.4"

def check_internet_connection():
    """Check internet connection using multiple methods"""
    methods = [
        check_via_requests,
        check_via_ping_google,
        check_via_ping_cloudflare,
        check_via_nslookup,
    ]
    
    for method in methods:
        try:
            if method():
                print(f"✓ Internet detected via {method.__name__}")
                return True
        except Exception as e:
            continue
    
    return False

def check_via_requests():
    """Check internet using requests to multiple reliable sites"""
    sites = [
        'https://www.google.com',
        'https://www.cloudflare.com',
        'https://www.github.com',
        'https://1.1.1.1',  # Cloudflare DNS
    ]
    
    for site in sites:
        try:
            response = requests.get(site, timeout=CONFIG['timeout'])
            if response.status_code < 500:  # Any successful or client error means connection
                return True
        except:
            continue
    
    return False

def check_via_ping_google():
    """Check internet via ping to Google DNS"""
    try:
        # For Windows
        if sys.platform == 'win32':
            result = subprocess.run(['ping', '-n', '1', '8.8.8.8'], 
                                  timeout=CONFIG['timeout'], 
                                  capture_output=True,
                                  encoding='utf-8',
                                  errors='ignore')
        # For Linux/Mac
        else:
            result = subprocess.run(['ping', '-c', '1', '8.8.8.8'], 
                                  timeout=CONFIG['timeout'], 
                                  capture_output=True,
                                  encoding='utf-8',
                                  errors='ignore')
        return result.returncode == 0
    except:
        return False

def check_via_ping_cloudflare():
    """Check internet via ping to Cloudflare DNS"""
    try:
        # For Windows
        if sys.platform == 'win32':
            result = subprocess.run(['ping', '-n', '1', '1.1.1.1'], 
                                  timeout=CONFIG['timeout'], 
                                  capture_output=True,
                                  encoding='utf-8',
                                  errors='ignore')
        # For Linux/Mac
        else:
            result = subprocess.run(['ping', '-c', '1', '1.1.1.1'], 
                                  timeout=CONFIG['timeout'], 
                                  capture_output=True,
                                  encoding='utf-8',
                                  errors='ignore')
        return result.returncode == 0
    except:
        return False

def check_via_nslookup():
    """Check internet via nslookup"""
    try:
        # For Windows
        if sys.platform == 'win32':
            result = subprocess.run(['nslookup', 'google.com'], 
                                  timeout=CONFIG['timeout'], 
                                  capture_output=True,
                                  encoding='utf-8',
                                  errors='ignore')
        # For Linux/Mac
        else:
            result = subprocess.run(['nslookup', 'google.com'], 
                                  timeout=CONFIG['timeout'], 
                                  capture_output=True,
                                  encoding='utf-8',
                                  errors='ignore')
        return result.returncode == 0
    except:
        return False

def get_django_changes():
    """Check Django project changes and generate appropriate message"""
    try:
        # Get git status with proper encoding
        status_result = subprocess.run(['git', 'status', '--porcelain'], 
                                      capture_output=True, 
                                      text=True,
                                      encoding='utf-8',
                                      errors='ignore')
        
        if not status_result.stdout.strip():
            return "No changes found"
        
        changes = status_result.stdout.strip().split('\n')
        
        # Analyze changes
        added = []
        modified = []
        deleted = []
        
        for change in changes:
            if not change.strip():
                continue
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
            for file in added[:5]:  # Only first 5 files
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
    
    # If log file doesn't exist yet, no need to rotate
    if not os.path.exists(log_file):
        return
    
    try:
        # Count lines in current log file
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        total_lines = len(lines)
        
        # Check if we need to rotate
        if total_lines >= CONFIG['max_log_lines']:
            print(f"⚠ Log file has {total_lines} lines (max: {CONFIG['max_log_lines']}). Rotating...")
            
            # Keep only the last N lines
            keep_lines = CONFIG['log_rotation_size']
            if keep_lines < total_lines:
                lines_to_keep = lines[-keep_lines:]
                
                # Write rotated log
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
            else:
                print(f"Log file has {total_lines} lines, no rotation needed.")
    
    except Exception as e:
        print(f"✗ Error rotating log file: {str(e)}")

def save_to_log_file(message, separator="="*60):
    """Save message to log file with timestamp and auto-rotation"""
    try:
        # Rotate log file if needed BEFORE adding new content
        rotate_log_file_if_needed()
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(CONFIG['log_file'], 'a', encoding='utf-8') as f:
            f.write(f"\n{separator}\n")
            f.write(f"[{timestamp}]\n")
            f.write(f"{separator}\n")
            f.write(f"{message}\n")
        
        print(f"✓ Log saved to {CONFIG['log_file']}")
        
        # Check current log size after writing
        try:
            with open(CONFIG['log_file'], 'r', encoding='utf-8', errors='ignore') as f:
                current_lines = len(f.readlines())
            print(f"  Current log size: {current_lines} lines")
        except:
            pass
            
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
    
    # Also save to main log file
    save_to_log_file(f"ERROR: {error_message}")

def run_git_command_safe(cmd, description=""):
    """Run git command safely with proper encoding"""
    try:
        if description:
            print(f"\n{description}...")
        
        result = subprocess.run(cmd, 
                              capture_output=True, 
                              text=True,
                              encoding='utf-8',
                              errors='ignore')
        
        if result.returncode != 0:
            error_msg = result.stderr.strip() if result.stderr else "Unknown error"
            raise Exception(f"Command failed: {' '.join(cmd)} - {error_msg}")
        
        return result.stdout.strip()
    except Exception as e:
        raise Exception(f"Error running git command: {str(e)}")

def get_git_info_safe():
    """Get comprehensive git information safely"""
    git_info = {}
    
    try:
        # Get current branch
        branch = run_git_command_safe(['git', 'branch', '--show-current'], "Getting current branch")
        git_info['branch'] = branch
        
        # Get remote URL
        remote = run_git_command_safe(['git', 'remote', '-v'], "Getting remote URLs")
        git_info['remote'] = remote
        
        # Get last 5 commits
        try:
            log_result = subprocess.run(['git', 'log', '--oneline', '-5'], 
                                       capture_output=True, 
                                       text=True,
                                       encoding='utf-8',
                                       errors='ignore')
            git_info['recent_commits'] = log_result.stdout.strip() if log_result.stdout else "No commits yet"
        except:
            git_info['recent_commits'] = "Could not retrieve commits"
        
        # Get git config user info
        try:
            user_name = run_git_command_safe(['git', 'config', 'user.name'], "Getting git user name")
            user_email = run_git_command_safe(['git', 'config', 'user.email'], "Getting git user email")
            git_info['user'] = f"{user_name} <{user_email}>"
        except:
            git_info['user'] = "Not configured"
        
        return git_info
        
    except Exception as e:
        git_info['error'] = f"Error getting git info: {str(e)}"
        return git_info

def verify_git_push():
    """Verify that push was successful by checking local vs remote"""
    try:
        # Get latest local commit
        local_commit = run_git_command_safe(['git', 'rev-parse', 'HEAD'], "Getting local commit")
        
        # Get latest remote commit
        try:
            remote_output = run_git_command_safe(['git', 'ls-remote', 'origin', f'refs/heads/{CONFIG["branch"]}'], 
                                                "Getting remote commit")
            if remote_output:
                remote_commit = remote_output.split()[0].strip()
            else:
                remote_commit = None
        except:
            remote_commit = None
        
        # Get commit messages for comparison
        local_msg = run_git_command_safe(['git', 'log', '--oneline', '-1'], "Getting commit message")
        
        print(f"\nPush Verification:")
        if local_commit:
            print(f"  Local commit:  {local_commit[:8]}...")
        if remote_commit:
            print(f"  Remote commit: {remote_commit[:8]}...")
        
        if remote_commit and local_commit == remote_commit:
            print(f"  ✓ Push verified: Local and remote are synchronized")
            return True, local_commit, remote_commit, local_msg
        elif remote_commit:
            print(f"  ⚠ Warning: Local and remote differ")
            return False, local_commit, remote_commit, local_msg
        else:
            print(f"  ℹ Could not verify push (no remote commit)")
            return True, local_commit, None, local_msg
            
    except Exception as e:
        print(f"  ✗ Could not verify push: {str(e)}")
        return False, None, None, str(e)

def run_git_commands():
    """Execute git commands with verification and logging"""
    global CURRENT_VERSION
    
    try:
        current_time = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")
        full_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Start log
        log_content = []
        log_content.append(f"GIT AUTO OPERATION STARTED - Version {CURRENT_VERSION}")
        log_content.append(f"Time: {full_timestamp}")
        log_content.append("")
        
        # Check for changes
        changes_message = get_django_changes()
        
        if changes_message == "No changes found":
            message = f"{current_time} - No changes to commit"
            print(message)
            log_content.append(message)
            save_to_log_file("\n".join(log_content))
            return True
        
        log_content.append("1. GIT ADD")
        log_content.append("-" * 40)
        
        # git add .
        print("\n1. Running git add ...")
        add_result = subprocess.run(['git', 'add', '.'], 
                                   capture_output=True, 
                                   text=True,
                                   encoding='utf-8',
                                   errors='ignore')
        
        if add_result.returncode != 0:
            raise Exception(f"Error in git add: {add_result.stderr}")
        
        log_content.append(f"✓ git add completed")
        if add_result.stdout.strip():
            log_content.append(f"Output: {add_result.stdout.strip()}")
        log_content.append("")
        print("   ✓ git add completed")
        
        log_content.append("2. GIT COMMIT")
        log_content.append("-" * 40)
        
        # Increment version before commit
        new_version = increment_version(CURRENT_VERSION)
        
        # Create commit message with version
        commit_msg = f"Version {new_version} - {current_time}\n{changes_message}"
        
        # Update current version
        CURRENT_VERSION = new_version
        save_version(CURRENT_VERSION)
        
        print(f"🎯 Committing as version: {CURRENT_VERSION}")
        
        # git commit
        print("\n2. Running git commit ...")
        commit_result = subprocess.run(['git', 'commit', '-m', commit_msg], 
                                      capture_output=True, 
                                      text=True,
                                      encoding='utf-8',
                                      errors='ignore')
        
        if commit_result.returncode != 0:
            raise Exception(f"Error in git commit: {commit_result.stderr}")
        
        # Get commit hash for reference
        commit_hash = run_git_command_safe(['git', 'rev-parse', '--short', 'HEAD'], "Getting commit hash")
        
        log_content.append(f"✓ git commit completed")
        log_content.append(f"Version: {CURRENT_VERSION}")
        log_content.append(f"Commit Hash: {commit_hash}")
        log_content.append(f"Commit Message:\n{commit_msg}")
        if commit_result.stdout.strip():
            log_content.append(f"Output: {commit_result.stdout.strip()}")
        log_content.append("")
        print(f"   ✓ git commit completed (commit: {commit_hash}, version: {CURRENT_VERSION})")
        
        log_content.append("3. GIT PUSH")
        log_content.append("-" * 40)
        
        print(f"\n3. Running git push to {CONFIG['branch']} branch...")
        push_result = subprocess.run(['git', 'push', '-u', 'origin', CONFIG['branch']], 
                                    capture_output=True, 
                                    text=True,
                                    encoding='utf-8',
                                    errors='ignore')
        
        if push_result.returncode != 0:
            raise Exception(f"Error in git push: {push_result.stderr}")
        
        log_content.append(f"✓ git push completed")
        log_content.append(f"Branch: {CONFIG['branch']}")
        if push_result.stdout.strip():
            log_content.append(f"Output: {push_result.stdout.strip()}")
        log_content.append("")
        print(f"   ✓ git push completed")
        
        log_content.append("4. PUSH VERIFICATION")
        log_content.append("-" * 40)
        
        # Verify push
        print("\n4. Verifying push...")
        time.sleep(2)  # Wait a bit for sync
        push_verified, local_commit, remote_commit, local_msg = verify_git_push()
        
        if push_verified:
            log_content.append("✓ Push verified successfully")
        else:
            log_content.append("⚠ Push verification warning")
        
        if local_commit:
            log_content.append(f"Local Commit:  {local_commit}")
        if remote_commit:
            log_content.append(f"Remote Commit: {remote_commit}")
            log_content.append(f"Match: {'Yes' if local_commit == remote_commit else 'No'}")
        
        log_content.append("")
        
        log_content.append("5. GIT INFORMATION SUMMARY")
        log_content.append("-" * 40)
        
        # Get comprehensive git info
        git_info = get_git_info_safe()
        
        if 'error' in git_info:
            log_content.append(f"Error getting git info: {git_info['error']}")
        else:
            log_content.append(f"Current Branch: {git_info.get('branch', 'N/A')}")
            log_content.append(f"Git User: {git_info.get('user', 'N/A')}")
            log_content.append("")
            if git_info.get('remote'):
                log_content.append("Remote URLs:")
                log_content.append(git_info.get('remote', 'N/A'))
            log_content.append("")
            if git_info.get('recent_commits'):
                log_content.append("Recent Commits (last 5):")
                log_content.append(git_info.get('recent_commits', 'N/A'))
        
        log_content.append("")
        log_content.append("OPERATION COMPLETED SUCCESSFULLY")
        log_content.append(f"Version: {CURRENT_VERSION}")
        log_content.append(f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        log_content.append(f"Commit: {commit_hash}")
        
        # Save all logs to file
        save_to_log_file("\n".join(log_content))
        
        # Print summary to console
        print(f"\n{current_time} - Operation completed successfully")
        print(f"🎯 New Version: {CURRENT_VERSION}")
        print(f"Commit: {commit_hash}")
        print(f"Message preview: {commit_msg[:100]}...")
        print(f"Push verified: {'Yes' if push_verified else 'Needs attention'}")
        print(f"✓ All logs saved to {CONFIG['log_file']}")
        
        return True
        
    except Exception as e:
        error_msg = f"Error executing git commands: {str(e)}"
        print(f"\n✗ {error_msg}")
        
        # Save error to log file too
        error_log = [
            f"GIT AUTO OPERATION FAILED - Version {CURRENT_VERSION}",
            f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Error: {error_msg}",
            "",
            "Last Git Status:",
            get_django_changes()
        ]
        save_to_log_file("\n".join(error_log))
        
        save_error_to_file(error_msg)
        return False

def get_interval_info(check_count):
    """Get interval information based on check count"""
    if check_count <= CONFIG['initial_checks']:
        interval = CONFIG['initial_interval']
        if CONFIG['initial_interval'] == 60:
            interval_type = "1 minute"
        else:
            interval_type = f"{CONFIG['initial_interval']} seconds"
    else:
        interval = CONFIG['normal_interval']
        if CONFIG['normal_interval'] == 60:
            interval_type = "1 minute"
        elif CONFIG['normal_interval'] == 300:
            interval_type = "5 minutes"
        else:
            interval_type = f"{CONFIG['normal_interval']} seconds"
    
    return interval, interval_type

def print_git_info_safe():
    """Print git information for debugging safely"""
    print("\nGit Information:")
    
    try:
        # Get current branch
        branch_result = subprocess.run(['git', 'branch', '--show-current'], 
                                      capture_output=True, 
                                      text=True,
                                      encoding='utf-8',
                                      errors='ignore')
        if branch_result.stdout.strip():
            print(f"  Current branch: {branch_result.stdout.strip()}")
        else:
            print(f"  Current branch: Not available")
        
        # Get remote URL
        remote_result = subprocess.run(['git', 'remote', '-v'], 
                                      capture_output=True, 
                                      text=True,
                                      encoding='utf-8',
                                      errors='ignore')
        if remote_result.stdout.strip():
            print(f"  Remote URLs:")
            for line in remote_result.stdout.strip().split('\n'):
                if line.strip():
                    # Clean the line for display
                    clean_line = line.encode('ascii', 'ignore').decode('ascii', 'ignore')
                    print(f"    {clean_line}")
        
        # Get last few commits (skip if there are encoding issues)
        try:
            log_result = subprocess.run(['git', 'log', '--oneline', '-3'], 
                                       capture_output=True, 
                                       text=True,
                                       encoding='utf-8',
                                       errors='ignore')
            if log_result.stdout.strip():
                print(f"  Recent commits:")
                lines = log_result.stdout.strip().split('\n')
                for i, line in enumerate(lines[:3]):
                    if line.strip():
                        # Clean the line for display
                        clean_line = line.encode('ascii', 'ignore').decode('ascii', 'ignore')
                        print(f"    {clean_line}")
        except:
            print(f"  Recent commits: Could not retrieve")
                
    except Exception as e:
        print(f"  Could not retrieve git info: {str(e)}")

def check_log_file_status():
    """Check and report log file status"""
    log_file = CONFIG['log_file']
    
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            line_count = len(lines)
            file_size = os.path.getsize(log_file) / 1024  # Size in KB
            
            print(f"\nLog File Status:")
            print(f"  File: {log_file}")
            print(f"  Lines: {line_count} / {CONFIG['max_log_lines']}")
            print(f"  Size: {file_size:.2f} KB")
            
            if line_count >= CONFIG['max_log_lines'] * 0.8:
                print(f"  ⚠ Warning: Log file is {line_count/CONFIG['max_log_lines']*100:.1f}% full")
            
            # Show last log entry timestamp if available
            if lines:
                last_lines = lines[-10:]  # Last 10 lines
                for line in reversed(last_lines):
                    if 'Time:' in line:
                        print(f"  Last entry: {line.strip().replace('Time:', '').strip()}")
                        break
            
        except Exception as e:
            print(f"  Could not check log file: {str(e)}")
    else:
        print(f"\nLog File Status: {log_file} does not exist yet.")

def show_version_progression():
    """Show how version progression will work"""
    print("\n📈 Version Progression System:")
    print("="*50)
    print("Starting from: 1.1.3")
    print("\nProgression rules:")
    print("  1.1.3 -> 1.1.4 -> ... -> 1.1.99")
    print("  1.1.99 -> 1.2.0 -> ... -> 1.2.99")
    print("  1.2.99 -> 1.3.0 -> ... -> 1.99.0")
    print("  1.99.0 -> 1.99.1 -> ... -> 1.99.99")
    print("  1.99.99 -> 2.0.0 -> ... -> 2.0.99")
    print("  2.0.99 -> 2.1.0 -> ...")
    print("="*50)

def main():
    """Main function"""
    # Load current version
    global CURRENT_VERSION
    CURRENT_VERSION = load_version()
    
    print("=== Automatic Git Script for Django Project ===\n")
    print(f"🎯 Current Version: {CURRENT_VERSION}")
    print(f"\nConfiguration:")
    print(f"  - First {CONFIG['initial_checks']} checks: every {CONFIG['initial_interval']} seconds")
    print(f"  - After that: every {CONFIG['normal_interval']} seconds")
    print(f"  - Max retries: {CONFIG['max_retries']}")
    print(f"  - Timeout: {CONFIG['timeout']} seconds")
    print(f"  - Target branch: {CONFIG['branch']}")
    print(f"  - Log file: {CONFIG['log_file']}")
    print(f"  - Max log lines: {CONFIG['max_log_lines']}")
    print(f"  - Keep after rotation: {CONFIG['log_rotation_size']} lines")
    print(f"  - Version file: {CONFIG['version_file']}")
    
    # Show version progression
    show_version_progression()
    
    # Check log file status
    check_log_file_status()
    
    # Initialize log file with rotation check
    try:
        rotate_log_file_if_needed()
        
        with open(CONFIG['log_file'], 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"GIT AUTO SCRIPT STARTED - Version {CURRENT_VERSION}\n")
            f.write(f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Configuration: {CONFIG}\n")
            f.write(f"Version progression: Auto-increment on each successful commit\n")
            f.write(f"{'='*80}\n")
        print(f"✓ Log file initialized: {CONFIG['log_file']}")
    except Exception as e:
        print(f"✗ Error initializing log file: {str(e)}")
    
    # Print git info safely
    print_git_info_safe()
    
    # Test internet methods
    print("\nTesting internet connection methods:")
    methods = [
        ("Requests", check_via_requests),
        ("Ping Google", check_via_ping_google),
        ("Ping Cloudflare", check_via_ping_cloudflare),
        ("NSLookup", check_via_nslookup),
    ]
    
    for name, method in methods:
        try:
            result = method()
            status = "✓" if result else "✗"
            print(f"  {name}: {status}")
        except Exception as e:
            print(f"  {name}: Error - {str(e)}")
    
    print("\nStarting main loop...")
    
    last_internet_status = False
    pending_operations = False
    check_count = 0
    failed_operations_count = 0
    
    while True:
        try:
            check_count += 1
            
            # Get interval based on check count
            interval, interval_type = get_interval_info(check_count)
            
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n{'='*60}")
            print(f"[{current_time}] Check #{check_count} (interval: {interval_type})")
            print(f"📦 Current Version: {CURRENT_VERSION}")
            print(f"{'='*60}")
            
            # Check internet with detailed logging
            print("Checking internet connection...")
            has_internet = check_internet_connection()
            
            if has_internet:
                print("\nInternet connection: ✓ CONNECTED")
                
                # If internet was previously down and operations were pending
                if not last_internet_status and pending_operations:
                    print("Internet connected! Executing pending operations...")
                    pending_operations = False
                
                # Execute git commands
                success = run_git_commands()
                
                if not success:
                    failed_operations_count += 1
                    if failed_operations_count >= CONFIG['max_retries']:
                        print(f"\n⚠ Maximum retries ({CONFIG['max_retries']}) reached. Suspending operations.")
                        pending_operations = False
                        failed_operations_count = 0
                    else:
                        pending_operations = True
                        print(f"\n⚠ Operation failed (attempt {failed_operations_count}/{CONFIG['max_retries']})")
                else:
                    failed_operations_count = 0  # Reset on success
                
                last_internet_status = True
                
            else:
                print("\nInternet connection: ✗ DISCONNECTED")
                print("All connection methods failed.")
                
                # Save check without internet to log
                no_internet_log = [
                    f"CHECK #{check_count} - NO INTERNET",
                    f"Time: {current_time}",
                    f"Status: Internet disconnected",
                    f"Pending operations: {'Yes' if pending_operations else 'No'}",
                    f"Next check in: {interval_type}"
                ]
                save_to_log_file("\n".join(no_internet_log), separator="-"*40)
                
                # If internet is down and was previously down, suspend operations
                if last_internet_status:
                    print("Internet disconnected, suspending operations...")
                    pending_operations = True
                
                last_internet_status = False
            
            # Status summary
            print(f"\n{'─'*40}")
            print(f"Status Summary:")
            print(f"{'─'*40}")
            print(f"  Total checks: {check_count}")
            print(f"  Current version: {CURRENT_VERSION}")
            if check_count <= CONFIG['initial_checks']:
                print(f"  Phase: Initial ({CONFIG['initial_checks'] - check_count} remaining)")
            else:
                print(f"  Phase: Normal")
            print(f"  Internet: {'Connected' if has_internet else 'Disconnected'}")
            print(f"  Pending ops: {'Yes' if pending_operations else 'No'}")
            print(f"  Failed attempts: {failed_operations_count}")
            print(f"  Next check: {interval_type}")
            
            # Check log file size periodically (every 10 checks)
            if check_count % 10 == 0:
                check_log_file_status()
            
            print(f"{'─'*40}")
            
            # Wait for next check
            print(f"\n⏰ Waiting {interval} seconds for next check...")
            for i in range(interval, 0, -10):
                if i <= 10:
                    print(f"   {i} seconds remaining...")
                    time.sleep(1)
                else:
                    if i == interval or i % 30 == 0:
                        print(f"   {i} seconds remaining...")
                    time.sleep(10)
            
        except KeyboardInterrupt:
            print(f"\n\n{'='*60}")
            print("🛑 Script stopped by user.")
            print(f"{'='*60}")
            print(f"Total checks performed: {check_count}")
            print(f"Final version: {CURRENT_VERSION}")
            print(f"Last check time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Final internet status: {'Connected' if last_internet_status else 'Disconnected'}")
            print(f"Pending operations: {'Yes' if pending_operations else 'No'}")
            
            # Check final log status
            check_log_file_status()
            
            # Save shutdown info to log
            shutdown_log = [
                f"SCRIPT STOPPED BY USER",
                f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                f"Total checks performed: {check_count}",
                f"Final version: {CURRENT_VERSION}",
                f"Final internet status: {'Connected' if last_internet_status else 'Disconnected'}",
                f"Pending operations: {'Yes' if pending_operations else 'No'}",
                f"Log file: {CONFIG['log_file']}",
                f"Max log lines configured: {CONFIG['max_log_lines']}"
            ]
            save_to_log_file("\n".join(shutdown_log))
            
            break
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(f"\n⚠ Error: {error_msg}")
            
            # Save error to log
            error_log = [
                f"UNEXPECTED ERROR IN MAIN LOOP",
                f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                f"Error: {error_msg}",
                f"Check count: {check_count}",
                f"Current version: {CURRENT_VERSION}"
            ]
            save_to_log_file("\n".join(error_log))
            
            save_error_to_file(error_msg)
            
            # Wait appropriate interval even on error
            interval, _ = get_interval_info(check_count)
            print(f"Waiting {interval} seconds before retry...")
            time.sleep(interval)

if __name__ == "__main__":
    # Check if git exists in project
    if not os.path.exists(".git"):
        print("Error: Git directory not found! Please run in Django project directory.")
        sys.exit(1)
    
    # Check if requests is installed
    try:
        import requests
    except ImportError:
        print("Error: 'requests' library is not installed.")
        print("Please install it using: pip install requests")
        sys.exit(1)
    
    # Check git configuration
    try:
        branch_result = subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        if branch_result.stdout.strip():
            CONFIG['branch'] = branch_result.stdout.strip()
    except:
        pass
    
    main()

    