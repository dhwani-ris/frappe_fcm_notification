#!/usr/bin/env python3
"""
Test script to debug file path issues
"""

import frappe
import os

def test_file_path():
    """Test file path resolution"""
    try:
        # Get Firebase settings
        firebase_settings = frappe.get_single("Firebase Settings")
        print(f"Service account JSON URL: {firebase_settings.service_account_json}")
        
        # Get file doc
        file_doc = frappe.get_doc("File", {"file_url": firebase_settings.service_account_json})
        file_path = file_doc.get_full_path()
        print(f"File path from get_full_path(): {file_path}")
        
        # Check if file exists
        if os.path.exists(file_path):
            print(f"✅ File exists at: {file_path}")
        else:
            print(f"❌ File not found at: {file_path}")
            
            # Try alternative path
            site_path = frappe.utils.get_site_path()
            alternative_path = os.path.join(site_path, "public", "files", os.path.basename(firebase_settings.service_account_json))
            print(f"Alternative path: {alternative_path}")
            
            if os.path.exists(alternative_path):
                print(f"✅ File exists at alternative path: {alternative_path}")
            else:
                print(f"❌ File not found at alternative path: {alternative_path}")
                
                # List files in the directory
                files_dir = os.path.join(site_path, "public", "files")
                if os.path.exists(files_dir):
                    print(f"Files in {files_dir}:")
                    for file in os.listdir(files_dir):
                        if file.endswith('.json'):
                            print(f"  - {file}")
                else:
                    print(f"Directory {files_dir} does not exist")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_file_path() 