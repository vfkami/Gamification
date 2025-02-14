#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Copyright © 2019-Present Lucas Castanheira
# lbcastanheira@inf.ufrgs.br
#


from flask import Flask
from flask import request, url_for, redirect, send_from_directory, make_response, render_template
from flask import jsonify
from time import sleep
from werkzeug.utils import secure_filename
import requests
import os

app = Flask(__name__)
import time
import datetime
import pickle
import urllib.parse as ul
import subprocess


class Ranking:
    scores = {}
    value = {'Join': 1, 'Question': 2}
    outs = {}
    univScores = {}
    sessScores = {}
    stateScores = {}


try:
    f = open("ongoing.txt", "r")
    ranking = pickle.load(f)
except IOError:
    print("No ongoing.txt, loading from scratch.")
    ranking = Ranking()

import operator


class Ranking:
    scores = {}
    value = {'Join': 1, 'Question': 2}
    outs = {}
    univScores = {}
    sessScores = {}
    stateScores = {}
    participated = {}


ranking = Ranking()

import operator
import sys
import traceback


def verificadorSigla(sigla):
    if sigla == 'AC':
        return 'ACRE'
    elif sigla == 'AL':
        return 'ALAGOAS'
    elif sigla == 'AM':
        return 'AMAZONAS'
    elif sigla == 'AP':
        return 'AMAPÁ'
    elif sigla == 'BA':
        return 'BAHIA'
    elif sigla == 'CE':
        return 'CEARÁ'
    elif sigla == 'DF':
        return 'DISTRITO FEDERAL'
    elif sigla == 'ES':
        return 'ESPIRITO SANTO'
    elif sigla == 'GO':
        return 'GOIAS'
    elif sigla == 'MA':
        return 'MARANHÃO'
    elif sigla == 'MG':
        return 'MINAS GERAIS'
    elif sigla == 'MS':
        return 'MATO GROSSO DO SUL'
    elif sigla == 'MT':
        return 'MATO GROSSO'
    elif sigla == 'PA':
        return 'PARÁ'
    elif sigla == 'PB':
        return 'PARAÍBA'
    elif sigla == 'PE':
        return 'PERNAMBUCO'
    elif sigla == 'PI':
        return 'PIAUÍ'
    elif sigla == 'PR':
        return 'PARANÁ'
    elif sigla == 'RJ':
        return 'RIO DE JANEIRO'
    elif sigla == 'RN':
        return 'RIO GRANDE DO NORTE'
    elif sigla == 'RO':
        return 'RONDÔNIA'
    elif sigla == 'RR':
        return 'RORAIMA'
    elif sigla == 'RS':
        return 'RIO GRANDE DO SUL'
    elif sigla == 'SC':
        return 'SANTA CATARINA'
    elif sigla == 'SE':
        return 'SERGIPE'
    elif sigla == 'SP':
        return 'SÃO PAULO'
    elif sigla == 'TO':
        return 'TOCANTINS'
    else:
        return 'EXTERIOR'


try:
    import mysql.connector

    db = mysql.connector.connect(
        host="45.55.64.56",
        user="d63551eebd92 ",
        passwd="ac3b4f15720d4083",
        database='csbc-gamification'
    )

    print(db)

    cursor = db.cursor()

    checkRepeatedTemplate = '''SELECT * FROM EventLogs WHERE Name=%s AND (participation = "Join" OR participation = "Question")'''

    insertLogTemplate = '''INSERT INTO EventLogs 
              (Name,Institution,state,session,participation,points,lastScore,updated_at)
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
    fetchStateTemplate = '''select state, count(*) from (SELECT * FROM `EventLogs` where participation = "join" GROUP by Name) res group by state order by count(*) desc'''

    fetchInstitutionTemplate = '''SELECT sigla, total FROM `rank_inst`'''

    fetchNameTemplate = '''SELECT Name, sigla, total FROM `rank_indv`'''

    fetchSessTemplate = '''SELECT session,SUM(points) FROM EventLogs where participation = "join" GROUP BY session ORDER BY SUM(points) DESC'''



    cursor.execute(fetchNameTemplate)

    for res in cursor:
        if res[1] is None:
            ranking.scores[res[0] + ' (NULL)'] = int(res[2])
        else:
            ranking.scores[res[0] + ' (' + res[1] + ')'] = int(res[2])

    cursor.execute(fetchInstitutionTemplate)
    for res in cursor:
        ranking.univScores[res[0]] = int(res[1])

    cursor.execute(fetchStateTemplate)
    for res in cursor:
        ranking.stateScores[verificadorSigla(res[0])] = int(res[1])

    cursor.execute(fetchSessTemplate)
    for res in cursor:
        ranking.sessScores[res[0]] = int(res[1])

    sql = True

except:
    traceback.print_exc(file=sys.stdout)
    sql = False
    print('no mysql connector')


@app.route('/qr/<string>/<sess>/<activity>')
def qr(string, sess, activity):
    if (sql):
        global cursor
        global db
        global insertLogTemplate
        db = mysql.connector.connect(
            host="45.55.64.56",
            user="d63551eebd92 ",
            passwd="ac3b4f15720d4083",
            database='csbc-gamification'
        )
        cursor = db.cursor()

    csv = string.replace(", ", ",").split(',')
    print(len(csv))
    if (len(csv)==4):
        state = csv[3]
        inst = csv[2]
        inst = inst[inst.find("(")+1:inst.find(")")]
    else:
        state = csv[2]
        inst = csv[1]
    if (csv[0] == "LISANDRO GRANVILLE"):
        state = "RS"
        inst = "UFRGS"
    
    id = csv[0] + ' (' + inst + ')'
    # if opt out or out then rewrite optout else score

    pointsDB = ranking.value[activity]
    if (activity == "Join"):
        cursor.execute(checkRepeatedTemplate, (csv[0],))
        result = cursor.fetchall()
        if (cursor.rowcount > 0):
            if (len(csv)==4):
                if (result[len(result) - 1][0] == csv[0] and result[len(result) - 1][1] == inst and
                            result[len(result) - 1][2] == state):
                        date_time_obj = datetime.datetime.strptime(result[len(result) - 1][7], '%Y-%m-%d %H:%M:%S.%f')
                        timesince = datetime.datetime.now() - date_time_obj
                        minutessince = int(timesince.total_seconds() / 60)
                        pointsDB = int(result[len(result) - 1][6]) + 1
                        if (minutessince < 30):
                            return ("0;" + str(minutessince))
            # cursor.execute(insertLogTemplate, (csv[0],csv[1],csv[2],sess,0,0,0,0))
            # db.commit()
            # return('0')
            else:
                if (result[len(result) - 1][0] == csv[0] and result[len(result) - 1][1] == csv[1] and
                            result[len(result) - 1][2] == csv[2]):
                        date_time_obj = datetime.datetime.strptime(result[len(result) - 1][7], '%Y-%m-%d %H:%M:%S.%f')
                        timesince = datetime.datetime.now() - date_time_obj
                        minutessince = int(timesince.total_seconds() / 60)
                        pointsDB = int(result[len(result) - 1][6]) + 1
                        if (minutessince < 30):
                            return ("0;" + str(minutessince))
            # cursor.execute(insertLogTemplate, (csv[0],csv[1],csv[2],sess,0,0,0,0))
            # db.commit()
            # return('0')
        else:
            ranking.sessScores[sess] = ranking.sessScores.get(sess, 0) + 1
    elif (activity == "Question"):
        cursor.execute(checkRepeatedTemplate, (csv[0],))
        result = cursor.fetchall()
        if (cursor.rowcount > 0):
            pointsDB = int(result[len(result) - 1][6]) + 2
        # cursor.execute(insertLogTemplate, (csv[0],csv[1],csv[2],sess,0,0,0,0))
        # db.commit()
        # return('0')
        else:
            ranking.sessScores[sess] = ranking.sessScores.get(sess, 0) + 2

    if (activity != 'Optout' and id not in ranking.outs):
        # get points for the activity being logged
        activityScore = ranking.value[activity]
        # Pts for guy and for institution
        points = ranking.scores.get(id, 0) + activityScore
        univPoints = ranking.univScores.get(inst, 0) + activityScore
        # Score
        ranking.scores[id] = points
        ranking.univScores[inst] = univPoints
    else:
        ranking.outs[id] = True

    ranking.stateScores[state] = ranking.stateScores.get(state, 0) + 1
    
    if (sql):
        cursor.execute(insertLogTemplate,(csv[0], inst, state, sess, activity, activityScore, pointsDB, datetime.datetime.now()))
        db.commit()

    return ('1;0')


class FromFile:
    translate = "-50%,-15%"
    title = "<b>Leaderboard SBRC 2019</b>"


@app.route('/apple-touch-icon.png')
def gtfo():
    return ('0')


@app.route('/apple-touch-icon-precomposed.png.html')
def aaaa():
    return ('0')


@app.route('/S', methods=['GET'])
def last():
    if (lastUp):
        return (redirect("http://d4c.wtf/static/arquivos/" + lastUp))
    else:
        return redirect('http://network.d4c.wtf/rasauto.mp4')


@app.route('/qrshow')
def qrshow():
    string = '''
        <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="en">
<head>
<title>Dashboard Example</title>
<style type="text/css">
body, html { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; }
iframe { border: none; width: 100%; height: 100%; display: none; }
iframe.active { display: block;}
</style>
<script src="http://code.jquery.com/jquery-latest.min.js" type="text/javascript"></script>
<script type="text/javascript">
var Dash = {
    nextIndex: 1,
    //Don't put too many items in this list
    dashboards: [
       {url: "http://45.55.64.56/qrshow/0", time: 1, refresh: true},
       {url: "http://45.55.64.56/qrshow/1", time: 20, refresh: true},
       {url: "http://45.55.64.56/qrshow/2", time: 20, refresh: true},
       {url: "http://45.55.64.56/qrshow/3", time: 20, refresh: true},
       {url: "http://45.55.64.56/qrshow/4", time: 20, refresh: true},
       {url: "http://45.55.64.56/patrocinio", time: 20, refresh: false},
       {url: "http://45.55.64.56/quarta", time: 130, refresh: true}
    ],
    startup: function () {
        for (var index = 0; index < Dash.dashboards.length; index++) {
						Dash.loadFrame(index);
				}
        setTimeout(Dash.display, Dash.dashboards[0].time * 1000);
    },
    loadFrame: function (index) {
				var iframe = document.getElementById(index);
				iframe.src = Dash.dashboards[index].url;
    },
    display: function () {
        var dashboard = Dash.dashboards[Dash.nextIndex];
				Dash.hideFrame(Dash.nextIndex - 1);
				if (dashboard.refresh) {
						Dash.loadFrame(Dash.nextIndex);
				}
				Dash.showFrame(Dash.nextIndex);
        Dash.nextIndex = (Dash.nextIndex + 1) % Dash.dashboards.length;
        setTimeout(Dash.display, dashboard.time * 1000);
    },
    hideFrame: function (index) {
				if (index < 0) {
						index = Dash.dashboards.length - 1;
				}
				$('#'+index).css({opacity: 1.0, visibility: "visible"}).animate({opacity: 0.0},2000);
				setTimeout(function() {true;},2000);
				document.getElementById(index).removeAttribute('class');
    },
    showFrame: function (index) {
				$('#'+index).css({opacity: 0.0, visibility: "visible"}).animate({opacity: 1.0},2000);
				document.getElementById(index).setAttribute('class', 'active');
    }
};
function fetchPage(url) {
    $.ajax({
        type: "GET",
        url: url,
        error: function(request, status) {
            alert('Error fetching ' + url);
        },
        success: function(data) {
            parse_hadoop_active_nodes(data.responseText);
        }
    });
}
function parse(data) {
    alert($(data).find("#nodes").text());
}
window.onload = Dash.startup;
</script>
</head>
<body>
<iframe id="0" class="active"></iframe>
<iframe id="1"></iframe>
<iframe id="2"></iframe>
<iframe id="3"></iframe>
<iframe id="4"></iframe>
<iframe id="5"></iframe>
<iframe id="6"></iframe>
</body>
</html>'''
    return string


@app.route("/favicon.ico")
def favicon():
    return ('322')


@app.route('/qrshow/0')
def qrshow0():
    if (sql):
        global cursor
        global db
        global insertLogTemplate
        db = mysql.connector.connect(
            host="45.55.64.56",
            user="d63551eebd92 ",
            passwd="ac3b4f15720d4083",
            database='csbc-gamification'
        )
        cursor = db.cursor()

    cursor.execute(fetchNameTemplate)

    for res in cursor:
        if res[1] is None:
            ranking.scores[res[0] + ' (NULL)'] = int(res[2])
        else:
            ranking.scores[res[0] + ' (' + res[1] + ')'] = int(res[2])

    cursor.execute(fetchInstitutionTemplate)
    for res in cursor:
        ranking.univScores[res[0]] = int(res[1])

    cursor.execute(fetchStateTemplate)
    for res in cursor:
        ranking.stateScores[verificadorSigla(res[0])] = int(res[1])

    cursor.execute(fetchSessTemplate)
    for res in cursor:
        ranking.sessScores[res[0]] = int(res[1])

    return 'Atualizando...'


@app.route('/qrshow/1')
def qrshow1():
    stringedScores = ''.join(['<li><mark>' + str(k) + '</mark>' + '<small>' + str(v) + '</small></li>' for k, v in
                              sorted(ranking.scores.items(), key=operator.itemgetter(1), reverse=True)[0:15]])

    string = '''
        <html>
		
		<head>
			<link href= "/static/css/NewStyle3.css" rel="stylesheet">
		</head>
        
		<body style="background-image: url(/static/background.png);">
			<div class="logo">
				<img src="/static/game_CSBC_LOGO.png" style=" width:500px;">
			</div>
			
			<div class="leaderboard_header"> 
				<div class="aux" style=" width:10%;"><p>Nº</p> </div>
    			<div class="aux" style=" width:68.5%;"> <p>NOME</p> </div>
    			<div class="aux" style=" width:18.1%;"> <p>PONTUAÇÃO</p> </div>
  			</div>
			
			<div class="leaderboard">
				<ol> '''+ stringedScores +''' <ol>
			</div>
			<div class="footer">
				<img src="/static/inf.png" style=" width:200px;">
			</div>
			
		</body>
	</html>'''

    return (string)


@app.route('/qrshow/2')
def qrshow2():
    univScores = ''.join(['<li><mark>' + str(k) + '</mark>' + '<small>' + str(v) + '</small></li>' for k, v in
                          sorted(ranking.univScores.items(), key=operator.itemgetter(1), reverse=True)[0:15]])

    string = '''
        <html>
		
		<head>
			<link href= "/static/css/NewStyle3.css" rel="stylesheet">
		</head>
        
		<body style="background-image: url(/static/background.png);">
			<div class="logo">
				<img src="/static/game_CSBC_LOGO.png" style=" width:500px;">
			</div>
			
			<div class="leaderboard_header"> 
				<div class="aux" style=" width:10%;"><p>Nº</p> </div>
    			<div class="aux" style=" width:68.5%;"> <p>INSTITUIÇÃO</p> </div>
    			<div class="aux" style=" width:18.1%;"> <p>PONTUAÇÃO</p> </div>
  			</div>
			
			<div class="leaderboard">
				<ol> '''+ univScores +''' <ol>
			</div>
			<div class="footer">
				<img src="/static/inf.png" style=" width:200px;">
			</div>
			
		</body>
	</html>'''

    return (string)


@app.route('/qrshow/3')
def qrshow3():
    sessScores = ''.join(['<li><mark>' + str(k) + '</mark>' + '<small>' + str(v) + '</small></li>' for k, v in
                          sorted(ranking.sessScores.items(), key=operator.itemgetter(1), reverse=True)[0:15]])

    string = '''
        <html>
		
		<head>
			<link href= "/static/css/NewStyle3.css" rel="stylesheet">
		</head>
        
		<body style="background-image: url(/static/background.png);">
			<div class="logo">
				<img src="/static/game_CSBC_LOGO.png" style=" width:500px;">
			</div>
			
			<div class="leaderboard_header"> 
				<div class="aux" style=" width:10%;"><p>Nº</p> </div>
    			<div class="aux" style=" width:68.5%;"> <p>SESSÃO</p> </div>
    			<div class="aux" style=" width:18.1%;"> <p>PONTUAÇÃO</p> </div>
  			</div>
			
			<div class="leaderboard">
				<ol> '''+ sessScores +''' <ol>
			</div>
			<div class="footer">
				<img src="/static/inf.png" style=" width:200px;">
			</div>
			
		</body>
	</html>'''
    return (string)


@app.route('/qrshow/4')
def qrshow4():
    stateScores = ''.join(['<li><mark>' + str(k) + '</mark>' + '<small>' + str(v) + '</small></li>' for k, v in
                           sorted(ranking.stateScores.items(), key=operator.itemgetter(1), reverse=True)[0:15]])

    string = '''
        <html>
		
		<head>
			<link href= "/static/css/NewStyle3.css" rel="stylesheet">
		</head>
        
		<body style="background-image: url(/static/background.png);">
			<div class="logo">
				<img src="/static/game_CSBC_LOGO.png" style=" width:500px;">
			</div>
			
			<div class="leaderboard_header"> 
				<div class="aux" style=" width:10%;"><p>Nº</p> </div>
    			<div class="aux" style=" width:68.5%;"> <p>ESTADO</p> </div>
    			<div class="aux" style=" width:18.1%;"> <p>PARTICIPANTES</p> </div>
  			</div>
			
			<div class="leaderboard">
				<ol> '''+ stateScores +''' <ol>
			</div>
			<div class="footer">
				<img src="/static/inf.png" style=" width:200px;">
			</div>
			
		</body>
	</html>'''

    return (string)


@app.route('/segunda')
def showsched2():
    return render_template('segunda.html')


@app.route('/terca')
def showsched3():
    return render_template('terca.html')


@app.route('/quarta')
def showsched4():
    return render_template('quarta.html')


@app.route('/quinta')
def showsched5():
    return render_template('quinta.html')


@app.route('/domingo')
def showsched6():
    return render_template('domingo.html')


@app.route('/sessions')
def sessions():
    # domingo = "CQEB(9-12),CQ(9-12),CQEB(14-16),CQ(14-16),CQEB(16:30-19),CQ(16:30-19)"
    # segundaManha = "JAI #1(9-12),WEI(9-12),CTD(9-12),WIT(9-12),SEMISH(9-12),SEMISH-hackaton(9-12),WPerformance(9-12),WTranS(9-12),ETC(9-12),CLOUDSCAPE-Brazil(9-12),ForumPG(9-12)"
	# segundaTarde = "JAI #1(16-19),WEI(16-19),CTD(16-19),WIT(16-19),SEMISH(16-19),SEMISH-hackaton(16-19),WPerformance(16-19),WTranS(16-19),ETC(16-19),CLOUDSCAPE-Brazil(16-19),ForumPG(16-19),SECOMU"
    # tercaManha = "JAI #2(9-12),WEI(9-12),CTD(9-12),WIT(9-12),SEMISH(9-12),SEMISH-hackaton(9-12),SBCUP(9-12),WPerformance(9-12),ETC(9-12),WORKSHOP-OnCloundNetworks(9-12),ReuniãoCEs(9-12)"
	# tercaTarde = "JAI #2(16-19),WEI(16-19),CTIC(16-19),WIT(16-19),SEMISH(16-19),SEMISH-hackaton(16-19),SBCUP(16-19),WPerformance(16-19),ETC(16-19),Reunião CNPQ/CAPES(16-19),SECOMU"
    # quartaManha ="JAI #3(9-12),WEI(9-12),BraSNAM(9-12),BreSci(9-12),Reunião SR SBC(9-12),SBCUP(9-12),WCAMA(9-12),WPIETF hackathon(9-12),WPIETF(9-12),COMPUTEC(9-12)"
	# quartaTarde = "JAI #3(16-19),WEI(16-19),BraSNAM(16-19),BreSci(16-19),IFIP/SBC(16-19),SBCUP(16-19),WCAMA(16-19),WPIETF hackathon(16-19),WPIETF(16-19),COMPUTEC(16-19),Apres. e Prem. do Selo de Inovacao da SBC,SECOMU"
    # quintaManha = "JAI #4(9-12),WEI(9-12),BraSNAM(9-12),BreSci(9-12),SBCUP(9-12),ENCompIP(9-12),WFIBRE(9-12),WPIETF(9-12),WASHES(9-12),COMPUTEC(9-12)"
	# quintaTarde = "JAI #4(16-19),WCAMA(16-19),BraSNAM(16-19),BreSci(16-19),SBCUP(16-19),ENCompIP(16-19),WFIBRE(16-19),WPIETF(16-19),WASHES(16-19),COMPUTEC(16-19),SECOMU"
    # session = domingo
    return "JAI #3(9-12),WEI(9-12),BraSNAM(9-12),BreSci(9-12),Reunião SR SBC(9-12),SBCUP(9-12),WCAMA(9-12),WPIETF hackathon(9-12),WPIETF(9-12),COMPUTEC(9-12)"


@app.route('/patrocinio')
def showpatrocinio():
    return render_template('patrocinio.html')


# app.run(host='0.0.0.0',port=80, threaded=True)
# requests.get('10.0.0.1')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

#SELECT *, SUM(points) as total FROM `EventLogs` WHERE DATE(updated_at) = '2019-07-15' GROUP BY Name order by total desc
