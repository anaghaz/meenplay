from flask import Blueprint,render_template,request,redirect,url_for,session
from database import *
public=Blueprint('public',__name__)

@public.route('/')
def home():
	return render_template('index.html')

@public.route('/login',methods=['get','post'])
def login():
	if 'submit' in request.form:
		username=request.form['username']
		password=request.form['password']
		q="select * from login where username='%s' and password='%s'"%(username,password)
		res=select(q)
		if res:
			session['lid']=res[0]['login_id']
			if res[0]['usertype']=="admin":
				z="select * from login where login_id='%s'"%(session['lid'])
				a=select(z)
				if a:
					session['login_id']=a[0]['login_id']
					return redirect(url_for('admin.admin_home'))
			elif res[0]['usertype']=="shop":
				z="select * from shops where login_id='%s'"%(session['lid'])
				a=select(z)
				if a:
					session['shop_id']=a[0]['shop_id']
					return redirect(url_for('shop.shop_home'))
			elif res[0]['usertype']=="user":
				z="select * from users where login_id='%s'"%(session['lid'])
				a=select(z)
				if a:
					session['user_id']=a[0]['user_id']
					return redirect(url_for('user.user_home'))				
	return render_template('login.html')

@public.route('/shop_register',methods=['get','post'])
def shop_register():
	if 'submit' in request.form:
		shop_name=request.form['shop_name']
		place=request.form['place']
		phone=request.form['phone']
		email=request.form['email']
		licensenumber=request.form['licensenumber']
		password=request.form['password']
		q="insert into login values(null,'%s','%s','pending')"%(shop_name,password)
		id=insert(q)
		z="insert into shops values(null,'%s','%s','%s','%s','%s','%s')"%(id,shop_name,place,phone,email,licensenumber)
		insert(z)
	return render_template('shop_register.html')

@public.route('/user_register',methods=['get','post'])
def user_register():
	if 'submit' in request.form:
		firstname=request.form['firstname']
		lastname=request.form['lastname']
		place=request.form['place']
		phone=request.form['phone']
		email=request.form['email']
		license=request.form['license']
		gender=request.form['gender']
		adhar=request.form['adhar']
		password=request.form['password']
		q="insert into login values(null,'%s','%s','user')"%(firstname,password)
		id=insert(q)
		z="insert into users values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(id,firstname,lastname,place,phone,email,license,gender,adhar)
		insert(z)
	return render_template('user_register.html')			