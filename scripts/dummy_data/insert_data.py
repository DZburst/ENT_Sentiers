from insert_classrooms import insert_classrooms
from insert_users import insert_users
from insert_subjects import insert_subjects
from insert_teaches import insert_teaches
from insert_classes import insert_classes
from insert_enrollments import insert_enrollments
from insert_grades import insert_grades
from insert_homeworks import insert_homeworks
from insert_remarks import insert_remarks
from insert_mails import insert_mails
from insert_mail_recipients import insert_mail_recipients
from insert_news import insert_news
def main():
    print("Starting data import...")
    insert_classrooms()
    insert_users()
    insert_subjects()
    insert_teaches()
    insert_classes()
    insert_enrollments()
    insert_grades()
    insert_homeworks()
    insert_remarks()
    insert_mails()
    insert_mail_recipients()
    insert_news()
    print("Data import completed successfully!")

if __name__ == "__main__":
    main()

    