"""
The Train Captain - Logger Utility
Handles application logging and error tracking
"""

import logging
import os
from datetime import datetime
from pathlib import Path
import traceback
import json
from typing import Optional, Dict, Any

class Logger:
    """Application logger with file and console output"""
    
    # Log levels
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """Singleton pattern to ensure single logger instance"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the logger"""
        if Logger._initialized:
            return
        
        # Create logs directory
        self.logs_dir = Path(__file__).parent.parent / 'logs'
        self.logs_dir.mkdir(exist_ok=True)
        
        # Setup logger
        self.logger = logging.getLogger('TrainCaptain')
        self.logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers
        self.logger.handlers.clear()
        
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # File handler - main log
        log_file = self.logs_dir / f'app_{datetime.now().strftime("%Y%m%d")}.log'
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # File handler - error log
        error_log_file = self.logs_dir / f'error_{datetime.now().strftime("%Y%m%d")}.log'
        error_handler = logging.FileHandler(error_log_file, encoding='utf-8')
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        self.logger.addHandler(error_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # Performance log file
        self.performance_log = self.logs_dir / f'performance_{datetime.now().strftime("%Y%m%d")}.log'
        
        Logger._initialized = True
        
        self.info("Logger initialized")
    
    def debug(self, message: str, *args, **kwargs):
        """Log debug message"""
        self.logger.debug(message, *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs):
        """Log info message"""
        self.logger.info(message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs):
        """Log warning message"""
        self.logger.warning(message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs):
        """Log error message"""
        self.logger.error(message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs):
        """Log critical message"""
        self.logger.critical(message, *args, **kwargs)
    
    def exception(self, message: str, *args, **kwargs):
        """Log exception with traceback"""
        self.logger.exception(message, *args, **kwargs)
    
    def log_user_action(self, user: str, action: str, details: Optional[Dict] = None):
        """Log user actions for audit trail"""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'user': user,
            'action': action,
            'details': details or {}
        }
        
        # Log to file
        audit_file = self.logs_dir / f'audit_{datetime.now().strftime("%Y%m")}.log'
        with open(audit_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_data) + '\n')
        
        self.info(f"User Action - {user}: {action}")
    
    def log_performance(self, operation: str, duration: float, details: Optional[Dict] = None):
        """Log performance metrics"""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'duration_ms': round(duration * 1000, 2),
            'details': details or {}
        }
        
        with open(self.performance_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_data) + '\n')
        
        if duration > 1.0:  # Log slow operations
            self.warning(f"Slow operation - {operation}: {duration:.2f}s")
    
    def log_error_with_context(self, error: Exception, context: Dict[str, Any]):
        """Log error with additional context"""
        error_data = {
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'context': context
        }
        
        # Log to separate error file
        error_file = self.logs_dir / f'errors_{datetime.now().strftime("%Y%m")}.json'
        
        errors = []
        if error_file.exists():
            with open(error_file, 'r', encoding='utf-8') as f:
                try:
                    errors = json.load(f)
                except:
                    errors = []
        
        errors.append(error_data)
        
        with open(error_file, 'w', encoding='utf-8') as f:
            json.dump(errors, f, indent=2)
        
        self.error(f"Error: {error}")
    
    def get_recent_logs(self, lines: int = 100) -> str:
        """Get recent log entries"""
        log_file = self.logs_dir / f'app_{datetime.now().strftime("%Y%m%d")}.log'
        
        if not log_file.exists():
            return "No logs found"
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = f.readlines()
                return ''.join(logs[-lines:])
        except Exception as e:
            return f"Error reading logs: {e}"
    
    def get_error_summary(self) -> Dict:
        """Get summary of errors"""
        error_file = self.logs_dir / f'errors_{datetime.now().strftime("%Y%m")}.json'
        
        if not error_file.exists():
            return {'total': 0, 'errors': []}
        
        try:
            with open(error_file, 'r', encoding='utf-8') as f:
                errors = json.load(f)
            
            # Summarize by type
            error_types = {}
            for error in errors:
                error_type = error['error_type']
                error_types[error_type] = error_types.get(error_type, 0) + 1
            
            return {
                'total': len(errors),
                'by_type': error_types,
                'latest': errors[-1] if errors else None
            }
        except Exception as e:
            return {'total': 0, 'error': str(e)}
    
    def cleanup_old_logs(self, days: int = 30):
        """Delete logs older than specified days"""
        try:
            current_time = datetime.now()
            for log_file in self.logs_dir.glob('*.log'):
                if log_file.name.startswith('app_'):
                    file_date_str = log_file.stem.split('_')[1]
                    try:
                        file_date = datetime.strptime(file_date_str, '%Y%m%d')
                        age = (current_time - file_date).days
                        if age > days:
                            log_file.unlink()
                            self.info(f"Deleted old log: {log_file.name}")
                    except:
                        continue
            
            # Clean old error JSON files
            for error_file in self.logs_dir.glob('errors_*.json'):
                file_date_str = error_file.stem.split('_')[1]
                try:
                    file_date = datetime.strptime(file_date_str, '%Y%m')
                    age_months = (current_time.year - file_date.year) * 12 + \
                                 (current_time.month - file_date.month)
                    if age_months > 3:  # Keep 3 months of error logs
                        error_file.unlink()
                        self.info(f"Deleted old error log: {error_file.name}")
                except:
                    continue
                    
        except Exception as e:
            self.error(f"Error cleaning up logs: {e}")


class PerformanceMonitor:
    """Context manager for performance monitoring"""
    
    def __init__(self, operation: str, logger: Logger, **kwargs):
        self.operation = operation
        self.logger = logger
        self.kwargs = kwargs
        self.start_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            duration = (datetime.now() - self.start_time).total_seconds()
            self.logger.log_performance(self.operation, duration, self.kwargs)
            
            if exc_type:
                self.logger.error(f"Error in {self.operation}: {exc_val}")


# Global logger instance
logger = Logger()

# Convenience functions
def debug(msg, *args, **kwargs):
    logger.debug(msg, *args, **kwargs)

def info(msg, *args, **kwargs):
    logger.info(msg, *args, **kwargs)

def warning(msg, *args, **kwargs):
    logger.warning(msg, *args, **kwargs)

def error(msg, *args, **kwargs):
    logger.error(msg, *args, **kwargs)

def critical(msg, *args, **kwargs):
    logger.critical(msg, *args, **kwargs)

def exception(msg, *args, **kwargs):
    logger.exception(msg, *args, **kwargs)

def log_user_action(user, action, details=None):
    logger.log_user_action(user, action, details)

def monitor(operation, **kwargs):
    """Decorator for monitoring function performance"""
    def decorator(func):
        def wrapper(*args, **wrapper_kwargs):
            with PerformanceMonitor(operation, logger, **kwargs):
                return func(*args, **wrapper_kwargs)
        return wrapper
    return decorator