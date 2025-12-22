# Red Devil Hub - Django Blog Application

A Manchester United-themed blog and community platform built with Django 6.0. This application allows fans to create posts, comment on content, interact through likes, and connect with other supporters through a members directory.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [User Authentication System](#user-authentication-system)
- [Database Models](#database-models)
- [Third-Party Packages](#third-party-packages)
- [Usage Guide](#usage-guide)
- [Admin Panel](#admin-panel)
- [Media Handling](#media-handling)

---

## Features

### Core Functionality
- **User Registration & Authentication**: Custom registration with automatic member profile creation
- **Blog Posts**: Create, read, update, and delete blog posts with media upload support
- **Comments**: Add comments to posts with optional media attachments
- **Like System**: Users can like/unlike posts
- **Members Directory**: Browse and search registered supporters
- **Profile Management**: View member profiles with contact information
- **Responsive Design**: Manchester United-themed UI with Bootstrap 5

### Security Features
- CSRF protection on all forms
- Login required decorators for sensitive operations
- Author-only edit/delete permissions for posts and comments
- Secure file upload handling

---

## Technology Stack

### Backend
- **Python**: 3.x
- **Django**: 6.0
- **Database**: SQLite3 (default, easily switchable to PostgreSQL/MySQL)

### Frontend
- **HTML5/CSS3**
- **Bootstrap**: 5.3.3
- **Bootstrap Icons**: 1.11.1
- **Google Fonts**: Oswald & Roboto

### Media Processing
- **Pillow**: 12.0.0 (for image handling)

---

## Project Structure

```
myblogproject/
│
├── blog/                          # Main blog application
│   ├── migrations/                # Database migrations
│   ├── templates/
│   │   └── blog/
│   │       ├── base.html         # Base template with navbar
│   │       ├── login.html        # Login page
│   │       ├── register.html     # Registration page
│   │       ├── post_list.html    # Homepage with all posts
│   │       ├── post_detail.html  # Individual post view
│   │       ├── post_form.html    # Create/edit post form
│   │       ├── post_edit.html    # Edit post template
│   │       └── post_confirm_delete.html
│   ├── __init__.py
│   ├── admin.py                  # Admin configuration for Post/Comment
│   ├── apps.py
│   ├── context_processors.py     # Custom context processor
│   ├── forms.py                  # PostForm for creating/editing posts
│   ├── models.py                 # Post and Comment models
│   ├── views.py                  # All blog views
│   └── urls.py                   # Blog URL patterns
│
├── members/                       # Members/supporters application
│   ├── migrations/
│   ├── templates/
│   │   ├── 404.html
│   │   ├── all_member.html       # Members directory
│   │   ├── details.html          # Member profile page
│   │   ├── main.html             # Supporters club homepage
│   │   ├── sample.html
│   │   ├── update_profile.html   # Profile picture update
│   │   └── upload_pic.html
│   ├── __init__.py
│   ├── admin.py                  # Admin configuration for Member
│   ├── apps.py
│   ├── forms.py                  # RegisterForm
│   ├── models.py                 # Member model
│   ├── views.py                  # Member views
│   └── urls.py                   # Member URL patterns
│
├── blog_project/                  # Project configuration
│   ├── __init__.py
│   ├── asgi.py                   # ASGI configuration
│   ├── settings.py               # Project settings
│   ├── urls.py                   # Root URL configuration
│   └── wsgi.py                   # WSGI configuration
│
├── media/                         # User-uploaded files
│   ├── post_media/               # Post images/videos
│   ├── comment_media/            # Comment attachments
│   └── profile_pics/             # Member profile pictures
│
├── db.sqlite3                    # SQLite database
├── manage.py                     # Django management script
└── requirements.txt              # Python dependencies
```

---

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment tool (recommended)

### Step-by-Step Installation

1. **Clone or Download the Project**
   ```bash
   cd myblogproject
   ```

2. **Create a Virtual Environment** (Recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   The `requirements.txt` contains:
   ```
   asgiref==3.11.0
   Django==6.0
   pillow==12.0.0
   setuptools==80.9.0
   sqlparse==0.5.4
   wheel==0.45.1
   ```

4. **Apply Database Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a Superuser** (for admin access)
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to set username, email, and password.

6. **Create Media Directories**
   ```bash
   # The directories will be created automatically, but you can create them manually:
   mkdir media
   mkdir media/post_media
   mkdir media/comment_media
   mkdir media/profile_pics
   ```

7. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

8. **Access the Application**
   - Homepage: `http://127.0.0.1:8000/`
   - Admin Panel: `http://127.0.0.1:8000/admin/`

---

## User Authentication System

### Overview
The application uses **Django's built-in authentication system** with custom extensions for member profiles.

### Authentication Flow

#### 1. Registration (`blog/views.py` - `register` function)
- **URL**: `/register/`
- **Method**: Custom function-based view
- **Process**:
  1. User fills out registration form (username, password1, password2)
  2. Server-side validation checks:
     - Username and password are provided
     - Passwords match
     - Username is unique
  3. Creates a new `User` object using `User.objects.create_user()`
  4. Automatically logs in the user after registration
  5. **Signal automatically creates a Member profile** (see Member model)
  6. Redirects to the post list page

#### 2. Login (`blog/views.py` - `login_view` function)
- **URL**: `/login/`
- **Method**: Django's `authenticate()` and `login()` functions
- **Process**:
  1. User submits username and password
  2. `authenticate()` verifies credentials
  3. If valid, `login()` creates a session
  4. Redirects to post list; otherwise shows error message

#### 3. Logout (`blog/views.py` - `logout_view` function)
- **URL**: `/logout/`
- **Method**: Django's `logout()` function
- **Process**: Destroys session and redirects to homepage

### Protected Views
Views requiring authentication use the `@login_required` decorator:

```python
from django.contrib.auth.decorators import login_required

@login_required
def post_create(request):
    # Only authenticated users can access
```

**Protected Functions**:
- `post_create` - Creating posts
- `add_comment` - Adding comments
- `post_edit` - Editing posts
- `post_delete` - Deleting posts
- `comment_delete` - Deleting comments
- `update_profile` - Updating profile pictures

### Authorization (Ownership Checks)
For edit/delete operations, the system verifies the user is the content owner:

```python
if post.author != request.user:
    return HttpResponseForbidden('You are not allowed to edit this post!')
```

### User-Member Relationship
- Each `User` automatically gets a linked `Member` profile via Django signals
- The relationship is established using `OneToOneField` in the Member model
- Signal: `create_member_profile` fires when a new User is created

---

## Database Models

### Blog App Models (`blog/models.py`)

#### 1. Post Model
Represents a blog post created by users.

```python
class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    media = models.FileField(upload_to='post_media/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='blog_posts', blank=True)
```

**Fields**:
- `title`: Post headline (max 255 characters)
- `body`: Main content (unlimited text)
- `media`: Optional image or video file
- `author`: Foreign key to Django's User model (post creator)
- `date_posted`: Automatically set when post is created
- `likes`: Many-to-many relationship with Users who liked the post

**Methods**:
- `total_likes()`: Returns the count of users who liked the post

**Relationships**:
- One author (User) can have many posts
- Many users can like a post
- Has many comments (reverse relationship)

#### 2. Comment Model
Represents comments on blog posts.

```python
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    media = models.FileField(upload_to='comment_media/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

**Fields**:
- `post`: Foreign key to the Post being commented on
- `author`: Foreign key to the User who wrote the comment
- `text`: Comment content
- `media`: Optional image or video attachment
- `created_at`: Timestamp of comment creation

**Relationships**:
- Each comment belongs to one post
- Each comment has one author
- When a post is deleted, all its comments are deleted (CASCADE)

### Members App Models (`members/models.py`)

#### 3. Member Model
Extended profile information for registered users.

```python
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to='profile_pics/', 
                                    default='profile_pics/default_avatar.png', 
                                    blank=True, null=True)
    emailaddress = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    joined_date = models.DateField(auto_now_add=True, null=True)
```

**Fields**:
- `user`: One-to-one link to Django's User model
- `firstname`: Member's first name
- `lastname`: Member's last name
- `profile_pic`: Profile picture (defaults to default_avatar.png)
- `emailaddress`: Contact email
- `phone_number`: Optional phone number
- `joined_date`: Date the member registered

**Signal Integration**:
```python
@receiver(post_save, sender=User)
def create_member_profile(sender, instance, created, **kwargs):
    if created:
        Member.objects.create(
            user=instance,
            firstname=instance.first_name or instance.username,
            lastname=instance.last_name,
            emailaddress=instance.email
        )
```

This signal automatically creates a Member profile whenever a new User is created.

### Database Relationships Diagram

```
User (Django built-in)
  |
  |-- OneToOne --> Member
  |
  |-- ForeignKey (author) --> Post
  |                            |
  |                            |-- ForeignKey --> Comment
  |                            |
  |                            |-- ManyToMany (likes) --> User
  |
  |-- ForeignKey (author) --> Comment
```

---

## Third-Party Packages

### 1. Pillow (12.0.0)
**Purpose**: Image processing and validation

**Integration**:
- Automatically installed with Django for `ImageField` support
- Handles image uploads in:
  - Post media files
  - Comment media files
  - Member profile pictures
- Validates image formats and processes uploaded files

**Configuration** (in `settings.py`):
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

**URL Configuration** (in `blog_project/urls.py`):
```python
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 2. Bootstrap 5.3.3 (CDN)
**Purpose**: Frontend styling and responsive design

**Integration**: Loaded via CDN in `base.html`:
```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
```

**Custom Styling**: Manchester United theme with CSS variables:
```css
--mufc-red: #DA291C;
--mufc-black: #000000;
--mufc-gold: #FBE122;
```

### 3. Bootstrap Icons (1.11.1)
**Purpose**: Icon library

**Integration**:
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
```

**Usage**: Icons for UI elements (user profile, arrows, hearts for likes, etc.)

### 4. Google Fonts
**Purpose**: Custom typography

**Fonts Used**:
- **Oswald**: Headers and brand text (bold, uppercase)
- **Roboto**: Body text

**Integration**:
```html
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@700&family=Roboto:wght@400;700&display=swap" rel="stylesheet">
```

---

## Usage Guide

### For End Users

#### Creating an Account
1. Navigate to the homepage
2. Click "Join the Club" or "Register"
3. Fill in username, password (twice for confirmation)
4. A Member profile is automatically created
5. You're logged in and redirected to the fan feed

#### Creating a Post
1. Log in to your account
2. Click "Write Post" in the navigation bar
3. Enter a title and body content
4. Optionally upload an image or video
5. Click "Post to Feed"

#### Interacting with Posts
- **View**: Click "Read Full Story" on any post
- **Like**: Click the heart icon (must be logged in)
- **Comment**: Scroll to the comments section, write your comment, optionally attach media
- **Edit/Delete**: Only available if you're the post author (buttons appear on post detail page)

#### Browsing Members
1. Click "Supporters Club" in the navbar
2. Use the search bar to find specific members
3. Click "View Profile" to see member details

### For Developers

#### Adding New Views
1. Define the view in `views.py`
2. Add URL pattern in `urls.py`
3. Create corresponding template in `templates/`
4. Add navigation links where appropriate

#### Customizing the Theme
- Edit CSS variables in `base.html`
- Modify Bootstrap classes in templates
- Change background image URL in the body styling

#### Adding New Models
1. Define model in `models.py`
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`
4. Register in `admin.py` for admin panel access

---

## Admin Panel

### Accessing the Admin Panel
1. Navigate to `http://127.0.0.1:8000/admin/`
2. Log in with superuser credentials

### Registered Models

#### Blog App
- **Posts**: View, edit, delete all posts
- **Comments**: Manage all comments

#### Members App
- **Members**: Custom admin display showing:
  - First name
  - Last name
  - Joined date
  - Email address

**Admin Configuration** (`members/admin.py`):
```python
class MemberAdmin(admin.ModelAdmin):
    list_display = ("firstname", "lastname", "joined_date", "emailaddress")
```

### Admin Capabilities
- Create, read, update, delete operations on all models
- Bulk actions (delete multiple items)
- Search and filter functionality
- User and group management

---

## Media Handling

### File Upload Structure

**Post Media**: Stored in `media/post_media/`
- Images: JPG, PNG, GIF
- Videos: MP4, MOV

**Comment Media**: Stored in `media/comment_media/`
- Same formats as post media

**Profile Pictures**: Stored in `media/profile_pics/`
- Default avatar: `default_avatar.png`

### Display Logic
The templates automatically detect file type and render appropriately:

```django
{% if post.media.url|lower|slice:"-4:" == ".mp4" or post.media.url|lower|slice:"-4:" == ".mov" %}
    <video width="100%" height="auto" controls>
        <source src="{{ post.media.url }}" type="video/mp4">
    </video>
{% else %}
    <img src="{{ post.media.url }}" class="img-fluid">
{% endif %}
```

### Security Notes
- All file uploads are validated by Pillow
- Files are stored outside the project root for security
- Media URLs are only accessible when properly configured in `urls.py`

---

## URL Patterns

### Blog App URLs (`/`)

| URL Pattern | View Function | Name | Description |
|------------|---------------|------|-------------|
| `/` | `post_list` | `post_list` | Homepage with all posts |
| `/posts/<int:pk>/` | `post_detail` | `post_detail` | Individual post view |
| `/register/` | `register` | `register` | User registration |
| `/login/` | `login_view` | `login` | User login |
| `/logout/` | `logout_view` | `logout` | User logout |
| `/posts/new/` | `post_create` | `post_create` | Create new post |
| `/posts/<int:pk>/comment/` | `add_comment` | `add_comment` | Add comment to post |
| `/posts/<int:pk>/edit/` | `post_edit` | `post_edit` | Edit post |
| `/posts/<int:pk>/delete/` | `post_delete` | `post_delete` | Delete post |
| `/like/<int:pk>` | `like_post` | `like_post` | Like/unlike post |
| `/comment/<int:pk>/delete/` | `comment_delete` | `comment_delete` | Delete comment |

### Members App URLs (`/members/`)

| URL Pattern | View Function | Name | Description |
|------------|---------------|------|-------------|
| `/members/` | `main` | `main` | Supporters club homepage |
| `/members/members/` | `members` | `members` | All members directory |
| `/members/members/details/<int:id>/` | `details` | `details` | Member profile page |
| `/members/register/` | `register_user` | `register` | Alternative registration (not used in UI) |

---

## Development Notes

### Custom Context Processor (`blog/context_processors.py`)
The project uses a custom context processor to make member statistics available globally across all templates.

**Configuration** (in `settings.py`):
```python
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                # ... other processors
                'blog.context_processors.member_stats',
            ],
        },
    },
]
```

**Implementation**:
```python
from members.models import Member

def member_stats(request):
    return {
        'total_fans': Member.objects.count(),
        'latest_members': Member.objects.all().order_by('-id')[:3]
    }
```

**What it does**:
- Makes `total_fans` and `latest_members` available in every template without manually passing them from views
- `total_fans`: Total count of registered members
- `latest_members`: The 3 most recently registered members

**Usage in templates**:
```django
<p>Total Supporters: {{ total_fans }}</p>

{% for member in latest_members %}
    <li>{{ member.firstname }} {{ member.lastname }}</li>
{% endfor %}
```

This is particularly useful in the sidebar of `post_list.html` where the latest members are displayed without needing to query them in the view.

### Django Signals
The project uses Django's signal system to automatically create Member profiles:
- Signal: `post_save` on User model
- Effect: Creates a Member instance whenever a User is created
- Location: `members/models.py`

### Template Inheritance
All templates extend `blog/base.html` which includes:
- Navigation bar
- Footer
- Manchester United theme styling
- Bootstrap and custom CSS
- JavaScript for smooth scrolling

### Form Handling
The project uses Django's ModelForm for simplified form handling:
- `PostForm`: For creating/editing posts
- `RegisterForm`: Extended UserCreationForm with additional fields

---

## Future Enhancement Ideas

- Email verification on registration
- Password reset functionality
- User profile editing (beyond profile pictures)
- Post categories/tags
- Advanced search and filtering
- Social media sharing integration
- Real-time notifications
- API endpoints for mobile app integration
- Multiple image uploads per post
- Comment likes/replies (nested comments)

---

## Troubleshooting

### Common Issues

**1. Media files not displaying**
- Check `MEDIA_URL` and `MEDIA_ROOT` in `settings.py`
- Ensure media URLs are added to `urlpatterns` in project `urls.py`
- Verify file permissions on media directory

**2. Database errors after model changes**
```bash
python manage.py makemigrations
python manage.py migrate
```

**3. Static files not loading**
```bash
python manage.py collectstatic
```

**4. Permission denied errors**
- Ensure the user running Django has write access to the media directory
- Check file permissions: `chmod 755 media/`

---

## Contributing

To contribute to this project:
1. Create a new branch for your feature
2. Make your changes
3. Test thoroughly
4. Submit a pull request with a clear description

---

## License

This project is for educational purposes. Manchester United trademarks and branding are property of Manchester United Football Club.

---

## Contact & Support

For issues, questions, or suggestions, please contact the project maintainer or open an issue in the project repository.

---

**Glory Glory Man United! 🔴⚫**