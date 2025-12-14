#!/usr/bin/env python3
"""
Trigger immediate git operations for the auto git script
"""

import os
import sys
import datetime

def create_force_run_flag():
    """Create a force run flag file"""
    force_file = 'force_git_run.flag'
    
    try:
        with open(force_file, 'w') as f:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"Force run requested at: {timestamp}\n")
            f.write(f"Triggered by: {sys.argv[0]}\n")
        
        print(f"✅ Force run flag created: {force_file}")
        print("📢 The git auto script will execute immediately on next check.")
        print("💡 Make sure the main script is running.")
        
        return True
    except Exception as e:
        print(f"❌ Error creating force run flag: {str(e)}")
        return False

def check_if_script_running():
    """Check if the main git auto script is running"""
    try:
        import psutil
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['cmdline'] and 'git_auto.py' in ' '.join(proc.info['cmdline']):
                    print(f"✅ Main script is running (PID: {proc.info['pid']})")
                    return True
            except:
                continue
        print("⚠️  Main script may not be running. Start it with: python git_auto.py")
        return False
    except ImportError:
        print("ℹ️  Install psutil for better monitoring: pip install psutil")
        return None

if __name__ == "__main__":
    print("🚀 Trigger Immediate Git Operations")
    print("="*40)
    
    # Check if main script might be running
    check_if_script_running()
    
    # Create the flag
    if create_force_run_flag():
        print("\n🎯 Operation triggered successfully!")
        print("\nNext steps:")
        print("1. The flag file 'force_git_run.flag' has been created")
        print("2. The main script will detect it on its next check")
        print("3. Git operations will execute immediately")
        print("4. The flag will be automatically removed after execution")
    else:
        print("\n❌ Failed to trigger operation")
    

