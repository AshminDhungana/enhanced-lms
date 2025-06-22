
# **Enhanced Learning Management System (LMS)**

## **Project Overview**

The Enhanced Learning Management System (LMS) is a web-based platform designed to facilitate comprehensive online education with multiple distinct user roles: **Admin**, **Instructor**, **Student**, and **Sponsor**. This system aims to provide a robust environment for managing courses, assessments, student progress, and even financial sponsorships.

## **Features**

This project implements the following key features:

* **Role-Based Access Control:** Differentiated access and functionalities for Admins, Instructors, Students, and Sponsors.  
* **User Management:** Admins can oversee all user accounts and roles.  
* **Course Management:**  
  * Instructors can create, update, and delete courses, modules, and lessons.  
  * Students can browse and enroll in courses.  
* **Assessment & Submission:**  
  * Instructors can create assignments/quizzes for courses.  
  * Instructors can grade student submissions and provide feedback.  
  * Students can view their assignments and submission details.  
* **Progress Tracking:** Students can track their course progress.  
* **Sponsorship Module:**  
  * Sponsors can fund students.  
  * Sponsors can track the progress of their sponsored students.  
  * Basic fund utilization tracking (via payments).  
* **Data Filtering & Searching:**  
  * Students (or any user) can search for courses by name, instructor, or difficulty level.  
  * Sponsors can filter sponsored students by status (completed/in-progress) and progress level.  
* **Data Pagination:** Course listings and sponsored student lists are paginated for efficient display of large datasets.  
* **Analytics Dashboards:**  
  * **Admin Dashboard:** Displays platform-wide metrics such as total users, active courses, total enrollments, and funds received.  
  * **Sponsor Dashboard:** Provides insights into sponsorship impact, total funds provided/utilized, and an overview of sponsored students' progress.  
* **Notifications & Emailing:**  
  * In-app notification system (bell icon with unread count and dropdown).  
  * Email notifications for key events (e.g., new assignments for students, assessment results for students).  
  * Console email backend used for development to view emails in the terminal.  
* **Proper Comments & Documentation:** All code includes clear explanations and documentation. Basic User and Developer Guides are provided.  
* **Basic API Testing:** Initial unit tests for core functionalities and views.

## **Roles**

* **Admin:** Full oversight of the platform, user management, and access to platform-wide analytics. (Login via custom dashboard or Django Admin).  
* **Instructor:** Manages courses, creates assessments, grades submissions, and monitors student engagement for their courses.  
* **Student:** Enrolls in courses, completes assignments, tracks personal progress, and receives notifications.  
* **Sponsor:** Funds students, tracks their academic progress, and monitors fund utilization.

## **Technologies Used**

* **Backend:**  
  * Django (Python Web Framework)  
  * SQLite (Default Database for Development)  
* **Frontend:**  
  * HTML, CSS  
  * Tailwind CSS (for styling, via CDN)  
  * django-crispy-forms & crispy\_tailwind (for form rendering)  
  * JavaScript (for dynamic UI elements like notification dropdown)  
  * Font Awesome (for icons)  
* **Version Control:** Git  
* **Development Environment:** GitHub Codespaces

## **Setup Instructions**

Follow these steps to get the Enhanced LMS up and running on your local machine (or in GitHub Codespaces):

### **1\. Clone the Repository**

If you're starting in a new Codespace, this step is often handled automatically. Otherwise, clone the project to your local machine:

git clone https://github.com/AshminDhungana/enhanced-lms.git  
cd enhanced-lms

### **2\. Create a Virtual Environment (Recommended)**

It's best practice to create a virtual environment to manage project dependencies:

python \-m venv venv

Activate the virtual environment:

* **On macOS/Linux:**  
  source venv/bin/activate

* **On Windows:**  
  .\\venv\\Scripts\\activate

### **3\. Install Dependencies**

=======
Enhanced Learning Management System (LMS)
Project Overview
The Enhanced Learning Management System (LMS) is a web-based platform designed to facilitate comprehensive online education with multiple distinct user roles: Admin, Instructor, Student, and Sponsor. This system aims to provide a robust environment for managing courses, assessments, student progress, and even financial sponsorships.

Features
This project implements the following key features:

Role-Based Access Control: Differentiated access and functionalities for Admins, Instructors, Students, and Sponsors.

User Management: Admins can oversee all user accounts and roles.

Course Management:

Instructors can create, update, and delete courses, modules, and lessons.

Students can browse and enroll in courses.

Assessment & Submission:

Instructors can create assignments/quizzes for courses.

Instructors can grade student submissions and provide feedback.

Students can view their assignments and submission details.

Progress Tracking: Students can track their course progress.

Sponsorship Module:

Sponsors can fund students.

Sponsors can track the progress of their sponsored students.

Basic fund utilization tracking (via payments).

Data Filtering & Searching:

Students (or any user) can search for courses by name, instructor, or difficulty level.

Sponsors can filter sponsored students by status (completed/in-progress) and progress level.

Data Pagination: Course listings and sponsored student lists are paginated for efficient display of large datasets.

Analytics Dashboards:

Admin Dashboard: Displays platform-wide metrics such as total users, active courses, total enrollments, and funds received.

Sponsor Dashboard: Provides insights into sponsorship impact, total funds provided/utilized, and an overview of sponsored students' progress.

Notifications & Emailing:

In-app notification system (bell icon with unread count and dropdown).

Email notifications for key events (e.g., new assignments for students, assessment results for students).

Console email backend used for development to view emails in the terminal.

Proper Comments & Documentation: All code includes clear explanations and documentation. Basic User and Developer Guides are provided.

Basic API Testing: Initial unit tests for core functionalities and views.

Roles
Admin: Full oversight of the platform, user management, and access to platform-wide analytics. (Login via custom dashboard or Django Admin).

Instructor: Manages courses, creates assessments, grades submissions, and monitors student engagement for their courses.

Student: Enrolls in courses, completes assignments, tracks personal progress, and receives notifications.

Sponsor: Funds students, tracks their academic progress, and monitors fund utilization.

Technologies Used
Backend:

Django (Python Web Framework)

SQLite (Default Database for Development)

Frontend:

HTML, CSS

Tailwind CSS (for styling, via CDN)

django-crispy-forms & crispy_tailwind (for form rendering)

JavaScript (for dynamic UI elements like notification dropdown)

Font Awesome (for icons)

Version Control: Git

Development Environment: GitHub Codespaces

Setup Instructions
Follow these steps to get the Enhanced LMS up and running on your local machine (or in GitHub Codespaces):

1. Clone the Repository
If you're starting in a new Codespace, this step is often handled automatically. Otherwise, clone the project to your local machine:

git clone https://github.com/AshminDhungana/enhanced-lms.git
cd enhanced-lms

2. Create a Virtual Environment (Recommended)
It's best practice to create a virtual environment to manage project dependencies:

python -m venv venv

Activate the virtual environment:

On macOS/Linux:

source venv/bin/activate

On Windows:

.\venv\Scripts\activate

3. Install Dependencies
>>>>>>> ab07129cee9371b8604edacd1a4c9a456f80ce29
Install the required Python packages using pip:

pip install django crispy-forms crispy-tailwind

<<<<<<< HEAD
### **4\. Run Database Migrations**

Apply the database migrations to create the necessary tables in your db.sqlite3 file:

python manage.py makemigrations  
python manage.py migrate

### **5\. Create a Superuser**

=======
4. Run Database Migrations
Apply the database migrations to create the necessary tables in your db.sqlite3 file:

python manage.py makemigrations
python manage.py migrate

5. Create a Superuser
>>>>>>> ab07129cee9371b8604edacd1a4c9a456f80ce29
Create an administrative user account to access the Django admin panel and manage your data:

python manage.py createsuperuser

Follow the prompts to set a username, email, and password for your superuser.

<<<<<<< HEAD
### **6\. Run the Development Server**

=======
6. Run the Development Server
>>>>>>> ab07129cee9371b8604edacd1a4c9a456f80ce29
Start the Django development server:

python manage.py runserver 0.0.0.0:8000

<<<<<<< HEAD
* If you are in **GitHub Codespaces**, a pop-up should appear offering to "Open in Browser" for port 8000\. Click it. If not, go to the "Ports" tab in the bottom panel and click the "Open in Browser" icon next to port 8000\.  
* If you are running **locally**, open your web browser and navigate to http://127.0.0.1:8000/ or http://localhost:8000/.

## **Usage**

After setting up and running the server:

* **Home Page:** Access the main landing page at /.  
* **Login:** Click "Login" or navigate to /login/.  
* **Access Admin:** Log in with your superuser credentials and you will be redirected to the custom Admin Dashboard (/admin-dashboard/). You can also access the traditional Django Admin at /admin/.  
* **Create Test Users:** In the Django Admin (/admin/), go to "Users" and create new users with different roles (Student, Instructor, Sponsor). Remember to set their Role in the "User profile" section.  
* **Explore Dashboards:** Log in with different user roles to see their respective dashboards:  
  * **Student:** /student-dashboard/  
  * **Instructor:** /instructor-dashboard/  
  * **Sponsor:** /sponsor-dashboard/  
* **Course Management:** As an **Instructor**, go to /courses/ to add, edit, or delete courses. From a course detail page, you can add assessments.  
* **Grading:** As an **Instructor**, check your dashboard for "Pending Submissions" and click through to grade them.  
* **Notifications:** Look for the bell icon in the top right. Unread notifications will show a count. Click to open the dropdown or "View All" to see your notification history.

## **Testing**

To run the project's unit tests:

1. Stop the development server (Ctrl \+ C in the terminal).  
2. Run the tests using Django's test runner:  
   python manage.py test core

   This will execute the tests defined in core/tests.py.

## **Contributing**

If you wish to contribute to this project:

1. Fork the repository.  
2. Create a new branch (git checkout \-b feature/your-feature-name).  
3. Make your changes and commit them (git commit \-m 'Add new feature X').  
4. Push your branch (git push origin feature/your-feature-name).  
5. Open a Pull Request.

## **License**

This project is open-source and available under the [MIT License](http://docs.google.com/LICENSE) (if you want to add a LICENSE file).

## **Contact**

For questions or issues, please contact \[Your Name/Email/GitHub Profile\].
=======
If you are in GitHub Codespaces, a pop-up should appear offering to "Open in Browser" for port 8000. Click it. If not, go to the "Ports" tab in the bottom panel and click the "Open in Browser" icon next to port 8000.

If you are running locally, open your web browser and navigate to http://127.0.0.1:8000/ or http://localhost:8000/.

Usage
After setting up and running the server:

Home Page: Access the main landing page at /.

Login: Click "Login" or navigate to /login/.

Access Admin: Log in with your superuser credentials and you will be redirected to the custom Admin Dashboard (/admin-dashboard/). You can also access the traditional Django Admin at /admin/.

Create Test Users: In the Django Admin (/admin/), go to "Users" and create new users with different roles (Student, Instructor, Sponsor). Remember to set their Role in the "User profile" section.

Explore Dashboards: Log in with different user roles to see their respective dashboards:

Student: /student-dashboard/

Instructor: /instructor-dashboard/

Sponsor: /sponsor-dashboard/

Course Management: As an Instructor, go to /courses/ to add, edit, or delete courses. From a course detail page, you can add assessments.

Grading: As an Instructor, check your dashboard for "Pending Submissions" and click through to grade them.

Notifications: Look for the bell icon in the top right. Unread notifications will show a count. Click to open the dropdown or "View All" to see your notification history.

Testing
To run the project's unit tests:

Stop the development server (Ctrl + C in the terminal).

Run the tests using Django's test runner:

python manage.py test core

This will execute the tests defined in core/tests.py.

Contributing
If you wish to contribute to this project:

Fork the repository.

Create a new branch (git checkout -b feature/your-feature-name).

Make your changes and commit them (git commit -m 'Add new feature X').

Push your branch (git push origin feature/your-feature-name).

Open a Pull Request.

License
This project is open-source and available under the MIT License (if you want to add a LICENSE file).

Contact
For questions or issues, please contact [Your Name/Email/GitHub Profile].
>>>>>>> ab07129cee9371b8604edacd1a4c9a456f80ce29
