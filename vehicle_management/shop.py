from flask import Blueprint,render_template,session,request,url_for,redirect
from database import *
import uuid
shop=Blueprint('shop',__name__)

@shop.route('/shop_home')
def shop_home():
	return render_template('shop_home.html')

@shop.route('/shop_manage_brand',methods=['get','post'])
def shop_manage_brand():
	data={}
	shop_id=session['shop_id']
	if 'submit' in request.form:
		brandname=request.form['brandname']
		q="insert into brand values(null,'%s','%s')"%(shop_id,brandname)
		insert(q)
		return redirect(url_for('shop.shop_home'))
	q="select * from brand where shop_id='%s'"%(shop_id)
	res=select(q)
	data['brand']=res	
	return render_template('shop_manage_brand.html',data=data)	

@shop.route('/shop_add_car',methods=['get','post'])
def shop_add_car():
	shop_id=session['shop_id']
	brand_id=request.args['brand_id']
	if 'submit' in request.form:
		car=request.form['car']
		q="insert into car values(null,'%s','%s')"%(brand_id,car)
		insert(q)
	return render_template('shop_add_car.html')	

@shop.route('/shop_view_car',methods=['get','post'])
def shop_view_car():
	shop_id=session['shop_id']
	data={}
	q="select * from car inner join brand using(brand_id) inner join shops using(shop_id) where shop_id='%s'"%(shop_id)
	res=select(q)
	data['car']=res
	return render_template('shop_view_car.html',data=data)	

@shop.route('/shop_add_model',methods=['get','post'])
def shop_add_model():
	
	car_id=request.args['car_id']
	shop_id=session['shop_id']
	if 'submit' in request.form:
		modelname=request.form['modelname']
		variant=request.form['variant']
		plate_no=request.form['plate_no']
		chasisno=request.form['chasisno']
		color=request.form['color']
		transmission=request.form['transmission']
		mileage=request.form['mileage']
		ctype=request.form['type']
		rentalrate=request.form['rentalrate']
		extrarate=request.form['extrarate']
		q="insert into model values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(car_id,modelname,variant,plate_no,chasisno,color,transmission,mileage,ctype,rentalrate,extrarate)
		insert(q)
		
	return render_template('shop_add_model.html')

@shop.route('/shop_view_model',methods=['get','post'])
def shop_view_model():
	shop_id=session['shop_id']
	data={}
	q="select * from model inner join car using(car_id) inner join brand using(brand_id) inner join shops using(shop_id) where shop_id='%s'"%(shop_id)
	res=select(q)
	data['model']=res
	return render_template('shop_view_model.html',data=data)

@shop.route('/shop_add_parts',methods=['get','post'])
def shop_add_parts():
	car_id=request.args['car_id']
	model_id=request.args['model_id']
	if 'submit' in request.form:
		partname=request.form['partname']
		description=request.form['description']
		price=request.form['price']
		image=request.files['image']
		path="static/uploads/"+str(uuid.uuid4())+image.filename
		image.save(path)
		q="insert into spareparts values(null,'%s','%s','%s','%s','%s')"%(model_id,partname,description,price,path)
		insert(q)
	return render_template('shop_add_parts.html')

@shop.route('/shop_view_booking',methods=['get','post'])
def shop_view_booking():
	shop_id=session['shop_id']
	data={}
	q="select * from booking inner join model using(model_id) inner join car using(car_id) inner join brand using(brand_id) inner join shops using(shop_id) inner join users using(user_id) where shop_id='%s'"%(shop_id)
	res=select(q)
	data['book']=res
	
	if 'action' in request.args:
		action=request.args['action']
		booking_id=request.args['booking_id']	
	else:
		action=None
	if action=="accept":
		q1="update booking set status='accept' where booking_id='%s'"%(booking_id)
		update(q1)
		return redirect(url_for('shop.shop_home'))
	if action=="reject":
		q2="update booking set status='reject' where booking_id='%s'"%(booking_id)
		update(q2)
		return redirect(url_for('shop.shop_home'))
	return render_template('shop_view_booking.html',data=data)

@shop.route('/shop_view_user',methods=['get','post'])
def shop_view_user():
	shop_id=session['shop_id']
	data={}
	user_id=request.args['user_id']
	booking_id=request.args['booking_id']
	q="select * from users where user_id='%s'"%(user_id)
	res=select(q)
	data['user']=res
	return render_template('shop_view_user.html',data=data)	

@shop.route('/shop_view_sbooking',methods=['get','post'])
def shop_view_sbooking():
	shop_id=session['shop_id']
	data={}
	z="select * from sbooking inner join users using(user_id) inner join shops using(shop_id) where shop_id='%s'"%(shop_id)
	res1=select(z)
	data['sbook']=res1
	if 'action' in request.args:
		action=request.args['action']
		sbooking_id=request.args['sbooking_id']	
	else:
		action=None	
	if action=="accept1":
		q3="update sbooking set status='accept' where sbooking_id='%s'"%(sbooking_id)
		update(q3)
	if action=="reject1":
		q4="update sbooking set status='reject' where sbooking_id='%s'"%(sbooking_id)
		update(q4)
	return render_template('shop_view_partsbooking.html',data=data)				

@shop.route('/shop_view_rating',methods=['get','post'])
def shop_view_rating():
	shop_id=session['shop_id']
	data={}
	q="select * from rating inner join booking using(booking_id) inner join model using(model_id) inner join car using(car_id) inner join brand using(brand_id) inner join shops using(shop_id) inner join users using(user_id) where shop_id='%s'"%(shop_id)
	res=select(q)
	data['rate']=res
	return render_template('shop_view_rating.html',data=data)

@shop.route('/shop_view_payment',methods=['get','post'])
def shop_view_payment():
	shop_id=session['shop_id']
	data={}
	booking_id=request.args['booking_id']
	user_id=request.args['user_id']
	q="select * from payment inner join booking using(booking_id) inner join model using(model_id) where booking_id='%s' and user_id='%s'"%(booking_id,user_id)
	res=select(q)
	data['pay']=res
	return render_template('shop_view_payment.html',data=data)	

@shop.route('/shop_view_parts_payment',methods=['get','post'])
def shop_view_parts_payment():
	data={}
	shop_id=session['shop_id']
	booking_id=request.args['sbooking_id']
	user_id=request.args['user_id']
	q="select * from payment where booking_id='%s'"%(booking_id)
	res=select(q)
	data['pay']=res
	return render_template('shop_view_parts_payment.html',data=data)						

@shop.route('/shop_view_notification',methods=['get','post'])
def shop_view_notification():
	data={}
	q="select * from notification"
	res=select(q)
	data['noti']=res
	return render_template('shop_view_notification.html',data=data)

@shop.route('/shop_logout',methods=['get','post'])
def shop_logout():
	if not session.get("lid") is None:
		return redirect(url_for("public.home"))
	else:
		return redirect(url_for("shop.shop_home"))

@shop.route('/shop_chat_user',methods=['get','post'])
def shop_chat_user():
	lid=session['lid']
	data={}
	data['lid']=lid
	rids=request.args['lids']
	q="select * from chat where (sender_id='%s' and reciever_id='%s') or (sender_id='%s' and reciever_id='%s')" %(lid,rids,rids,lid)
	res=select(q)
	data['chat']=res
	if 'submit' in request.form:
		chat=request.form['reply']
		z="insert into chat values(null,'%s','%s','%s',curdate())"%(lid,rids,chat)
		insert(z)
		return redirect(url_for('shop.shop_chat_user',lids=rids))
	return render_template('shop_chat_user.html',data=data)

@shop.route('/shop_view_chatingusers',methods=['get','post'])
def shop_view_chatingusers():
	data={}
	lid=session['lid']
	q="select * from users where login_id in (select if(sender_id='%s',reciever_id,sender_id) from chat where sender_id='%s' or reciever_id='%s')" %(lid,lid,lid)
	print(q)
	res=select(q)
	data['chat']=res
	return render_template('shop_view_chatingusers.html',data=data)
