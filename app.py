from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
import requests
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from werkzeug.security import generate_password_hash, check_password_hash

title = ""
overview = ""
rating = 0
img_link = ""
movielist = []
app = Flask(__name__)
Bootstrap5(app)
app.config['SECRET_KEY'] = 'mysecretKeyYY'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'       # your Gmail address
app.config['MAIL_PASSWORD'] = 'your_app_password'          # your Gmail app password
app.config['MAIL_USE_TLS'] = True




mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

def generate_token(email):
    return s.dumps(email, salt='email-confirm')

def verify_token(token, expiration=3600):
    try:
        return s.loads(token, salt='email-confirm', max_age=expiration)
    except:
        return None




class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)



login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


# CONFIGURE TABLES
class Watched(db.Model):
    __tablename__ = "watched"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(1000), nullable=False)
    overview: Mapped[str] = mapped_column(String(5000), nullable=False)
    rating: Mapped[float] = mapped_column(Float(500), nullable=False)
    img_link: Mapped[str] = mapped_column(String(5000), nullable=False)

class Watchlist(db.Model):
    __tablename__ = "watchlist"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(1000), nullable=False)
    overview: Mapped[str] = mapped_column(String(5000), nullable=False)
    rating: Mapped[float] = mapped_column(Float(500), nullable=False)
    img_link: Mapped[str] = mapped_column(String(5000), nullable=False)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))



with app.app_context():
    db.create_all()



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))





@app.route("/moviecheck", methods=["GET","POST"])
@login_required
def moviecheck():
    global movielist
    movielist.clear()
    API_KEY = 'your_api_key'  # Replace with your TMDB API key
    BASE_URL = 'https://api.themoviedb.org/3'
    url = f'{BASE_URL}/search/movie'
    query = request.form['moviename']
    params = {
        'api_key': API_KEY,
        'query': query
    }
    response = requests.get(url, params=params)
    movielist = response.json()['results']
    return render_template("moviecheck.html", lists=response.json()['results'])

@app.route("/")
def home():
    if current_user.is_authenticated:
        return render_template("front.html",data=current_user,flag=1)
    return render_template("home.html")

@app.route("/login",methods=["POST","GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == "POST":
        password = request.form["password"]
        result = db.session.execute(db.select(User).where(User.email == request.form["email"]))

        user = result.scalar()
        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template("login.html")


@app.route("/register", methods=["POST","GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == "POST":

        user = db.session.execute(db.select(User).where(User.email == request.form['email'])).scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            request.form['password'],
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=request.form['email'],
            name=request.form['name'],
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template("signup.html")

@app.route("/addwatched/<id>")
@login_required
def addwatched(id):
    global movielist
    global title
    global overview
    global rating
    global img_link
    print(movielist)
    print(type(id))
    for item in movielist:
        print(item)
        print(item['id'])
        print(type(item['id']))
        if str(item['id']).__eq__(id):
            print(item)
            title = item['original_title']
            overview = item['overview']
            rating = item['vote_average']
            img_link = "https://image.tmdb.org/t/p/w500"+str(item['poster_path'])
            break


    movie = db.session.execute(
        db.select(Watched).where(Watched.user_id == current_user.id).where(Watched.overview == overview)).scalar()
    if movie:
        return redirect(url_for('watched'))

    new_movie = Watched(
        title = title,
        overview = overview,
        rating = rating,
        img_link = img_link,
        user_id = current_user.id
    )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for('watched'))

@app.route("/removewatched/<moviename>")
@login_required
def removewatched(moviename):

    data_to_delete = db.session.execute(
        db.select(Watched).where(Watched.user_id == current_user.id).where(Watched.title == str(moviename))).scalar()
    db.session.delete(data_to_delete)
    db.session.commit()
    return redirect(url_for('watched'))



@app.route("/addwatchlist/<id>")
@login_required
def addwatchlist(id):
    global movielist
    global title
    global overview
    global rating
    global img_link
    print(movielist)
    for item in movielist:
        print(item)
        print(item['id'])
        print(type(item['id']))
        if str(item['id']).__eq__(id):
            title = item['original_title']
            overview = item['overview']
            rating = item['vote_average']
            img_link = "https://image.tmdb.org/t/p/w500"+str(item['poster_path'])
            break


    movie = db.session.execute(
        db.select(Watchlist).where(Watchlist.user_id == current_user.id).where(Watchlist.overview == overview)).scalar()
    if movie:
        return redirect(url_for('watchlist'))

    new_movie = Watchlist(
        title=title,
        overview=overview,
        rating=rating,
        img_link=img_link,
        user_id = current_user.id
    )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for('watchlist'))


@app.route("/removewatchlist/<moviename>")
@login_required
def removewatchlist(moviename):
    data_to_delete = db.session.execute(
        db.select(Watchlist).where(Watchlist.user_id == current_user.id).where(Watchlist.title == str(moviename))).scalar()
    db.session.delete(data_to_delete)
    db.session.commit()
    return redirect(url_for('watchlist'))



@app.route("/watched")
@login_required
def watched():
    watched_movies = db.session.execute(
        db.select(Watched).where(Watched.user_id == current_user.id)).scalars()
    return render_template("watched.html",movies=watched_movies)



@app.route("/watchlist")
@login_required
def watchlist():
    watchlist_movies = db.session.execute(
        db.select(Watchlist).where(Watchlist.user_id == current_user.id)).scalars()
    return render_template("watchlist.html", movies=watchlist_movies)


@app.route("/forgot-password",methods=["GET","POST"])
def forget_password():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        email = request.form['email']
        print(email)
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        print(user)
        if user:
            print(email)
            token = generate_token(email)
            reset_url = url_for('reset_password', token=token, _external=True)
            msg = Message('Password Reset Link',
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[email])
            msg.body = f'Click the link to reset your password: {reset_url}'
            mail.send(msg)
            return render_template('message.html', message="Check your email for the password reset link.")
        else:
            print(email)
            flash("Email not found.")
            return redirect(url_for('forget_password'))
    return render_template('forgot.html')

@app.route('/reset-password/<token>', methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    email = verify_token(token)
    user = db.session.execute(db.select(User).where(User.email == email)).scalar()
    # print(user)
    if not email:
        return render_template('message.html', message="Invalid or expired token.")
    if request.method == 'POST':
        password = request.form['password']
        confirm = request.form['confirm']
        print(password,confirm)
        if password.__eq__(confirm):
            print(password, confirm)
            hash_and_salted_password = generate_password_hash(
                password,
                method='pbkdf2:sha256',
                salt_length=8
            )
            user.password = hash_and_salted_password
            db.session.commit()
            login_user(user)
            return render_template('success.html')
        else:
            return render_template('message.html', message="Password do not match",sub_message="Try Again")
    return render_template('reset-password.html', token=token)




if __name__ == "__main__":
    app.run(debug=True)