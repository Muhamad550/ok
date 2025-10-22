# MaBlog

MaBlog is a feature-rich blogging platform API built using Django and Django REST Framework (DRF). It allows users to create, manage, and interact with blog posts and comments while ensuring secure user authentication and authorization. This project is the capstone submission for the ALX Backend Web Development program.

---

## Features

### User Management

- **User Registration:** Users can register by providing a username, email, and password with validation checks for password confirmation and username uniqueness.
- **Login & Logout:** Secure login using username and password. The platform supports both token-based and session-based authentication.
- **Authorization:** Token and session management ensure secure access to restricted endpoints.

### Blog Post Management

- **CRUD Operations:** Users can create, view, update, and delete blog posts.
- **Post Categories:** Each blog post can be associated with a category for better organization.
- **Like Feature:** Users can like blog posts.
- **Post Status Management:** Blog posts can be marked as either `draft` or `published`.

### Commenting System

- **CRUD Operations:** Users can add, update, and delete comments on blog posts.
- **Comment Ownership:** Only comment authors can edit or delete their comments.

### Security

- **Authentication:** The platform uses both token-based and session-based authentication.
- **Authorization:** Only authors can modify or delete their own posts and comments.

---

## Project Structure

```
Mablog/
├── blog/                      # Main blogging app
│   ├── models.py              # Data models (BlogPost, Category, Comment)
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

---

## API Endpoints

### User Endpoints:

- **Register:** `POST /register/`
- **Login:** `POST /login/`
- **Logout:** `POST /logout/`

### Blog Post Endpoints:

- **List & Create Posts:** `GET, POST /posts/`
- **Retrieve, Update, Delete Post:** `GET, PUT, DELETE /posts/<id>/`
- **Posts by Category:** `GET /posts/category/<category_id>/`
- **Posts by Author:** `GET /posts/author/<author_id>/`

### Comment Endpoints:

- **List & Create Comments:** `GET, POST /posts/<post_id>/comments/`
- **Retrieve, Update, Delete Comment:** `GET, PUT, DELETE /comments/<id>/`

---

## Setup and Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Zaid-dev2000/mablog.git
   cd mablog
   ```

2. **Create and Activate Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Database Migrations:**

   ```bash
   python manage.py migrate
   ```

5. **Run the Development Server:**

   ```bash
   python manage.py runserver
   ```

6. **Access the API:**
   Visit `http://127.0.0.1:8000/` in your browser or use tools like Postman.

---

##

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests on the [GitHub repository](https://github.com/Zaid-dev2000/mablog).

---

## License

This project is licensed under the MIT License.

---

## Contact

- **GitHub:** [Zaid-dev2000](https://github.com/Zaid-dev2000)
- **Email:** [elouakhchachizaid\@gmail.com]

---

