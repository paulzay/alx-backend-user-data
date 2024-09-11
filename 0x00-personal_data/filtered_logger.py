#!/usr/bin/env python3
""" regex-ing"""
import logging
import re
import os
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: list):
        """ Constructor """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Format method """
        return filter_datum(self.fields, self.REDACTION, super().format(record), self.SEPARATOR)


def filter_datum(fields, redaction: str, message: str, separator: str):
    for field in fields:
        message = re.sub(f"{field}=.*?{separator}", f"{field}={redaction}{separator}", message)
    return message

def get_logger() -> logging.Logger:
    """ Get logger method """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    ch = logging.StreamHandler()
    ch.setFormatter(RedactingFormatter(fields=("name", "email", "phone", "ssn", "password")))
    logger.addHandler(ch)
    return logger


def get_db():
    """ Get DB method """
    db = os.getenv('PERSONAL_DATA_DB_NAME', '')
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    return mysql.connector.connect(
        host=host,
        database=db,
        user=username,
        password=password
    )


def main():
    """ Main method """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        message = f"name={row[0]}; email={row[1]}; phone={row[2]}; " +\
            f"ssn={row[3]}; password={row[4]};ip={row[5]}; " +\
            f"last_login={row[6]}; user_agent={row[7]};"
        print(message)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
