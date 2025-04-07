CREATE TABLE USERS (
    _id SERIAL PRIMARY KEY,
    _name VARCHAR(50) NOT NULL,
    _surname VARCHAR(50) NOT NULL,
    _age INT NOT NULL CHECK (_age >= 0),
    _username VARCHAR(50) UNIQUE NOT NULL,
    _password_hash TEXT NOT NULL,
    _email VARCHAR(100) UNIQUE CHECK ((_age >= 18 AND _email IS NOT NULL) OR (_age < 18 AND _email IS NULL)),
    _role VARCHAR(20) CHECK (_role IN ('admin', 'teacher', 'student')),
    _parent_name VARCHAR(50),
    _parent_email VARCHAR(100) UNIQUE,
    CHECK ((_age < 18 AND _parent_name IS NOT NULL AND _parent_email IS NOT NULL) OR (_age >= 18))
);

CREATE TABLE NEWS (
    _id SERIAL PRIMARY KEY,
    _title VARCHAR(255) NOT NULL,
    _content TEXT,
    _image_url TEXT,
    _created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE SUBJECTS (
    _id SERIAL PRIMARY KEY,
    _name VARCHAR(50) NOT NULL,
    _teacher_id INT REFERENCES USERS(_id) ON DELETE CASCADE
);

CREATE TABLE CLASSROOMS (
    _id SERIAL PRIMARY KEY,
    _name VARCHAR(10) UNIQUE NOT NULL,
    _nb_seats INT NOT NULL CHECK (_nb_seats > 0)
);

CREATE TABLE CLASSES (
    _id SERIAL PRIMARY KEY,
    _name VARCHAR(50) NOT NULL,
    _subject_id INT REFERENCES SUBJECTS(_id) ON DELETE CASCADE,
    _students INT[] NOT NULL,
    _level VARCHAR(15) CHECK (level IN ('Débutant', 'Intermédiaire', 'Avancé')),
    _classroom_id INT REFERENCES CLASSROOMS(_id) ON DELETE CASCADE,
    _start_time TIME NOT NULL,
    _end_time TIME NOT NULL,
    _day_of_week VARCHAR(10) CHECK (_day_of_week IN ('Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'))
);

CREATE TABLE GRADES (
    _id SERIAL PRIMARY KEY,
    _student_id INT REFERENCES USERS(_id) ON DELETE CASCADE,
    _subject_id INT REFERENCES SUBJECTS(_id) ON DELETE CASCADE,
    _grade DECIMAL(4,2) CHECK (_grade BETWEEN 0 AND 20),
    _comment TEXT,
    _date_assigned DATE NOT NULL
);

CREATE TABLE REMARKS (
    _id SERIAL PRIMARY KEY,
    _student_id INT REFERENCES USERS(_id) ON DELETE CASCADE,
    _teacher_id INT REFERENCES USERS(_id) ON DELETE CASCADE,
    _content TEXT NOT NULL,
    _created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE HOMEWORKS (
    _id SERIAL PRIMARY KEY,
    _class_id INT REFERENCES CLASSES(_id) ON DELETE CASCADE,
    _subject_id INT REFERENCES SUBJECTS(_id) ON DELETE CASCADE,
    _title VARCHAR(255) NOT NULL,
    _description TEXT,
    _due_date DATE NOT NULL DEFAULT CURRENT_DATE + INTERVAL '1 week'
);

CREATE TABLE ABSENCES (
    _id SERIAL PRIMARY KEY,
    _student_id INT REFERENCES USERS(_id) ON DELETE CASCADE,
    _date DATE NOT NULL,
    _class_id INT REFERENCES CLASSES(_id) ON DELETE CASCADE,
    _status VARCHAR(15) CHECK (_status IN ('Justifiée', 'Injustifiée')) DEFAULT 'Injustifiée',
    _justification TEXT
);

CREATE TABLE MESSAGES (
    _id SERIAL PRIMARY KEY,
    _sender_id INT REFERENCES USERS(_id) ON DELETE CASCADE,
    _receiver_id INT REFERENCES USERS(_id) ON DELETE CASCADE,
    _subject VARCHAR(255) NOT NULL,
    _content TEXT NOT NULL,
    _sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    _read BOOLEAN DEFAULT FALSE
);