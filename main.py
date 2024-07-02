from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

config = {
    "host" : "127.0.0.1",
    "port" : "3306",
    "user" : "root",
    "database" : "socialnet"
}

class user_register(BaseModel):
    username: str
    nome: str
    cognome: str
    password: str

@app.post("/api/register")
def registrazione(user : user_register):
    conn = mysql.connector.connect(**config)
    cursor  = conn.cursor(dictionary=True)
    cursor.execute("INSERT INTO users (username, nome, cognome, password) VALUES (%s,%s,%s,%s)", (user.username, user.nome, user.cognome, user.password))
    conn.commit()
    conn.close()
    return {"msg" : "utente inserito con successo"}
    
@app.get("/api/allusers")
def all_users():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * from users")
    users = cursor.fetchall()
    conn.close()
    return users
    
@app.get("/api/user/{username}")
def user(username : str):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * from users WHERE username = '{username}' ")
    user = cursor.fetchone()
    conn.close()
    if user :
        return user
    else : 
        return {"msg" : "utente not found"}
    
class post(BaseModel):
    auth: str
    content: str

#rotta di creazione post tramite metodo post
@app.post("/api/create_post")
def create_post(username: post):
    conn = mysql.connector.connect(**config) # host = config#host
    cursor  = conn.cursor(dictionary=True)
    cursor.execute("INSERT INTO posts(auth, content) VALUES (%s,%s)", (username.auth, username.content))
    conn.commit()
    conn.close()
    return {
        "msg" : "tutto andato a buon fine"
    }

@app.get("/api/home")
def all_post():
    conn = mysql.connector.connect(**config)
    cursor  = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    conn.close()
    return posts

class message(BaseModel):
    receiver: str
    message_text: str

@app.post("/api/send_message/{sender}")
def send_message(sender: str, message: message):
    conn = mysql.connector.connect(**config)
    cursor  = conn.cursor(dictionary=True)
    cursor.execute("INSERT INTO messages(sender, receiver, message_text) VALUES (%s, %s, %s)", (sender, message.receiver, message.message_text))
    conn.commit()
    conn.close()
    return {"msg": "messaggio creato"}

@app.get("/api/read_message/{username}")
def read_message(username: str):
    conn = mysql.connector.connect(**config)
    cursor  = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * from messages WHERE receiver = '{username}' ")
    messages = cursor.fetchall()
    conn.close()
    return messages

