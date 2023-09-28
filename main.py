######################################## importacao ################################################

from py_rpautom import python_utils as pyutils
from py_rpautom import web_utils as webutils
from app.dicionario_preparar_ambiente import *
from app.excecoes import *
import app.generico as generico
import app.youtube_utils as youtube
from time import sleep
import os
######################################## Var Global ################################################

mensagem_excecao = ""
caminho_absoluto = pyutils.coletar_arvore_caminho(__file__) + "\\"
caminho_absoluto_config = caminho_absoluto + 'config.ini'
caminho_absoluto_canais_youtube = caminho_absoluto + 'arquivo_site_youtube.txt'
site_youtube = ''
nome_usuario = os.getenv('USERNAME')
caminho_web_driver = f'C:\\Users\\{nome_usuario}\\webdrivers\\edgedriver'
data_util = pyutils.retornar_data_hora_atual(parametro="%d_%m_%Y")
nome_navegador_ = ''
executavel_= ''
login_yb = ""
senha_yb = ""
mensagem_comentario = ""
caminho_absoluto_com_arquivo_log = ''
caminho_absoluto_com_arquivo_log_cais_e_video = ''
usuario_comentario = ''
login_yb = ''
senha_yb = ''

####################################### Global ###################################################


def preparar_ambiente():

    from app.excecoes import (
        lista_erros_preparar_ambiente,
    )

    global data_util
    global site_youtube
    global caminho_absoluto_config
    global caminho_absoluto_com_arquivo_log
    global nome_navegador_
    global mensagem_excecao
    global senha_yb
    global login_yb
    global caminho_absoluto_canais_youtube
    global mensagem_comentario
    global caminho_absoluto_com_arquivo_log_cais_e_video
    global usuario_comentario
    global executavel_
    
    try:
        
        for variavel_coletada in list(variaveis_configuracao):
            nome_bloco_config_ = variaveis_configuracao[variavel_coletada]['nome_bloco_config']
            nome_variavel_ = variaveis_configuracao[variavel_coletada]['nome_variavel']
            encoding_ = variaveis_configuracao[variavel_coletada]['encoding']
            criar_pasta_ = variaveis_configuracao[variavel_coletada]['criar_pasta']

            valor_coletado = pyutils.ler_variavel_ambiente(
                arquivo_config = caminho_absoluto_config, 
                nome_bloco_config = nome_bloco_config_, 
                nome_variavel = nome_variavel_,
                encoding = encoding_
            )

            globals()[variavel_coletada] = valor_coletado

            if criar_pasta_ is True:
                if pyutils.caminho_existente(caminho=nome_variavel_):
                    pyutils.criar_pasta(caminho=nome_variavel_)

        
        caminho_absoluto_log = caminho_absoluto + 'logs'
        caminho_absoluto_log = caminho_absoluto_log.removesuffix('\\')
        nome_arquivo_log = f'\\log_{data_util}.txt' 
        caminho_absoluto_com_arquivo_log = caminho_absoluto_log + nome_arquivo_log

        ano = pyutils.retornar_data_hora_atual(parametro="%Y") 
        nome_arquivo_log_todos_videos = f'\\log_cais_e_videos_{ano}.txt' 
        pasta_comentarios = caminho_absoluto_log + '\\pasta_comentarios'
        caminho_absoluto_com_arquivo_log_cais_e_video = pasta_comentarios + nome_arquivo_log_todos_videos

        #Capturando login da variavel de ambiente do windows
        try:
            login_yb = os.environ['usuario_yt']
            if login_yb == "":
                raise
        except:
            print(lista_erros_preparar_ambiente['login_yb'])

        #Capturando senha da variavel de ambiente do windows
        try:
            senha_yb = os.environ['senha_yt']
            if senha_yb == "":
                raise
        except:
            print(lista_erros_preparar_ambiente['senha_yb'])

        #Capturar caminho absoluto de lista de arquivos dentro da pasta
        lista_arquivos_web_drivers = pyutils.retornar_arquivos_em_pasta(
            caminho=caminho_web_driver, 
            filtro = '**/*'
        )

        if not lista_arquivos_web_drivers == []:
            executavel_ = max(lista_arquivos_web_drivers)

        if not pyutils.caminho_existente(caminho=caminho_absoluto_log):
            pyutils.criar_pasta(caminho=caminho_absoluto_log)

        if not pyutils.caminho_existente(caminho=pasta_comentarios):
            pyutils.criar_pasta(caminho=pasta_comentarios)

        if not pyutils.caminho_existente(caminho=caminho_absoluto_com_arquivo_log):
            pyutils.gravar_log_em_arquivo(
                arquivo=caminho_absoluto_com_arquivo_log,
                conteudo=[
                    'nivel',
                    'data_atual',
                    'status',
                    'mensagem',
                    'nome_video'
                ],
                modo='w',
                encoding='utf8',
                delimitador=';',
                nova_linha='\n',
            )

        if not pyutils.caminho_existente(caminho=caminho_absoluto_com_arquivo_log_cais_e_video):
            pyutils.gravar_log_em_arquivo(
                arquivo=caminho_absoluto_com_arquivo_log_cais_e_video,
                conteudo=[
                    'data_atual',
                    'status',
                    'mensagem',
                    'canal',
                    'nome_video'
                ],
                modo='w',
                encoding='utf8',
                delimitador=';',
                nova_linha='\n',
            )

        nivel="INFO"
        status = 'OK'
        mensagem = 'Preparar ambiente finalizado com sucesso'
        nome_video = '-'
        pyutils.gravar_log_em_arquivo(
            arquivo=caminho_absoluto_com_arquivo_log,
            conteudo=[
                nivel,
                data_util,
                status,
                mensagem,
                nome_video
            ],
            modo='a',
            encoding='utf8',
            delimitador=';',
            nova_linha='\n',
        )
        
    except Exception as erro:
        print(f"Erro na linha {erro.__traceback__.tb_lineno}")
        print(f"Mensagem: \n {erro}\n")
        breakpoint()
        if str(erro) in list(lista_erros_configuracao.values()):
            mensagem_excecao = str(erro)
            nivel = "WARNING"

        if mensagem_excecao == '':
            nivel = 'CRITICAL'

        if not nivel.upper() == 'INFO':
            mensagem_excecao = {
                f'Erro na linha {erro.__traceback__.tb_lineno}'
            }

        status = 'NOK'
        nome_video = '-'
        pyutils.gravar_log_em_arquivo(
            arquivo=caminho_absoluto_com_arquivo_log,
            conteudo=[
                nivel,
                data_util,
                status,
                mensagem_excecao,
                nome_video
            ],
            modo='a',
            encoding='utf8',
            delimitador=';',
            nova_linha='\n',
        )

    finally:
        if not mensagem_excecao == "":
            raise SyntaxError(mensagem_excecao)
    return True


def iniciar_processos():
    global data_util
    global site_youtube
    global caminho_absoluto_config
    global caminho_absoluto_com_arquivo_log
    global nome_navegador_
    global mensagem_excecao
    global senha_yb
    global login_yb
    

    try:

        generico.iniciar_navegador(
            site=site_youtube, 
            _nome_navegador_=nome_navegador_, 
            _executavel_=executavel_
        )
        
        webutils.esperar_pagina_carregar()       
        
    except Exception as erro:
        print(f"Erro na linha {erro.__traceback__.tb_lineno}")
        print(f"Mensagem: \n {erro}\n")

        if str(erro) in list(lista_erros_configuracao.values()):
            mensagem_excecao = str(erro)
            nivel = "WARNING"

        if mensagem_excecao == '':
            nivel = 'CRITICAL'

        if not nivel.upper() == 'INFO':
            mensagem_excecao = {
                f'Erro na linha {erro.__traceback__.tb_lineno}'
            }

        status = 'NOK'
        nome_video = '-'
        pyutils.gravar_log_em_arquivo(
            arquivo=caminho_absoluto_com_arquivo_log,
            conteudo=[
                data_util,
                status,
                mensagem_excecao,
                nome_video
            ],
            modo='a',
            encoding='utf8',
            delimitador=';',
            nova_linha='\n',
        )

    finally:
        if not mensagem_excecao == "":
            raise SyntaxError(mensagem_excecao)


def executar_processos():
    global data_util
    global site_youtube
    global caminho_absoluto_config
    global caminho_absoluto_com_arquivo_log
    global nome_navegador_
    global mensagem_excecao
    global senha_yb
    global login_yb

    try:
        
        """
        def validar_retorno(validar:bool):
            if validar is False:
                mensagem = ""
                raise SyntaxError(str(mensagem))#"""
        """
        validar_retorno(
            validar=youtube.fazer_login(
                login=login_yb, 
                senha=senha_yb
            )
        )#"""
        
        retorno_arquivo_txt = pyutils.abrir_arquivo_texto(
                caminho=caminho_absoluto_canais_youtube,
            )

        lista_canais_youtuber = retorno_arquivo_txt.split('\n')

        #Retirando duplicidades de canais
        lista_canais_youtuber_ = []
        for linha in lista_canais_youtuber:
            if not lista_canais_youtuber_.__contains__(linha) and not linha == '':
                lista_canais_youtuber_.append(linha)

        retorno_arquivo_txt = pyutils.abrir_arquivo_texto(
                caminho=caminho_absoluto_com_arquivo_log_cais_e_video,
            )
        
        lista_comentarios_ja_enviados = retorno_arquivo_txt.split('\n')
        
        lista_nome_videos = []
        lista = []
        for indice in range(len(lista_comentarios_ja_enviados)):
            if indice == 0:
                continue
            lista = lista_comentarios_ja_enviados[indice].split(';')
            lista_nome_videos.append(lista[len(lista)-1])

        for indice in range(len(lista_canais_youtuber)):
            validar_aba = youtube.acessar_e_clicar_aba_youtube(link=lista_canais_youtuber[indice], aba="Vídeos")
            ...

        status = "OK"
        data_util_ = pyutils.retornar_data_hora_atual(parametro="%d/%m/%Y %H:%M:%S")
        nome_video = ""
        pyutils.gravar_log_em_arquivo(
            arquivo=caminho_absoluto_com_arquivo_log_cais_e_video,
            conteudo=[
                data_util_,
                status,
                mensagem_comentario,
                lista_canais_youtuber[indice],
                nome_video
            ],
            modo='a',
            encoding='utf8',
            delimitador=';',
            nova_linha='\n',
        )

        pyutils.gravar_log_em_arquivo(
            arquivo=caminho_absoluto_com_arquivo_log,
            conteudo=[
                data_util,
                status,
                mensagem_comentario,
                nome_video + f"|nome canal: {lista_canais_youtuber[indice]}"
            ],
            modo='a',
            encoding='utf8',
            delimitador=';',
            nova_linha='\n',
        )

        webutils.abrir_pagina(url=site_youtube)
        webutils.esperar_pagina_carregar()

        webutils.encerrar_navegador()
        
    except Exception as erro:
        print(f"Erro na linha {erro.__traceback__.tb_lineno}")
        print(f"Mensagem: \n {erro}\n")
        breakpoint()
        if str(erro) in list(lista_erros_configuracao.values()):
            mensagem_excecao = str(erro)
            nivel = "WARNING"

        if mensagem_excecao == '':
            nivel = 'CRITICAL'

        if not nivel.upper() == 'INFO':
            mensagem_excecao = {
                f'Erro na linha {erro.__traceback__.tb_lineno}'
            }

        status = 'NOK'
        nome_video = '-'
        pyutils.gravar_log_em_arquivo(
            arquivo=caminho_absoluto_com_arquivo_log,
            conteudo=[
                data_util,
                status,
                mensagem_excecao,
                nome_video
            ],
            modo='a',
            encoding='utf8',
            delimitador=';',
            nova_linha='\n',
        )
    finally:
        if not mensagem_excecao == "":
            raise SyntaxError(mensagem_excecao)

preparar_ambiente()
iniciar_processos()
executar_processos()