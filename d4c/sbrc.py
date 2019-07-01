#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#
#Copyright © 2019-Present Lucas Castanheira
#lbcastanheira@inf.ufrgs.br
#


from flask import Flask
from flask import request, url_for, redirect, send_from_directory,make_response,render_template
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
import re
import subprocess
class Ranking:
    scores={}
    value={'Join':1,'Question':2}
    outs={}
    univScores={}
    sessScores={}
    stateScores={}


try:
    f=open("ongoing.txt", "r")
    ranking=pickle.load(f)
except IOError:
    print("No ongoing.txt, loading from scratch.")
    ranking=Ranking()

import operator


class Ranking:
    scores={}
    value={'Join':1,'Question':1}
    outs={}
    univScores={}
    sessScores={}
    stateScores={}
    participated={}


ranking=Ranking()



import operator
import sys
import traceback

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

    checkRepeatedTemplate='''SELECT Name FROM EventLogs WHERE Name = %s AND session = %s AND participation = "Join"'''

    insertLogTemplate = '''INSERT INTO EventLogs 
              (Name,Institution,state,session,participation,points,lastScore,updated_at)
              VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())'''
    fetchStateTemplate= '''SELECT state,SUM(points)
  FROM EventLogs
 GROUP BY state
 ORDER BY SUM(points) DESC'''



    fetchInstitutionTemplate= ''' SELECT Institution,SUM(points)
 FROM EventLogs
 GROUP BY Institution
 ORDER BY SUM(points) DESC'''

    fetchNameTemplate= ''' SELECT Name,Institution,SUM(points)
 FROM EventLogs
 GROUP BY Name
 ORDER BY SUM(points) DESC'''


    fetchSessTemplate= ''' SELECT session,SUM(points)
 FROM EventLogs
 GROUP BY session
 ORDER BY SUM(points) DESC'''


    cursor.execute(fetchNameTemplate)
	
    for res in cursor:
        ranking.scores[res[0]+' ('+res[1]+')']=int(res[2])

    cursor.execute(fetchInstitutionTemplate)
    for res in cursor:
        ranking.univScores[res[0]]=int(res[1])

    cursor.execute(fetchStateTemplate)
    for res in cursor:
        ranking.stateScores[res[0]]=int(res[1])
    
    cursor.execute(fetchSessTemplate)
    for res in cursor:
        ranking.sessScores[res[0]]=int(res[1])


    sql=True

except:
    traceback.print_exc(file=sys.stdout)
    sql=False
    print('no mysql connector')



@app.route('/qr/<string>/<sess>/<activity>')

def qr(string,sess,activity):
    if(sql):
        global cursor
        global db
        global insertLogTemplate
    csv=string.split(',')
    inst=csv[1]
    id=csv[0]+' ('+inst+')'
    state=csv[2]
    #if opt out or out then rewrite optout else score
    
    
    if(activity=="Join"):

        cursor.execute(checkRepeatedTemplate,(csv[0],sess))
        cursor.fetchall()
        if(cursor.rowcount>0):
            cursor.execute(insertLogTemplate,(csv[0],csv[1],csv[2],sess,0,0,0))
            db.commit()
            return('1')
        else:
            ranking.sessScores[sess] = ranking.sessScores.get(sess,0) + 1

    
    if(activity != 'Optout' and id not in ranking.outs):
        #get points for the activity being logged
        activityScore=ranking.value[activity]
        #Pts for guy and for institution
        points = ranking.scores.get(id,0) + activityScore
        univPoints = ranking.univScores.get(inst,0) + activityScore
        #Score
        ranking.scores[id]=points
        ranking.univScores[inst]=univPoints
    else:
        ranking.outs[id]=True

    ranking.stateScores[state] = ranking.stateScores.get(state,0) + 1


    if(sql):
        cursor.execute(insertLogTemplate,(csv[0],csv[1],csv[2],sess,activity,activityScore,points))
        db.commit()

    return('0')


class FromFile:
    translate="-50%,-15%"
    title="<b>Leaderboard SBRC 2019</b>"


@app.route('/apple-touch-icon.png')
def gtfo():
    return ('0')
@app.route('/apple-touch-icon-precomposed.png.html')
def aaaa():
    return('0')

@app.route('/S',methods=['GET'])
def last():
    if(lastUp):
        return(redirect("http://d4c.wtf/static/arquivos/"+lastUp))
    else:
        return redirect('http://network.d4c.wtf/rasauto.mp4')


@app.route('/qrshow')
def qrshow():
    string='''
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
       {url: "http://sbrc.inf.ufrgs.br/qrshow/1", time: 8, refresh: true},
       {url: "http://sbrc.inf.ufrgs.br/qrshow/2", time: 8, refresh: true},
       {url: "http://sbrc.inf.ufrgs.br/qrshow/3", time: 8, refresh: true},
       {url: "http://sbrc.inf.ufrgs.br/patrocinio", time: 8, refresh: false},
       {url: "http://sbrc.inf.ufrgs.br/segunda", time: 60, refresh: true}
       
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
</body>
</html>'''
    return string


@app.route("/favicon.ico")
def favicon():
    return('322')
@app.route('/qrshow/1')
def qrshow1():
    stringedScores=''.join(['<li><mark>'+str(k)+'</mark>'+'<small>'+str(v)+'</small></li>' for k,v in sorted(ranking.scores.items(), key=operator.itemgetter(1), reverse=True)[0:5]])
    
    string='''
        <head>
        <link rel="stylesheet" type="text/css" href="/static/css/timer.css">
        <link rel="stylesheet" type="text/css" href="/static/css/leaderboard.css">
        </head>
        <body style="background:#000000">
        <div style="width:500px;height:1000px;">
        <img src="/static/bg.png"  style="position:absolute;top:0px;width:100%;height:100%" alt="bg"></img>
<div class="centered">'''+FromFile.title+'''</div>

        <div class="leaderboard" style="zoom: 210%;-webkit-transform: translate(-43px, -235px);transform: translate(-43px, -235px);-ms-transform: translate(-43px, -235px);">
        <h1>
        <svg class="ico-cup">
        <use xlink:href="#cup"></use>
        </svg>
        Participantes
        </h1>
        <ol>'''+stringedScores+'''
            </ol>
            </div>
            
            
            <svg style="display: none;">
            <symbol id="cup" x="0px" y="0px"
            width="25px" height="26px" viewBox="0 0 25 26" enable-background="new 0 0 25 26" xml:space="preserve">
            <path fill="#F26856" d="M21.215,1.428c-0.744,0-1.438,0.213-2.024,0.579V0.865c0-0.478-0.394-0.865-0.88-0.865H6.69
            C6.204,0,5.81,0.387,5.81,0.865v1.142C5.224,1.641,4.53,1.428,3.785,1.428C1.698,1.428,0,3.097,0,5.148
            C0,7.2,1.698,8.869,3.785,8.869h1.453c0.315,0,0.572,0.252,0.572,0.562c0,0.311-0.257,0.563-0.572,0.563
            c-0.486,0-0.88,0.388-0.88,0.865c0,0.478,0.395,0.865,0.88,0.865c0.421,0,0.816-0.111,1.158-0.303
            c0.318,0.865,0.761,1.647,1.318,2.31c0.686,0.814,1.515,1.425,2.433,1.808c-0.04,0.487-0.154,1.349-0.481,2.191
            c-0.591,1.519-1.564,2.257-2.975,2.257H5.238c-0.486,0-0.88,0.388-0.88,0.865v4.283c0,0.478,0.395,0.865,0.88,0.865h14.525
            c0.485,0,0.88-0.388,0.88-0.865v-4.283c0-0.478-0.395-0.865-0.88-0.865h-1.452c-1.411,0-2.385-0.738-2.975-2.257
            c-0.328-0.843-0.441-1.704-0.482-2.191c0.918-0.383,1.748-0.993,2.434-1.808c0.557-0.663,1-1.445,1.318-2.31
            c0.342,0.192,0.736,0.303,1.157,0.303c0.486,0,0.88-0.387,0.88-0.865c0-0.478-0.394-0.865-0.88-0.865
            c-0.315,0-0.572-0.252-0.572-0.563c0-0.31,0.257-0.562,0.572-0.562h1.452C23.303,8.869,25,7.2,25,5.148
            C25,3.097,23.303,1.428,21.215,1.428z M5.238,7.138H3.785c-1.116,0-2.024-0.893-2.024-1.99c0-1.097,0.908-1.99,2.024-1.99
            c1.117,0,2.025,0.893,2.025,1.99v2.06C5.627,7.163,5.435,7.138,5.238,7.138z M18.883,21.717v2.553H6.118v-2.553H18.883
            L18.883,21.717z M13.673,18.301c0.248,0.65,0.566,1.214,0.947,1.686h-4.24c0.381-0.472,0.699-1.035,0.947-1.686
            c0.33-0.865,0.479-1.723,0.545-2.327c0.207,0.021,0.416,0.033,0.627,0.033c0.211,0,0.42-0.013,0.627-0.033
            C13.195,16.578,13.344,17.436,13.673,18.301z M12.5,14.276c-2.856,0-4.93-2.638-4.93-6.273V1.73h9.859v6.273
            C17.43,11.638,15.357,14.276,12.5,14.276z M21.215,7.138h-1.452c-0.197,0-0.39,0.024-0.572,0.07v-2.06
            c0-1.097,0.908-1.99,2.024-1.99c1.117,0,2.025,0.893,2.025,1.99C23.241,6.246,22.333,7.138,21.215,7.138z"/>
            </symbol>
            </svg>
            </div>

            <div id="countdown">
            <svg style="width:40px;height:40px;transform:scale(3)">
            <circle r="18" cx="20" cy="20"></circle>
            </svg>
            </div>
	    <img width="300px" height="auto" style="position: absolute;right: 0px;bottom: 0px;" src="/static/inf.png" />
            </body>
            
            
            
            
            '''
        
    return(string)

@app.route('/qrshow/2')
def qrshow2():
    univScores=''.join(['<li><mark>'+str(k)+'</mark>'+'<small>'+str(v)+'</small></li>' for k,v in sorted(ranking.univScores.items(), key=operator.itemgetter(1), reverse=True)[0:5]])
    
    string='''
        <head>
        <link rel="stylesheet" type="text/css" href="/static/css/timer.css">
        <link rel="stylesheet" type="text/css" href="/static/css/leaderboard.css">
        </head>
 <body style="background:#000000">
        <img src="/static/bg.png"  style="position:absolute;top:0px;width:100%;height:100%" alt="bg"></img>
        <div class="centered">'''+FromFile.title+'''</div>
        <div class="leaderboard" style="zoom: 210%;-webkit-transform: translate(-43px, -235px);transform: translate(-43px, -235px);-ms-transform: translate(-43px, -235px);">
        <h1>
        <svg class="ico-cup">
        <use xlink:href="#cup"></use>
        </svg>
        Instituições
        </h1>
        <ol>'''+univScores+'''
            </ol>
            </div>
            
            <svg style="display: none;">
            <symbol id="cup" x="0px" y="0px"
            width="25px" height="26px" viewBox="0 0 25 26" enable-background="new 0 0 25 26" xml:space="preserve">
            <path fill="#F26856" d="M21.215,1.428c-0.744,0-1.438,0.213-2.024,0.579V0.865c0-0.478-0.394-0.865-0.88-0.865H6.69
            C6.204,0,5.81,0.387,5.81,0.865v1.142C5.224,1.641,4.53,1.428,3.785,1.428C1.698,1.428,0,3.097,0,5.148
            C0,7.2,1.698,8.869,3.785,8.869h1.453c0.315,0,0.572,0.252,0.572,0.562c0,0.311-0.257,0.563-0.572,0.563
            c-0.486,0-0.88,0.388-0.88,0.865c0,0.478,0.395,0.865,0.88,0.865c0.421,0,0.816-0.111,1.158-0.303
            c0.318,0.865,0.761,1.647,1.318,2.31c0.686,0.814,1.515,1.425,2.433,1.808c-0.04,0.487-0.154,1.349-0.481,2.191
            c-0.591,1.519-1.564,2.257-2.975,2.257H5.238c-0.486,0-0.88,0.388-0.88,0.865v4.283c0,0.478,0.395,0.865,0.88,0.865h14.525
            c0.485,0,0.88-0.388,0.88-0.865v-4.283c0-0.478-0.395-0.865-0.88-0.865h-1.452c-1.411,0-2.385-0.738-2.975-2.257
            c-0.328-0.843-0.441-1.704-0.482-2.191c0.918-0.383,1.748-0.993,2.434-1.808c0.557-0.663,1-1.445,1.318-2.31
            c0.342,0.192,0.736,0.303,1.157,0.303c0.486,0,0.88-0.387,0.88-0.865c0-0.478-0.394-0.865-0.88-0.865
            c-0.315,0-0.572-0.252-0.572-0.563c0-0.31,0.257-0.562,0.572-0.562h1.452C23.303,8.869,25,7.2,25,5.148
            C25,3.097,23.303,1.428,21.215,1.428z M5.238,7.138H3.785c-1.116,0-2.024-0.893-2.024-1.99c0-1.097,0.908-1.99,2.024-1.99
            c1.117,0,2.025,0.893,2.025,1.99v2.06C5.627,7.163,5.435,7.138,5.238,7.138z M18.883,21.717v2.553H6.118v-2.553H18.883
            L18.883,21.717z M13.673,18.301c0.248,0.65,0.566,1.214,0.947,1.686h-4.24c0.381-0.472,0.699-1.035,0.947-1.686
            c0.33-0.865,0.479-1.723,0.545-2.327c0.207,0.021,0.416,0.033,0.627,0.033c0.211,0,0.42-0.013,0.627-0.033
            C13.195,16.578,13.344,17.436,13.673,18.301z M12.5,14.276c-2.856,0-4.93-2.638-4.93-6.273V1.73h9.859v6.273
            C17.43,11.638,15.357,14.276,12.5,14.276z M21.215,7.138h-1.452c-0.197,0-0.39,0.024-0.572,0.07v-2.06
            c0-1.097,0.908-1.99,2.024-1.99c1.117,0,2.025,0.893,2.025,1.99C23.241,6.246,22.333,7.138,21.215,7.138z"/>
            </symbol>
            </svg>
            
            <div id="countdown">
            <svg style="width:40px;height:40px;transform:scale(3)">
            <circle r="18" cx="20" cy="20"></circle>
            </svg>
            </div>
            <img width="300px" height="auto" style="position: absolute;right: 0px;bottom: 0px;" src="/static/inf.png" />
  
            </body>
            
            '''
        
    return(string)


@app.route('/qrshow/3')
def qrshow3():
    sessScores=''.join(['<li><mark>'+str(k)+'</mark>'+'<small>'+str(v)+'</small></li>' for k,v in sorted(ranking.sessScores.items(), key=operator.itemgetter(1), reverse=True)[0:5]])
    
    string='''
        <head>
        <link rel="stylesheet" type="text/css" href="/static/css/timer.css">
        <link rel="stylesheet" type="text/css" href="/static/css/leaderboard.css">
        </head>
 <body style="background:#000000">
        <img src="/static/bg.png"  style="position:absolute;top:0px;width:100%;height:100%" alt="bg"></img>
        <div class="centered">'''+FromFile.title+'''</div>
        <div class="leaderboard" style="zoom: 210%;-webkit-transform: translate(-43px, -235px);transform: translate(-43px, -235px);-ms-transform: translate(-43px, -235px);">
        <h1>
        <svg class="ico-cup">
        <use xlink:href="#cup"></use>
        </svg>
        Sessões
        </h1>
        <ol>'''+sessScores+'''
            </ol>
            </div>
            
            <svg style="display: none;">
            <symbol id="cup" x="0px" y="0px"
            width="25px" height="26px" viewBox="0 0 25 26" enable-background="new 0 0 25 26" xml:space="preserve">
            <path fill="#F26856" d="M21.215,1.428c-0.744,0-1.438,0.213-2.024,0.579V0.865c0-0.478-0.394-0.865-0.88-0.865H6.69
            C6.204,0,5.81,0.387,5.81,0.865v1.142C5.224,1.641,4.53,1.428,3.785,1.428C1.698,1.428,0,3.097,0,5.148
            C0,7.2,1.698,8.869,3.785,8.869h1.453c0.315,0,0.572,0.252,0.572,0.562c0,0.311-0.257,0.563-0.572,0.563
            c-0.486,0-0.88,0.388-0.88,0.865c0,0.478,0.395,0.865,0.88,0.865c0.421,0,0.816-0.111,1.158-0.303
            c0.318,0.865,0.761,1.647,1.318,2.31c0.686,0.814,1.515,1.425,2.433,1.808c-0.04,0.487-0.154,1.349-0.481,2.191
            c-0.591,1.519-1.564,2.257-2.975,2.257H5.238c-0.486,0-0.88,0.388-0.88,0.865v4.283c0,0.478,0.395,0.865,0.88,0.865h14.525
            c0.485,0,0.88-0.388,0.88-0.865v-4.283c0-0.478-0.395-0.865-0.88-0.865h-1.452c-1.411,0-2.385-0.738-2.975-2.257
            c-0.328-0.843-0.441-1.704-0.482-2.191c0.918-0.383,1.748-0.993,2.434-1.808c0.557-0.663,1-1.445,1.318-2.31
            c0.342,0.192,0.736,0.303,1.157,0.303c0.486,0,0.88-0.387,0.88-0.865c0-0.478-0.394-0.865-0.88-0.865
            c-0.315,0-0.572-0.252-0.572-0.563c0-0.31,0.257-0.562,0.572-0.562h1.452C23.303,8.869,25,7.2,25,5.148
            C25,3.097,23.303,1.428,21.215,1.428z M5.238,7.138H3.785c-1.116,0-2.024-0.893-2.024-1.99c0-1.097,0.908-1.99,2.024-1.99
            c1.117,0,2.025,0.893,2.025,1.99v2.06C5.627,7.163,5.435,7.138,5.238,7.138z M18.883,21.717v2.553H6.118v-2.553H18.883
            L18.883,21.717z M13.673,18.301c0.248,0.65,0.566,1.214,0.947,1.686h-4.24c0.381-0.472,0.699-1.035,0.947-1.686
            c0.33-0.865,0.479-1.723,0.545-2.327c0.207,0.021,0.416,0.033,0.627,0.033c0.211,0,0.42-0.013,0.627-0.033
            C13.195,16.578,13.344,17.436,13.673,18.301z M12.5,14.276c-2.856,0-4.93-2.638-4.93-6.273V1.73h9.859v6.273
            C17.43,11.638,15.357,14.276,12.5,14.276z M21.215,7.138h-1.452c-0.197,0-0.39,0.024-0.572,0.07v-2.06
            c0-1.097,0.908-1.99,2.024-1.99c1.117,0,2.025,0.893,2.025,1.99C23.241,6.246,22.333,7.138,21.215,7.138z"/>
            </symbol>
            </svg>
            <div id="countdown">
            <svg style="width:40px;height:40px;transform:scale(3)">
            <circle r="18" cx="20" cy="20"></circle>
            </svg>
            </div>
            <img width="300px" height="auto" style="position: absolute;right: 0px;bottom: 0px;" src="/static/inf.png" />
            </body>
            
            '''
        
    return(string)


@app.route('/qrshow/4')
def qrshow4():
    stateScores=''.join(['<li><mark>'+str(k)+'</mark>'+'<small>'+str(v)+'</small></li>' for k,v in sorted(ranking.stateScores.items(), key=operator.itemgetter(1), reverse=True)[0:5]])
    
    string='''
        <head>
        <link rel="stylesheet" type="text/css" href="/static/css/timer.css">
        <link rel="stylesheet" type="text/css" href="/static/css/leaderboard.css">
        </head>
 <body style="background:#000000">
        <img src="/static/bg.png"  style="position:absolute;top:0px;width:100%;height:100%" alt="bg"></img>
        <div class="centered">'''+FromFile.title+'''</div>
        <div class="leaderboard" style="zoom: 210%;-webkit-transform: translate(-43px, -235px);transform: translate(-43px, -235px);-ms-transform: translate(-43px, -235px);">
        <h1>
        <svg class="ico-cup">
        <use xlink:href="#cup"></use>
        </svg>
        Estados
        </h1>
        <ol>'''+stateScores+'''
            </ol>
            </div>
            
            <svg style="display: none;">
            <symbol id="cup" x="0px" y="0px"
            width="25px" height="26px" viewBox="0 0 25 26" enable-background="new 0 0 25 26" xml:space="preserve">
            <path fill="#F26856" d="M21.215,1.428c-0.744,0-1.438,0.213-2.024,0.579V0.865c0-0.478-0.394-0.865-0.88-0.865H6.69
            C6.204,0,5.81,0.387,5.81,0.865v1.142C5.224,1.641,4.53,1.428,3.785,1.428C1.698,1.428,0,3.097,0,5.148
            C0,7.2,1.698,8.869,3.785,8.869h1.453c0.315,0,0.572,0.252,0.572,0.562c0,0.311-0.257,0.563-0.572,0.563
            c-0.486,0-0.88,0.388-0.88,0.865c0,0.478,0.395,0.865,0.88,0.865c0.421,0,0.816-0.111,1.158-0.303
            c0.318,0.865,0.761,1.647,1.318,2.31c0.686,0.814,1.515,1.425,2.433,1.808c-0.04,0.487-0.154,1.349-0.481,2.191
            c-0.591,1.519-1.564,2.257-2.975,2.257H5.238c-0.486,0-0.88,0.388-0.88,0.865v4.283c0,0.478,0.395,0.865,0.88,0.865h14.525
            c0.485,0,0.88-0.388,0.88-0.865v-4.283c0-0.478-0.395-0.865-0.88-0.865h-1.452c-1.411,0-2.385-0.738-2.975-2.257
            c-0.328-0.843-0.441-1.704-0.482-2.191c0.918-0.383,1.748-0.993,2.434-1.808c0.557-0.663,1-1.445,1.318-2.31
            c0.342,0.192,0.736,0.303,1.157,0.303c0.486,0,0.88-0.387,0.88-0.865c0-0.478-0.394-0.865-0.88-0.865
            c-0.315,0-0.572-0.252-0.572-0.563c0-0.31,0.257-0.562,0.572-0.562h1.452C23.303,8.869,25,7.2,25,5.148
            C25,3.097,23.303,1.428,21.215,1.428z M5.238,7.138H3.785c-1.116,0-2.024-0.893-2.024-1.99c0-1.097,0.908-1.99,2.024-1.99
            c1.117,0,2.025,0.893,2.025,1.99v2.06C5.627,7.163,5.435,7.138,5.238,7.138z M18.883,21.717v2.553H6.118v-2.553H18.883
            L18.883,21.717z M13.673,18.301c0.248,0.65,0.566,1.214,0.947,1.686h-4.24c0.381-0.472,0.699-1.035,0.947-1.686
            c0.33-0.865,0.479-1.723,0.545-2.327c0.207,0.021,0.416,0.033,0.627,0.033c0.211,0,0.42-0.013,0.627-0.033
            C13.195,16.578,13.344,17.436,13.673,18.301z M12.5,14.276c-2.856,0-4.93-2.638-4.93-6.273V1.73h9.859v6.273
            C17.43,11.638,15.357,14.276,12.5,14.276z M21.215,7.138h-1.452c-0.197,0-0.39,0.024-0.572,0.07v-2.06
            c0-1.097,0.908-1.99,2.024-1.99c1.117,0,2.025,0.893,2.025,1.99C23.241,6.246,22.333,7.138,21.215,7.138z"/>
            </symbol>
            </svg>
	    <img width="300px" height="auto" style="position: absolute;right: 0px;bottom: 0px;" src="/static/inf.png" />
            </body>
            
            
            '''
        
    return(string)



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
	#segunda = "JAI #1(9-12),JAI #1(16-19),WEI(9-12),WEI(16-19),CTD(9-12),CTD(16-19),WIT(9-12),WIT(16-19),SEMISH(9-12),SEMISH(16-19),SEMISH-hackaton(9-12),SEMISH-hackaton(16-19),WPerformance(9-12),WPerformance(16-19),WTranS(9-12),WTranS(16-19),ETC(9-12),ETC(16-19),CLOUDSCAPE-Brazil(9-12),CLOUDSCAPE-Brazil(16-19),ForumPG(9-12),ForumPG(16-19),SECOMU" 
	#terca = "JAI #2(9-12),JAI #2_(16-19),WEI(9-12),WEI(16-19),CTD(9-12),CTIC(16-19),WIT(9-12),WIT(16-19),SEMISH(9-12),SEMISH(16-19),SEMISH-hackaton(9-12),SEMISH-hackaton(16-19),SBCUP(9-12),SBCUP(16-19),WPerformance(9-12),WPerformance(16-19),ETC(9-12),ETC(16-19),WORKSHOP-OnCloundNetworks(9-12),ReuniãoCEs(9-12),Reunião CNPQ/CAPES(16-19),SECOMU" 
	#quarta ="JAI #3(9-12),JAI #3_(16-19),WEI(9-12),WEI(16-19),BraSNAM(9-12),BraSNAM(16-19),BreSci(9-12),BreSci(16-19),Reunião SR SBC(9-12),IFIP/SBC(16-19),SBCUP(9-12),SBCUP(16-19),WCAMA(9-12),WCAMA(16-19),WPIETF hackathon(9-12),WPIETF hackathon(16-19),WPIETF(9-12),WPIETF(16-19),COMPUTEC(9-12),COMPUTEC(16-19),Apres. e Prem. do Selo de Inovacao da SBC,SECOMU"
	#quinta ="JAI #4(9-12),JAI #4(16-19),WEI(9-12),WCAMA(16-19),BraSNAM(9-12),BraSNAM(16-19),BreSci(9-12),BreSci(16-19),SBCUP(9-12),SBCUP(16-19),ENCompIP(9-12),ENCompIP(16-19),WFIBRE(9-12),WFIBRE(16-19),WPIETF(9-12),WPIETF(16-19),WASHES(9-12),WASHES(16-19),COMPUTEC(9-12),COMPUTEC(16-19),SECOMU"
	
	session = domingo;
	
	return sessions
	
	
@app.route('/patrocinio')
def showpatrocinio():
    return render_template('patrocinio.html')


#app.run(host='0.0.0.0',port=80, threaded=True)
#requests.get('10.0.0.1')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
