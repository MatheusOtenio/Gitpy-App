# GitHub Account Manager

A desktop application built with Python and CustomTkinter for managing GitHub accounts through the GitHub REST API.

## Features

### 🔐 Authentication
- Secure GitHub Personal Access Token (PAT) authentication
- Token masking for security

### 🎨 User Interface
- Clean and intuitive CustomTkinter-based GUI
- Token input field with masking
- Username and target username fields
- Functionality dropdown menu
- Action execution button
- Scrollable output display

### 🧩 Implemented Features

#### 🟦 Social
- Follow/Unfollow users
- List following and followers
- Automatic unfollow for non-followers

#### 🟩 Repositories
- List user repositories
- Create new repositories
- Delete repositories
- Toggle repository visibility

## Download and Installation

### Option 1: Download Released Version
1. Download the latest release ZIP from the GitHub Releases page
2. Extract the ZIP file to your desired location
3. Double-click GitPy.exe to run the application

### Option 2: Build from Source
1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python github_manager_app.py
```

### System Requirements
- Windows operating system
- Windows Visual C++ Redistributable (commonly pre-installed)
- Active internet connection for GitHub API access
- Sufficient permissions to run executables

## Building Executable

To create a standalone executable:
```bash
pyinstaller --noconfirm --onefile --windowed github_manager_app.py
```

## GitHub Token

To use this application, you need a GitHub Personal Access Token (PAT):

1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate a new token with the required permissions
3. Copy the token and use it to authenticate in the application

## Development

The application is structured into modules:
- `github_manager_app.py`: Main application and GUI
- `github_api.py`: GitHub API integration and operations

## Security Note

Never share your Personal Access Token. The application stores the token only in memory during runtime.