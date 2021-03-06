from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Login
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    # Info
    name = db.Column(db.String)
    cpf = db.Column(db.String)
    gender = db.Column(db.String)  # transformar
    birthday = db.Column(db.Date)

    books = db.relationship("UserBook", backref='user', lazy='dynamic')

    def set_password(self, pswd):
        self.password = generate_password_hash(pswd)

    def check_password(self, pswd):
        return check_password_hash(self.password, pswd)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return "<User %r>" % self.email


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Info
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)  # create an specific table
    publisher = db.Column(db.String, nullable=False)  # create an specific table
    gender = db.Column(db.String, nullable=False)  # create an specific table
    isbn = db.Column(db.String)

    def __repr__(self):
        return "<Book %r>" % self.title


class UserBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    book_id = db.Column(db.Integer, db.ForeignKey(Book.id), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    quality = db.Column(db.String)
    status = db.Column(db.String)

    book = db.relationship(Book, foreign_keys=book_id)
    owner = db.relationship(User, foreign_keys=owner_id)

    def __repr__(self):
        return "<UserBook %r>" % self.id


class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    id_borrower = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    id_book = db.Column(db.Integer, db.ForeignKey(UserBook.id), nullable=False)
    final_date = db.Column(db.Date, nullable=False)

    borrower = db.relationship(User, foreign_keys=id_borrower)
    book = db.relationship(UserBook, foreign_keys=id_book)

    def __repr__(self):
        return "<Borrow %r>" % self.id
