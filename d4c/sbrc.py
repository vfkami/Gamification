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
        database='csbc-gamification',
	charset='utf8'
    )

    print(db)

    cursor = db.cursor()

    checkRepeatedTemplate = '''SELECT * FROM EventLogs WHERE Name=%s AND (participation = "Join" OR participation = "Question")'''

    insertLogTemplate = '''INSERT INTO EventLogs 
              (Name,Institution,state,session,participation,points,lastScore,updated_at)
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
    fetchStateTemplate = '''SELECT state,SUM(points)
  FROM EventLogs
 GROUP BY state
 ORDER BY SUM(points) DESC'''

    fetchInstitutionTemplate = ''' SELECT INSTITUICOES.SIGLA,SUM(points)
 FROM EventLogs
 LEFT OUTER JOIN INSTITUICOES ON INSTITUICOES.NomeCompleto=EventLogs.Institution
 GROUP BY INSTITUICOES.Sigla
 ORDER BY SUM(points) DESC'''

    fetchNameTemplate = '''SELECT Name,sigla,SUM(points) FROM EventLogs LEFT OUTER JOIN INSTITUICOES ON INSTITUICOES.NomeCompleto=EventLogs.Institution GROUP BY Name ORDER BY SUM(points) DESC'''

    fetchSessTemplate = ''' SELECT session,SUM(points)
 FROM EventLogs
 GROUP BY session
 ORDER BY SUM(points) DESC'''

    cursor.execute(fetchNameTemplate)

    for res in cursor:
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
    csv = string.split(',')
    inst = csv[1]
    id = csv[0] + ' (' + inst + ')'
    state = verificadorSigla(csv[2])
    # if opt out or out then rewrite optout else score

    pointsDB = ranking.value[activity]
    if (activity == "Join"):
        cursor.execute(checkRepeatedTemplate, (csv[0],))
        result = cursor.fetchall()
        if (cursor.rowcount > 0):
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
        cursor.execute(insertLogTemplate,
                       (csv[0], csv[1], csv[2], sess, activity, activityScore, pointsDB, datetime.datetime.now()))
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
       {url: "http://gercom.ddns.net:8082/qrshow/0", time: 1, refresh: true},
       {url: "http://gercom.ddns.net:8082/qrshow/1", time: 60, refresh: true},
       {url: "http://gercom.ddns.net:8082/qrshow/2", time: 60, refresh: true},
       {url: "http://gercom.ddns.net:8082/qrshow/3", time: 60, refresh: true},
       {url: "http://gercom.ddns.net:8082/patrocinio", time: 60, refresh: false},
       {url: "http://gercom.ddns.net:8082/segunda", time: 60, refresh: true}

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
</body>
</html>'''
    return string


@app.route("/favicon.ico")
def favicon():
    return ('322')


@app.route('/qrshow/0')
def qrshow0():
    cursor.execute(fetchNameTemplate)

    for res in cursor:
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
        <html><head>
		<style>
			body {
			  color: #000000;
			  font-family: 'Open Sans', sans-serif;
			}

			.logo{
			  height: auto;
			  width: 100%;
			  text-align: center;
			}

			.leaderboard {
			  position: absolute;
			  width: 100%;
			  height: auto;
			}

			.leaderboard ol {
			  counter-reset: leaderboard;
			  margin-left: -20px;
			}

			.leaderboard ol li {
			  position: relative;
			  list-style:none;
			  font-size: 14px;
			  counter-increment: leaderboard;
			  padding: 18px 0px 40px 0px;
			  cursor: pointer;
			}

			.leaderboard ol li::before {
			  content: counter(leaderboard);
			  position: absolute;
			  top: 0px;
			  left: 0px;
			  width: 10%;
			  padding: 18px 0px 18px 0px;
			  background: purple;
			  color: #fff;
			  border-radius: 15px;
			  text-align: center;
			}

			.leaderboard ol li mark {
			  border-radius: 15px;
			  position: absolute;
			  z-index: 2;
			  top: 0;
			  left: 11%;
			  width: 66%;
			  padding: 18px 0px 18px 0px;
			  background: purple;
			  color: #fff;
			  text-align: center;
			}

			.leaderboard ol li small {
			  border-radius: 15px;
			  position: absolute;
			  top: 0;
			  left: 78%;
			  width: 19%;
			  padding: 18px 0px 18px 0px;
			  background: green;
			  color: #fff;
			  text-align: center;
			}


			#numero{
			  position:relative;
			  top: 0px;
			  left: 0px;
			  width: 10%;
			  height: 50px;
			  background: darkblue;
			  color: #fff;
			  border-radius: 15px;
			  text-align: center;
			  float: left;
			}

			#nome{
			  position:relative;
			   margin: 0px 5px 0px 5px;
			  top: 0px;
			  left: 0px;
			  width: 68%;
			  height: 50px;
			  background: darkblue;
			  color: #fff;
			  border-radius: 15px;
			  text-align: center;
			  float: left;
			}
			#pts{
			  border-radius: 10px;
			  position: relative;
			  top: 0px;
			  left: 0px;
			  width: 20%;
			  height: 50px;
			  background: darkblue;
			  color: #fff;
			  border-radius: 15px;
			  text-align: center;
			  float: left;
			}


			#box{
			  padding: 0px 0px 50px 20px;
			}

		</style>

        </head>
        <body style="background-image: url(/static/bg_game_CSBC.png);">
        <div>
			<div class="logo">
				<img src="/static/game_CSBC_LOGO.png" style="  width:500px;">
			</div>
			<div id="box"> 
				<div id="numero"><p>Nº</p> </div>
    			<div id="nome"> <p>NOME</p> </div>
    			<div id="pts"> <p>PONTUAÇÃO</p> </div>
  			</div>
			<div class="leaderboard">
				<ol>''' + stringedScores + '''</ol>
			</div>
        </div>
		</body></html>'''

    return (string)


@app.route('/qrshow/2')
def qrshow2():
    univScores = ''.join(['<li><mark>' + str(k) + '</mark>' + '<small>' + str(v) + '</small></li>' for k, v in
                          sorted(ranking.univScores.items(), key=operator.itemgetter(1), reverse=True)[0:15]])

    string = '''
        <html><head>
		<style>
			body {
			  color: #000000;
			  font-family: 'Open Sans', sans-serif;
			}

			.logo{
			  height: auto;
			  width: 100%;
			  text-align: center;
			}

			.leaderboard {
			  position: absolute;
			  width: 100%;
			  height: auto;
			}

			.leaderboard ol {
			  counter-reset: leaderboard;
			  margin-left: -20px;
			}

			.leaderboard ol li {
			  position: relative;
			  list-style:none;
			  font-size: 14px;
			  counter-increment: leaderboard;
			  padding: 18px 0px 40px 0px;
			  cursor: pointer;
			}

			.leaderboard ol li::before {
			  content: counter(leaderboard);
			  position: absolute;
			  top: 0px;
			  left: 0px;
			  width: 10%;
			  padding: 18px 0px 18px 0px;
			  background: purple;
			  color: #fff;
			  border-radius: 15px;
			  text-align: center;
			}

			.leaderboard ol li mark {
			  border-radius: 15px;
			  position: absolute;
			  z-index: 2;
			  top: 0;
			  left: 11%;
			  width: 66%;
			  padding: 18px 0px 18px 0px;
			  background: purple;
			  color: #fff;
			  text-align: center;
			}

			.leaderboard ol li small {
			  border-radius: 15px;
			  position: absolute;
			  top: 0;
			  left: 78%;
			  width: 19%;
			  padding: 18px 0px 18px 0px;
			  background: green;
			  color: #fff;
			  text-align: center;
			}


			#numero{
			  position:relative;
			  top: 0px;
			  left: 0px;
			  width: 10%;
			  height: 50px;
			  background: darkblue;
			  color: #fff;
			  border-radius: 15px;
			  text-align: center;
			  float: left;
			}

			#nome{
			  position:relative;
			   margin: 0px 5px 0px 5px;
			  top: 0px;
			  left: 0px;
			  width: 68%;
			  height: 50px;
			  background: darkblue;
			  color: #fff;
			  border-radius: 15px;
			  text-align: center;
			  float: left;
			}
			#pts{
			  border-radius: 10px;
			  position: relative;
			  top: 0px;
			  left: 0px;
			  width: 20%;
			  height: 50px;
			  background: darkblue;
			  color: #fff;
			  border-radius: 15px;
			  text-align: center;
			  float: left;
			}


			#box{
			  padding: 0px 0px 50px 20px;
			}

		</style>

        </head>
        <body style="background-image: url(/static/bg_game_CSBC.png);">
        <div>
			<div class="logo">
				<img src="/static/game_CSBC_LOGO.png" style="  width:500px;">
			</div>
			<div id="box"> 
				<div id="numero"><p>Nº</p> </div>
    			<div id="nome"> <p>INSTITUIÇÃO</p> </div>
    			<div id="pts"> <p>PONTUAÇÃO</p> </div>
  			</div>
			<div class="leaderboard">
				<ol>''' + univScores + '''</ol>
			</div>
        </div>
		</body></html>'''

    return (string)


@app.route('/qrshow/3')
def qrshow3():
    sessScores = ''.join(['<li><mark>' + str(k) + '</mark>' + '<small>' + str(v) + '</small></li>' for k, v in
                          sorted(ranking.sessScores.items(), key=operator.itemgetter(1), reverse=True)[0:15]])

    string = '''
        <html><head>
		<style>
			body {
			  color: #000000;
			  font-family: 'Open Sans', sans-serif;
			}

			.logo{
			  height: auto;
			  width: 100%;
			  text-align: center;
			}

			.leaderboard {
			  position: absolute;
			  width: 100%;
			  height: auto;
			}

			.leaderboard ol {
			  counter-reset: leaderboard;
			  margin-left: -20px;
			}

			.leaderboard ol li {
			  position: relative;
			  list-style:none;
			  font-size: 14px;
			  counter-increment: leaderboard;
			  padding: 18px 0px 40px 0px;
			  cursor: pointer;
			}

			.leaderboard ol li::before {
			  content: counter(leaderboard);
			  position: absolute;
			  top: 0px;
			  left: 0px;
			  width: 10%;
			  padding: 18px 0px 18px 0px;
			  background: purple;
			  color: #fff;
			  border-radius: 15px;
			  text-align: center;
			}

			.leaderboard ol li mark {
			  border-radius: 15px;
			  position: absolute;
			  z-index: 2;
			  top: 0;
			  left: 11%;
			  width: 66%;
			  padding: 18px 0px 18px 0px;
			  background: purple;
			  color: #fff;
			  text-align: center;
			}

			.leaderboard ol li small {
			  border-radius: 15px;
			  position: absolute;
			  top: 0;
			  left: 78%;
			  width: 19%;
			  padding: 18px 0px 18px 0px;
			  background: green;
			  color: #fff;
			  text-align: center;
			}


			#numero{
			  position:relative;
			  top: 0px;
			  left: 0px;
			  width: 10%;
			  height: 50px;
			  background: darkblue;
			  color: #fff;
			  border-radius: 15px;
			  text-align: center;
			  float: left;
			}

			#nome{
			  position:relative;
			   margin: 0px 5px 0px 5px;
			  top: 0px;
			  left: 0px;
			  width: 68%;
			  height: 50px;
			  background: darkblue;
			  color: #fff;
			  border-radius: 15px;
			  text-align: center;
			  float: left;
			}
			#pts{
			  border-radius: 10px;
			  position: relative;
			  top: 0px;
			  left: 0px;
			  width: 20%;
			  height: 50px;
			  background: darkblue;
			  color: #fff;
			  border-radius: 15px;
			  text-align: center;
			  float: left;
			}


			#box{
			  padding: 0px 0px 50px 20px;
			}

		</style>

        </head>
        <body style="background-image: url(/static/bg_game_CSBC.png);">
        <div>
			<div class="logo">
				<img src="/static/game_CSBC_LOGO.png" style="  width:500px;">
			</div>
			<div id="box"> 
				<div id="numero"><p>Nº</p> </div>
    			<div id="nome"> <p>SESSÃO</p> </div>
    			<div id="pts"> <p>PONTUAÇÃO</p> </div>
  			</div>
			<div class="leaderboard">
				<ol>''' + sessScores + '''</ol>
			</div>
        </div>
		</body></html>'''
    return (string)


@app.route('/qrshow/4')
def qrshow4():
    stateScores = ''.join(['<li><mark>' + str(k) + '</mark>' + '<small>' + str(v) + '</small></li>' for k, v in
                           sorted(ranking.stateScores.items(), key=operator.itemgetter(1), reverse=True)[0:15]])

    string = '''
        <html><head>
		<style>
			body {
			  color: #000000;
			  font-family: 'Open Sans', sans-serif;
			}

			.logo{
			  height: auto;
			  width: 100%;
			  text-align: center;
			}

			.leaderboard {
			  position: absolute;
			  width: 100%;
			  height: auto;
			}

			.leaderboard ol {
			  counter-reset: leaderboard;
			  margin-left: -20px;
			}

			.leaderboard ol li {
			  position: relative;
			  list-style:none;
			  font-size: 14px;
			  counter-increment: leaderboard;
			  padding: 18px 0px 40px 0px;
			  cursor: pointer;
			}

			.leaderboard ol li::before {
			  content: counter(leaderboard);
			  position: absolute;
			  top: 0px;
			  left: 0px;
			  width: 10%;
			  padding: 18px 0px 18px 0px;
			  background: purple;
			  color: #fff;
			  border-radius: 15px;
			  text-align: center;
			}

			.leaderboard ol li mark {
			  border-radius: 15px;
			  position: absolute;
			  z-index: 2;
			  top: 0;
			  left: 11%;
			  width: 66%;
			  padding: 18px 0px 18px 0px;
			  background: purple;
			  color: #fff;
			  text-align: center;
			}

			.leaderboard ol li small {
			  border-radius: 15px;
			  position: absolute;
			  top: 0;
			  left: 78%;
			  width: 19%;
			  padding: 18px 0px 18px 0px;
			  background: green;
			  color: #fff;
			  text-align: center;
			}


			#numero{
			  position:relative;
			  top: 0px;
			  left: 0px;
			  width: 10%;
			  height: 50px;
			  background: darkblue;
			  color: #fff;
			  border-radius: 15px;
			  text-align: center;
			  float: left;
			}

			#nome{
			  position:relative;
			   margin: 0px 5px 0px 5px;
			  top: 0px;
			  left: 0px;
			  width: 68%;
			  height: 50px;
			  background: darkblue;
			  color: #fff;
			  border-radius: 15px;
			  text-align: center;
			  float: left;
			}
			#pts{
			  border-radius: 10px;
			  position: relative;
			  top: 0px;
			  left: 0px;
			  width: 20%;
			  height: 50px;
			  background: darkblue;
			  color: #fff;
			  border-radius: 15px;
			  text-align: center;
			  float: left;
			}


			#box{
			  padding: 0px 0px 50px 20px;
			}

		</style>

        </head>
        <body style="background-image: url(/static/bg_game_CSBC.png);">
        <div>
			<div class="logo">
				<img src="/static/game_CSBC_LOGO.png" style="  width:500px;">
			</div>
			<div id="box"> 
				<div id="numero"><p>Nº</p> </div>
    			<div id="nome"> <p>ESTADO</p> </div>
    			<div id="pts"> <p>PONTUAÇÃO</p> </div>
  			</div>
			<div class="leaderboard">
				<ol>''' + stateScores + '''</ol>
			</div>
        </div>
		</body></html>'''

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


@app.route('/sexta')
def showsched6():
    return render_template('sexta.html')


@app.route('/sessions')
def sessions():
    domingo = "CQEB(9-12),CQEB(9-12),CQEB(14-16),CQEB(14-16),CQEB(16:30-19),CQEB(16:30-19)"
    # segunda = "JAI #1(9-12),JAI #1(16-19),WEI(9-12),WEI(16-19),CTD(9-12),CTD(16-19),WIT(9-12),WIT(16-19),SEMISH(9-12),SEMISH(16-19),SEMISH-hackaton(9-12),SEMISH-hackaton(16-19),WPerformance(9-12),WPerformance(16-19),WTranS(9-12),WTranS(16-19),ETC(9-12),ETC(16-19),CLOUDSCAPE-Brazil(9-12),CLOUDSCAPE-Brazil(16-19),ForumPG(9-12),ForumPG(16-19),SECOMU"
    # terca = "JAI #2(9-12),JAI #2_(16-19),WEI(9-12),WEI(16-19),CTD(9-12),CTIC(16-19),WIT(9-12),WIT(16-19),SEMISH(9-12),SEMISH(16-19),SEMISH-hackaton(9-12),SEMISH-hackaton(16-19),SBCUP(9-12),SBCUP(16-19),WPerformance(9-12),WPerformance(16-19),ETC(9-12),ETC(16-19),WORKSHOP-OnCloundNetworks(9-12),ReuniãoCEs(9-12),Reunião CNPQ/CAPES(16-19),SECOMU"
    # quarta ="JAI #3(9-12),JAI #3_(16-19),WEI(9-12),WEI(16-19),BraSNAM(9-12),BraSNAM(16-19),BreSci(9-12),BreSci(16-19),Reunião SR SBC(9-12),IFIP/SBC(16-19),SBCUP(9-12),SBCUP(16-19),WCAMA(9-12),WCAMA(16-19),WPIETF hackathon(9-12),WPIETF hackathon(16-19),WPIETF(9-12),WPIETF(16-19),COMPUTEC(9-12),COMPUTEC(16-19),Apres. e Prem. do Selo de Inovacao da SBC,SECOMU"
    # quinta ="JAI #4(9-12),JAI #4(16-19),WEI(9-12),WCAMA(16-19),BraSNAM(9-12),BraSNAM(16-19),BreSci(9-12),BreSci(16-19),SBCUP(9-12),SBCUP(16-19),ENCompIP(9-12),ENCompIP(16-19),WFIBRE(9-12),WFIBRE(16-19),WPIETF(9-12),WPIETF(16-19),WASHES(9-12),WASHES(16-19),COMPUTEC(9-12),COMPUTEC(16-19),SECOMU"
    session = domingo
    return "CQEB(9-12),CQEB(9-12),CQEB(14-16),CQEB(14-16),CQEB(16:30-19),CQEB(16:30-19),teste"


@app.route('/patrocinio')
def showpatrocinio():
    return render_template('patrocinio.html')


# app.run(host='0.0.0.0',port=80, threaded=True)
# requests.get('10.0.0.1')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
