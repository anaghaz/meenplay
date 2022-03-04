from flask import Blueprint,render_template,session,request,url_for,redirect
from database import *

user=Blueprint('user',__name__)

@user.route('/user_home',methods=['get','post'])
def user_home():
	return render_template('user_home.html')

@user.route('/user_view_model',methods=['get','post'])
def user_view_model():
	user_id=session['user_id']
	data={}
	q="select * from model inner join car using(car_id)"
	res=select(q)
	data['model']=res
	if 'action' in request.args:
		action=request.args['action']
		model_id=request.args['model_id']
		rentalrate=request.args['rentalrate']
		extrarate=request.args['extrarate']
		
	else:
		action=None
	if action=="insert":
		amount=int(rentalrate)+int(extrarate)
		z="insert into booking values(null,'%s','%s','%s',curdate(),'pending')"%(user_id,model_id,amount)
		insert(z)		
	return render_template('user_view_model.html',data=data)

@user.route('/user_view_spareparts',methods=['get','post'])
def user_view_spareparts():
	user_id=session['user_id']
	data={}
	q="select * from spareparts inner join model using(model_id) inner join car using(car_id) inner join brand using(brand_id) inner join shops using(shop_id)"
	res=select(q)
	data['parts']=res
	return render_template('user_view_spareparts.html',data=data)

@user.route('/user_book_parts',methods=['get','post'])
def user_book_parts():
	user_id=session['user_id']
	data={}
	part_id=request.args['part_id']
	model_id=request.args['model_id']
	price=request.args['price']
	shop_id=request.args['shop_id']
	data['price']=price
	if 'submit' in request.form:
		quantity=request.form['quantity']
		amount=request.form['total_amount']
		q="select * from sbooking where user_id='%s' and status='pending'"%(user_id)
		res=select(q)
		data['sbook']=res
		if res:
			id=res[0]['sbooking_id']
			z="update sbooking set total=total+'%s' where sbooking_id='%s'"%(amount,id)
			update(z)
			x="select * from sbookingchild where sbooking_id='%s' and part_id='%s'"%(id,part_id)
			res1=select(x)
			if res1:
				y="update sbookingchild set amount=amount+'%s',quantity=quantity+'%s' where sbooking_id='%s' and part_id='%s'"%(amount,quantity,id,part_id)
				update(y)
				return redirect(url_for('user.user_home'))
			else:
				a="insert into sbookingchild values(null,'%s','%s','%s','%s')"%(id,part_id,quantity,amount)	
				insert(a)
				return redirect(url_for('user.user_home'))
		else:
			q1="insert into sbooking values(null,'%s','%s','%s',curdate(),'pending')"%(user_id,shop_id,amount)
			id=insert(q1)
			q2="insert into sbookingchild values(null,'%s','%s','%s','%s')"%(id,part_id,quantity,amount)
			insert(q2)
			return redirect(url_for('user.user_home'))		
	return render_template('user_book_parts.html',data=data)

@user.route('/user_view_booking',methods=['get','post'])
def user_view_booking():
	user_id=session['user_id']
	data={}
	q="select * from booking inner join model using(model_id) inner join car using(car_id) inner join brand using(brand_id) inner join shops using(shop_id) where user_id='%s'"%(user_id)
	res=select(q)
	data['book']=res
	q1="select * from sbooking inner join shops using(shop_id) where user_id='%s'"%(user_id)
	res1=select(q1)
	data['sbook']=res1
	return render_template('user_view_booking.html',data=data)

@user.route('/user_payment',methods=['get','post'])
def user_payment():
	data={}
	user_id=session['user_id']
	booking_id=request.args['booking_id']
	total=request.args['total']
	data['total']=total
	if 'submit' in request.form:
		amount=request.form['amount']
		q="insert into payment values(null,'%s','%s',curdate())"%(booking_id,amount)
		insert(q)
		z="update booking set status='paid' where user_id='%s' and booking_id='%s'"%(user_id,booking_id)
		update(z)
		return redirect(url_for('user.user_view_booking'))
	return render_template('user_payment.html',data=data)

@user.route('/user_makepayment',methods=['get','post'])
def user_makepayment():
	data={}
	user_id=session['user_id']
	sbooking_id=request.args['sbooking_id']
	total=request.args['total']
	data['total']=total
	if 'submit' in request.form:
		amount=request.form['amount']
		q="insert into payment values(null,'%s','%s',curdate())"%(sbooking_id,amount)
		insert(q)
		z="update sbooking set status='paid' where user_id='%s' and sbooking_id='%s'"%(user_id,sbooking_id)
		update(z)
	return render_template('user_payment.html',data=data)

@user.route('/user_add_rating',methods=['get','post'])
def user_add_rating():
	user_id=session['user_id']
	booking_id=request.args['booking_id']
	if 'submit' in request.form:
		rate=request.form['rate']
		review=request.form['review']
		q="insert into rating values(null,'%s','%s','%s',curdate())"%(booking_id,rate,review,)
		res=insert(q)
		return redirect(url_for('user.user_home'))
	return render_template('user_add_rating.html')

@user.route('/user_add_ratings',methods=['get','post'])
def user_add_ratings():
	user_id=session['user_id']	
	sbooking_id=request.args['sbooking_id']
	if 'submit' in request.form:
		rate=request.form['rate']
		review=request.form['review']
		q="insert into rating values(null,'%s','%s','%s',curdate())"%(sbooking_id,rate,review,)
		res=insert(q)
		return redirect(url_for('user.user_home'))
	return render_template('user_add_rating.html')

@user.route('/user_send_complaint',methods=['get','post'])
def user_send_complaint():
	user_id=session['user_id']
	if 'submit' in request.form:
		complaint=request.form['complaint']
		q="insert into complaint values(null,'%s','%s','pending',curdate())"%(user_id,complaint)
		insert(q)
	return render_template('user_send_complaint.html')	

@user.route('/user_view_notification',methods=['get','post'])
def user_view_notification():
	data={}
	q="select * from notification"
	res=select(q)
	data['noti']=res
	return render_template('user_view_notification.html',data=data)	

@user.route('/user_view_reply',methods=['get','post'])
def user_view_reply():
	data={}
	user_id=session['user_id']
	q="select * from complaint where user_id='%s'"%(user_id)
	res=select(q)
	data['reply']=res
	return render_template('user_view_reply.html',data=data)

@user.route('/user_logout',methods=['get','post'])
def user_logout():
	if not session.get("lid") is None:
		return redirect(url_for("public.home"))
	else:
		return redirect(url_for("user.user_home"))

@user.route('/user_chat',methods=['get','post'])
def user_chat():
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
		return redirect(url_for('user.user_chat',lids=rids))
	return render_template('user_chat_shop.html',data=data)

@user.route('/user_view_chatingusers',methods=['get','post'])
def user_view_chatingusers():
	data={}
	lid=session['lid']
	q="select * from shops where login_id in (select if(sender_id='%s',reciever_id,sender_id) from chat where sender_id='%s' or reciever_id='%s')" %(lid,lid,lid)
	print(q)
	res=select(q)
	data['chat']=res
	return render_template('user_view_chatingusers.html',data=data)	