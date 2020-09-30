from flask import Flask, g, request, Response, make_response
from flask import session, render_template, Markup
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

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
# @app.route("/")
# def helloworld():
#     return "Hello Flask World!" # 응답


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
    lst = [ ("노래1", "때껄룩"), ("노래2", "기리보이"), ("노래3", "수현"), ("노래4", "유노윤호")]
    lst1 = [ (1, "노래1", "때껄룩", False), (2, "노래2", "기리보이", True), (3, "노래3", "수현",False), (4, "노래4", "유노윤호", True)]
    return render_template('index.html', title=tit, mu=h, lst=lst, lst1=lst1, lst2=[])


@app.route('/tmpl2')
def tmpl2():
    a = (1, "만남1", "김건모", False, [])
    b = (2, "만남2", "노사연", True, [a])
    c = (3, "만남3", "익명", False, [a,b])
    d = (4, "만남4", "익명", False, [a,b,c])

    return render_template("index.html", lst3=[a,b,c,d])


class Nav:
    def __init__(self, title, url='#', children=[]):
        self.title = title
        self.url = url
        self.children = children

@app.route('/tmpl3')
def tmpl3():
    py = Nav("파이썬", "https://www.naver.com")
    java = Nav("자바", "https://www.naver.com")
    t_prg = Nav("프로그래밍 언어", "https://www.naver.com", [py, java])

    jinja = Nav("jinja", "https://www.naver.com")
    gc = Nav("Genshi, cheetah", "https://www.naver.com")
    flask = Nav("플라스크", "https://www.naver.com", [jinja, gc])

    spr = Nav("스프링", "https://www.naver.com")
    ndjs = Nav("노드JS", "https://www.naver.com")
    t_webf = Nav("웹 프레임워크", "https://www.naver.com", [flask, spr, ndjs])

    my = Nav("나의 일상", "https://www.naver.com")
    issue = Nav("이슈 게시판", "https://www.naver.com")
    t_others = Nav("기타", "https://www.naver.com", [my, issue])

    return render_template("index.html", navs=[t_prg, t_webf, t_others])


@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/top100')
def top100():
    return render_template('application.html', title="Main!!")

class FormInput:
    def __init__(self, id, name , value, checked, text):
        self.id = id
        self.name = name
        self.value = value
        self.checked = checked
        self.text = text


@app.route('/')
def idx():
    rds=[]
    for i in [1,2,3]:
        id='r'+str(i)
        name='radiotest'
        value=i
        checked=''
        if i == 2:
            checked='checked'
        text = 'RadioTest' + str(i)
        rds.append(FormInput(id, name, value, checked, text))
    
    #today = date.today()
    #today = datetime.now()
    today = '2020-09-26 12:01'
    d = datetime.strptime("2020-01-01", "%Y-%m-%d")
    #sdt = d.weekday()*-1
    #print(sdt)
    #nextMonth = d + relativedelta(months=1)
    #print(nextMonth)
    #mm = d.month
    #print(mm)
    #edt = (nextMonth-timedelta(1)).day+1
    #print(edt)
    #return render_template('app.html', ttt='TestTTT', mm=mm, edt=edt, sdt=sdt, radioList=rds, today=today)
    #year = 2020
    year = request.args.get('year', date.today().year, int)
    return render_template('app.html', ttt='TestTTT', year=year, radioList=rds, today=today)

@app.template_filter('ymd')               # cf. Handlebars' helper
def datetime_ymd(dt, fmt='%m-%d'):
    if isinstance(dt, date):
        #return dt.strftime(fmt)
        return "<strong>%s</strong>" %dt.strftime(fmt)
    else:
        return dt


@app.template_filter('symd')               # cf. Handlebars' helper
def datetime_symd(dt, fmt='%m-%d'):
    if isinstance(dt, date):
        #return dt.strftime(fmt)
        return "<strong>%s</strong>" %dt.strftime(fmt)
    else:
        return dt

@app.template_filter('simpledate')               # cf. Handlebars' helper
def simpledate(dt):
    if not isinstance(dt, date):
        dt = datetime.strptime(dt, '%Y-%M-%d %H:%m')

    if (datetime.now()-dt).days<1:
        fmt = "%H:%m"
    else:
        fmt = "%M/%d"

    return "<strong>%s</strong>" % dt.strftime(fmt)

def make_date(dt, fmt):
    if not isinstance(dt, date):
        return datetime.strptime(dt, fmt)
    else:
        return dt

@app.template_filter('sdt')
def sdt(dt, fmt='%Y-%m-%d'):
    d = make_date(dt, fmt)
    wd = d.weekday()
    # if wd==6:
    #     return 1
    # else:
    #     return wd
    return (-1 if wd == 6 else wd) * -1

@app.template_filter('month')
def month(dt, fmt='%Y-%m-%d'):
    d = make_date(dt, fmt)
    return d.month

@app.template_filter('edt')
def edt(dt, fmt='%Y-%m-%d'):
    d = make_date(dt, fmt)
    nextMonth = d + relativedelta(months=1)
    return (nextMonth-timedelta(1)).day + 1