# state_service/app.py
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, String, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

load_dotenv()
app = Flask(__name__)

DB_URL = os.getenv("DB_URL", "postgresql://user:password@localhost:5432/telegram_bot_db")
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Модели таблиц
class UserState(Base):
    __tablename__ = "user_states"
    chat_id = Column(String, primary_key=True)
    count = Column(Integer, default=0)
    number = Column(String, default="")
    email = Column(String, default="")
    first_name = Column(String, default="")
    last_name = Column(String, default="")
    button_text = Column(String, default="")

class GlobalData(Base):
    __tablename__ = "global_data"
    id = Column(Integer, primary_key=True, default=1)
    data = Column(JSON, default=list)  # Список nodes как JSON

# Создаем таблицы при запуске (в prod: Alembic)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.route('/get_state/<chat_id>', methods=['GET'])
def get_state(chat_id):
    db = next(get_db())
    state = db.query(UserState).filter(UserState.chat_id == chat_id).first()
    if state:
        result = {
            "count": state.count,
            "number": state.number,
            "email": state.email,
            "first_name": state.first_name,
            "last_name": state.last_name,
            "button_text": state.button_text
        }
        return jsonify({"state": result}), 200
    return jsonify({"state": {}}), 200

@app.route('/set_state/<chat_id>', methods=['POST'])
def set_state(chat_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400
    
    db = next(get_db())
    state = db.query(UserState).filter(UserState.chat_id == chat_id).first()
    if not state:
        state = UserState(chat_id=chat_id)
        db.add(state)
    
    # Обновляем поля из data
    for key, value in data.items():
        if hasattr(state, key):
            setattr(state, key, value)
    
    db.commit()
    return jsonify({"status": "State set"}), 200

@app.route('/get_custom_data', methods=['GET'])
def get_custom_data():
    db = next(get_db())
    global_data = db.query(GlobalData).filter(GlobalData.id == 1).first()
    if global_data:
        return jsonify({"data": global_data.data}), 200
    return jsonify({"data": []}), 200

@app.route('/set_custom_data', methods=['POST'])
def set_custom_data():
    data = request.get_json()
    if not data or 'data' not in data:
        return jsonify({"error": "No data"}), 400
    
    db = next(get_db())
    global_data = db.query(GlobalData).filter(GlobalData.id == 1).first()
    if not global_data:
        global_data = GlobalData(id=1, data=data['data'])
        db.add(global_data)
    else:
        global_data.data = data['data']
    
    db.commit()
    return jsonify({"status": "Custom data set"}), 200

@app.route('/increment_count/<chat_id>', methods=['POST'])
def increment_count(chat_id):
    db = next(get_db())
    state = db.query(UserState).filter(UserState.chat_id == chat_id).first()
    if not state:
        state = UserState(chat_id=chat_id, count=1)
        db.add(state)
    else:
        state.count += 1
    db.commit()
    return jsonify({"count": state.count}), 200

@app.route('/decrement_count/<chat_id>', methods=['POST'])
def decrement_count(chat_id):
    db = next(get_db())
    state = db.query(UserState).filter(UserState.chat_id == chat_id).first()
    if state:
        state.count = max(0, state.count - 1)
        db.commit()
    return jsonify({"count": state.count or 0}), 200

@app.route('/set_number/<chat_id>', methods=['POST'])
def set_number(chat_id):
    data = request.get_json()
    number = data.get('number', '') if data else ''
    db = next(get_db())
    state = db.query(UserState).filter(UserState.chat_id == chat_id).first()
    if not state:
        state = UserState(chat_id=chat_id, number=number)
        db.add(state)
    else:
        state.number = number
    db.commit()
    return jsonify({"status": "Number set"}), 200

@app.route('/set_email/<chat_id>', methods=['POST'])
def set_email(chat_id):
    data = request.get_json()
    email = data.get('email', '') if data else ''
    db = next(get_db())
    state = db.query(UserState).filter(UserState.chat_id == chat_id).first()
    if not state:
        state = UserState(chat_id=chat_id, email=email)
        db.add(state)
    else:
        state.email = email
    db.commit()
    return jsonify({"status": "Email set"}), 200

@app.route('/clear_all', methods=['POST'])
def clear_all():
    db = next(get_db())
    db.query(UserState).delete()
    db.query(GlobalData).delete()
    db.commit()
    return jsonify({"status": "All cleared"}), 200

if __name__ == "__main__":
    app.run(port=5002, debug=True)
