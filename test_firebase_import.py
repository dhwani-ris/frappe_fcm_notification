#!/usr/bin/env python3
"""
Test script to verify Firebase imports are working correctly
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all Firebase-related imports"""
    try:
        print("Testing Firebase imports...")
        
        # Test Firebase client import
        from frappe_fcm_notification.frappe_fcm_notification.utils.firebase_client import get_firebase_client
        print("✓ Firebase client import successful")
        
        # Test events import
        from frappe_fcm_notification.frappe_fcm_notification.events.push_notification_events import send_notification
        print("✓ Push notification events import successful")
        
        # Test API import
        from frappe_fcm_notification.frappe_fcm_notification.api.fcm import register_fcm_token
        print("✓ FCM API import successful")
        
        # Test tasks import
        from frappe_fcm_notification.frappe_fcm_notification.tasks.scheduled_tasks import process_scheduled_notifications
        print("✓ Scheduled tasks import successful")
        
        # Test startup import
        from frappe_fcm_notification.frappe_fcm_notification.startup.startup import initialize_firebase
        print("✓ Startup import successful")
        
        print("\n✅ All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1) 