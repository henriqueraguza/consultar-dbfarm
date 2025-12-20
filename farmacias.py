# coloque isso no TOPO do arquivo, antes de importar playwright
import sys
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

def ultrafarma(remedio):
    from playwright.sync_api import sync_playwright
    import pandas as pd
    remedio = remedio

    with sync_playwright() as pw:
        navegador = pw.chromium.launch(headless=True)

        pagina = navegador.new_page()
        #Entrando na página
        pagina.goto("https://www.ultrafarma.com.br/")
        campo_pesquisa = pagina.get_by_role("textbox", name="Digite o nome, a marca ou o")
        campo_pesquisa.click()
        campo_pesquisa.fill(remedio)
        campo_pesquisa.press('Enter')
        pagina.wait_for_load_state('networkidle')
        #Pegando produtos
        produtos = pagina.locator('div.product-item')

        nomes = []
        preços = []

        for i in range(produtos.count()):
            produto = produtos.nth(i)
            
            nome = produto.get_attribute('data-product-name')
            if nome:
                nomes.append(nome)
            preço = produto.get_attribute('data-product-price')
            if preço:
                preços.append(float(preço))
        
        #print(nomes)
        #print(preços)

    df = pd.DataFrame({'Produtos':nomes,'Preços':(preços)})

    menorpreço = df['Preços'].min()
    melhorcompra = df['Produtos'][df['Preços'].argmin()]
    #print(f'Melhor compra: {menorpreço} {melhorcompra}')
    return [menorpreço,melhorcompra]

def dsp(remedio):
    from playwright.sync_api import sync_playwright
    import pandas as pd
    remedio = remedio

    with sync_playwright() as pw:
        navegador = pw.chromium.launch(headless=True)

        pagina = navegador.new_page()
        #Entrando na página
        pagina.goto("https://www.drogariasaopaulo.com.br/")
        #pagina.wait_for_load_state("networkidle")
        campo_pesquisa = pagina.get_by_role("textbox", name="O que você precisa?")
        campo_pesquisa.click()
        campo_pesquisa.fill(remedio)
        campo_pesquisa.press('Enter')
        pagina.wait_for_load_state('networkidle')
        produtos = pagina.locator('div.descricao-prateleira')
        #print(produtos.all_inner_texts())
        nomes = []
        preços = []
        for i in range(produtos.count()):
            produto = produtos.nth(i)
            nome = produto.locator('a.collection-link').inner_text()
            if nome:
                nomes.append(nome)

            if produto.locator('a.valor-por:not([hidden])').count()>0 and produto.locator('a.valor-por:not([hidden])').is_visible():
                preço = produto.locator('a.valor-por:not([hidden])').first.inner_text()
                if preço:
                    preços.append(preço)
                else:
                    if produto.locator('span.valor-unidade').count()>0 and produto.locator('span.valor-unidade').is_visible():
                        preço2 = produto.locator('span.valor-unidade').inner_text()
                        if preço2:
                            preços.append(preço2)
                        else:
                            continue
        try:
            preços_num = [float(p.replace('R$','').replace(',','.')) for p in preços]
        except:
            preços_num = [float(p.replace('\n','').replace('.','').replace(',','.').replace('A partir deR$','').replace('*','')) for p in preços]

    if len(preços_num) < len(nomes):
        nomes = nomes[:len(preços_num)]
    df = pd.DataFrame({'Produtos':nomes,'Preços':preços_num})
    menorpreço = df['Preços'].min()
    melhorcompra = df['Produtos'][df['Preços'].argmin()]
    print(f'Melhor compra: {menorpreço} {melhorcompra}')
    return [menorpreço,melhorcompra]

def paguemenos(remedio):
    from playwright.sync_api import sync_playwright
    import pandas as pd
    remedio = remedio

    with sync_playwright() as pw:
        navegador = pw.chromium.launch(headless=True)

        pagina = navegador.new_page()
        #Entrando na página
        pagina.goto("https://www.paguemenos.com.br/")
        #pagina.wait_for_load_state("networkidle")
        campo_pesquisa = pagina.locator('input.paguemenos-store-theme-9-x-inputNovaBusca')
        campo_pesquisa.click()
        campo_pesquisa.fill(remedio)
        campo_pesquisa.press('Enter')
        pagina.wait_for_timeout(32000)
        produtos = pagina.locator('div.w-100.relative.paguemenos-store-theme-9-x-ProductCardCustomContainer')
        #print(produtos.count())

        nomes = []
        preços = []
        for i in range(produtos.count()):
            produto = produtos.nth(i)
            nome = produto.locator('h2.paguemenos-store-theme-9-x-productName')
            nomes.append(nome.text_content())

            normal = produto.locator('h2.paguemenos-store-theme-9-x-sellingPrice').first
            if normal.count()>0:
                print(normal.text_content())
                preços.append(normal.text_content())
            else:
                promo = produto.locator('div.paguemenos-store-theme-9-x-price').first
                if promo.count()>0:
                    promo.text_content()
                    preços.append(promo.text_content())
                else:
                    continue
        preços_num = [float(p.replace('R$','').replace('\xa0','').replace(',','.')) for p in preços]

    if len(preços_num) < len(nomes):
         nomes = nomes[:len(preços_num)]
    df = pd.DataFrame({'Produtos':nomes,'Preços':preços_num})
    menorpreço = df['Preços'].min()
    melhorcompra = df['Produtos'][df['Preços'].argmin()]
    print(f'Melhor compra: {menorpreço} {melhorcompra}')
    return [menorpreço,melhorcompra]

def drogasil(remedio):
    from playwright.sync_api import sync_playwright
    import pandas as pd
    remedio = remedio

    with sync_playwright() as pw:

        navegador = pw.chromium.launch(headless=True)

        pagina = navegador.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36')
        #Entrando na página
        pagina.goto("https://www.drogasil.com.br/")
        #pagina.wait_for_load_state('networkidle')
        pagina.wait_for_timeout(48000)
        campo_pesquisa = pagina.get_by_placeholder('Buscar na Drogasil')
        campo_pesquisa.click()
        campo_pesquisa.fill(remedio)
        campo_pesquisa.press('Enter')
        pagina.wait_for_load_state('networkidle') #se der problema, volta esse
        
        #pagina.locator('article[data-price-type]').first.wait_for(state="visible", timeout=30000)

        produtosnormal = pagina.locator('article[data-price-type="NORMAL"]')
        nomesnormal = []
        preçosnormal = []
        for i in range(produtosnormal.count()):
            produtonormal = produtosnormal.nth(i)
            nome = produtonormal.locator('a.sc-dc2ce483-2.fHfTUC')
            nomesnormal.append(nome.text_content())
            
            preço = produtonormal.locator('div.sc-a6051c85-1.ddnpbj')
            if preço.count()>0:
                preçosnormal.append(preço.text_content())
            else:
                continue
        preçosn = [float((p.replace('R$','').replace(',','.'))) for p in preçosnormal]

        produtosdepor = pagina.locator('article[data-price-type="DE_POR"]')
        #pagina.wait_for_timeout(32000)
        nomesdepor = []
        preçosdepor = []
        for i in range(produtosdepor.count()):
            produtodepor = produtosdepor.nth(i)
            nome = produtodepor.locator('a.sc-dc2ce483-2.fHfTUC')
            if nome.count()>0:
                nomesdepor.append(nome.text_content())
            else:
                nome = produtodepor.locator('a.sc-b98174b6-2.bZigEu')
                if nome.count()>0:
                    nomesdepor.append(nome.text_content())
                else:
                    continue
            
            preço = produtodepor.locator('div.sc-9555d9d4-3.sc-9555d9d4-5.dyjMud.btOduN')
            if preço.count()>0:
                preçosdepor.append(preço.text_content())
            else:
                continue
        preçosd = [float(p.replace('R$','').replace(',','.')) for p in preçosdepor]

        produtosprom = pagina.locator('article[data-price-type="LMPM"]')
        #print(produtosprom.count())

        nomesprom = []
        preçosprom = []
        for i in range(produtosprom.count()):
            produtoprom = produtosprom.nth(i)
            nome = produtoprom.locator('a.sc-dc2ce483-2.fHfTUC')
            if nome.count()>0:
                nomesprom.append(nome.text_content())
            else:
                nome = produtoprom.locator('a.sc-b98174b6-2.bZigEu')
                if nome.count()>0:
                    nomesprom.append(nome.text_content())
                else:
                    continue
            
            preço = produtoprom.locator('div.sc-24575961-0.iuEYem')
            if preço.count()>0:
                preçosprom.append(preço.text_content())
            else:
                continue
        
        preçosp = [float(p.replace('R$','').replace(',','.')) for p in preçosprom]

        produtospbm = pagina.locator('article[data-price-type="PBM"]')
        nomespbm = []
        preçospbm = []

        for i in range(produtospbm.count()):
            produtopbm = produtospbm.nth(i)
            nome = produtopbm.locator('a.sc-b98174b6-2.bZigEu')
            if nome.count()>0:
                nomespbm.append(nome.text_content())
            else:    
                 continue
            
            preço = produtopbm.locator('div.sc-9555d9d4-3.sc-9555d9d4-5.dyjMud.btOduN')
            if preço.count()>0:
                preçospbm.append(preço.text_content())
            else:
                continue
        preçospb = [float((p.replace('R$ ','').replace('.','').replace(',','.'))) for p in preçospbm]

        meds = pagina.locator('article[data-card="medication"]')
        nomesmed = []
        preçosmed = []

        for i in range(meds.count()):
            med = meds.nth(i)
            nome = med.locator('a.sc-b98174b6-2.jQIZrj')
            if nome.count()>0:
                nomesmed.append(nome.text_content())
            else:
                continue

            preço = med.locator('div.sc-9555d9d4-3.sc-9555d9d4-5.dyjMud.btOduN')
            if preço.count()>0:
                preçosmed.append(preço.text_content())
            else:
                continue
        preçosm = [float((p.replace('R$ ','').replace('.','').replace(',','.'))) for p in preçosmed]

        preçosgeral = []
        preçosgeral = preçosn + preçosd + preçosp + preçospb + preçosm
        produtos = nomesnormal + nomesdepor + nomesprom + nomespbm + nomesmed

        if len(preçosgeral) < len(produtos):
            produtos = produtos[:len(preçosgeral)]
        
    df = pd.DataFrame({'Produtos':produtos,'Preços':preçosgeral})
    menorpreço = df['Preços'].min()
    melhorcompra = df['Produtos'][df['Preços'].argmin()]
    print(f'Melhor compra: {menorpreço} {melhorcompra}')

    return [menorpreço,melhorcompra]

