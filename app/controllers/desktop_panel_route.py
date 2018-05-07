import paramiko
from flask import Blueprint, render_template, redirect, url_for, request
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
def desktop_file(desktop_id):
    desktop = db.session.query(Desktop).filter(Desktop.id == desktop_id).first()

    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在known_hosts文件上的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname=desktop.server, port=desktop.port, username=desktop.user, password=desktop.server_password)
    # 执行命令

    stdin, stdout, stderr = ssh.exec_command('ls -lt')
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
            suffix = 'null'
        files.append([info_list[3], info_list[4], info_list[-1], filename, suffix])

    return render_template('desktop.html', files=files, desktop_id=desktop.id)


@panel.route('/desktop/cat/<int:desktop_id>/<string:filename>')
@panel.route('/desktop/cat/<int:desktop_id>/<string:filename>/<string:suffix>')
def file_cat(desktop_id, filename, suffix=None):
    desktop = db.session.query(Desktop).filter(Desktop.id == desktop_id).first()

    if suffix == 'null':
        return redirect(url_for('panel.file_cat', desktop_id=desktop_id, filename=filename))

    if suffix:
        file_name = filename + '.' + suffix
    else:
        file_name = filename
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在known_hosts文件上的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname=desktop.server, port=desktop.port, username=desktop.user, password=desktop.server_password)
    # 执行命令
    stdin, stdout, stderr = ssh.exec_command('cat {}'.format(file_name))
    # 获取结果
    result = stdout.read().decode()

    # 获取错误提示（stdout、stderr只会输出其中一个）
    err = stderr.read()
    # 关闭连接
    ssh.close()

    text = '<p><small>' + result.replace('\n', '<br>').replace(' ', '&nbsp;') + '</small></p>'

    return render_template('file_cat.html', text=text)


@panel.route('/desktop/remove/<int:desktop_id>/<string:filename>')
@panel.route('/desktop/remove/<int:desktop_id>/<string:filename>/<string:suffix>')
def file_remove(desktop_id, filename, suffix=None):
    desktop = db.session.query(Desktop).filter(Desktop.id == desktop_id).first()

    if suffix == 'null':
        file_name = filename

    else:
        file_name = filename + '.' + suffix
    print(file_name)
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在known_hosts文件上的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname=desktop.server, port=desktop.port, username=desktop.user, password=desktop.server_password)

    ssh.exec_command('rm {}'.format(file_name))

    ssh.close()

    return redirect(url_for('panel.desktop_file', desktop_id=desktop_id))


@panel.route('/desktop/rename/<int:desktop_id>/<string:filename>', methods=['POST'])
@panel.route('/desktop/rename/<int:desktop_id>/<string:filename>/<string:suffix>', methods=['POST'])
def file_rename(desktop_id, filename, suffix=None):
    if request.method == 'POST':
        name = request.form['name']
    else:
        return redirect(url_for('panel.desktop', desktop_id=desktop_id))
    desktop = db.session.query(Desktop).filter(Desktop.id == desktop_id).first()

    if suffix == 'null':
        return redirect(url_for('panel.file_rename_no_suffix', desktop_id=desktop_id, filename=filename, new_name=name))

    if suffix:
        file_name = filename + '.' + suffix
    else:
        file_name = filename
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在known_hosts文件上的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname=desktop.server, port=desktop.port, username=desktop.user, password=desktop.server_password)
    # 执行命令
    ssh.exec_command('mv {0} {1}'.format(file_name, name))

    # 关闭连接
    ssh.close()

    return redirect(url_for('panel.desktop_file', desktop_id=desktop_id))


@panel.route('/desktop/rename/<int:desktop_id>/<string:filename>/<string:new_name>', methods=['GET'])
def file_rename_no_suffix(desktop_id, filename, new_name):

    desktop = db.session.query(Desktop).filter(Desktop.id == desktop_id).first()

    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在known_hosts文件上的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname=desktop.server, port=desktop.port, username=desktop.user, password=desktop.server_password)
    # 执行命令
    ssh.exec_command('mv {0} {1}'.format(filename, new_name))

    # 关闭连接
    ssh.close()

    return redirect(url_for('panel.desktop_file', desktop_id=desktop_id))


@panel.route('/desktop/add/<int:desktop_id>', methods=['POST'])
def file_add(desktop_id):
    if request.method == 'POST':
        name = request.form['name']
    else:
        return redirect(url_for('panel.desktop', desktop_id=desktop_id))

    desktop = db.session.query(Desktop).filter(Desktop.id == desktop_id).first()

    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在known_hosts文件上的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname=desktop.server, port=desktop.port, username=desktop.user, password=desktop.server_password)
    # 执行命令
    ssh.exec_command('echo '' > {}'.format(name))

    ssh.close()

    return redirect(url_for('panel.desktop_file', desktop_id=desktop_id))


@panel.route('/desktop/change/<int:desktop_id>/<string:filename>', methods=['POST'])
@panel.route('/desktop/change/<int:desktop_id>/<string:filename>/<string:suffix>', methods=['POST'])
def file_change(desktop_id, filename, suffix=None):
    if request.method == 'POST':
        name = request.form['text']
    else:
        return redirect(url_for('panel.desktop', desktop_id=desktop_id))
    desktop = db.session.query(Desktop).filter(Desktop.id == desktop_id).first()

    if suffix == 'null':
        return redirect(url_for('panel.file_rename_no_suffix', desktop_id=desktop_id, filename=filename, new_name=name))

    if suffix:
        file_name = filename + '.' + suffix
    else:
        file_name = filename
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在known_hosts文件上的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname=desktop.server, port=desktop.port, username=desktop.user, password=desktop.server_password)
    # 执行命令
    ssh.exec_command('mv {0} {1}'.format(file_name, name))

    # 关闭连接
    ssh.close()

    return redirect(url_for('panel.desktop_file', desktop_id=desktop_id))


@panel.route('/desktop/change/<int:desktop_id>/<string:filename>/<string:new_name>', methods=['GET'])
def file_change_no_suffix(desktop_id, filename, new_name):

    desktop = db.session.query(Desktop).filter(Desktop.id == desktop_id).first()

    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在known_hosts文件上的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname=desktop.server, port=desktop.port, username=desktop.user, password=desktop.server_password)
    # 执行命令
    ssh.exec_command('mv {0} {1}'.format(filename, new_name))

    # 关闭连接
    ssh.close()

    return redirect(url_for('panel.desktop_file', desktop_id=desktop_id))