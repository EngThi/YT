import os, asyncio, random, time
from dotenv import load_dotenv
import nodriver as uc

# Carrega credenciais (opcionais)
load_dotenv()
EMAIL = os.getenv("YOUTUBE_EMAIL")
PASSWORD = os.getenv("YOUTUBE_PASSWORD")

# Configuração de screenshots temporários
SCREENSHOT_DIR = "temp_screenshots"
SCREENSHOT_LIFETIME = 300  # 5 minutos em segundos

def ensure_screenshot_dir():
    """Cria diretório de screenshots se não existir"""
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)

def cleanup_old_screenshots():
    """Remove screenshots antigos para não ocupar armazenamento"""
    if not os.path.exists(SCREENSHOT_DIR):
        return
    
    current_time = time.time()
    for filename in os.listdir(SCREENSHOT_DIR):
        filepath = os.path.join(SCREENSHOT_DIR, filename)
        if os.path.isfile(filepath):
            file_age = current_time - os.path.getctime(filepath)
            if file_age > SCREENSHOT_LIFETIME:
                try:
                    os.remove(filepath)
                    print(f"🗑️ Screenshot antigo removido: {filename}")
                except Exception as e:
                    print(f"⚠️ Erro ao remover {filename}: {e}")

async def take_screenshot(page, step_name):
    """Tira screenshot temporário de um passo específico"""
    try:
        ensure_screenshot_dir()
        timestamp = int(time.time())
        filename = f"{step_name}_{timestamp}.png"
        filepath = os.path.join(SCREENSHOT_DIR, filename)
        
        await page.save_screenshot(filepath)
        print(f"📸 Screenshot salvo: {filename} (será removido em 5 min)")
        
        # Limpa screenshots antigos
        cleanup_old_screenshots()
        
    except Exception as e:
        print(f"⚠️ Erro ao tirar screenshot: {e}")

async def human_typing(page, element, text):
    """Simula digitação humana com delays aleatórios"""
    await element.click()
    await asyncio.sleep(random.uniform(0.5, 1.0))
    
    # Limpa o campo primeiro
    await element.clear()
    await asyncio.sleep(random.uniform(0.3, 0.8))
    
    # Digita caractere por caractere
    for char in text:
        await element.send_keys(char)
        await asyncio.sleep(random.uniform(0.05, 0.15))
    
    await asyncio.sleep(random.uniform(0.5, 1.5))

async def wait_and_click(page, selector, timeout=10):
    """Aguarda elemento aparecer e clica nele"""
    try:
        element = await page.wait_for(selector, timeout=timeout)
        if element:
            await asyncio.sleep(random.uniform(0.5, 1.5))
            await element.click()
            return True
    except Exception as e:
        print(f"⚠️ Elemento {selector} não encontrado: {e}")
    return False
    """Simula movimentos e ações humanas"""
    await asyncio.sleep(random.uniform(1, 3))
    # Simula scroll aleatório
    for _ in range(random.randint(2, 4)):
        scroll_y = random.randint(100, 400)
        await page.evaluate(f"window.scrollBy(0, {scroll_y})")
        await asyncio.sleep(random.uniform(0.5, 1.0))

async def main():
    """Função principal de automação stealth"""
    print("🤖 Iniciando automação stealth do YouTube...")
    
    browser = None
    try:
        # Limpa screenshots antigos no início
        cleanup_old_screenshots()
        
        # Inicia browser stealth com configurações para container
        print("🔧 Configurando browser stealth...")
        browser = await uc.start(
            headless=True,
            no_sandbox=True,
            user_data_dir="profile_data",
            browser_executable_path="/usr/bin/chromium-browser",
            browser_args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--remote-debugging-port=0",
                "--disable-background-timer-throttling",
                "--disable-backgrounding-occluded-windows",
                "--disable-renderer-backgrounding"
            ]
        )
        print("✅ Browser iniciado com sucesso!")

        # PONTO ESSENCIAL 1: Acesso inicial ao YouTube
        print("🎥 PASSO 1: Acessando YouTube diretamente...")
        page1 = await browser.get("https://www.youtube.com/")
        await asyncio.sleep(3)  # Aguarda carregamento
        
        title = await page1.evaluate("document.title")
        print(f"📄 Página carregada: {title}")
        
        # Screenshot do acesso inicial
        await take_screenshot(page1, "01_youtube_inicial")
        
        # PONTO ESSENCIAL 2: Processo de Login
        print("🔐 PASSO 2: Iniciando processo de login...")
        
        if not EMAIL or not PASSWORD:
            print("❌ ERRO: Credenciais não encontradas!")
            print("📝 Configure suas credenciais no arquivo .env:")
            print("   YOUTUBE_EMAIL=seu.email@gmail.com")
            print("   YOUTUBE_PASSWORD=suaSenhaSegura")
            await take_screenshot(page1, "02_erro_credenciais")
            return
        
        print(f"👤 Fazendo login com: {EMAIL}")
        
        # Procura pelo botão Sign In
        print("🔍 Procurando botão 'Sign in'...")
        sign_in_clicked = False
        
        # Tenta vários seletores para o botão Sign in
        sign_in_selectors = [
            "a[aria-label*='Sign in']",
            "a[href*='accounts.google.com']",
            "button[aria-label*='Sign in']",
            "tp-yt-paper-button[aria-label*='Sign in']",
            "#sign-in-button",
            "a[href*='ServiceLogin']"
        ]
        
        for selector in sign_in_selectors:
            try:
                sign_in_button = await page1.select(selector)
                if sign_in_button:
                    print(f"✅ Botão Sign in encontrado: {selector}")
                    await take_screenshot(page1, "02a_botao_sign_in_encontrado")
                    
                    await sign_in_button.click()
                    await asyncio.sleep(3)  # Aguarda redirecionamento
                    sign_in_clicked = True
                    break
            except Exception as e:
                continue
        
        if not sign_in_clicked:
            print("⚠️ Botão Sign in não encontrado, tentando acesso direto ao Google...")
            await page1.get("https://accounts.google.com/ServiceLogin?service=youtube")
            await asyncio.sleep(3)
        
        await take_screenshot(page1, "02b_pagina_login_google")
        
        # Verifica se estamos na página de login do Google
        current_url = await page1.evaluate("window.location.href")
        print(f"🌐 URL atual: {current_url}")
        
        if "accounts.google.com" in current_url:
            print("📧 Inserindo email...")
            
            # Aguarda a página carregar completamente
            await asyncio.sleep(3)
            
            # Aguarda e preenche o campo de email
            email_selectors = [
                "input[type='email']",
                "input#identifierId", 
                "input[name='identifier']",
                "#identifierId",
                "input[aria-label*='email']"
            ]
            
            email_filled = False
            for selector in email_selectors:
                try:
                    print(f"🔍 Tentando seletor: {selector}")
                    # Aguarda o elemento aparecer
                    email_input = await page1.wait_for(selector, timeout=5)
                    if email_input:
                        print(f"✅ Campo de email encontrado: {selector}")
                        await human_typing(page1, email_input, EMAIL)
                        email_filled = True
                        break
                except Exception as e:
                    print(f"⚠️ Seletor {selector} falhou: {e}")
                    continue
            
            if not email_filled:
                print("❌ Campo de email não encontrado! Tentando aguardar mais...")
                await asyncio.sleep(5)
                await take_screenshot(page1, "02c_debug_pagina_completa")
                
                # Tenta novamente com wait mais longo
                try:
                    email_input = await page1.wait_for("input", timeout=10)
                    if email_input:
                        print("✅ Campo genérico encontrado, tentando usar...")
                        await human_typing(page1, email_input, EMAIL)
                        email_filled = True
                except Exception as e:
                    print(f"❌ Falha definitiva no campo de email: {e}")
                    await take_screenshot(page1, "02c_erro_campo_email")
                    return
            
            await take_screenshot(page1, "02d_email_preenchido")
            
            # Clica em "Next" / "Avançar"
            print("➡️ Clicando em 'Next'...")
            next_clicked = await wait_and_click(page1, "#identifierNext")
            if not next_clicked:
                # Tenta outros seletores
                next_selectors = ["button[jsname='LgbsSe']", "input[type='submit']", "#next"]
                for selector in next_selectors:
                    if await wait_and_click(page1, selector):
                        break
            
            await asyncio.sleep(3)  # Aguarda carregar página de senha
            await take_screenshot(page1, "02e_pagina_senha")
            
            # Preenche senha
            print("🔑 Inserindo senha...")
            password_selectors = [
                "input[type='password']",
                "input[name='password']",
                "#password input"
            ]
            
            password_filled = False
            for selector in password_selectors:
                try:
                    password_input = await page1.select(selector)
                    if password_input:
                        print(f"✅ Campo de senha encontrado: {selector}")
                        await human_typing(page1, password_input, PASSWORD)
                        password_filled = True
                        break
                except Exception as e:
                    continue
            
            if not password_filled:
                print("❌ Campo de senha não encontrado!")
                await take_screenshot(page1, "02f_erro_campo_senha")
                return
            
            await take_screenshot(page1, "02g_senha_preenchida")
            
            # Clica em "Next" / "Entrar"
            print("🔐 Finalizando login...")
            login_clicked = await wait_and_click(page1, "#passwordNext")
            if not login_clicked:
                # Tenta outros seletores
                login_selectors = ["button[jsname='LgbsSe']", "input[type='submit']", "#submit"]
                for selector in login_selectors:
                    if await wait_and_click(page1, selector):
                        break
            
            # Aguarda redirecionamento para YouTube
            print("⏳ Aguardando redirecionamento para YouTube...")
            await asyncio.sleep(5)
            
            # Verifica se o login foi bem-sucedido
            final_url = await page1.evaluate("window.location.href")
            if "youtube.com" in final_url:
                print("✅ Login realizado com sucesso!")
                await take_screenshot(page1, "02h_login_sucesso")
            else:
                print(f"⚠️ Possível problema no login. URL atual: {final_url}")
                await take_screenshot(page1, "02i_login_problema")
        
        else:
            print("❌ Não foi possível acessar a página de login do Google")
            await take_screenshot(page1, "02j_erro_acesso_google")

        # PONTO ESSENCIAL 3: Navegação e interação
        print("🧭 PASSO 3: Iniciando navegação humana...")
        await human_navigation(page1)
        
        # Screenshot após navegação
        await take_screenshot(page1, "03_apos_navegacao")
        
        # Verifica URL atual
        url = await page1.evaluate("window.location.href")
        print(f"🌐 URL atual: {url}")

        # PONTO ESSENCIAL 4: Abertura de segunda aba
        print("🔗 PASSO 4: Abrindo nova aba para diversificar navegação...")
        page2 = await browser.get("https://www.youtube.com/trending", new_tab=True)
        await asyncio.sleep(2)
        
        title2 = await page2.evaluate("document.title")
        print(f"📄 Segunda aba carregada: {title2}")
        
        # Screenshot da segunda aba
        await take_screenshot(page2, "04_segunda_aba_trending")
        
        # PONTO ESSENCIAL 5: Navegação na segunda aba
        print("🎯 PASSO 5: Navegação na página de trending...")
        await human_navigation(page2)
        
        # Screenshot final
        await take_screenshot(page2, "05_navegacao_final")

        # PONTO ESSENCIAL 6: Finalização
        print("✅ PASSO 6: Automação executada com sucesso!")
        print("📊 Resumo da sessão:")
        print(f"   - Aba 1: {title}")
        print(f"   - Aba 2: {title2}")
        print(f"   - Screenshots salvos em: {SCREENSHOT_DIR}")
        print("⏳ Aguardando 3 segundos antes de finalizar...")
        await asyncio.sleep(3)
        
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")
        # Screenshot do erro se possível
        try:
            if 'page1' in locals():
                await take_screenshot(page1, "erro_execucao")
        except:
            pass
    
    finally:
        print("🔚 Finalizando automação...")
        if browser:
            try:
                browser.stop()
            except:
                pass

async def cleanup_task():
    """Tarefa assíncrona para limpeza periódica de screenshots"""
    while True:
        await asyncio.sleep(60)  # Verifica a cada minuto
        cleanup_old_screenshots()

if __name__ == "__main__":
    # Executa automação principal
    asyncio.run(main())
    
    # Limpa screenshots após execução
    print("🧹 Limpeza final de screenshots...")
    cleanup_old_screenshots()
