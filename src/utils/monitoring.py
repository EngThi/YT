"""
Monitoring System - Sistema de Monitoramento Avançado
====================================================

Sistema de monitoramento com métricas, health checks e alertas.
"""

import time
import psutil
import asyncio
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from .logger import get_logger


@dataclass
class PerformanceMetric:
    """Métrica de performance"""
    name: str
    value: float
    unit: str
    timestamp: datetime
    category: str = "general"
    tags: Dict[str, str] = None


@dataclass
class HealthCheckResult:
    """Resultado de health check"""
    component: str
    status: str  # healthy, warning, critical
    message: str
    latency_ms: float
    timestamp: datetime


class PerformanceMonitor:
    """Monitor de performance do sistema"""
    
    def __init__(self):
        self.logger = get_logger("performance_monitor")
        self.metrics: List[PerformanceMetric] = []
        self.start_time = time.time()
        
    def record_metric(self, name: str, value: float, unit: str = "ms", 
                     category: str = "general", tags: Dict[str, str] = None):
        """Registra uma métrica de performance"""
        metric = PerformanceMetric(
            name=name,
            value=value,
            unit=unit,
            timestamp=datetime.now(),
            category=category,
            tags=tags or {}
        )
        
        self.metrics.append(metric)
        self.logger.performance_metric(name, value, unit)
        
        # Mantém apenas últimas 1000 métricas
        if len(self.metrics) > 1000:
            self.metrics = self.metrics[-1000:]
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Obtém métricas do sistema"""
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "uptime_seconds": time.time() - self.start_time,
            "process_count": len(psutil.pids())
        }
    
    def get_metrics_summary(self, category: str = None, 
                          last_minutes: int = 60) -> Dict[str, Any]:
        """Resumo das métricas"""
        cutoff_time = datetime.now() - timedelta(minutes=last_minutes)
        
        filtered_metrics = [
            m for m in self.metrics 
            if m.timestamp >= cutoff_time and (category is None or m.category == category)
        ]
        
        if not filtered_metrics:
            return {"count": 0, "metrics": []}
        
        by_name = {}
        for metric in filtered_metrics:
            if metric.name not in by_name:
                by_name[metric.name] = []
            by_name[metric.name].append(metric.value)
        
        summary = {}
        for name, values in by_name.items():
            summary[name] = {
                "count": len(values),
                "avg": sum(values) / len(values),
                "min": min(values),
                "max": max(values),
                "latest": values[-1]
            }
        
        return {
            "count": len(filtered_metrics),
            "timeframe_minutes": last_minutes,
            "metrics": summary
        }


class HealthChecker:
    """Sistema de health checks"""
    
    def __init__(self):
        self.logger = get_logger("health_checker")
        self.checks: List[HealthCheckResult] = []
    
    async def check_component_health(self, component: str, 
                                   check_func: callable) -> HealthCheckResult:
        """Executa health check de um componente"""
        start_time = time.time()
        
        try:
            result = await check_func() if asyncio.iscoroutinefunction(check_func) else check_func()
            latency = (time.time() - start_time) * 1000
            
            if result is True:
                status, message = "healthy", "Component is functioning normally"
            elif isinstance(result, dict):
                status = result.get("status", "healthy")
                message = result.get("message", "Component check completed")
            else:
                status, message = "warning", f"Unexpected result: {result}"
                
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            status, message = "critical", f"Health check failed: {str(e)}"
        
        health_result = HealthCheckResult(
            component=component,
            status=status,
            message=message,
            latency_ms=latency,
            timestamp=datetime.now()
        )
        
        self.checks.append(health_result)
        self.logger.info(f"Health check {component}: {status} ({latency:.1f}ms)")
        
        return health_result
    
    async def check_browser_health(self, browser_manager) -> HealthCheckResult:
        """Health check específico do browser"""
        def browser_check():
            if browser_manager.browser is None:
                return {"status": "critical", "message": "Browser not initialized"}
            return {"status": "healthy", "message": "Browser is running"}
        
        return await self.check_component_health("browser", browser_check)
    
    async def check_config_health(self) -> HealthCheckResult:
        """Health check das configurações"""
        def config_check():
            try:
                from .config import get_config
                config = get_config()
                if config.app_name and config.version:
                    return {"status": "healthy", "message": "Configuration loaded successfully"}
                return {"status": "warning", "message": "Configuration incomplete"}
            except Exception as e:
                return {"status": "critical", "message": f"Configuration error: {e}"}
        
        return await self.check_component_health("config", config_check)
    
    async def check_logs_health(self) -> HealthCheckResult:
        """Health check do sistema de logs"""
        def logs_check():
            try:
                import os
                logs_dir = "logs"
                if os.path.exists(logs_dir):
                    log_files = [f for f in os.listdir(logs_dir) if f.endswith('.log')]
                    if log_files:
                        return {"status": "healthy", "message": f"Found {len(log_files)} log files"}
                    return {"status": "warning", "message": "No log files found"}
                return {"status": "critical", "message": "Logs directory not found"}
            except Exception as e:
                return {"status": "critical", "message": f"Logs check error: {e}"}
        
        return await self.check_component_health("logs", logs_check)
    
    def get_overall_health(self) -> Dict[str, Any]:
        """Status geral de saúde do sistema"""
        if not self.checks:
            return {"status": "unknown", "message": "No health checks performed"}
        
        latest_checks = {}
        for check in reversed(self.checks):
            if check.component not in latest_checks:
                latest_checks[check.component] = check
        
        status_priority = {"healthy": 0, "warning": 1, "critical": 2}
        overall_status = "healthy"
        
        for check in latest_checks.values():
            if status_priority.get(check.status, 2) > status_priority[overall_status]:
                overall_status = check.status
        
        return {
            "status": overall_status,
            "components": len(latest_checks),
            "last_check": max(check.timestamp for check in latest_checks.values()).isoformat(),
            "details": {comp: {"status": check.status, "message": check.message} 
                       for comp, check in latest_checks.items()}
        }


class AutomationMonitor:
    """Monitor completo para automação"""
    
    def __init__(self):
        self.performance = PerformanceMonitor()
        self.health = HealthChecker()
        self.logger = get_logger("automation_monitor")
        self.session_start = datetime.now()
    
    async def full_health_check(self, browser_manager=None) -> Dict[str, Any]:
        """Executa todos os health checks"""
        self.logger.info("🔍 Executando health check completo...")
        
        checks = [
            self.health.check_config_health(),
            self.health.check_logs_health()
        ]
        
        if browser_manager:
            checks.append(self.health.check_browser_health(browser_manager))
        
        # Executa todos os checks
        await asyncio.gather(*checks)
        
        # Obtém status geral
        overall_health = self.health.get_overall_health()
        system_metrics = self.performance.get_system_metrics()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "session_duration": str(datetime.now() - self.session_start),
            "health": overall_health,
            "system": system_metrics,
            "performance": self.performance.get_metrics_summary(last_minutes=30)
        }
        
        self.logger.info(f"🏥 Health check concluído: {overall_health['status']}")
        return report
    
    def track_operation(self, operation_name: str):
        """Decorator para tracking de operações"""
        def decorator(func):
            async def async_wrapper(*args, **kwargs):
                start_time = time.time()
                self.logger.automation_start(operation_name)
                
                try:
                    result = await func(*args, **kwargs)
                    duration = (time.time() - start_time) * 1000
                    
                    self.performance.record_metric(
                        f"{operation_name}_duration", 
                        duration, 
                        "ms", 
                        "automation"
                    )
                    
                    self.logger.automation_success(operation_name, duration/1000)
                    return result
                    
                except Exception as e:
                    duration = (time.time() - start_time) * 1000
                    self.performance.record_metric(
                        f"{operation_name}_error", 
                        duration, 
                        "ms", 
                        "automation_errors"
                    )
                    
                    self.logger.automation_failure(operation_name, str(e), duration/1000)
                    raise
            
            def sync_wrapper(*args, **kwargs):
                start_time = time.time()
                self.logger.automation_start(operation_name)
                
                try:
                    result = func(*args, **kwargs)
                    duration = (time.time() - start_time) * 1000
                    
                    self.performance.record_metric(
                        f"{operation_name}_duration", 
                        duration, 
                        "ms", 
                        "automation"
                    )
                    
                    self.logger.automation_success(operation_name, duration/1000)
                    return result
                    
                except Exception as e:
                    duration = (time.time() - start_time) * 1000
                    self.performance.record_metric(
                        f"{operation_name}_error", 
                        duration, 
                        "ms", 
                        "automation_errors"
                    )
                    
                    self.logger.automation_failure(operation_name, str(e), duration/1000)
                    raise
            
            import inspect
            if inspect.iscoroutinefunction(func):
                return async_wrapper
            else:
                return sync_wrapper
        
        return decorator


# Instância global
monitor = AutomationMonitor()


def get_monitor() -> AutomationMonitor:
    """Obtém instância do monitor"""
    return monitor


if __name__ == "__main__":
    # Teste do sistema de monitoramento
    async def test_monitoring():
        monitor = AutomationMonitor()
        
        # Teste de métricas
        monitor.performance.record_metric("test_metric", 150.5, "ms", "test")
        
        # Teste de health check
        report = await monitor.full_health_check()
        
        print("📊 Relatório de Monitoramento:")
        print(f"Status: {report['health']['status']}")
        print(f"Componentes: {report['health']['components']}")
        print(f"Sistema CPU: {report['system']['cpu_percent']:.1f}%")
        print(f"Sistema Memória: {report['system']['memory_percent']:.1f}%")
        
        return report
    
    import asyncio
    asyncio.run(test_monitoring())
