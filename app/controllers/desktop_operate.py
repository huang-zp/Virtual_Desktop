import paramiko
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import User_Desktop, Desktop
from app.engines import db

desktop_operate = Blueprint('desktop_operate', __name__, url_prefix='')
param_location = ('json', )


@desktop_operate.route('/desktop/list')
@login_required
def desktop_list():
    desktop_id_list = db.session.query(User_Desktop.desktop_id).filter(User_Desktop.user_id == current_user.id).all()
    if desktop_id_list:
        desktop_id_list = [value[0] for value in desktop_id_list]

    desktops = db.session.query(Desktop).filter(Desktop.id.in_(desktop_id_list)).all()
    return render_template('desktop_list.html', desktops=desktops)


@desktop_operate.route('/desktop/delete/<int:desktop_id>')
def desktop_delete(desktop_id):
    desktop = db.session.query(Desktop).filter(Desktop.id == desktop_id).first()
    db.session.delete(desktop)
    db.session.commit()
    return redirect(url_for('desktop_operate.desktop_list'))


@desktop_operate.route('/desktop/add', methods=['POST', 'GET'])
def desktop_add():
    if request.method == 'POST':

        server_user = request.form['server_user']

        server_password = request.form['server_password']
        server_ip = request.form['server_ip']
        server_name = request.form['server_name']
        server_system = request.form['server_system']
        server_port = request.form['server_port']
        desktop_desc = request.form['desktop_desc']
        if server_user == '' or server_ip == '' or server_password == '':
            flash(" 检查某些字段是否为空")
            return redirect(url_for('desktop_operate.desktop_add'))

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=server_ip, port=22, username=server_user, password=server_password)
        except Exception as e:
            flash("服务器IP、用户名、密码可能错误")
            return redirect(url_for('desktop_operate.desktop_add'))

        desktop = Desktop()
        desktop.server_password = server_password
        desktop.user = server_user
        desktop.name = server_name
        desktop.system = server_system
        desktop.port = server_port
        desktop.server = server_ip
        desktop.description = desktop_desc
        db.session.add(desktop)
        db.session.commit()
        db.session.query(Desktop).order_by(Desktop.create_time.desc()).filter(Desktop.server == server_ip).first()
        user_desktop = User_Desktop()
        user_desktop.user_id = current_user.id
        user_desktop.desktop_id = desktop.id
        db.session.add(user_desktop)
        db.session.commit()
        return redirect(url_for('desktop_operate.desktop_list'))

    return render_template('desktop_add.html')


@desktop_operate.route('/desktop/change/<int:desktop_id>', methods=['POST', 'GET'])
def desktop_change(desktop_id):
    desktop = db.session.query(Desktop).filter(Desktop.id == desktop_id).first()
    if request.method == 'POST':

        server_user = request.form['server_user']

        server_password = request.form['server_password']
        server_ip = request.form['server_ip']
        server_name = request.form['server_name']
        server_system = request.form['server_system']
        server_port = request.form['server_port']
        desktop_desc = request.form['desktop_desc']
        if server_user == '' or server_ip == '' or server_password == '':
            flash(" 检查某些字段是否为空")
            return redirect(url_for('desktop_operate.desktop_change', desktop_id=desktop.id))

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=server_ip, port=22, username=server_user, password=server_password)
        except Exception as e:
            flash("服务器IP、用户名、密码可能错误")
            return redirect(url_for('desktop_operate.desktop_change', desktop_id=desktop.id))

        desktop.server_password = server_password
        desktop.user = server_user
        desktop.name = server_name
        desktop.system = server_system
        desktop.port = server_port
        desktop.server = server_ip
        desktop.description = desktop_desc
        db.session.add(desktop)
        db.session.query(Desktop).order_by(Desktop.create_time.desc()).filter(Desktop.server == server_ip).first()
        user_desktop = User_Desktop()
        user_desktop.user_id = current_user.id
        user_desktop.desktop_id = desktop.id
        db.session.add(user_desktop)
        db.session.commit()
        return redirect(url_for('desktop_operate.desktop_list'))
    return render_template('desktop_change.html', desktop=desktop)
