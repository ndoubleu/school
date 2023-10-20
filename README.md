
# Django Backend application for SchoolProject

Install:



## Run Locally

Clone the project

```bash
  git clone https://github.com/ndoubleu/school.git
```

Go to the project directory

```bash
  cd school
```

Create env and install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python manage.py runserver
```


## User roles

There are 3 types of user roles: is_director, is_teacher and is_student. Only directors can create another users.

In django admin, every user has different type of permissions.

Directors can add teachers, groups, subjects and students.
Teachers can add grades
Students can view self grades and subjects.




## API Reference

#### Get group grades, only accessible for teachers and director

```http
  GET api/reports/group/${id}
```

#### Get grade of student, accessible only for student

```http
  GET /api/reports/student/${id}
```


#### Swagger documentation

```http
  GET /
```


