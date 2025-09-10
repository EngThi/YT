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

async def human_navigation(page):
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
        
        # PONTO ESSENCIAL 2: Verificação de login (se necessário)
        print("🔐 PASSO 2: Verificando status de login...")
        try:
            # Verifica se há botão de login na página
            login_button = await page1.select("a[aria-label*='Sign in']")
            if login_button:
                print("👤 Status: Usuário não logado")
                await take_screenshot(page1, "02_nao_logado")
                
                # Se credenciais estão disponíveis, pode tentar login
                if EMAIL and PASSWORD:
                    print("🔑 Credenciais encontradas, mas mantendo navegação sem login")
                else:
                    print("ℹ️ Navegação sem login (modo anônimo)")
            else:
                print("✅ Status: Possivelmente logado ou página diferente")
                await take_screenshot(page1, "02_status_login")
                
        except Exception as e:
            print(f"⚠️ Erro ao verificar login: {e}")
            await take_screenshot(page1, "02_erro_login")

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
