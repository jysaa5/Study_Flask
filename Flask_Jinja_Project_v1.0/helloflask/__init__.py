from flask import Flask, g, request, Response, make_response
from flask import session, render_template, Markup
from datetime import datetime, date, timedelta

# Flask  생성
app = Flask(__name__)
# debug 모드를 true로 변환
app.debug = True

# trim_blocks app config
# app.jinja_env.trim_blocks = True


# app 아래에 보통 config를 넣는다.
app.config.update(
	SECRET_KEY='X1243yRH!mMwf',
    # 모든 사용자가 동일한 SESSION_COOKIE_NAME을 갖는다.
	SESSION_COOKIE_NAME='pyweb_flask_session',
	PERMANENT_SESSION_LIFETIME=timedelta(31)      # 31 days  cf. minutes=30
)


# request 요청을 처리하기 전에 실행
@app.before_request
def before_request():
    print("before_request!!!")
    g.str = "한글"


@app.route("/gg")
def helloworld2():
    return "Hello Flask World!"+getattr(g, 'str', '111') #세번째 인자는 default 값

# URI를 정의하는 것을 route이다.
@app.route("/")
def helloworld():
    return "Hello Flask World!" # 응답


@app.route('/res1')
def res1():
    custom_res = Response("Custom Response", 200, {'test': 'ttt'}) #json부분은 헤더로 들어 간다.
    return make_response(custom_res)


# WSGI(WebServer Gateway Interface)
@app.route('/test_wsgi')
def wsgi_test():
    def application(environ, start_response):
        body = 'The request method was %s' % environ['REQUEST_METHOD']
        headers = [ ('Content-Type', 'text/plain'), 
					('Content-Length', str(len(body))) ]
        start_response('200 OK', headers)
        return [body]

    return make_response(application)


@app.route('/rp')
def rp():
    #q = request.args.get('q')
    q = request.args.getlist('q')
    return "q=%s" % str(q)



# 윈도우 hosts 파일 수정해야 함.
# app.config['SERVER_NAME'] = 'local.com:5000'
# @app.route("/sd")
# def helloworld_local():
#     return "Hello Local.com!"

# @app.route("/sd", subdomain="g")
# def helloworld3():
#     return "Hello G.Local.com!!!"

# request 처리 용 함수
def ymd(fmt):
    def trans(date_str):
        return datetime.strptime(date_str, fmt)
    return trans


@app.route('/dt')
def dt():
    datestr = request.values.get('date', date.today(), type=ymd('%Y-%m-%d'))
    return "우리나라 시간 형식: " + str(datestr)

@app.route('/reqenv')
def reqenv():
    return ('REQUEST_METHOD: %(REQUEST_METHOD) s <br>'
        'SCRIPT_NAME: %(SCRIPT_NAME) s <br>'
        'PATH_INFO: %(PATH_INFO) s <br>'
        'QUERY_STRING: %(QUERY_STRING) s <br>'
        'SERVER_NAME: %(SERVER_NAME) s <br>'
        'SERVER_PORT: %(SERVER_PORT) s <br>'
        'SERVER_PROTOCOL: %(SERVER_PROTOCOL) s <br>'
        'wsgi.version: %(wsgi.version) s <br>'
        'wsgi.url_scheme: %(wsgi.url_scheme) s <br>'
        'wsgi.input: %(wsgi.input) s <br>'
        'wsgi.errors: %(wsgi.errors) s <br>'
        'wsgi.multithread: %(wsgi.multithread) s <br>'
        'wsgi.multiprocess: %(wsgi.multiprocess) s <br>'
        'wsgi.run_once: %(wsgi.run_once) s') % request.environ

# 쿠키 굽기 & Session 만들기
@app.route('/wc')
def wc():
    key = request.args.get('key')
    val = request.args.get('val')
    res = Response("SET COOKIE")
    res.set_cookie(key, val)

    # session 객체는 플라스크가 생성해서 준다.
    session['Token'] = '123X'
    return make_response(res)


# 쿠키 value 찾기
@app.route('/rc')
def rc():
    key = request.args.get('key') # token
    val = request.cookies.get(key)
    return "cookie['" + key +"] = " +val+ ","+ session.get('Token')


@app.route('/delsess')
def delsess():
    if session.get('Token'):
        del session['Token']
    return "Session이 삭제되었습니다!"

#templtes 폴더명은 flask에서 기본으로 갖고 있어서 templates 아래에 있으면 경로 설정을 따로 안해도 된다.
# title 딕셔너리로 줄수 있다.
@app.route('/tmpl')
def tmpl():
    #return render_template('index.html', title="Title")
    #return render_template('index.html', title="<strong>Title</strong>") 
    #return render_template('index.html', title=Markup("<strong>Title</strong>")) 
    tit = Markup("<strong>Title</strong>")
    mu = Markup("<h1>iii=<i>%s</i></h1>")
    h = mu % "Italic"
    print(">>>>>>>>>>>", type(tit))
    print("h= ", h)
    bold = Markup("<b>Bold</b>")
    bold2 = Markup.escape("<b>Bold</b>")
    bold3 = bold2.unescape()
    print(bold, bold2, bold3)
    return render_template('index.html', title=tit, mu=h)
