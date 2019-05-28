Instruções:

Ambos os modulos se comunicam por HTTP/HTTPS com uma URL mandando requisicoes da forma 

URL/<string>/<sess>/<activity>

onde string é tudo que foi lido no qrcode, sess e activity sao parametros passados para os apps android e iOS.

Para modulo android, optionsSession e optionPart são as variáveis que contem as listas de sessões e tipos de participação, respectivamente. Alterar URL destino da requisicao.

Abrir o projeto com android studio e buildar o APK (build > build app)


Para modulo iOS, dropDown.optionArray e dropDownSess.optionArray sao as variareis com as listas mencionadas acima, de sessões e participações, respectivamente. Alterar URL destino da requisicao.

Abrir o projeto com o Xcode, escolher um device (dropdown perto do botão "play")


Para o BackEnd, instalar flask, python, gunicorn, pickle, mysqlconnector.

instalar mysql na maquina e criar uma database, as consultas ao BD esta todas no inicio do arquivo sbrc.py, lembrar de editar parâmetros para conexão ao BD e alterar consultas.


em @app.route('/qrshow/1') fica um exemplo de tela de gamificação. A classe ranking mantem tudo que fica na memória de trabalho para ser exibido nas telas.


executar o seguinte comando na pasta d4c

"gunicorn --workers=9 --bind 0.0.0.0:80 wsgi" 

Para debug, usar flask
