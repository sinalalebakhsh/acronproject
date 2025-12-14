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
    'force_run_file': 'force_git_run.flag',  # File to trigger immediate run
}

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
                                  capture_output=True)
        # For Linux/Mac
        else:
            result = subprocess.run(['ping', '-c', '1', '8.8.8.8'], 
                                  timeout=CONFIG['timeout'], 
                                  capture_output=True)
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
                                  capture_output=True)
        # For Linux/Mac
        else:
            result = subprocess.run(['ping', '-c', '1', '1.1.1.1'], 
                                  timeout=CONFIG['timeout'], 
                                  capture_output=True)
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
                                  capture_output=True)
        # For Linux/Mac
        else:
            result = subprocess.run(['nslookup', 'google.com'], 
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

def check_force_run_flag():
    """Check if force run flag file exists"""
    flag_file = CONFIG['force_run_file']
    if os.path.exists(flag_file):
        try:
            with open(flag_file, 'r') as f:
                content = f.read().strip()
            
            # Remove the flag file after reading
            os.remove(flag_file)
            print(f"\n🚨 FORCE RUN FLAG DETECTED! Triggering immediate git operation...")
            return True
        except:
            return False
    return False

def create_force_run_flag():
    """Create a force run flag file (can be called from another script or manually)"""
    flag_file = CONFIG['force_run_file']
    try:
        with open(flag_file, 'w') as f:
            f.write(f"Force run requested at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"✓ Force run flag created: {flag_file}")
        print("The script will execute git operations immediately on next check.")
        return True
    except Exception as e:
        print(f"✗ Error creating force run flag: {str(e)}")
        return False

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
        
        status_result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True
        )
        git_info['status'] = status_result.stdout.strip()
        
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
        
        count_result = subprocess.run(
            ['git', 'rev-list', '--count', 'HEAD'],
            capture_output=True,
            text=True
        )
        git_info['total_commits'] = count_result.stdout.strip()
        
        return git_info
        
    except Exception as e:
        git_info['error'] = f"Error getting git info: {str(e)}"
        return git_info

def verify_git_push():
    """Verify that push was successful by checking local vs remote"""
    try:
        local_commit = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            capture_output=True,
            text=True
        ).stdout.strip()
        
        remote_commit = subprocess.run(
            ['git', 'ls-remote', 'origin', f'refs/heads/{CONFIG["branch"]}'],
            capture_output=True,
            text=True
        ).stdout.split()[0].strip()
        
        local_msg = subprocess.run(
            ['git', 'log', '--oneline', '-1'],
            capture_output=True,
            text=True
        ).stdout.strip()
        
        print(f"\nPush Verification:")
        print(f"  Local commit:  {local_commit[:8]}... - {local_msg}")
        print(f"  Remote commit: {remote_commit[:8]}...")
        
        if local_commit == remote_commit:
            print(f"  ✓ Push verified: Local and remote are synchronized")
            return True, local_commit, remote_commit, local_msg
        else:
            print(f"  ⚠ Warning: Local and remote differ")
            return False, local_commit, remote_commit, local_msg
            
    except Exception as e:
        print(f"  ✗ Could not verify push: {str(e)}")
        return False, None, None, str(e)

def run_git_commands(force_run=False):
    """Execute git commands with verification and logging"""
    try:
        current_time = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")
        full_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_content = []
        if force_run:
            log_content.append(f"🚨 FORCE GIT OPERATION STARTED (Manual Trigger)")
        else:
            log_content.append(f"GIT AUTO OPERATION STARTED")
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
        
        commit_full_hash = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            capture_output=True,
            text=True
        ).stdout.strip()
        
        log_content.append(f"✓ git commit completed")
        log_content.append(f"Commit Hash: {commit_hash} ({commit_full_hash})")
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
        
        log_content.append("4. PUSH VERIFICATION")
        log_content.append("-" * 40)
        
        print("\n4. Verifying push...")
        time.sleep(2)
        push_verified, local_commit, remote_commit, local_msg = verify_git_push()
        
        if push_verified:
            log_content.append("✓ Push verified successfully")
        else:
            log_content.append("⚠ Push verification warning")
        
        if local_commit and remote_commit:
            log_content.append(f"Local Commit:  {local_commit}")
            log_content.append(f"Remote Commit: {remote_commit}")
            log_content.append(f"Match: {'Yes' if local_commit == remote_commit else 'No'}")
        
        log_content.append("")
        
        log_content.append("5. GIT INFORMATION SUMMARY")
        log_content.append("-" * 40)
        
        git_info = get_git_info()
        
        if 'error' in git_info:
            log_content.append(f"Error getting git info: {git_info['error']}")
        else:
            log_content.append(f"Current Branch: {git_info.get('branch', 'N/A')}")
            log_content.append(f"Git User: {git_info.get('user', 'N/A')}")
            log_content.append(f"Total Commits: {git_info.get('total_commits', 'N/A')}")
            log_content.append("")
            log_content.append("Remote URLs:")
            log_content.append(git_info.get('remote', 'N/A'))
            log_content.append("")
            log_content.append("Recent Commits (last 5):")
            log_content.append(git_info.get('recent_commits', 'N/A'))
            log_content.append("")
            log_content.append("Current Status:")
            log_content.append(git_info.get('status', 'N/A') if git_info.get('status') else "Clean working directory")
        
        log_content.append("")
        if force_run:
            log_content.append("🚨 FORCE OPERATION COMPLETED SUCCESSFULLY")
        else:
            log_content.append("OPERATION COMPLETED SUCCESSFULLY")
        log_content.append(f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        log_content.append(f"Commit: {commit_hash}")
        
        save_to_log_file("\n".join(log_content))
        
        print(f"\n{current_time} - Operation completed successfully")
        if force_run:
            print(f"🚨 FORCE RUN - Manual trigger executed")
        print(f"Commit: {commit_hash}")
        print(f"Message preview: {commit_msg[:100]}...")
        print(f"Push verified: {'Yes' if push_verified else 'Needs attention'}")
        print(f"✓ All logs saved to {CONFIG['log_file']}")
        
        return True
        
    except Exception as e:
        error_msg = f"Error executing git commands: {str(e)}"
        print(f"\n✗ {error_msg}")
        
        error_log = [
            f"GIT AUTO OPERATION FAILED",
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

def print_git_info():
    """Print git information for debugging"""
    try:
        print("\nGit Information:")
        
        branch_result = subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True,
            text=True
        )
        current_branch = branch_result.stdout.strip()
        print(f"  Current branch: {current_branch}")
        
        remote_result = subprocess.run(
            ['git', 'remote', '-v'],
            capture_output=True,
            text=True
        )
        print(f"  Remote URLs:")
        for line in remote_result.stdout.strip().split('\n'):
            if line:
                print(f"    {line}")
        
        log_result = subprocess.run(
            ['git', 'log', '--oneline', '-3'],
            capture_output=True,
            text=True
        )
        print(f"  Recent commits:")
        for line in log_result.stdout.strip().split('\n'):
            if line:
                print(f"    {line}")
                
    except Exception as e:
        print(f"  Could not retrieve git info: {str(e)}")

def check_log_file_status():
    """Check and report log file status"""
    log_file = CONFIG['log_file']
    
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            line_count = len(lines)
            file_size = os.path.getsize(log_file) / 1024
            
            print(f"\nLog File Status:")
            print(f"  File: {log_file}")
            print(f"  Lines: {line_count} / {CONFIG['max_log_lines']}")
            print(f"  Size: {file_size:.2f} KB")
            
            if line_count >= CONFIG['max_log_lines'] * 0.8:
                print(f"  ⚠ Warning: Log file is {line_count/CONFIG['max_log_lines']*100:.1f}% full")
            
        except Exception as e:
            print(f"  Could not check log file: {str(e)}")

def main():
    """Main function"""
    print("=== Automatic Git Script for Django Project ===\n")
    print(f"Configuration:")
    print(f"  - First {CONFIG['initial_checks']} checks: every {CONFIG['initial_interval']} seconds")
    print(f"  - After that: every {CONFIG['normal_interval']} seconds")
    print(f"  - Max retries: {CONFIG['max_retries']}")
    print(f"  - Timeout: {CONFIG['timeout']} seconds")
    print(f"  - Target branch: {CONFIG['branch']}")
    print(f"  - Log file: {CONFIG['log_file']}")
    print(f"  - Max log lines: {CONFIG['max_log_lines']}")
    print(f"  - Force run flag file: {CONFIG['force_run_file']}")
    print(f"\n💡 To trigger immediate git operation, create file: {CONFIG['force_run_file']}")
    print(f"   You can use: 'python -c \"import sys; sys.path.insert(0, '.'); from git_auto import create_force_run_flag; create_force_run_flag()\"'")
    
    check_log_file_status()
    
    try:
        rotate_log_file_if_needed()
        
        with open(CONFIG['log_file'], 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"GIT AUTO SCRIPT STARTED\n")
            f.write(f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Configuration: {CONFIG}\n")
            f.write(f"Force run file: {CONFIG['force_run_file']}\n")
            f.write(f"{'='*80}\n")
        print(f"✓ Log file initialized: {CONFIG['log_file']}")
    except Exception as e:
        print(f"✗ Error initializing log file: {str(e)}")
    
    print_git_info()
    
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
            
            interval, interval_type = get_interval_info(check_count)
            
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n{'='*60}")
            print(f"[{current_time}] Check #{check_count} (interval: {interval_type})")
            print(f"{'='*60}")
            
            # Check for force run flag FIRST
            force_run = check_force_run_flag()
            
            # Check internet
            print("Checking internet connection...")
            has_internet = check_internet_connection()
            
            if has_internet:
                print("\nInternet connection: ✓ CONNECTED")
                
                if not last_internet_status and pending_operations:
                    print("Internet connected! Executing pending operations...")
                    pending_operations = False
                
                # Execute git commands (force run or normal)
                if force_run or (not pending_operations and has_internet):
                    success = run_git_commands(force_run=force_run)
                    
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
                        failed_operations_count = 0
                
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
                
                # If force run was requested but no internet, keep it pending
                if force_run:
                    print("⚠ Force run requested but no internet. Will execute when internet is available.")
                    pending_operations = True
                
                if last_internet_status:
                    print("Internet disconnected, suspending operations...")
                    pending_operations = True
                
                last_internet_status = False
            
            # Status summary
            print(f"\n{'─'*40}")
            print(f"Status Summary:")
            print(f"{'─'*40}")
            print(f"  Total checks: {check_count}")
            if check_count <= CONFIG['initial_checks']:
                print(f"  Phase: Initial ({CONFIG['initial_checks'] - check_count} remaining)")
            else:
                print(f"  Phase: Normal")
            print(f"  Internet: {'Connected' if has_internet else 'Disconnected'}")
            print(f"  Pending ops: {'Yes' if pending_operations else 'No'}")
            print(f"  Failed attempts: {failed_operations_count}")
            print(f"  Force run triggered: {'Yes' if force_run else 'No'}")
            print(f"  Next check: {interval_type}")
            
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
            print(f"Last check time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Final internet status: {'Connected' if last_internet_status else 'Disconnected'}")
            print(f"Pending operations: {'Yes' if pending_operations else 'No'}")
            
            check_log_file_status()
            
            shutdown_log = [
                f"SCRIPT STOPPED BY USER",
                f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                f"Total checks performed: {check_count}",
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
            
            error_log = [
                f"UNEXPECTED ERROR IN MAIN LOOP",
                f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                f"Error: {error_msg}",
                f"Check count: {check_count}"
            ]
            save_to_log_file("\n".join(error_log))
            
            save_error_to_file(error_msg)
            
            interval, _ = get_interval_info(check_count)
            print(f"Waiting {interval} seconds before retry...")
            time.sleep(interval)

if __name__ == "__main__":
    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--force' or sys.argv[1] == '-f':
            print("🚨 Force run triggered via command line")
            create_force_run_flag()
            print("Flag created. If script is running, it will execute immediately.")
            print("If script is not running, start it and it will detect the flag.")
            sys.exit(0)
        elif sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print("Usage:")
            print("  python git_auto.py                    # Start normally")
            print("  python git_auto.py --force  or -f     # Create force run flag")
            print("  python git_auto.py --help   or -h     # Show this help")
            sys.exit(0)
    
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
            text=True
        )
        if branch_result.stdout.strip():
            CONFIG['branch'] = branch_result.stdout.strip()
    except:
        pass
    
    main()


