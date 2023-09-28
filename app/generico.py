from py_rpautom import web_utils as webutils
import urllib3
import warnings
import os

def iniciar_navegador(site="", _nome_navegador_="", _executavel_=""):
    urllib3.disable_warnings()
    os.environ['WDM_SSL_VERIFY'] = '0'
    os.environ['WDM_LOG_LEVEL'] = '0'
    warnings.filterwarnings('ignore')

    options_=(
        '--start-maximized',
        '--disable-logging',
        '--log-level=3',
        'output=/dev/null',
        '--enable-gpu-debugging=false',
        '--enable-gpu-driver-debug-logging=false',
        '--disable-gl-error-limit',
    )

    try:
        webutils.iniciar_navegador(
            url=site, 
            nome_navegador=_nome_navegador_, 
            options=options_
        )
    except:
        webutils.iniciar_navegador(
            url=site, 
            nome_navegador=_nome_navegador_, 
            executavel=_executavel_,
            options=options_,
            baixar_webdriver_previamente=False
        )