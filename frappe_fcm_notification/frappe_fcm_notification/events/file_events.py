def validate(file, method):
    if (file.attached_to_doctype == "Firebase Settings" 
        and file.attached_to_field == "service_account_json"):
        
        if getattr(file, "custom_skip_s3_upload", None) is not None:
            file.custom_skip_s3_upload = 1

    return True