"""
Browser Manager - Gerenciamento Stealth do Browser
==================================================

Gerenciador avançado de browser com recursos de stealth e anti-detecção.
"""

import asyncio
import os
import json
import random
from typing import Optional, Dict, Any, List
from pathlib import Path

try:
    import nodriver as uc
except ImportError:
    print("⚠️  nodriver não encontrado. Execute: pip install nodriver")
    uc = None

from ..security.fingerprint_spoofing import AdvancedStealthEngine, ContextRotator


class BrowserManager:
    """Gerenciador avançado de browser stealth"""
    
    def __init__(self, profile_name: str = "default"):
        self.profile_name = profile_name
        self.browser = None
        self.page = None
        self.stealth_engine = AdvancedStealthEngine()
        self.context_rotator = ContextRotator()
        self.profile_dir = self._get_profile_directory()
        
    def _get_profile_directory(self) -> str:
        """Retorna diretório do profile"""
        profiles_dir = Path("browser_profiles")
        profiles_dir.mkdir(exist_ok=True)
        return str(profiles_dir / self.profile_name)
    
    async def launch_stealth_browser(self, headless: bool = False, 
                                   context_rotation: bool = True) -> tuple:
        """Lança browser com máxima furtividade"""
        
        try:
            if uc is None:
                raise ImportError("nodriver não está disponível")
            
            # Seleciona contexto (rotação ou aleatório)
            if context_rotation:
                context = self.context_rotator.get_next_context()
                profile_dir = os.path.join(self.profile_dir, context['profile_dir'])
            else:
                profile_dir = self.profile_dir
            
            # Configurações stealth do browser
            stealth_args = self.stealth_engine.get_stealth_browser_args()
            fingerprint = await self.stealth_engine.setup_realistic_browser()
            
            # Argumentos customizados para máxima furtividade
            custom_args = [
                f'--user-agent={fingerprint["user_agent"]}',
                f'--window-size={fingerprint["viewport"]["width"]},{fingerprint["viewport"]["height"]}',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                '--disable-extensions',
                '--disable-plugins',
                '--disable-images',  # Melhora performance
                '--disable-javascript-harmony-shipping',
                '--disable-client-side-phishing-detection',
                '--disable-sync',
                '--disable-background-networking',
                '--metrics-recording-only',
                '--disable-default-apps',
                '--mute-audio',
            ]
            
            all_args = stealth_args + custom_args
            
            print(f"🚀 Lançando browser stealth (Profile: {profile_dir})")
            
            # Lança browser
            self.browser = await uc.start(
                headless=headless,
                user_data_dir=profile_dir,
                args=all_args
            )
            
            # Obtém página principal
            self.page = await self.browser.get('about:blank')
            
            # Aplica scripts de stealth
            await self.stealth_engine.inject_stealth_scripts(self.page)
            
            # Configura fingerprint do browser
            await self._setup_browser_fingerprint(fingerprint)
            
            print("✅ Browser stealth configurado com sucesso")
            return self.browser, self.page
            
        except Exception as e:
            print(f"❌ Erro ao lançar browser: {e}")
            raise
    
    async def _setup_browser_fingerprint(self, fingerprint: Dict[str, Any]):
        """Configura fingerprint completo do browser"""
        
        # Define timezone
        await self.page.emulate_timezone(fingerprint['timezone'])
        
        # Define localização
        if 'geolocation' in fingerprint:
            await self.page.emulate_geolocation(
                latitude=fingerprint['geolocation']['latitude'],
                longitude=fingerprint['geolocation']['longitude'],
                accuracy=fingerprint['geolocation']['accuracy']
            )
        
        # Injeta scripts adicionais de fingerprint
        await self.page.evaluate(f"""
            // Override screen properties
            Object.defineProperty(screen, 'width', {{
                get: () => {fingerprint['viewport']['width']}
            }});
            Object.defineProperty(screen, 'height', {{
                get: () => {fingerprint['viewport']['height']}
            }});
            Object.defineProperty(screen, 'availWidth', {{
                get: () => {fingerprint['viewport']['width']}
            }});
            Object.defineProperty(screen, 'availHeight', {{
                get: () => {fingerprint['viewport']['height'] - 40}
            }});
            
            // Override language
            Object.defineProperty(navigator, 'language', {{
                get: () => '{fingerprint['language'].split(',')[0]}'
            }});
            
            // Override platform
            Object.defineProperty(navigator, 'platform', {{
                get: () => '{fingerprint['platform']}'
            }});
            
            // Mock battery API
            Object.defineProperty(navigator, 'getBattery', {{
                get: () => () => Promise.resolve({{
                    charging: true,
                    chargingTime: 0,
                    dischargingTime: Infinity,
                    level: {random.uniform(0.8, 1.0)}
                }})
            }});
        """)
    
    async def navigate_safely(self, url: str, wait_for: str = "domcontentloaded",
                            timeout: int = 30000) -> bool:
        """Navega para URL com verificações de segurança"""
        try:
            print(f"🌐 Navegando para: {url}")
            
            # Adiciona delay humano antes da navegação
            await asyncio.sleep(random.uniform(1.0, 3.0))
            
            # Navega para a URL
            await self.page.goto(url, wait_until=wait_for, timeout=timeout)
            
            # Verifica se a página carregou corretamente
            await self._verify_page_load()
            
            # Pequena pausa após carregamento
            await asyncio.sleep(random.uniform(2.0, 4.0))
            
            print("✅ Navegação concluída com sucesso")
            return True
            
        except Exception as e:
            print(f"❌ Erro na navegação: {e}")
            return False
    
    async def _verify_page_load(self):
        """Verifica se a página carregou adequadamente"""
        try:
            # Aguarda o documento estar pronto
            await self.page.wait_for_function("document.readyState === 'complete'", timeout=10000)
            
            # Verifica se não há erros visíveis
            error_indicators = [
                'text="This page isn\'t working"',
                'text="Something went wrong"',
                'text="Access denied"',
                'class*="error"',
                'id*="error"'
            ]
            
            for indicator in error_indicators:
                try:
                    error_element = await self.page.find(indicator, timeout=1000)
                    if error_element:
                        print(f"⚠️  Possível erro detectado na página: {indicator}")
                        break
                except:
                    continue  # Sem erro encontrado, continua
                    
        except Exception as e:
            print(f"⚠️  Não foi possível verificar carregamento da página: {e}")
    
    async def take_screenshot(self, filename: str = None, full_page: bool = False) -> str:
        """Captura screenshot com nome automático"""
        try:
            if not filename:
                timestamp = int(asyncio.get_event_loop().time())
                filename = f"screenshot_{timestamp}.png"
            
            screenshots_dir = Path("temp_screenshots")
            screenshots_dir.mkdir(exist_ok=True)
            
            screenshot_path = screenshots_dir / filename
            
            await self.page.screenshot(
                path=str(screenshot_path),
                full_page=full_page
            )
            
            print(f"📸 Screenshot salvo: {screenshot_path}")
            return str(screenshot_path)
            
        except Exception as e:
            print(f"❌ Erro ao capturar screenshot: {e}")
            return ""
    
    async def get_page_info(self) -> Dict[str, Any]:
        """Obtém informações da página atual"""
        try:
            info = {
                'url': self.page.url,
                'title': await self.page.title(),
                'ready_state': await self.page.evaluate('document.readyState'),
                'viewport': await self.page.evaluate('({width: window.innerWidth, height: window.innerHeight})'),
                'user_agent': await self.page.evaluate('navigator.userAgent'),
                'cookies_count': len(await self.page.cookies()),
                'timestamp': asyncio.get_event_loop().time()
            }
            return info
        except Exception as e:
            print(f"❌ Erro ao obter informações da página: {e}")
            return {}
    
    async def clear_browser_data(self, clear_cookies: bool = True, 
                               clear_cache: bool = True,
                               clear_local_storage: bool = True):
        """Limpa dados do browser"""
        try:
            if clear_local_storage:
                await self.page.evaluate("""
                    localStorage.clear();
                    sessionStorage.clear();
                """)
            
            if clear_cookies:
                cookies = await self.page.cookies()
                for cookie in cookies:
                    await self.page.delete_cookie(cookie['name'])
            
            print("🧹 Dados do browser limpos")
            
        except Exception as e:
            print(f"❌ Erro ao limpar dados: {e}")
    
    async def close_browser(self, save_session: bool = True):
        """Fecha browser com opção de salvar sessão"""
        try:
            if save_session and self.page:
                # Salva cookies da sessão
                cookies = await self.page.cookies()
                session_file = Path(self.profile_dir) / "last_session.json"
                
                session_data = {
                    'cookies': cookies,
                    'url': self.page.url,
                    'timestamp': asyncio.get_event_loop().time()
                }
                
                with open(session_file, 'w') as f:
                    json.dump(session_data, f, indent=2)
                
                print("💾 Sessão salva")
            
            if self.browser:
                await self.browser.close()
                print("🔒 Browser fechado")
                
        except Exception as e:
            print(f"❌ Erro ao fechar browser: {e}")
    
    async def restore_session(self) -> bool:
        """Restaura sessão anterior"""
        try:
            session_file = Path(self.profile_dir) / "last_session.json"
            
            if not session_file.exists():
                print("📝 Nenhuma sessão anterior encontrada")
                return False
            
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            # Verifica se a sessão não é muito antiga (24 horas)
            current_time = asyncio.get_event_loop().time()
            session_age = current_time - session_data.get('timestamp', 0)
            
            if session_age > 86400:  # 24 horas
                print("⏰ Sessão muito antiga, iniciando nova sessão")
                return False
            
            # Restaura cookies
            if 'cookies' in session_data:
                await self.page.add_cookies(session_data['cookies'])
            
            # Navega para última URL (opcional)
            if 'url' in session_data and session_data['url'] != 'about:blank':
                await self.navigate_safely(session_data['url'])
            
            print("🔄 Sessão restaurada com sucesso")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao restaurar sessão: {e}")
            return False
    
    def __enter__(self):
        """Context manager support"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager cleanup"""
        if self.browser:
            asyncio.create_task(self.close_browser())


# Factory function para criar browser manager
def create_browser_manager(profile: str = "default") -> BrowserManager:
    """Factory para criar BrowserManager"""
    return BrowserManager(profile_name=profile)
