**Overview**

![GitHub Logo](/Overview.png)

Principais Modulos:

App iOS/Android: Escaneia os QR codes e envia para o servidor por HTTP/S

Backend Python: Aplica as regras do esquema especifico de Gamificacao (e.g., Pontos por sessão, se o usuario pode pontuar mais de uma vez em uma sessão, etc...) e guarda as requisicões no banco de dados MySQL. O backend quando religado sempre carrega os dados a partir do BD MySQL.

Frontend Python: composto de 4 telas que exibem os top 5 **Participantes**, **Instituicoes**, **Sessões**, **Estados**

**Instruções:**

**Gerais**

Ambos os modulos se comunicam por HTTP/HTTPS com uma URL mandando requisicoes da forma 

**```URL/<string>/<sess>/<activity>```**

Onde string é tudo que foi lido no qrcode, sess e activity sao parametros passados para os apps android e iOS em dois campos de selecao.


**Especificas**

Para **modulo android**, Alterar URL destino da requisição na linha 30 do arquivo Gamification/BarcodeReaderSample-master/app/src/main/java/com/varvet/barcodereadersample/MainActivity.kt

    Abrir o projeto com android studio e buildar o APK (build > build apk)


Para **modulo iOS**, Alterar URL destino da requisicao na Linha 55  do arquivo Gamification/QRCodeReader/Example/QRCodeReader.swift/ViewController.swift


    Abrir o projeto com o **Xcode**, escolher um iPhone conectado ao Mac (dropdown perto do botão "play") e apertar play


Para o **BackEnd**, instalar flask, python, gunicorn, pickle, mysqlconnector e MySQL.

    Criar uma database no mysql, as consultas ao BD esta todas no inicio do arquivo sbrc.py, lembrar de editar parâmetros para conexão ao BD e alterar consultas para se adequarem a base de dados que foi criada.

    Em @app.route('/qrshow/1') fica um exemplo de tela de gamificação. A classe ranking mantem tudo que fica na memória de trabalho para ser exibido nas telas.


**Para Executar Backend**

Executar o seguinte comando na pasta d4c

    "gunicorn --workers=9 --bind 0.0.0.0:80 wsgi" 

**Para debug**

    "python3 sbrc.py"


**Copyright (C) Lucas Castanheira 2019**
