#!/usr/bin/env python3
"""
Debug script to test Firebase initialization
"""

import frappe
import os

def debug_firebase():
    """Debug Firebase initialization"""
    try:
        print("=== Firebase Debug Information ===")
        
        # Check if Firebase Settings exist
        if frappe.db.exists("Firebase Settings", "Firebase Settings"):
            firebase_settings = frappe.get_single("Firebase Settings")
            print(f"✅ Firebase Settings found")
            print(f"   - Is Active: {firebase_settings.is_active}")
            print(f"   - Project ID: {firebase_settings.project_id}")
            print(f"   - Service Account JSON: {firebase_settings.service_account_json}")
            
            if firebase_settings.service_account_json:
                # Check file
                file_doc = frappe.get_doc("File", {"file_url": firebase_settings.service_account_json})
                file_path = file_doc.get_full_path()
                print(f"   - File Path: {file_path}")
                print(f"   - File Exists: {os.path.exists(file_path)}")
                
                if not os.path.exists(file_path):
                    # Try alternative path
                    site_path = frappe.utils.get_site_path()
                    alternative_path = os.path.join(site_path, "public", "files", os.path.basename(firebase_settings.service_account_json))
                    print(f"   - Alternative Path: {alternative_path}")
                    print(f"   - Alternative Exists: {os.path.exists(alternative_path)}")
                    
                    if os.path.exists(alternative_path):
                        print(f"   - Using alternative path for testing")
                        file_path = alternative_path
                
                if os.path.exists(file_path):
                    # Try to read the JSON file
                    try:
                        import json
                        with open(file_path, 'r') as f:
                            json_content = json.load(f)
                        print(f"   - JSON file is valid")
                        print(f"   - Project ID in JSON: {json_content.get('project_id')}")
                        print(f"   - Client Email: {json_content.get('client_email')}")
                    except Exception as e:
                        print(f"   - Error reading JSON: {e}")
                else:
                    print(f"   - ❌ File not found at any path")
            else:
                print(f"   - ❌ No service account JSON uploaded")
        else:
            print(f"❌ Firebase Settings not found")
        
        print("\n=== Testing Firebase Client ===")
        
        # Test Firebase client
        from frappe_fcm_notification.frappe_fcm_notification.utils.firebase_client import get_firebase_client
        client = get_firebase_client()
        print(f"Client created: {client}")
        print(f"App initialized: {client.app is not None}")
        
        if client.app:
            print(f"✅ Firebase app is initialized")
            print(f"   - Project ID: {client.app.project_id}")
        else:
            print(f"❌ Firebase app is not initialized")
            
            # Try force re-initialization
            print("\n=== Trying Force Re-initialization ===")
            result = client.force_reinitialize()
            print(f"Re-initialization result: {result}")
            
            if client.app:
                print(f"✅ Firebase app is now initialized")
                print(f"   - Project ID: {client.app.project_id}")
            else:
                print(f"❌ Firebase app still not initialized")
        
        print("\n=== Test Connection ===")
        result = client.test_connection()
        print(f"Test connection result: {result}")
        
    except Exception as e:
        print(f"Error during debug: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_firebase() 