import os, asyncio, random
from dotenv import load_dotenv
import nodriver as uc

# Carrega credenciais (opcionais - para login automático)
load_dotenv()
EMAIL = os.getenv("YOUTUBE_EMAIL")
PASSWORD = os.getenv("YOUTUBE_PASSWORD")

async def human_typing(page, selector, text):
    """Simula digitação humana com delays aleatórios"""
    for char in text:
        await page.type(selector, char, delay=random.randint(50, 150))
    await asyncio.sleep(random.uniform(0.5, 1.5))

async def human_navigation(page):
    """Simula movimentos de mouse aleatórios"""
    for _ in range(random.randint(3, 7)):
        await page.mouse.move(random.randint(0, 800), random.randint(0, 600))
        await asyncio.sleep(random.uniform(0.2, 0.5))

async def main():
    """Função principal de automação stealth"""
    print("🤖 Iniciando automação stealth do YouTube...")
    
    # Inicia browser stealth com configurações para container
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

    try:
        # Aba 1: Acesso direto ao YouTube
        print("🎥 Acessando YouTube diretamente...")
        page1 = await browser.new_page()
        await page1.goto("https://www.youtube.com/")
        await human_navigation(page1)
        
        title = await page1.title()
        print(f"📄 Página carregada: {title}")
        
        # Opcional: fazer login se necessário
        try:
            # Verifica se há botão de login
            sign_in_button = await page1.query_selector('a[aria-label*="Fazer login"], a[href*="accounts.google.com"]')
            if sign_in_button and EMAIL and PASSWORD:
                print("🔐 Botão de login encontrado, realizando login...")
                await sign_in_button.click()
                await page1.wait_for_navigation()
                
                # Processo de login
                await human_typing(page1, 'input[type="email"]', EMAIL)
                await page1.click("#identifierNext")
                await page1.wait_for_selector('input[type="password"]', timeout=15000)
                await human_typing(page1, 'input[type="password"]', PASSWORD)
                await page1.click("#passwordNext")
                await page1.wait_for_navigation()
                print("✅ Login realizado com sucesso!")
            else:
                print("ℹ️ Navegando sem login ou credenciais não configuradas")
        except Exception as login_error:
            print(f"⚠️ Login opcional falhou (continuando sem login): {login_error}")
        
        await human_navigation(page1)

        # Aba 2: Outras ações no YouTube
        print("🔍 Abrindo nova aba para navegação...")
        page2 = await browser.new_page()
        await page2.goto("https://www.youtube.com/")
        await human_navigation(page2)
        title = await page2.title()
        print(f"📄 Título da página 2: {title}")

        # Exemplo: Pesquisa e interação
        print("🔍 Realizando pesquisa de teste...")
        await page2.click("input#search")
        await human_typing(page2, "input#search", "automation tutorial")
        await page2.keyboard.press("Enter")
        await page2.wait_for_selector("ytd-video-renderer", timeout=10000)
        await human_navigation(page2)
        print("✅ Pesquisa realizada com sucesso!")

        # Aguarda antes de finalizar
        print("⏳ Aguardando 10 segundos antes de finalizar...")
        await asyncio.sleep(10)
        
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")
    
    finally:
        print("🔚 Finalizando automação...")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
