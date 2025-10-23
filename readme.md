# Article-Blog

Article-Blog is a feature-rich blogging platform API built using Django and Django REST Framework (DRF). It allows users to create, manage, and interact with articles and reviews while ensuring secure user authentication and authorization. This project is the capstone submission for the ALX Backend Web Development program.

## Features

### User Management
- **User Registration**: Users can register by providing a username, email, and password with validation checks for password confirmation and username uniqueness.
- **Login & Logout**: Secure login using username and password. The platform supports both token-based and session-based authentication.
- **Authorization**: Token and session management ensure secure access to restricted endpoints.

### Article Management
- **CRUD Operations**: Users can create, view, update, and delete articles.
- **Article Topics**: Each article can be associated with a topic for better organization.
- **Publication Status**: Articles can be marked as either draft or published.

### Review System
- **CRUD Operations**: Users can add, update, and delete reviews on articles.
- **Review Ownership**: Only review authors can edit or delete their reviews.

### Security
- **Authentication**: The platform uses both token-based and session-based authentication.
- **Authorization**: Only authors can modify or delete their own articles and reviews.

## Project Structure

```
Article-Blog/
├── blog/                      # Main blogging app
│   ├── models.py              # Data models (Article, Topic, Review)
│   ├── serializers.py         # Data serialization
│   ├── views.py               # API endpoints and business logic
│   ├── urls.py                # App-level routing
│   └── tests.py               # Unit tests
├── blogging_platform/         # Project-level settings and configurations
│   ├── settings.py            # Project configurations
│   └── urls.py                # Project-wide URL management
├── db.sqlite3                 # SQLite development database
├── manage.py                  # Django CLI for project management
├── requirements.txt           # Project dependencies
├── README.md                  # Project documentation
└── venv/                      # Python virtual environment
```

## API Endpoints

### User Endpoints:
- Register: POST /api/register/
- Login: POST /api/login/
- Logout: POST /api/logout/

### Article Endpoints:
- List & Create Articles: GET, POST /api/articles/
- Retrieve, Update, Delete Article: GET, PUT, DELETE /api/articles/<slug>/
- Articles by Topic: GET /api/topics/<topic_id>/articles/

### Topic Endpoints:
- List Topics: GET /api/topics/

### Review Endpoints:
- List & Create Reviews: GET, POST /api/articles/<article_id>/reviews/
- Retrieve, Update, Delete Review: GET, PUT, DELETE /api/reviews/<id>/

## Setup and Installation

### Clone the Repository:
```bash
git clone https://github.com/Muhamad550/Article-Blog.git
cd Article-Blog
```

### Create and Activate Virtual Environment:
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### Install Dependencies:
```bash
pip install -r requirements.txt
```

### Apply Database Migrations:
```bash
python manage.py migrate
```

### Run the Development Server:
```bash
python manage.py runserver
```

### Access the API: 
Visit http://127.0.0.1:8000/ in your browser or use tools like Postman.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests on the GitHub repository.

## Contact
- GitHub: [Muhamad550](https://github.com/Muhamad550)
- Email: ma8287225@gmail.com
