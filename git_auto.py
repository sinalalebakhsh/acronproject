import subprocess
import time
import datetime
import os
import sys
import requests
from pathlib import Path

# Optional: For Persian date (install with: pip install jdatetime)
# import jdatetime

# def get_persian_date():
#     """Get Persian (Shamsi) date and time"""
#     now = jdatetime.datetime.now()
#     return now.strftime("%y.%m.%d %H:%M:%S")

# Configuration
CONFIG = {
    'initial_interval': 60,      # 1 minute in seconds
    'normal_interval': 300,      # 5 minutes in seconds
    'initial_checks': 3,         # Number of initial checks
    'max_retries': 3,            # Maximum retries for failed operations
    'error_log_dir': 'git_auto_errors',
    'timeout': 10,               # Timeout for internet checks in seconds
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

def run_git_commands():
    """Execute git commands"""
    try:
        # Date and time
        current_time = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")
        
        # Check for changes
        changes_message = get_django_changes()
        
        if changes_message == "No changes found":
            print(f"{current_time} - No changes to commit")
            return True
        
        # git add .
        print("Running git add ...")
        add_result = subprocess.run(['git', 'add', '.'], 
                                   capture_output=True, 
                                   text=True)
        
        if add_result.returncode != 0:
            raise Exception(f"Error in git add: {add_result.stderr}")
        
        # Create commit message
        commit_msg = f"{current_time}\n{changes_message}"
        
        # git commit
        print("Running git commit ...")
        commit_result = subprocess.run(['git', 'commit', '-m', commit_msg], 
                                      capture_output=True, 
                                      text=True)
        
        if commit_result.returncode != 0:
            raise Exception(f"Error in git commit: {commit_result.stderr}")
        
        # git push
        print("Running git push ...")
        push_result = subprocess.run(['git', 'push', '-u', 'origin'], 
                                    capture_output=True, 
                                    text=True)
        
        if push_result.returncode != 0:
            raise Exception(f"Error in git push: {push_result.stderr}")
        
        print(f"{current_time} - Operation completed successfully")
        print(f"Commit message:\n{commit_msg}")
        return True
        
    except Exception as e:
        error_msg = f"Error executing git commands: {str(e)}"
        print(error_msg)
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

def print_network_info():
    """Print network information for debugging"""
    print("\nNetwork Information:")
    print(f"Platform: {sys.platform}")
    
    # Try to get IP configuration
    try:
        if sys.platform == 'win32':
            ipconfig = subprocess.run(['ipconfig'], capture_output=True, text=True)
            print("IP Config (first 10 lines):")
            for line in ipconfig.stdout.split('\n')[:10]:
                print(f"  {line}")
        else:
            ifconfig = subprocess.run(['ifconfig'], capture_output=True, text=True)
            if ifconfig.returncode != 0:
                ifconfig = subprocess.run(['ip', 'addr'], capture_output=True, text=True)
            print("Network Config (first 10 lines):")
            for line in ifconfig.stdout.split('\n')[:10]:
                print(f"  {line}")
    except:
        print("  Could not retrieve network configuration")

def test_internet_methods():
    """Test all internet checking methods"""
    print("\nTesting internet connection methods:")
    
    methods = [
        ("Requests", check_via_requests),
        ("Ping Google", check_via_ping_google),
        ("Ping Cloudflare", check_via_ping_cloudflare),
        ("NSLookup", check_via_nslookup),
    ]
    
    results = []
    for name, method in methods:
        try:
            result = method()
            status = "✓" if result else "✗"
            results.append(f"{name}: {status}")
            print(f"  {name}: {status}")
        except Exception as e:
            results.append(f"{name}: Error - {str(e)}")
            print(f"  {name}: Error - {str(e)}")
    
    return results

def main():
    """Main function"""
    print("=== Automatic Git Script for Django Project ===\n")
    print(f"Configuration:")
    print(f"  - First {CONFIG['initial_checks']} checks: every {CONFIG['initial_interval']} seconds")
    print(f"  - After that: every {CONFIG['normal_interval']} seconds")
    print(f"  - Max retries: {CONFIG['max_retries']}")
    print(f"  - Timeout: {CONFIG['timeout']} seconds")
    
    # Print network info for debugging
    print_network_info()
    
    # Test internet methods
    test_results = test_internet_methods()
    
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
            print(f"\n{'='*50}")
            print(f"[{current_time}] Check #{check_count} (interval: {interval_type})")
            print(f"{'='*50}")
            
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
                        print(f"Maximum retries ({CONFIG['max_retries']}) reached. Suspending operations.")
                        pending_operations = False
                        failed_operations_count = 0
                    else:
                        pending_operations = True
                        print(f"Operation failed (attempt {failed_operations_count}/{CONFIG['max_retries']})")
                else:
                    failed_operations_count = 0  # Reset on success
                
                last_internet_status = True
                
            else:
                print("\nInternet connection: ✗ DISCONNECTED")
                print("All connection methods failed.")
                
                # If internet is down and was previously down, suspend operations
                if last_internet_status:
                    print("Internet disconnected, suspending operations...")
                    pending_operations = True
                
                last_internet_status = False
            
            # Status summary
            print(f"\nStatus Summary:")
            print(f"  - Total checks: {check_count}")
            if check_count <= CONFIG['initial_checks']:
                print(f"  - Initial phase: {CONFIG['initial_checks'] - check_count} checks remaining")
            else:
                print(f"  - Normal phase active")
            print(f"  - Internet status: {'Connected' if has_internet else 'Disconnected'}")
            print(f"  - Pending operations: {'Yes' if pending_operations else 'No'}")
            print(f"  - Next check in: {interval_type}")
            
            # Wait for next check
            print(f"\nWaiting {interval} seconds for next check...")
            time.sleep(interval)
            
        except KeyboardInterrupt:
            print(f"\n\n{'='*50}")
            print("Script stopped by user.")
            print(f"Total checks performed: {check_count}")
            print(f"Last check time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Final internet status: {'Connected' if last_internet_status else 'Disconnected'}")
            print(f"{'='*50}")
            break
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(f"\nError: {error_msg}")
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
    
    main()


    