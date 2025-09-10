import os, asyncio, random
from dotenv import load_dotenv
import nodriver as uc

# Carrega credenciais
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
    
    # Inicia browser stealth
    browser = await uc.start(
        headless=False,
        user_data_dir="profile_data",
        stealth_arguments={
            "languages": ["pt-BR", "pt"],
            "vendor": "Google Inc.",
            "platform": "Win32",
            "webgl_vendor": "Intel Inc.",
            "renderer": "Intel Iris OpenGL Engine"
        }
    )

    try:
        # Aba 1: Login YouTube
        print("📧 Realizando login no YouTube...")
        page1 = await browser.new_page()
        await page1.goto("https://accounts.google.com/ServiceLogin")
        
        # Verifica se as credenciais foram carregadas
        if not EMAIL or not PASSWORD:
            print("❌ Credenciais não encontradas no arquivo .env")
            print("📝 Crie um arquivo .env com:")
            print("YOUTUBE_EMAIL=seu.email@gmail.com")
            print("YOUTUBE_PASSWORD=suaSenhaSegura")
            return
        
        await human_typing(page1, 'input[type="email"]', EMAIL)
        await page1.click("#identifierNext")
        await page1.wait_for_selector('input[type="password"]', timeout=15000)
        await human_typing(page1, 'input[type="password"]', PASSWORD)
        await page1.click("#passwordNext")
        await page1.wait_for_url("https://www.youtube.com/", timeout=20000)
        await human_navigation(page1)
        print("✅ Login realizado com sucesso!")

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
