-- Create the student_scores database if it doesn't exist
CREATE DATABASE IF NOT EXISTS student_scores;
-- drop database student_scores;
-- Use the student_scores database
USE student_scores;

-- Create the students table
CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    score FLOAT DEFAULT 0.0,
    subject VARCHAR(255) DEFAULT 'None',
    easy_questions_solved INT DEFAULT 0,
    medium_questions_solved INT DEFAULT 0,
    hard_questions_solved INT DEFAULT 0
);

-- Function to check a student's password
DELIMITER $$
CREATE FUNCTION check_password(in_name VARCHAR(255), in_password VARCHAR(255))
RETURNS BOOLEAN DETERMINISTIC
BEGIN
    DECLARE user_password VARCHAR(255);
    SELECT password INTO user_password FROM students WHERE name = in_name;
    IF user_password = in_password THEN
        RETURN 1;
    ELSE
        RETURN 0;
    END IF;
END
$$
DELIMITER ;

-- Function to check if a student exists by name
DELIMITER $$
CREATE FUNCTION check_student_name(sname VARCHAR(255)) RETURNS INT DETERMINISTIC
BEGIN
    DECLARE student_exists INT;
    SET student_exists = (
        SELECT COUNT(*) FROM students WHERE name = sname
    );

    IF student_exists > 0 THEN
        RETURN 1;
    ELSE
        RETURN 0;
    END IF;
END $$;
DELIMITER ;

-- Function to add a new student
DELIMITER $$
CREATE FUNCTION add_student(
    sname VARCHAR(255),
    spassword VARCHAR(255)
) RETURNS INT DETERMINISTIC
BEGIN
    INSERT INTO students (name, password)
    VALUES (sname, spassword);

    RETURN LAST_INSERT_ID();
END $$;

DELIMITER ;

-- Procedure to update a student's score and solved questions
DELIMITER $$
CREATE PROCEDURE UpdateStudentScore(
    IN p_name VARCHAR(255),
    IN p_score FLOAT,
    IN p_subject VARCHAR(255),
    IN p_easy INT,
    IN p_medium INT,
    IN p_hard INT
)
BEGIN
    UPDATE students
    SET
        score = p_score,
        subject = p_subject,
        easy_questions_solved = p_easy,
        medium_questions_solved = p_medium,
        hard_questions_solved = p_hard
    WHERE name = p_name;

    IF ROW_COUNT() > 0 THEN
        SELECT 'Student score updated successfully.' AS message;
    ELSE
        SELECT 'Student not found or score not updated.' AS message;
    END IF;
END $$;
DELIMITER ;

Select * from students;
