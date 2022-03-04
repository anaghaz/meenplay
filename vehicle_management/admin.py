from flask import Blueprint,render_template,session,request,url_for,redirect
from database import *
admin=Blueprint('admin',__name__)

@admin.route('/admin_home')
def admin_home():
	return render_template('admin_home.html')

@admin.route('/admin_view_shop',methods=['get','post'])
def admin_view_shop():
	data={}
	q="select * from shops"
	res=select(q)
	data['shop']=res
	if 'action' in request.args:
		action=request.args['action']
		login_id=request.args['login_id']
	else:
		action=None
	if action=="accept":
		z="update login set usertype='shop' where login_id='%s'"%(login_id)
		update(z)
	if action=="reject":
		z="update login set usertype='reject' where login_id='%s'"%(login_id)
		update(z)			
	return render_template('admin_view_shop.html',data=data)

@admin.route('/admin_view_model',methods=['get','post'])
def admin_view_model():	
	data={}
	q="select * from model inner join car using(car_id)"
	res=select(q)
	data['model']=res
	return render_template('admin_view_model.html',data=data)	

@admin.route('/admin_view_booking',methods=['get','post'])
def admin_view_booking():
	data={}
	q="select * from booking inner join model using(model_id) inner join users using(user_id)"
	res=select(q)
	data['book']=res
	q1="select * from sbooking inner join shops using(shop_id) inner join users using(user_id)"
	res1=select(q1)
	data['sbook']=res1
	return render_template('admin_view_booking.html',data=data)		

@admin.route('/admin_view_bookingusers',methods=['get','post'])
def admin_view_bookingusers():
	data={}
	user_id=request.args['user_id']
	q="select * from users where user_id='%s'"%(user_id)
	res=select(q)
	data['user']=res
	return render_template('admin_view_bookingusers.html',data=data)

@admin.route('admin_view_complaints',methods=['get','post'])
def admin_view_complaints():
	data={}
	q="select * from complaint inner join users using(user_id)"
	res=select(q)
	data['complaintsview']=res
	j=0
	for i in range(1,len(res)+1):
		print('submit'+str(i))
		if 'submit'+str(i) in request.form:
			reply=request.form['reply'+str(i)]
			print(reply)
			print(j)
			print(res[j]['complaint_id'])
			q="update complaint set reply='%s' where complaint_id='%s'"%(reply,res[j]['complaint_id'])
			update(q)
			return redirect(url_for('admin.admin_view_complaints'))
	j=j+1
	return render_template('admin_view_complaints.html',data=data)

@admin.route('admin_send_notification',methods=['get','post'])
def admin_send_notification():
	if 'submit' in request.form:
		notification=request.form['notification']
		description=request.form['description']
		q="insert into notification values(null,'%s','%s',curdate())"%(notification,description)
		insert(q)
	return render_template('admin_send_notification.html')

@admin.route('/admin_logout',methods=['get','post'])
def admin_logout():
	if not session.get("lid") is None:
		return redirect(url_for("public.home"))
	else:
		return redirect(url_for("admin.admin_home"))			