import os
from flask import Flask, render_template, redirect, session, request, flash
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename

from database import db, User, Product, FollowData
from form import SignupForm, LoginForm, ProductForm
app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

keyword = ['모자', '안경', '셔츠', '바지', '신발', '악세사리', '선글라스']

@app.route("/")
def main():
    return render_template("index.html", Product=Product.query.all())

@app.route("/myinfo")
def myinfo():
    return render_template("myinfo.html", Product=Product.query.all(), FollowData=FollowData.query.all())

@app.route("/followingshop/<id>", methods=["GET","POST"])
def followingshop(id):
    return render_template("followingshop.html", Product=Product.query.all(), id=id)

@app.route('/follow/<uploader>',methods=['GET'])
def follow(uploader):
    followdata = FollowData()
    followdata.follower = session['user_id']
    followdata.following = uploader

    db.session.add(followdata)
    db.session.commit()

    flash('팔로우 완료')
    return redirect('/')

@app.route('/unfollow/<int:fid>',methods=['GET'])
def unfollow(fid):
    followdata = FollowData.query.filter_by(fid=fid).first()
    db.session.delete(followdata)
    db.session.commit()

    flash('팔로우 취소')
    return redirect('/')

@app.route("/sale", methods=["GET","POST"])
def sale():

    form = ProductForm()
    if form.validate_on_submit():
        filename: str = secure_filename(form.photo.data.filename)

        product = Product()
        product.uploader = session['user_id']
        product.photo = filename
        product.name = form.data.get('name')
        product.price = form.data.get('price')
        product.check = form.data.get('check')
        product.keyword = form.data.get('keyword')
        product.descript = form.data.get('descript')


        db.session.add(product)
        db.session.commit()
        flash('제품정보 등록완료')
        return redirect('/')

    return render_template('sale.html', form=form)

@app.route("/update/<int:pid>", methods=["GET","POST"])
def update(pid):

    form = ProductForm()
    if form.validate_on_submit():
        filename: str = secure_filename(form.photo.data.filename)

        update_product = Product.query.filter_by(pid=pid).first()
        update_product.uploader = session['user_id']
        update_product.photo = filename
        update_product.name = form.data.get('name')
        update_product.price = form.data.get('price')
        update_product.check = form.data.get('check')
        update_product.keyword = form.data.get('keyword')
        update_product.descript = form.data.get('descript')

        db.session.commit()
        flash('제품정보 수정완료')
        return redirect('/')

    return render_template('update.html', form=form, Product=Product.query.all())

@app.route("/search", methods=["GET","POST"])
def search():
    if request.method == 'GET':
        result = request.args.get('search_word')

    return render_template('search.html', Product=Product.query.all(), search_word=result, keyword=keyword)

@app.route("/detail/<int:pid>", methods=["GET","POST"])
def detail(pid):
    return render_template("detail.html", Product=Product.query.all(), pid=pid, FollowData=FollowData.query.all())

@app.route("/signup", methods=["GET","POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        select_user = User.query.filter_by().all()
        for user in select_user:
            if user.user_id == form.data.get('user_id'):
                flash('중복된 아이디입니다.')
                return redirect('/signup')

        user = User()
        user.user_id = form.data.get('user_id')
        user.user_pw = form.data.get('user_pw')

        db.session.add(user)
        db.session.commit()
        flash('회원가입 완료')

        return redirect('/login')

    return render_template('signup.html', form=form)

@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        select_user = User.query.filter_by().all()
        for user in select_user:
            if user.user_id == form.data.get('user_id') and user.user_pw == form.data.get('user_pw'):
                session['user_id'] = form.data.get('user_id')
                flash('로그인 완료')
                return redirect('/')

        flash('잘못된 아이디와 비밀번호입니다.')
        return redirect('/login')

    return render_template('login.html', form=form)

@app.route('/logout',methods=['GET'])
def logout():
    session.pop('user_id',None)
    flash('로그아웃 완료')
    return redirect('/')

if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(__file__))
    dbfile = os.path.join(basedir, 'db.sqlite')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '0000'

    csrf = CSRFProtect()
    csrf.init_app(app)

    db.init_app(app)
    db.app = app
    db.create_all()

    app.run(debug=True)