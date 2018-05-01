import paramiko
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import User_Desktop, Desktop
from app.engines import db

panel = Blueprint('panel', __name__, url_prefix='')
param_location = ('json', )


@panel.route('/desktop/panel')
@login_required
def desktop_panel():
    desktop_id_list = db.session.query(User_Desktop.desktop_id).filter(User_Desktop.user_id == current_user.id).all()
    if desktop_id_list:
        desktop_id_list = [value[0] for value in desktop_id_list]

    desktops = db.session.query(Desktop).filter(Desktop.id.in_(desktop_id_list)).all()
    return render_template('desktop_panel.html', desktops=desktops)


@panel.route('/desktop/<int:desktop_id>')
def desktop(desktop_id):
    desktop = db.session.query(Desktop).filter(Desktop.id == desktop_id).first()

    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在known_hosts文件上的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname=desktop.server, port=desktop.port, username=desktop.user, password=desktop.server_password)
    # 执行命令
    if 'Mac' in desktop.system:
        stdin, stdout, stderr = ssh.exec_command('cd Desktop && ls -l')
    else:
        stdin, stdout, stderr = ssh.exec_command('cd Desktop && ls -l')
    # 获取结果
    result = stdout.read().decode()

    # 获取错误提示（stdout、stderr只会输出其中一个）
    err = stderr.read()
    # 关闭连接
    ssh.close()
    files = []
    result_lists = result.split('\n')
    for result in result_lists[1:-1]:
        info = ' '.join(result.split())
        info_list = info.split(' ')
        if '.' in info_list[-1]:
            filename = info_list[-1].split('.')[0]
            suffix = info_list[-1].split('.')[1]
        else:
            filename = info_list[-1]
            suffix = ''
        files.append([info_list[3], info_list[4], info_list[-1], filename, suffix])

    return render_template('desktop.html', files=files, desktop_id=desktop.id)


@panel.route('/desktop/cat/<int:desktop_id>/<string:filename>/<string:suffix>')
def file_cat(desktop_id, filename, suffix):
    desktop = db.session.query(Desktop).filter(Desktop.id == desktop_id).first()
    file = filename + '.'+ suffix
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在known_hosts文件上的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname=desktop.server, port=desktop.port, username=desktop.user, password=desktop.server_password)
    # 执行命令
    stdin, stdout, stderr = ssh.exec_command('cd Desktop && cat {}'.format(file))
    # 获取结果
    result = stdout.read().decode()

    # 获取错误提示（stdout、stderr只会输出其中一个）
    err = stderr.read()
    # 关闭连接
    ssh.close()

    text = '<p><small>' + result.replace('\n', '<br>').replace(' ', '&nbsp;') + '</small></p>'

    print(text)
    return render_template('file_cat.html', text=text)


@panel.route('/desktop/remove/<int:desktop_id>/<string:filename>/<string:suffix>')
def file_remove(desktop_id, filename, suffix):
    desktop = db.session.query(Desktop).filter(Desktop.id == desktop_id).first()

    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在known_hosts文件上的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname=desktop.server, port=desktop.port, username=desktop.user, password=desktop.server_password)
    # 执行命令
    if 'Mac' in desktop.system:
        stdin, stdout, stderr = ssh.exec_command('cd Desktop && ls -l')
    else:
        stdin, stdout, stderr = ssh.exec_command('cd Desktop && ls -l')
    # 获取结果
    result = stdout.read().decode()

    # 获取错误提示（stdout、stderr只会输出其中一个）
    err = stderr.read()
    # 关闭连接
    ssh.close()
    files = []
    result_lists = result.split('\n')
    for result in result_lists[1:-1]:
        info = ' '.join(result.split())
        info_list = info.split(' ')

        files.append([info_list[3], info_list[4], info_list[-1]])

    return render_template('desktop.html', files=files, desktop_id=desktop.id)


@panel.route('/desktop/rename/<int:desktop_id>/<string:filename>/<string:suffix>')
def file_rename(desktop_id, filename, suffix):
    desktop = db.session.query(Desktop).filter(Desktop.id == desktop_id).first()

    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在known_hosts文件上的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname=desktop.server, port=desktop.port, username=desktop.user, password=desktop.server_password)
    # 执行命令
    if 'Mac' in desktop.system:
        stdin, stdout, stderr = ssh.exec_command('cd Desktop && ls -l')
    else:
        stdin, stdout, stderr = ssh.exec_command('cd Desktop && ls -l')
    # 获取结果
    result = stdout.read().decode()

    # 获取错误提示（stdout、stderr只会输出其中一个）
    err = stderr.read()
    # 关闭连接
    ssh.close()
    files = []
    result_lists = result.split('\n')
    for result in result_lists[1:-1]:
        info = ' '.join(result.split())
        info_list = info.split(' ')

        files.append([info_list[3], info_list[4], info_list[-1]])

    return render_template('desktop.html', files=files, desktop_id=desktop.id)


@panel.route('/desktop/add/<int:desktop_id>/<string:filename>/<string:suffix>')
def file_add(desktop_id, filename, suffix):
    desktop = db.session.query(Desktop).filter(Desktop.id == desktop_id).first()

    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在known_hosts文件上的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname=desktop.server, port=desktop.port, username=desktop.user, password=desktop.server_password)
    # 执行命令
    if 'Mac' in desktop.system:
        stdin, stdout, stderr = ssh.exec_command('cd Desktop && ls -l')
    else:
        stdin, stdout, stderr = ssh.exec_command('cd Desktop && ls -l')
    # 获取结果
    result = stdout.read().decode()

    # 获取错误提示（stdout、stderr只会输出其中一个）
    err = stderr.read()
    # 关闭连接
    ssh.close()
    files = []
    result_lists = result.split('\n')
    for result in result_lists[1:-1]:
        info = ' '.join(result.split())
        info_list = info.split(' ')

        files.append([info_list[3], info_list[4], info_list[-1]])

    return render_template('desktop.html', files=files, desktop_id=desktop.id)