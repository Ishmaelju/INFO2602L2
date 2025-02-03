import click, sys
from models import db, User, Todo,Category,TodoCategory
from app import app
from sqlalchemy.exc import IntegrityError


@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.create_all()
  bob = User('bob', 'bob@mail.com', 'bobpass')
  bob.todos.append(Todo('wash car'))
  db.session.add(bob)
  db.session.commit()
  print(bob)
  print('database intialized')

@app.cli.command("get-user", help = "Retrives a User")
@click.argument('username', default = 'bob')
def get_user(username):
  bob = User.query.filter_by(username=username).first()
  if not bob:
    print(f'{username} is not found')
    return
  print (bob)

@app.cli.command('get-users')
def get_users():
  users = User.query.all()
  print(users)

@app.cli.command("change-email")
@click.argument("username", default = "bob")
@click.argument('email', default = "bobnew@mail.com")
def change_email(username, email):
  bob = User.query.filter_by(username=username).first()
  if not bob:
    print(f'{username} is not found')
    return
  bob.email = email
  db.session.add(bob)
  db.session.commit()
  print(bob)

@app.cli.command("create-user")
@click.argument("username", default = "rick")
@click.argument("email", default = "rick@gmail.com")
@click.argument("password", default = "rickpassword")
def create_user(username, email, password):
  newuser= User(username, email, password)
  try:
    db.session.add(newuser)
    db.session.commit()
  except IntegrityError as e:
    db.session.rollback()
    print("Username or email already taken")
  else:
    print(newuser)

@app.cli.command("delete-user")
@click.argument("username", default = "bob")
def delete_user (username):
  user = User.query.filter_by(username=username).first()
  if not user:
    print(f'{username} not found')
    return
  db.session.delete(user)
  db.session.commit()
  print(f'{username} deleted')


@app.cli.command('get-todos')
@click.argument('username', default = 'bob')
def get_user_todos(username):
  bob = User.query.filter_by(username=username).first()
  if not bob:
    print(f'{username} not found')
    return
  print(bob.todos)

@app.cli.command('add-todo')
@click.argument("username", default = "bob")
@click.argument("text", default = "wash car")
def add_todo(username, text):
  user = User.query.filter_by(username=username).first()
  if not user:
    print(f'{username} is not found')
    return
  new_todo = Todo(text)
  user.todos.append(new_todo)
  db.session.add(user)
  db.session.commit()
  print("todo added")

@app.cli.command("toggle-todo")
@click.argument("username", default = "bob")
@click.argument("todo_id", default = 1)
def toggle_todo(username, todo_id):
  user = User.query.filter_by(username=username).first()
  if not user:
    print(f'{username} is not found')
    return
  
  todo= Todo.query.filter_by(id=todo_id, user_id=user.id).first()

  if not todo:
    print(f'{username} has no todo of id {todo_id}')
    return

  todo.toggle()
  print(f'{todo.text} is {"done" if todo.done else "not done"}')
          


@app.cli.command('add-category', help ="Adds a category to a todo")
@click.argument("username", default ='bob')
@click.argument("todo_id", default = 1)
@click.argument("category", default = 'chores')
def add_todo_category(username,todo_id, category):
  user = User.query.filter_by(username=username).first()
  if not user:
    print(f'{username} not found')
    return
  
  res = user.add_todo_category(todo_id, category)
  if not res:
    print(f'{username} has no todo id {todo_id}')
    return
  
  print('Category added')
