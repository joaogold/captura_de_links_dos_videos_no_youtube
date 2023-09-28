from py_rpautom import web_utils as webutils


def validar_login():
    try:
        try:
            webutils.aguardar_elemento(
                identificador="//span[text()='Fazer login']", 
                tipo_elemento = 'xpath', 
                comportamento_esperado = 'ELEMENT_TO_BE_CLICKABLE', 
                tempo = 3
            )
        except:
            webutils.aguardar_elemento(
                identificador="//span[text()='Fazer login']", 
                tipo_elemento = 'xpath', 
                comportamento_esperado = 'ELEMENT_TO_BE_CLICKABLE', 
                tempo = 30
            )

        coletar_dados = webutils.coletar_atributo(
            seletor="//span[text()='Fazer login']", 
            atributo="innerHTML", 
            tipo_elemento="xpath"
        )

        if coletar_dados == "Fazer login":
            return True
        else:
            return False
    except:
        return False
    
def limpar_campo_box(autocomplete=""):
    try:
        webutils.esperar_pagina_carregar()
        webutils.aguardar_elemento(
            dentificador=f"//input[@autocomplete='{autocomplete}']", 
            tipo_elemento = 'xpath', 
            comportamento_esperado = 'ELEMENT_TO_BE_CLICKABLE', 
            tempo = 30
        )

        webutils.escrever_em_elemento(
            seletor=f"//input[@autocomplete='{autocomplete}']", 
            texto="", 
            tipo_elemento="xpath"
        )
        webutils.esperar_pagina_carregar()
        return True
    except:
        return False
    
def fazer_login(login="", senha=""):
    try:
        
        if validar_login() is True:
            webutils.esperar_pagina_carregar()
            
            webutils.aguardar_elemento(
                identificador="//span[text()='Fazer login']", 
                tipo_elemento = 'xpath', 
                comportamento_esperado = 'ELEMENT_TO_BE_CLICKABLE', 
                tempo = 30
            )
            
            webutils.clicar_elemento(
                seletor="//a[@aria-label='Fazer login'][1]", 
                tipo_elemento="xpath"
            )

            webutils.esperar_pagina_carregar()

            limpar_campo_box(autocomplete="username")
            
            webutils.escrever_em_elemento(
                seletor="//input[@autocomplete='username']", 
                texto=login, 
                tipo_elemento="xpath"
            )

            webutils.clicar_elemento(
                seletor="//span[text()='Avançar']", 
                tipo_elemento="xpath"
            )

            webutils.esperar_pagina_carregar()
            webutils.aguardar_elemento(
                identificador="//input[@autocomplete='current-password']", 
                tipo_elemento = 'xpath', 
                comportamento_esperado = 'ELEMENT_TO_BE_CLICKABLE', 
                tempo = 30
            )
            limpar_campo_box(autocomplete="current-password")
            
            webutils.esperar_pagina_carregar()
            webutils.clicar_elemento(
                seletor="//input[@autocomplete='current-password']", 
                tipo_elemento="xpath"
            )
            webutils.escrever_em_elemento(
                seletor="//input[@autocomplete='current-password']", 
                texto=senha, 
                tipo_elemento="xpath"
            )

            webutils.clicar_elemento(
                seletor="//span[text()='Avançar']", 
                tipo_elemento="xpath"
            )

            webutils.esperar_pagina_carregar()
            
            return True
        else:
            return False
    except:
        return False
    
def acessar_e_clicar_aba_youtube(link="", aba=""):

    try:

        webutils.abrir_pagina(url=link)
        
        webutils.esperar_pagina_carregar()

        webutils.aguardar_elemento(
            identificador=f"//div[text()='{aba}']//ancestor::tp-yt-paper-tab", 
            tipo_elemento = 'xpath', 
            comportamento_esperado = 'ELEMENT_TO_BE_CLICKABLE', 
            tempo = 10
        )

        webutils.clicar_elemento(    
            seletor=f"//div[text()='{aba}']//ancestor::tp-yt-paper-tab",      
            tipo_elemento="xpath"
        )

        webutils.esperar_pagina_carregar()

        return True
    
    except Exception as erro:

        return False

