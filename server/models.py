from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Authors must have a name")
        if db.session.query(Author).filter_by(name=name).first():
            raise ValueError("Author name already exists")
        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number should be exactly ten digits")
        return value
    
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    category = db.Column(db.Enum('Fiction', 'Non-Fiction'), nullable=False)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_content(self, key, value):
        if len(value) < 250:
            raise ValueError("Content must be at least 250 characters long")
        return value
    
    @validates('summary')
    def validate_summary(self, key, value):
        if value and len(value) > 250:
            raise ValueError("Summary can be a maximum of 250 characters")
        return value
    @validates('category')
    def validate_category(self, key, category):
        if category != 'Fiction' and category != 'Non-Fiction':
            raise ValueError("Category must be Fiction or Non-Fiction.")
        return category
    @validates('title')
    def validate_title(self, key, value):
        if not any(keyword in value for keyword in ["Won't Believe", "Secret", "Top", "Guess"]):
            raise ValueError("Title must contain one of the following: Wont Believe,Secret, Top, Guess")
        return value
    
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary}, category={self.category})'

