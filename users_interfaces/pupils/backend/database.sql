CREATE TABLE USERS (
    _id INTEGER PRIMARY KEY AUTOINCREMENT,
    _created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    _active BOOLEAN DEFAULT TRUE,
    _name VARCHAR(50) NOT NULL,
    _surname VARCHAR(50) NOT NULL,
    _age INT NOT NULL CHECK (_age >= 0),
    _username VARCHAR(50) UNIQUE NOT NULL,
    _password_hash TEXT NOT NULL,
    _profile_pic TEXT,
    _email VARCHAR(100) UNIQUE,
    _phone VARCHAR(20) UNIQUE,
    _role VARCHAR(20) CHECK (_role IN ('admin', 'teacher', 'student', 'secretary')),
    _parent_name VARCHAR(50),
    _parent_email VARCHAR(100),
    _parent_phone VARCHAR(20),
    CHECK ((_age < 15 AND _parent_name IS NOT NULL AND _parent_email IS NOT NULL AND _parent_phone IS NOT NULL) OR (_age >= 15))
);

CREATE TABLE CLASSROOMS (
    _id INTEGER PRIMARY KEY AUTOINCREMENT,
    _name VARCHAR(10) UNIQUE NOT NULL,
    _nb_seats INT NOT NULL CHECK (_nb_seats > 0)
);

CREATE TABLE SUBJECTS (
    _id INTEGER PRIMARY KEY AUTOINCREMENT,
    _name VARCHAR(50) NOT NULL CHECK (_name IN ('Quran', 'Tajwid', 'Nourania', 'Langue Arabe', 'Eveil a la Foi', 'Education Religieuse')),
    UNIQUE (_name)
);

CREATE TABLE TEACHES (
    _teacher_id INT NOT NULL,
    _subject_id INT NOT NULL,
    PRIMARY KEY (_teacher_id, _subject_id),
    FOREIGN KEY (_teacher_id) REFERENCES USERS(_id) ON DELETE CASCADE,
    FOREIGN KEY (_subject_id) REFERENCES SUBJECTS(_id) ON DELETE CASCADE
);

CREATE TABLE CLASSES (
    _id INTEGER PRIMARY KEY AUTOINCREMENT,
    _subject_id INT,
    _teacher_id INT,
    _level VARCHAR(15) CHECK (_level IN ('Debutant', 'Intermediaire', 'Avance', NULL)),
    _classroom_id INT,
    _start_time TIME NOT NULL,
    _end_time TIME NOT NULL,
    _day_of_week VARCHAR(10) CHECK (_day_of_week IN ('Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche')),
    _is_online BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (_subject_id) REFERENCES SUBJECTS(_id) ON DELETE CASCADE,
    FOREIGN KEY (_teacher_id) REFERENCES USERS(_id) ON DELETE CASCADE,
    FOREIGN KEY (_classroom_id) REFERENCES CLASSROOMS(_id) ON DELETE CASCADE
);

CREATE TABLE ENROLLMENTS (
    _id INTEGER PRIMARY KEY AUTOINCREMENT,
    _student_id INT,
    _class_id INT,
    _enrolled_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (_student_id, _class_id),
    FOREIGN KEY (_student_id) REFERENCES USERS(_id) ON DELETE CASCADE,
    FOREIGN KEY (_class_id) REFERENCES CLASSES(_id) ON DELETE CASCADE
);

CREATE TABLE GRADES (
    _id INTEGER PRIMARY KEY AUTOINCREMENT,
    _student_id INT,
    _subject_id INT,
    _grade DECIMAL(4,2) CHECK (_grade IS NULL OR _grade BETWEEN 0 AND 20),
    _date DATE NOT NULL,
    _comment TEXT,
    FOREIGN KEY (_student_id) REFERENCES USERS(_id) ON DELETE CASCADE,
    FOREIGN KEY (_subject_id) REFERENCES SUBJECTS(_id) ON DELETE CASCADE
);

CREATE TABLE REMARKS (
    _id INTEGER PRIMARY KEY AUTOINCREMENT,
    _student_id INT,
    _subject_id INT,
    _content TEXT NOT NULL,
    _date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (_student_id) REFERENCES USERS(_id) ON DELETE CASCADE,
    FOREIGN KEY (_subject_id) REFERENCES SUBJECTS(_id) ON DELETE CASCADE
);

CREATE TABLE HOMEWORKS (
    _id INTEGER PRIMARY KEY AUTOINCREMENT,
    _class_id INT,
    _description TEXT NOT NULL,
    _issued_at DATE NOT NULL,
    FOREIGN KEY (_class_id) REFERENCES CLASSES(_id) ON DELETE CASCADE
);

CREATE TABLE MAILS (
    _id INTEGER PRIMARY KEY AUTOINCREMENT,
    _subject VARCHAR(255) NOT NULL,
    _content TEXT NOT NULL,
    _sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    _sender_id INT,
    FOREIGN KEY (_sender_id) REFERENCES USERS(_id) ON DELETE CASCADE
);

CREATE TABLE MAIL_RECIPIENTS (
    _id INTEGER PRIMARY KEY AUTOINCREMENT,
    _is_read BOOLEAN DEFAULT FALSE,
    _folder VARCHAR(20) CHECK (_folder IN ('Boite de Reception', 'Envoyes', 'Brouillons', 'Corbeille', 'Favoris')) DEFAULT 'Boite de Reception',
    _mail_id INT NOT NULL,
    _receiver_id INT NOT NULL,
    FOREIGN KEY (_mail_id) REFERENCES MAILS(_id) ON DELETE CASCADE,
    FOREIGN KEY (_receiver_id) REFERENCES USERS(_id) ON DELETE CASCADE
);

CREATE TABLE NEWS (
    _id INTEGER PRIMARY KEY AUTOINCREMENT,
    _title VARCHAR(255) NOT NULL,
    _content TEXT,
    _image_url TEXT
);