import os
import random
import sqlite3
from pathlib import Path
from random import choice

from gtts import gTTS

from kyrgyz_audio import settings


def init_db():
    global db, cursor
    db = sqlite3.connect(
        Path(__file__).parent.parent / "db.sqlite"
    )
    cursor = db.cursor()

def create_tables():
    # cursor.execute("""
    #     --sql
    #     DROP TABLE IF EXISTS stories;
    # """)

    cursor.execute("""
        --sql
        CREATE TABLE IF NOT EXISTS stories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            text INTEGER,
            audio TEXT
        );
    """)

    cursor.execute("""
        --sql
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            t_id INTEGER
        );
    """)

    db.commit()

def save_audio_file(text, file_name):
    audio_directory = os.path.join(settings.MEDIA_ROOT, 'audio')

    if not os.path.exists(audio_directory):
        os.makedirs(audio_directory)

    audio_file_path = os.path.join('audio', file_name)

    tts = gTTS(text, lang='ru')
    tts.save(os.path.join(settings.MEDIA_ROOT, audio_file_path))
    print(audio_file_path)
    return audio_file_path

def insert_story(name, description, text):
    audio = save_audio_file(text, f"{name}.mp3")
    cursor.execute("""
        --sql
        INSERT INTO stories (name, description, text, audio) VALUES
        (:name, :description, :text, :audio)
    """, {
        'name': name,
        'description': description,
        'text': text,
        'audio': audio
    })
    db.commit()

def insert_user(name, t_id):
    cursor.execute("""
        --sql
        INSERT INTO users (name, t_id) VALUES
        (:name, :t_id)
    """, {
        'name': name,
        't_id': t_id,
    })
    db.commit()

def get_story():
    cursor.execute("""
        --sql
        SELECT * FROM stories
    """)
    return choice(cursor.fetchall())

def get_users():
    cursor.execute("""
        --sql
        SELECT * FROM users
    """)
    return cursor.fetchall()


def get_story_by_id(id):
    cursor.execute("""
        --sql
        SELECT * FROM stories WHERE id=:id 
    """,{
        "id" : id
    })
    return cursor.fetchone()

def get_random_books():
    cursor.execute("""
        --sql
        SELECT * FROM stories
    """)
    return random.shuffle(cursor.fetchone())[:10]