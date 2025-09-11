"""
Login Handler - Estratégias Inteligentes de Login
=================================================

Sistema avançado de login com múltiplas estratégias e detecção inteligente.
"""

import asyncio
import random
from typing import Optional, Dict, Any, List
from enum import Enum

from ..automation.human_simulator import HumanBehaviorSimulator
from ..security.credential_manager import CredentialManager


class LoginStrategy(Enum):
    """Estratégias de login disponíveis"""
    SESSION_RESTORE = "session_restore"
    AUTOMATIC_LOGIN = "automatic_login"
    MANUAL_ASSISTED = "manual_assisted"
    HYBRID_APPROACH = "hybrid_approach"


class LoginResult(Enum):
    """Resultados possíveis do login"""
    SUCCESS = "success"
    FAILED = "failed"
    REQUIRES_2FA = "requires_2fa"
    ACCOUNT_LOCKED = "account_locked"
    CAPTCHA_REQUIRED = "captcha_required"
    MANUAL_INTERVENTION = "manual_intervention"


class YouTubeLoginHandler:
    """Handler inteligente para login no YouTube"""
    
    def __init__(self, browser_manager, credential_manager: CredentialManager = None):
        self.browser_manager = browser_manager
        self.credential_manager = credential_manager or CredentialManager()
        self.human_simulator = HumanBehaviorSimulator()
        self.max_retry_attempts = 3
        
    async def login(self, strategy: LoginStrategy = LoginStrategy.HYBRID_APPROACH) -> LoginResult:
        """Executa login com estratégia especificada"""
        
        print(f"🔐 Iniciando login com estratégia: {strategy.value}")
        
        try:
            if strategy == LoginStrategy.SESSION_RESTORE:
                return await self._try_session_restore()
            
            elif strategy == LoginStrategy.AUTOMATIC_LOGIN:
                return await self._automatic_login()
            
            elif strategy == LoginStrategy.MANUAL_ASSISTED:
                return await self._manual_assisted_login()
            
            elif strategy == LoginStrategy.HYBRID_APPROACH:
                return await self._hybrid_login_approach()
            
            else:
                print("❌ Estratégia de login não reconhecida")
                return LoginResult.FAILED
                
        except Exception as e:
            print(f"❌ Erro durante login: {e}")
            return LoginResult.FAILED
    
    async def _hybrid_login_approach(self) -> LoginResult:
        """Abordagem híbrida - tenta múltiplas estratégias"""
        
        strategies = [
            (LoginStrategy.SESSION_RESTORE, "Verificando sessão existente"),
            (LoginStrategy.AUTOMATIC_LOGIN, "Tentando login automático"),
            (LoginStrategy.MANUAL_ASSISTED, "Solicitando assistência manual")
        ]
        
        for strategy, description in strategies:
            print(f"🔄 {description}...")
            
            if strategy == LoginStrategy.SESSION_RESTORE:
                result = await self._try_session_restore()
            elif strategy == LoginStrategy.AUTOMATIC_LOGIN:
                result = await self._automatic_login()
            else:
                result = await self._manual_assisted_login()
            
            if result == LoginResult.SUCCESS:
                return result
            
            # Pausa entre tentativas
            await asyncio.sleep(random.uniform(2.0, 4.0))
        
        return LoginResult.FAILED
    
    async def _try_session_restore(self) -> LoginResult:
        """Tenta restaurar sessão existente"""
        
        # Navega para YouTube
        await self.browser_manager.navigate_safely('https://www.youtube.com')
        
        # Verifica se já está logado
        if await self._is_logged_in():
            print("✅ Já logado - usando sessão existente")
            return LoginResult.SUCCESS
        
        # Tenta restaurar sessão salva
        if await self.browser_manager.restore_session():
            await asyncio.sleep(random.uniform(2.0, 4.0))
            
            if await self._is_logged_in():
                print("✅ Sessão restaurada com sucesso")
                return LoginResult.SUCCESS
        
        print("📝 Sessão não disponível")
        return LoginResult.FAILED
    
    async def _automatic_login(self) -> LoginResult:
        """Tentativa de login automático"""
        
        # Obtém credenciais
        credentials = self.credential_manager.get_credentials()
        if not credentials:
            print("❌ Credenciais não disponíveis para login automático")
            return LoginResult.MANUAL_INTERVENTION
        
        print("🤖 Iniciando login automático...")
        
        try:
            # Navega para página de login
            await self.browser_manager.navigate_safely('https://accounts.google.com/signin')
            
            # Aguarda página de login carregar
            await asyncio.sleep(random.uniform(2.0, 4.0))
            
            # Preenche email
            result = await self._fill_email_field(credentials['email'])
            if result != LoginResult.SUCCESS:
                return result
            
            # Preenche senha
            result = await self._fill_password_field(credentials['password'])
            if result != LoginResult.SUCCESS:
                return result
            
            # Verifica sucesso do login
            await asyncio.sleep(random.uniform(3.0, 6.0))
            
            if await self._check_login_success():
                print("🎉 Login automático realizado com sucesso!")
                await self.browser_manager.navigate_safely('https://www.youtube.com')
                return LoginResult.SUCCESS
            else:
                print("❌ Login automático falhou")
                return LoginResult.FAILED
                
        except Exception as e:
            print(f"❌ Erro no login automático: {e}")
            return LoginResult.FAILED
    
    async def _fill_email_field(self, email: str) -> LoginResult:
        """Preenche campo de email"""
        try:
            # Localiza campo de email
            email_selectors = [
                'input[type="email"]',
                'input[id="identifierId"]',
                'input[name="identifier"]',
                'input[autocomplete="username"]'
            ]
            
            email_field = None
            for selector in email_selectors:
                try:
                    email_field = await self.browser_manager.page.find(selector, timeout=3000)
                    if email_field:
                        break
                except:
                    continue
            
            if not email_field:
                print("❌ Campo de email não encontrado")
                return LoginResult.FAILED
            
            # Preenche email com simulação humana
            await self.human_simulator.human_click(self.browser_manager.page, email_field)
            await self.human_simulator.human_typing(email_field, email)
            
            # Clica em "Próximo"
            next_button = await self._find_next_button()
            if next_button:
                await self.human_simulator.human_click(self.browser_manager.page, next_button)
                await asyncio.sleep(random.uniform(2.0, 4.0))
            
            return LoginResult.SUCCESS
            
        except Exception as e:
            print(f"❌ Erro ao preencher email: {e}")
            return LoginResult.FAILED
    
    async def _fill_password_field(self, password: str) -> LoginResult:
        """Preenche campo de senha"""
        try:
            # Aguarda campo de senha aparecer
            password_selectors = [
                'input[type="password"]',
                'input[name="password"]',
                'input[autocomplete="current-password"]'
            ]
            
            password_field = None
            for selector in password_selectors:
                try:
                    password_field = await self.browser_manager.page.find(selector, timeout=5000)
                    if password_field:
                        break
                except:
                    continue
            
            if not password_field:
                print("❌ Campo de senha não encontrado")
                
                # Verifica se há captcha ou outros bloqueios
                if await self._detect_captcha():
                    return LoginResult.CAPTCHA_REQUIRED
                
                return LoginResult.FAILED
            
            # Preenche senha com simulação humana
            await self.human_simulator.human_click(self.browser_manager.page, password_field)
            await self.human_simulator.human_typing(password_field, password, simulate_mistakes=False)
            
            # Clica em "Próximo" ou "Entrar"
            login_button = await self._find_login_button()
            if login_button:
                await self.human_simulator.human_click(self.browser_manager.page, login_button)
                await asyncio.sleep(random.uniform(2.0, 4.0))
            
            return LoginResult.SUCCESS
            
        except Exception as e:
            print(f"❌ Erro ao preencher senha: {e}")
            return LoginResult.FAILED
    
    async def _find_next_button(self):
        """Localiza botão 'Próximo'"""
        next_selectors = [
            'button[id="identifierNext"]',
            'button:has-text("Próximo")',
            'button:has-text("Next")',
            'input[type="submit"]',
            'button[type="submit"]'
        ]
        
        for selector in next_selectors:
            try:
                button = await self.browser_manager.page.find(selector, timeout=2000)
                if button:
                    return button
            except:
                continue
        
        return None
    
    async def _find_login_button(self):
        """Localiza botão de login"""
        login_selectors = [
            'button[id="passwordNext"]',
            'button:has-text("Entrar")',
            'button:has-text("Sign in")',
            'button:has-text("Login")',
            'input[type="submit"]',
            'button[type="submit"]'
        ]
        
        for selector in login_selectors:
            try:
                button = await self.browser_manager.page.find(selector, timeout=2000)
                if button:
                    return button
            except:
                continue
        
        return None
    
    async def _detect_captcha(self) -> bool:
        """Detecta presença de captcha"""
        captcha_indicators = [
            'div[class*="captcha"]',
            'iframe[src*="captcha"]',
            'div[class*="recaptcha"]',
            'text="Please verify"',
            'text="Verificação necessária"'
        ]
        
        for indicator in captcha_indicators:
            try:
                element = await self.browser_manager.page.find(indicator, timeout=1000)
                if element:
                    print("🤖 Captcha detectado")
                    return True
            except:
                continue
        
        return False
    
    async def _check_login_success(self) -> bool:
        """Verifica se o login foi bem-sucedido"""
        
        # Indicadores de sucesso
        success_indicators = [
            'accounts.google.com/b/0/ManageAccount',
            'myaccount.google.com',
            'text="Conta Google"',
            'button[aria-label*="Conta"]',
            'img[alt*="Avatar"]'
        ]
        
        # Indicadores de erro
        error_indicators = [
            'text="Senha incorreta"',
            'text="Wrong password"',
            'text="Couldn\'t sign in"',
            'text="Não foi possível fazer login"',
            'div[class*="error"]',
            'div[class*="warning"]'
        ]
        
        # Verifica erros primeiro
        for indicator in error_indicators:
            try:
                error = await self.browser_manager.page.find(indicator, timeout=1000)
                if error:
                    print(f"❌ Erro de login detectado: {indicator}")
                    return False
            except:
                continue
        
        # Verifica sucessos
        for indicator in success_indicators:
            try:
                success = await self.browser_manager.page.find(indicator, timeout=3000)
                if success:
                    print(f"✅ Login bem-sucedido detectado: {indicator}")
                    return True
            except:
                continue
        
        # Verifica URL atual
        current_url = self.browser_manager.page.url
        if any(domain in current_url for domain in ['myaccount.google.com', 'accounts.google.com/ManageAccount']):
            return True
        
        return False
    
    async def _manual_assisted_login(self) -> LoginResult:
        """Login assistido manual"""
        
        print("\n" + "="*60)
        print("🔐 LOGIN MANUAL ASSISTIDO")
        print("="*60)
        print("📋 Uma nova aba será aberta para login manual")
        print("📋 Faça login normalmente no Google/YouTube")
        print("📋 Após o login, volte para este terminal")
        print("="*60)
        
        try:
            # Abre aba para login manual
            manual_page = await self.browser_manager.browser.new_page()
            await manual_page.goto('https://accounts.google.com/signin')
            
            # Aguarda login manual
            print("\n⏳ Aguardando login manual...")
            input("▶️  Pressione ENTER após fazer login manualmente: ")
            
            # Fecha aba manual
            await manual_page.close()
            
            # Navega para YouTube na aba principal
            await self.browser_manager.navigate_safely('https://www.youtube.com')
            
            # Verifica se está logado
            if await self._is_logged_in():
                print("🎉 Login manual realizado com sucesso!")
                return LoginResult.SUCCESS
            else:
                print("❌ Login manual não detectado")
                return LoginResult.FAILED
                
        except Exception as e:
            print(f"❌ Erro no login manual: {e}")
            return LoginResult.FAILED
    
    async def _is_logged_in(self) -> bool:
        """Verifica se está logado no YouTube"""
        
        login_indicators = [
            'button[aria-label*="Conta do Google"]',
            'button[aria-label*="conta"]',
            'img[id="avatar-btn"]',
            'button[id="avatar-btn"]',
            'yt-img-shadow[id="avatar"]',
            '[aria-label*="Avatar"]'
        ]
        
        for indicator in login_indicators:
            try:
                element = await self.browser_manager.page.find(indicator, timeout=3000)
                if element:
                    print(f"✅ Login detectado: {indicator}")
                    return True
            except:
                continue
        
        # Verifica se há botão de "Fazer login"
        signin_buttons = [
            'a:has-text("Fazer login")',
            'a:has-text("Sign in")',
            'paper-button:has-text("FAZER LOGIN")'
        ]
        
        for button in signin_buttons:
            try:
                element = await self.browser_manager.page.find(button, timeout=2000)
                if element:
                    print("📝 Botão de login encontrado - não está logado")
                    return False
            except:
                continue
        
        print("🤔 Status de login incerto")
        return False
    
    async def logout(self) -> bool:
        """Faz logout da conta"""
        try:
            print("🚪 Fazendo logout...")
            
            # Clica no avatar
            avatar_selectors = [
                'button[id="avatar-btn"]',
                'yt-img-shadow[id="avatar"]',
                'button[aria-label*="conta"]'
            ]
            
            avatar = None
            for selector in avatar_selectors:
                try:
                    avatar = await self.browser_manager.page.find(selector, timeout=3000)
                    if avatar:
                        break
                except:
                    continue
            
            if not avatar:
                print("❌ Avatar não encontrado para logout")
                return False
            
            await self.human_simulator.human_click(self.browser_manager.page, avatar)
            await asyncio.sleep(random.uniform(1.0, 2.0))
            
            # Clica em "Sair"
            logout_selectors = [
                'a:has-text("Sair")',
                'a:has-text("Sign out")',
                'yt-formatted-string:has-text("Sair")'
            ]
            
            logout_button = None
            for selector in logout_selectors:
                try:
                    logout_button = await self.browser_manager.page.find(selector, timeout=3000)
                    if logout_button:
                        break
                except:
                    continue
            
            if logout_button:
                await self.human_simulator.human_click(self.browser_manager.page, logout_button)
                await asyncio.sleep(random.uniform(2.0, 4.0))
                
                print("✅ Logout realizado com sucesso")
                return True
            else:
                print("❌ Botão de logout não encontrado")
                return False
                
        except Exception as e:
            print(f"❌ Erro durante logout: {e}")
            return False
