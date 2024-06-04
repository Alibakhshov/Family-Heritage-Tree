# Family Heritage Tree

## Introduction

The Family Heritage Tree project is a web application designed to create, manage, and visualize family trees. Built using HTML, CSS, JavaScript, and Django, this platform allows users to enter family data and explore their lineage through interactive visualizations.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Demo video](#video-demo)
- [Screenshots](#screenshots)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)

## Installation

To get started with the Family Heritage Tree, follow these steps:

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Django

### Setting up a Virtual Environment

It's recommended to use a virtual environment to manage the dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Installing Dependencies

Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

### Running the Application

Navigate to the project directory and run the server:

```bash
python manage.py runserver
```

## Usage

To use the Family Heritage Tree application:

1. Open your web browser.
2. Navigate to `http://127.0.0.1:8000/`.
3. Start by creating your user account and then begin adding family members to your tree.

## Features

- **Interactive Tree Visualization**: View your family tree in an interactive graphical format.
- **User Authentication**: Secure user authentication system.
- **Data Management**: Add, edit, and delete family member entries with ease.

## Dependencies

- Django: The project is built on the Django web framework.
- HTML/CSS/JS: Used for designing and client-side scripting.

## Configuration

No additional configuration is required after the initial setup.

## Video Demo

<a href="https://drive.google.com/file/d/1Zv0gy827GQ9lWz8-ECB4JEsOWV4OtFBT/view" target="_blank"> Link to video</a>

## Screenshots

- **Main Interface**
  ![Main Interface](Screenshots/dashboard.png)
  
- **Family Tree Visualization**
  ![Family Tree Visualization](Screenshots/famTree.png)
  
- **Family Tree Add**
  ![Family Tree Add](Screenshots/famTreeAdd.png)
  
- **Family Tree Details**
  ![Family Tree Details](Screenshots/famTreeDetails.png)
  
- **Gallery Page**
  ![Gallery Page](Screenshots/gallery.png)
  
- **About Page - Contact**
  ![About Page - Contact](Screenshots/aboutContact.png)
  
- **About Page - Overview**
  ![About Page - Overview](Screenshots/aboutOverview.png)
  
- **Settings Page - General**
  ![Settings Page - General](Screenshots/settingsGeneral.png)
  
- **Settings Page - Info**
  ![Settings Page - Info](Screenshots/settingsInfo.png)
  
- **Settings Page - Social Media**
  ![Settings Page - Social Media](Screenshots/settingsSocialMedia.png)

- **User Login Page**
  ![User Login Page](Screenshots/authentication/login.png)
  
- **User Registration Page**
  ![User Registration Page](Screenshots/authentication/register.png)
  
- **Reset Password Page**
  ![Reset Password Page](Screenshots/authentication/reset.png)
  
- **User Message Page**
  ![User Message Page](Screenshots/authentication/message.png)



## Troubleshooting

For common issues:
- Ensure all dependencies are installed as per the `requirements.txt`.
- Check the Django server logs for any error messages.

