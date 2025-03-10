CREATE TABLE USERS (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) CHECK (role IN ('admin', 'teacher', 'student', 'parent')),
    parent_id INT REFERENCES USERS(id) ON DELETE SET NULL
);

CREATE TABLE NEWS (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE SUBJECTS (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    teacher_id INT REFERENCES USERS(id) ON DELETE CASCADE
);

CREATE TABLE CLASSROOMS (
    id SERIAL PRIMARY KEY,
    name VARCHAR(10) UNIQUE NOT NULL,
    nb_seats INT NOT NULL CHECK (nb_seats > 0)
);

CREATE TABLE CLASSES (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    subject_id INT REFERENCES SUBJECTS(id) ON DELETE CASCADE,
    students INT[] NOT NULL,
    level VARCHAR(15) CHECK (level IN ('Débutant', 'Intermédiaire', 'Avancé')),
    classroom_id INT REFERENCES CLASSROOMS(id) ON DELETE CASCADE,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    day_of_week VARCHAR(10) CHECK (day_of_week IN ('Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'))
);

CREATE TABLE GRADES (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES USERS(id) ON DELETE CASCADE,
    subject_id INT REFERENCES SUBJECTS(id) ON DELETE CASCADE,
    grade DECIMAL(4,2) CHECK (grade BETWEEN 0 AND 20),
    comment TEXT,
    date_assigned DATE NOT NULL
);

CREATE TABLE REMARKS (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES USERS(id) ON DELETE CASCADE,
    teacher_id INT REFERENCES USERS(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE HOMEWORKS (
    id SERIAL PRIMARY KEY,
    class_id INT REFERENCES CLASSES(id) ON DELETE CASCADE,
    subject_id INT REFERENCES SUBJECTS(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    due_date DATE NOT NULL DEFAULT CURRENT_DATE + INTERVAL '1 week'
);

CREATE TABLE ABSENCES (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES USERS(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    class_id INT REFERENCES CLASSES(id) ON DELETE CASCADE,
    status VARCHAR(15) CHECK (status IN ('Justifiée', 'Injustifiée')) DEFAULT 'Injustifiée',
    justification TEXT
);

CREATE TABLE MESSAGES (
    id SERIAL PRIMARY KEY,
    sender_id INT REFERENCES USERS(id) ON DELETE CASCADE,
    receiver_id INT REFERENCES USERS(id) ON DELETE CASCADE,
    subject VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read BOOLEAN DEFAULT FALSE
);