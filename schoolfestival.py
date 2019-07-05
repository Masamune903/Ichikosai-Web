"""
If you are a member of erectronocal comunication club and want to edit this file,
please download this file and use text editor even if you don't have to do so.
"""
import datetime
from flask import Flask,request,json,jsonify
import ssl
import mysql.connector
import hashlib
from flask_cors import CORS
isRain = False
update = 1
app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('/etc/letsencrypt/live/ichikosai.net/cert.pem',
                        '/etc/letsencrypt/live/ichikosai.net/privkey.pem')
def singleProject(where):#例外処理OK
    try:
        conn = mysql.connector.connect(user='user_name',password='xMw5jVwq',host='localhost',database='schoolfestival')
        cur = conn.cursor()
        cur.execute("SELECT cat,`key`,manager_name,project,id from projects WHERE `key` = '" + where + "';")
        column = cur.fetchall()
    except Exception as e:
        print('想定外のエラー')
        print(e.args)
        print('データベース接続in　singleProject')
        return []
    if len(column) == 0:
        return column
        #対応する名前の企画なし
    else:
        return column[0]
        #対応する名前の企画あり
def login(req,_type):#例外処理OK
    if _type == 'normal':
        try:
            #POSTデコーディングinログイン
            body = req
            key=body['key']
        except IndexError as e:
            print (e.args)
            print('POSTデコーディングinログイン')
            print(body)
            #パラメーターに空文字列の可能性
            return {'result':'error'},''
        except Exception as e:
            print('想定外のエラー')
            print (e.args)
            print('POSTデコーディングinログイン')
            print(body)
            return {'result':'error'},''
        try:
            #MySQL接続inログイン
            conn = mysql.connector.connect(user='user_name',password='xMw5jVwq',host='localhost',database='schoolfestival')
            cur = conn.cursor()
            cur.execute("SELECT password from projects WHERE `key` = '" + key +"';")
            column = cur.fetchall()   
            cur.close()
            conn.close()
            if column == []:
                print(body)
                return jsonify({'result':'fail'})
        except KeyError as e:
            print(e.args)
            print('MySQL接続inログイン')
            print(body)
            return {'result':'error'},''
            #パラメーターのKEYにkeyが含まれていない可能性
        except Exception as e:
            print('想定外のエラー')
            print (e.args)
            print('MySQL接続inログイン')
            print(body)
            return {'result':'error'},''
        try:
            #パスワード評価inログイン
            md5 = hashlib.md5()
            encoded = body['pass'].encode('utf-8')
            md5.update(encoded)
            password = md5.hexdigest()
            return column[0][0] == password,body
        except KeyError as e:
            print(type(e))
            print(e.args)
            print(e)
            print('パスワード評価inログイン')
            print(body)
            return {'result':'error'},''
            #パラメーターのKEYにpasswordが含まれていない、もしくはpasswordの値がNoneなどの不正な値の可能性
        except IndexError as e:
            print(type(e))
            print(e.args)
            print(e)
            print('パスワード評価inログイン')
            print(body)
            return {'result':'error'},''
            #keyの中身が存在しないアカウントを指定している可能性
        except Exception as e:
            print('想定外のエラー')
            print (e.args)
            print('パスワード評価inログイン')
            print(body)
            return {'result':'error'},''
    elif _type == 'super':
        try:
            #POSTデコーディングinログイン
            body = req
        except IndexError as e:
            print (e.args)
            print('POSTデコーディングinログイン')
            print(body)
            #パラメーターに空文字列の可能性
            return {'result':'error'},''
        except Exception as e:
            print('想定外のエラー')
            print (e.args)
            print('POSTデコーディングinログイン')
            print(body)
            return {'result':'error'},''
        if body['key'] == 'adm':
            try:
                #MySQL接続inログイン
                conn = mysql.connector.connect(user='user_name',password='xMw5jVwq',host='localhost',database='schoolfestival')
                cur = conn.cursor()
                cur.execute("SELECT content from specialinformation WHERE `title` = 'adm';")
                column = cur.fetchall()   
                cur.close()
                conn.close()
            except KeyError as e:
                print(e.args)
                print('MySQL接続inログイン')
                print(body)
                return {'result':'error'},''
                #パラメーターのKEYにkeyが含まれていない可能性
            except Exception as e:
                print('想定外のエラー')
                print (e.args)
                print('MySQL接続inログイン')
                print(body)
                return {'result':'error'},''
            try:
                #パスワード評価inログイン
                md5 = hashlib.md5()
                encoded = body['pass'].encode('utf-8')
                md5.update(encoded)
                password = md5.hexdigest()
                return column[0][0] == password,body
            except KeyError as e:
                print(type(e))
                print(e.args)
                print(e)
                print('パスワード評価inログイン')
                print(body)
                return {'result':'error'},''
                #パラメーターのKEYにpasswordが含まれていない、もしくはpasswordの値がNoneなどの不正な値の可能性
            except IndexError as e:
                print(type(e))
                print(e.args)
                print(e)
                print('パスワード評価inログイン')
                print(body)
                return {'result':'error'},''
                #keyの中身が存在しないアカウントを指定している可能性
            except Exception as e:
                print('想定外のエラー')
                print (e.args)
                print('パスワード評価inログイン')
                print(body)
                return {'result':'error'},''
        else:
            return {'result':'error'},''
    else :
        return {'result':'error'},''
    #------------------------------------------------------------------    
@app.route('/add',methods=['POST'])
def makeProjects():
    conn = mysql.connector.connect(user='user_name',password='xMw5jVwq',host='localhost',database='schoolfestival')
    params = request.get_json()
    cat = params['cat']
    manager_name = params['manager_name']
    key = params['key']
    id = params['id']
    project = params['project']
    md5 = hashlib.md5()
    encoded = params['pass'].encode('utf-8')
    md5.update(encoded)
    password = md5.hexdigest()
        
    cur = conn.cursor()

    mysql_sentence = "INSERT INTO projects (cat,manager_name,password,`key`,project,wait,status,id) VALUES ('" + cat + "','"+ manager_name + "','" + password + "','"+ key + "','"+ project +"','0','preparing','" + id + "');"
    cur.execute(mysql_sentence)
    cur.close()
    conn.commit()
    conn.close()
    msg = {
        "mode":"It is add"
    }
    return jsonify(msg)
@app.route('/login',methods=['POST'])
def loginMethod():#例外処理OK
    data = request.get_json()
    evalation,_ = login(req=data,_type='normal')
    if evalation == True:
        return jsonify({'result':'success'})
    elif evalation == False:
        return jsonify({'result':'fail'})
    else:
        return jsonify(evalation)
@app.route('/wait/<string:updCount>',methods = ['GET'])
def wait(updCount):
    try:
        global update
        global isRain
    except Exception as e:
        print('想定外のエラー')
        print(e.args)
        print('パラメータ取得in待ち時間取得')
        print(updCount)
        return jsonify({'result':'error'})
    if updCount != str(update):
        try:
            conn = mysql.connector.connect(user='user_name',password='xMw5jVwq',host='localhost',database='schoolfestival')
            cur = conn.cursor()
            cur.execute("SELECT `key`,wait,status from projects;")
            columns = cur.fetchall()
            #('wait')
            cur.close()
            conn.close()
        except Exception as e:
            print('想定外のエラー')
            print(e.args)
            print('データベース接続in待ち時間取得')
            print(updCount)
            return jsonify({'result':'error'})
        try:
            congData = {}
            msg = {'state':'updated','updCount':update,'isRain':isRain}
        except Exception as e:
            print('想定外のエラー')
            print(e.args)
            print('データベース接続in待ち時間取得')
            print(updCount)
            return jsonify({'result':'error'})
        try:
            for column in columns:
                congData[column[0]]={'condition':column[2],'val':column[1]}
        except IndexError as e:
            print(e.args)
            print('データ取得in待ち時間取得')
            print(updCount)
            return jsonify({'result':'error'})
            #データベースに必要なデータが入っていない
        except Exception as e:
            print('想定外のエラー')
            print(e.args)
            print('データ取得in待ち時間取得')
            print(updCount)
            return jsonify({'result':'error'})
        try:
            msg['congData'] = congData
            msg['result'] = 'success'
            return jsonify(msg)
        except Exception as e:
            print('想定外のエラー')
            print(e.args)
            print('更新ありレスポンスデータ作成in待ち時間取得')
            print(updCount)
            return jsonify({'result':'error'})
    else:
        try:
            msg = {'state':'noUpd','result':'success','updCount':update}
            return jsonify(msg)
        except Exception as e:
            print('想定外のエラー')
            print(e.args)
            print('更新なしレスポンスデータ作成in待ち時間取得')
            print(updCount)
            return jsonify({'result':'error'})
@app.route('/list/<string:key>',methods = ['GET'])
def projectlist(key):
    result = ''
    if key == '*':
        try:
            conn = mysql.connector.connect(user='user_name',password='xMw5jVwq',host='localhost',database='schoolfestival')
            cur = conn.cursor()
            cur.execute("SELECT cat,`key`,manager_name,project,id from projects;")
            columns = cur.fetchall()
            #('cat', 'name', 'icon','project')
            cur.close()
            conn.close()
            msg = {}
            classProjects = {}
            volunteerProjects = {}
            marketingProjects = {}
        except Exception as e:
            print('想定外のエラー')
            print(e.args)
            print('データベース接続in一覧取得')
            print(key)
            return jsonify({'result':'error'})
        try:
            for column in columns:
                if column[0] == 'cls1':
                    manager = {'grade':1,'name':column[2],'index':column[4]}
                    classProjects[column[1]] = {'manager':manager,'project':json.loads(column[3])}
                if column[0] == 'cls2':
                    manager = {'grade':2,'name':column[2],'index':column[4]}
                    classProjects[column[1]] = {'manager':manager,'project':json.loads(column[3])}
                if column[0] == 'cls3':
                    manager = {'grade':3,'name':column[2],'index':column[4]}
                    classProjects[column[1]] = {'manager':manager,'project':json.loads(column[3])}
                if column[0] == 'vol':
                    manager = {'grade':0,'name':column[2],'index':column[4]}
                    volunteerProjects[column[1]] = {'manager':manager,'project':json.loads(column[3])}
                if column[0] == 'com':
                    manager = {'grade':0,'name':column[2],'index':column[4]}
                    marketingProjects[column[1]] = {'manager':manager,'project':json.loads(column[3])}
            msg ={'classProjects':classProjects,'volunteerProjects':volunteerProjects,'marketingProjects':marketingProjects}
            pro = {'projects':msg,'result':'success'}
        except KeyError as e:
            print(e.args)
            print('レスポンスデータ作成in一覧取得')
            print(key)
            return jsonify({'result':'error'})
            #データベースに必要なデータが含まれていない可能性
        except Exception as e:
            print('想定外のエラー')
            print(e.args)
            print('レスポンスデータ作成in一覧取得')
            print(key)
            return jsonify({'result':'error'})
        try:
            return jsonify(pro)
        except Exception as e:
            print('想定外のエラー')
            print(e.args)
            print('レスポンスデータ変換in一覧取得')
            print(key)
            return jsonify({'result':'error'})
    else:
        msg = {}
        columns = []
        classProjects = {}
        volunteerProjects = {}
        marketingProjects = {}
        if isinstance(key,list):
            pass
        else:
            key = [key]
        for i in key:
            column =  singleProject(i)
            if len(column) == 0:
                result = 'fail'
                continue
            columns.append(column)
        for c in columns:
            try:
                if c[0] == 'cls1':
                    manager = {'grade':1,'name':c[2],'index':c[4]}
                    classProjects[c[1]] = {'manager':manager,'project':json.loads(c[3])}
                if c[0] == 'cls2':
                    manager = {'grade':2,'name':c[2],'index':c[4]}
                    classProjects[c[1]] = {'manager':manager,'project':json.loads(c[3])}
                if c[0] == 'cls3':
                    manager = {'grade':3,'name':c[2],'index':c[4]}
                    classProjects[c[1]] = {'manager':manager,'project':json.loads(c[3])}
                if c[0] == 'vol':
                    manager = {'grade':0,'name':c[2],'index':c[4]}
                    volunteerProjects[c[1]] = {'manager':manager,'project':json.loads(c[3])}
                if c[0] == 'com':
                    manager = {'grade':0,'name':c[2],'index':c[4]}
                    marketingProjects[c[1]] = {'manager':manager,'project':json.loads(c[3])}
            except KeyError as e:
                print(e.args)
                print('レスポンスデータ作成in企画データ取得')
                print(key)
                return jsonify({'result':'error'})
                #データベースに必要なデータが含まれていない可能性
        msg ={'classProjects':classProjects,'volunteerProjects':volunteerProjects,'marketingProjects':marketingProjects}
        pro = {'projects':msg,'result':'success'}
        if result == '':
            pro = {'projects':msg,'result':'success'}
        else:
            pro = {'projects':msg,'result':'partly error'}
            print(key)
            #keyパラメータに間違いがある
        return jsonify(pro)
@app.route('/waitUpdate',methods=['POST'])
def wait_update():#例外処理OK
    data = request.get_json()
    correct,data = login(req=data,_type='normal')
    if correct == True:
        try:
            key = data['key']
        except KeyError as e:
            print(e.args)
            print('keyパラメータ取得in待ち時間更新')
            print(data)
            return jsonify({'result':'error'})
            #パラメーターのKEYにkeyが含まれていない、もしくはkeyの値がNoneなどの不正な値の可能性
        except Exception as e:
            print('想定外のエラー')
            print(e.args)
            print('keyパラメータ取得in待ち時間更新')
            print(data)
            return jsonify({'result':'error'})
        try:
            status = data['state']
        except KeyError as e:
            print(e.args)
            print('stateパラメータ取得in待ち時間更新')
            print(data)
            return jsonify({'result':'error'})
            #パラメーターのKEYにstatusが含まれていない、もしくはstatusの値がNoneなどの不正な値の可能性
        except Exception as e:
            print('想定外のエラー')
            print(e.args)
            print('stateパラメータ取得in待ち時間更新')
            print(data)
            return jsonify({'result':'error'})
        try:
            if status == 'opening' or status == 'soonend':
                wait = data['val']
            else:
                wait = 0
        except KeyError as e:
            print(e.args)
            print('valパラメータ取得in待ち時間更新')
            print(data)
            return jsonify({'result':'error'})
            #パラメーターのKEYにwaitが含まれていない、もしくはwaitの値がNoneなどの不正な値の可能性
        except Exception as e:
            print('想定外のエラー')
            print(e.args)
            print('データベース更新in待ち時間更新')
            print(data)
            return jsonify({'result':'error'})
        try:
            conn = mysql.connector.connect(user='user_name',password='xMw5jVwq',host='localhost',database='schoolfestival')
            cur = conn.cursor()
            mysql_sentence = "UPDATE projects SET wait = '" + str(wait) + "', status = '" + status + "' WHERE `key` = '" + key +"';"
            cur.execute(mysql_sentence)
            cur.close()
            conn.commit()
            conn.close()
            global update
            update += 1
            return jsonify({'result':'success'})
        except Exception as e:
            print('想定外のエラー')
            print(e.args)
            print('データベース更新in待ち時間更新')
            print(data)
            return jsonify({'result':'error'})
        except Exception as e:
            print('想定外のエラー')
            print(e.args)
            print('データベース更新in待ち時間更新')
            print(data)
            return jsonify({'result':'error'})
    elif correct == False:
        return jsonify({'result':'fail','cause':'you do not have authority'})
    else:
        return jsonify({'result':'error'})
@app.route('/information/<string:updCount>',methods=['GET'])
def information(updCount):
    try:
        dt_now = datetime.datetime.now()
        now = int(str(dt_now.month).zfill(2)+str(dt_now.day).zfill(2)+str(dt_now.hour).zfill(2)+str(dt_now.minute).zfill(2)+str(dt_now.second).zfill(2))
        conn = mysql.connector.connect(user='user_name',password='xMw5jVwq',host='localhost',database='schoolfestival')
        cur = conn.cursor()
        cur.execute("SELECT content from specialinformation WHERE title = 'infoUpdCount';")
        columns = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        print('想定外のエラー')
        print(e.args)
        print('データベース接続inお知らせ取得')
        print(updCount)
        return jsonify({'result':'error'})
    try:
        infoUpdCount = columns[0][0]
        if int(infoUpdCount) != int(updCount):
            msg = {'state':'updated','updCount':infoUpdCount,'result':'success'}
            conn = mysql.connector.connect(user='user_name',password='xMw5jVwq',host='localhost',database='schoolfestival')
            cur = conn.cursor()
            cur.execute("SELECT num,state,title,category,time,subject,updCount from infolog WHERE  `updCount` >" + updCount + " AND `updCount` < " + str(now) + ";")
            columns = cur.fetchall()
            cur.close()
            conn.close()
            infoLog = []
            infoData = {}
            for column in columns:
                arr = {'title':column[2],'category':column[3],'time':column[4],'subject':column[5]}
                infoData[column[0]] = arr
                infoLog.append({'id':column[0],'state':column[1],'updCount':column[6]})
            msg['infoLog']=infoLog
            msg['infoData']=infoData
            return jsonify(msg)
        return jsonify({"result":"success","state":"noUpd"})
    except Exception as e:
        print('想定外のエラー')
        print(e.args)
        print('データベース接続2inお知らせ取得')
        print(updCount)
        return jsonify({'result':'error'})
@app.route('/informationUpdate',methods=['POST'])
def information_update():
    data = request.get_json()
    correct,data = login(req=data,_type='super')
    if correct == True:
        try:
            num = data['id']
        except KeyError as e:
            print(e.args)
            print('num(id)パラメータ取得inお知らせ')
            print(data)
            return jsonify({'result':'error'})
            #パラメーターのKEYにidが含まれていない、もしくはidの値がNoneなどの不正な値の可能性
        except Exception as e:
            print('想定外のエラー')
            print(e.args)
            print('num(id)パラメータ取得inお知らせ')
            print(data)
            return jsonify({'result':'error'})
            
        try:
            state = data['type']
        except KeyError as e:
            print(e.args)
            print('stateパラメータ取得inお知らせ')
            print(data)
            return jsonify({'result':'error'})
            
        except Exception as e:
            print('想定外のエラー')
            print(e.args)
            print('stateパラメータ取得inお知らせ')
            print(data)
            return jsonify({'result':'error'})
            
        try:
            title = data['title']
        except KeyError as e:
            print(e.args)
            print('titleパラメータ取得inお知らせ')
            print(data)
            return jsonify({'result':'error'})
            
        except Exception as e:
            print('想定外のエラー')
            print(e.args)
            print('titleパラメータ取得inお知らせ')
            print(data)
            return jsonify({'result':'error'})
            
        try:
            category = data['category']
        except KeyError as e:
            print(e.args)
            print('categoryパラメータ取得inお知らせ')
            print(data)
            return jsonify({'result':'error'})
            
        except Exception as e:
            print('想定外のエラー')
            print(e.args)
            print('categoryパラメータ取得inお知らせ')
            print(data)
            return jsonify({'result':'error'})
            
        try:
            time = data['time']
        except KeyError as e:
            print(e.args)
            print('timeパラメータ取得inお知らせ')
            print(data)
            return jsonify({'result':'error'})
            
        except Exception as e:
            print('想定外のエラー')
            print(e.args)
            print('timeパラメータ取得inお知らせ')
            print(data)
            return jsonify({'result':'error'})
            
        try:
            subject = data['subject']
            if data['files']!= '':
                files = data['files']
                print(files)
                fileArrey = files.split(',')
            else:
                fileArrey = []
        except KeyError as e:
            print(e.args)
            print('subjectパラメータ取得inお知らせ')
            print(data)
            return jsonify({'result':'error'})
            
        except Exception as e:
            print('想定外のエラー')
            print(e.args)
            print('subjectパラメータ取得inお知らせ')
            print(data)
            return jsonify({'result':'error'})
            
        dt_now = datetime.datetime.now()
        infoupdCount = int(str(dt_now.month).zfill(2)+str(dt_now.day).zfill(2)+str(dt_now.hour).zfill(2)+str(dt_now.minute).zfill(2)+str(dt_now.second).zfill(2))
            

        try:
            conn = mysql.connector.connect(user='user_name',password='xMw5jVwq',host='localhost',database='schoolfestival')
            cur = conn.cursor()
            mysql_sentence = "UPDATE specialinformation SET content = '" + str(infoupdCount) + "' WHERE title = 'infoupdCount';"
            cur.execute(mysql_sentence)
            cur.close()
            conn.commit()
            conn.close()
        except Exception as e:
            print('想定外のエラー')
            print(e.args)
            print('データベース接続3inお知らせ')
            return jsonify({'result':'error'})
            
        


        try:
            conn = mysql.connector.connect(user='user_name',password='xMw5jVwq',host='localhost',database='schoolfestival')
            cur = conn.cursor()
            mysql_sentence = "INSERT INTO infolog (num,state,title,category,time,subject,updCount) VALUES ('" + num + "','"+ state + "','" + title + "','" + category + "','" + time + "','" + subject + "',"+ str(infoupdCount) + ");"
            cur.execute(mysql_sentence)
            cur.close()
            conn.commit()
            conn.close()
        except Exception as e:
            print('想定外のエラー')
            print(e.args)
            print('データベース接続4inお知らせ')
            return jsonify({'result':'error'})
            
        try:
            for afile in fileArrey:
                conn = mysql.connector.connect(user='user_name',password='xMw5jVwq',host='localhost',database='schoolfestival')
                cur = conn.cursor()
                mysql_sentence = "INSERT INTO files (num,path) VALUES ('" + num + "','" + afile + "');"
                cur.execute(mysql_sentence)
                cur.close()
                conn.commit()
                conn.close()
        except Exception as e:
            print('想定外のエラー')
            print(e.args)
            print('データベース接続5inお知らせ')
            return jsonify({'result':'error'})
            
        
        return jsonify({'result':'success'})


        
        
    else:
        return jsonify({'result':'fail'})
@app.route('/israin',methods=['POST'])
def israin():
    body = request.get_json()
    global update
    global isRain
    update += 1
    isRain = bool(body['isRain'])
    return jsonify({'result':'success'})
@app.route('/edit',methods=['POST'])
def editProjectContent():#例外処理OK
    data = request.get_json()
    correct,data = login(req=data,_type='normal')
    if correct == True:
        try:
            cat = data['cat']
        except KeyError as e:
            print(e.args)
            print('catパラメータ取得in企画情報更新')
            print(data)
            return jsonify({'result':'error'})
        except Exception as e:
            print('想定外のエラー')
            print(e.args)
            print('catパラメータ取得in企画情報更新')
            print(data)
            return jsonify({'result':'error'})
        try:
            key = data['key']
        except KeyError as e:
            print(e.args)
            print('keyパラメータ取得in企画情報更新')
            print(data)
            return jsonify({'result':'error'})
        except Exception as e:
            print('想定外のエラー')
            print(e.args)
            print('keyパラメータ取得in企画情報更新')
            print(data)
            return jsonify({'result':'error'})
        try:
            #project = json.dumps(data['project'])
            project = data['project']

        except KeyError as e:
            print(e.args)
            print('projectsパラメータ取得in企画情報更新')
            print(data)
            return jsonify({'result':'error'})
        except Exception as e:
            print('想定外のエラー')
            print(e.args)
            print('projectsパラメータ取得in企画情報更新')
            print(data)
            return jsonify({'result':'error'})
        try:
            
            
            mysql_sentence = "UPDATE projects SET project='" + project + "',cat='" + cat + "' WHERE `key`='" + key + "';"
            
            #UPDATE projects SET project='{"project":{"name":"","type":"perform","information":[{"tag":"","time":"","intro":"","place":""}]}}',cat="vol" WHERE `key`="den";
            conn = mysql.connector.connect(user='user_name',password='xMw5jVwq',host='localhost',database='schoolfestival')
            cur = conn.cursor()
            cur.execute(mysql_sentence)
            cur.close()
            conn.commit()
            conn.close()
        except Exception as e:
            print('想定外のエラー')
            print(e.args)
            print('データベースin企画情報更新')
            print(data)
            return jsonify({'result':'error'})
        return jsonify({'result':'success'})
    else:
        return jsonify({'result':'fail'})
@app.route('/timetable')
def timetable():
    conn = mysql.connector.connect(user='user_name',password='xMw5jVwq',host='localhost',database='schoolfestival')
    cur = conn.cursor()
    cur.execute("SELECT name,manager,time,place FROM timetable;")
    columns = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    resp = []
    for colmun in columns:
        resp.append({'name':colmun[0],'manager':colmun[1],'time':colmun[2],'place':colmun[3]})
    return jsonify(resp)

@app.route('/')
def index():
    return jsonify({'result':'Hello'})
if __name__=="__main__":
    app.run(host='ichikosai.net',port=8443,threaded=True,ssl_context=context)