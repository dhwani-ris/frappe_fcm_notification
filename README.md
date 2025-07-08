# Frappe FCM Notification

A comprehensive Firebase Cloud Messaging (FCM) integration app for Frappe Framework that enables sending push notifications to mobile devices and web browsers.

## Features

- 🔥 **Firebase Integration**: Complete Firebase Admin SDK integration with service account authentication
- 📱 **Multi-Platform Support**: Send notifications to Android, iOS, and Web devices
- 👥 **Role-Based Targeting**: Target users by roles, specific users, or custom filters
- ⏰ **Scheduled Notifications**: Schedule notifications for future delivery
- 📊 **Delivery Statistics**: Track notification delivery success rates and failures
- 🔄 **Automatic Retry**: Retry failed notifications with configurable retry logic
- 🧹 **Token Management**: Automatic cleanup of expired/invalid FCM tokens
- 🔒 **Security**: Role-based permissions and secure credential storage
- 📈 **Dashboard**: Real-time statistics and monitoring dashboard

## Installation

### Prerequisites

- Frappe Framework (v14 or later)
- Python 3.10+
- Firebase project with FCM enabled

### 1. Install the App

```bash
# Navigate to your Frappe bench directory
cd /path/to/your/bench

# Install the app
bench get-app frappe_fcm_notification

# Install dependencies
bench pip install firebase-admin>=6.2.0

# Migrate the app
bench migrate

# Clear cache
bench clear-cache

# Restart Frappe server
bench restart
```

### 2. Setup Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select existing project
3. Enable Cloud Messaging in the project settings
4. Generate a new service account key:
   - Go to Project Settings > Service Accounts
   - Click "Generate new private key"
   - Download the JSON file

### 3. Configure Firebase Settings

1. In Frappe Desk, go to **Frappe FCM Notification > Firebase Settings**
2. Fill in the required fields:
   - **Project Name**: Your Firebase project name
   - **Project ID**: Your Firebase project ID
   - **Service Account JSON**: Upload the downloaded JSON file
   - **Is Active**: Check to enable FCM
3. Click "Test Connection" to verify setup
4. Save the settings

### 4. Verify Installation

Run the verification scripts to ensure everything is properly installed:

```bash
# Open Frappe console
bench --site your-site.com console

# Test imports first
exec(open('test_imports.py').read())
test_imports()

# Run verification script
exec(open('verify_installation.py').read())
verify_installation()
```

## Usage

### Sending Notifications

#### 1. Create a New Notification

1. Go to **Frappe FCM Notification > Push Notification Manager**
2. Click "New"
3. Fill in the notification details:
   - **Notification Title**: The title of your notification
   - **Notification Body**: The message content
   - **Target Type**: Choose from:
     - All Users: Send to all enabled users
     - By Role: Target specific user roles
     - Specific Users: Target individual users
     - Custom Filter: Use custom user filters
   - **Notification Type**: Immediate or Scheduled
4. Click "Save" and then "Send Now" for immediate notifications

#### 2. Target Types

**All Users**
- Sends to all enabled users in the system

**By Role**
- Select specific roles from the dropdown
- All users with those roles will receive the notification

**Specific Users**
- Manually select individual users
- Useful for targeted communications

**Custom Filter**
- Use JSON filters to target users based on custom criteria
- Example: `{"enabled": 1, "creation": [">=", "2024-01-01"]}`

### Mobile App Integration

#### 1. Save FCM Token

```javascript
// In your mobile app or web app
frappe.call({
    method: 'frappe_fcm_notification.api.fcm.save_fcm_token',
    args: {
        token: 'your-fcm-token-here',
        device_type: 'Android' // or 'iOS', 'Web'
    },
    callback: function(r) {
        if (r.message && r.message.success) {
            console.log('Token saved successfully');
        }
    }
});
```

#### 2. Delete FCM Token

```javascript
frappe.call({
    method: 'frappe_fcm_notification.api.fcm.delete_fcm_token',
    args: { token: 'your-fcm-token-here' },
    callback: function(r) {
        if (r.message && r.message.success) {
            console.log('Token deleted successfully');
        }
    }
});
```

### API Endpoints

#### Whitelisted APIs (for mobile apps)

- `frappe_fcm_notification.api.fcm.save_fcm_token`
- `frappe_fcm_notification.api.fcm.test_firebase_connection`
- `frappe_fcm_notification.api.fcm.send_test_notification`
- `frappe_fcm_notification.api.fcm.get_user_tokens`
- `frappe_fcm_notification.api.fcm.delete_fcm_token`

## Configuration

### Scheduled Tasks

The app includes several scheduled tasks that run automatically:

- **Process Scheduled Notifications**: Runs every 5 minutes
- **Cleanup Expired Tokens**: Runs daily at 2 AM
- **Retry Failed Notifications**: Runs every 15 minutes

### Permissions

- **System Manager**: Full access to all FCM features
- **All Users**: Can create and manage their own notifications
- **Firebase Settings**: Restricted to System Manager only

## Troubleshooting

### Common Issues

1. **Firebase Connection Failed**
   - Verify your service account JSON file is correct
   - Check that FCM is enabled in your Firebase project
   - Ensure the project ID matches between Frappe and Firebase

2. **Notifications Not Delivered**
   - Check if FCM tokens are active and valid
   - Verify target users have active FCM tokens
   - Check Firebase console for delivery reports

3. **Scheduled Notifications Not Sending**
   - Ensure the scheduled task is running
   - Check the scheduled datetime is in the future
   - Verify Firebase settings are active

### Debug Mode

Enable debug logging by adding to your `site_config.json`:

```json
{
    "fcm_debug": true
}
```

## Development

### Project Structure

```
frappe_fcm_notification/
├── frappe_fcm_notification/
│   ├── api/                    # API endpoints
│   ├── events/                 # Document event handlers
│   ├── permissions/            # Permission functions
│   ├── tasks/                  # Scheduled tasks
│   ├── utils/                  # Utility functions
│   └── doctype/               # DocType definitions
├── public/                    # Frontend assets
│   ├── js/                    # JavaScript files
│   └── css/                   # CSS files
└── hooks.py                   # App hooks
```

### Adding Custom Features

1. **Custom Notification Templates**
   - Extend the `Push Notification Manager` DocType
   - Add template fields and logic

2. **Custom Target Filters**
   - Modify the `get_target_users` function in events
   - Add new target types

3. **Custom Delivery Reports**
   - Extend the delivery statistics functionality
   - Add custom reporting methods

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:

- Create an issue on GitHub
- Contact: bhushan.barbuddhe@dhwaniris.com
- Documentation: [Link to docs]

## Changelog

### v1.0.0
- Initial release
- Firebase FCM integration
- Role-based targeting
- Scheduled notifications
- Token management
- Delivery statistics
