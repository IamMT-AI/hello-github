"""
Common logging utilities
Addresses the log-metrics draft issue with placeholder for Prometheus integration.
"""

import logging
import time
from typing import Any, Dict, Optional
from functools import wraps

import structlog


def setup_logging(level: str = "INFO", json_format: bool = True) -> None:
    """
    Set up structured logging for the application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_format: Whether to use JSON formatting for logs
    """
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.ConsoleRenderer()
            if not json_format
            else structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, level.upper())
        ),
        logger_factory=structlog.WriteLoggerFactory(),
        context_class=dict,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """
    Get a structured logger instance.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured structlog logger
    """
    return structlog.get_logger(name)


def log_execution_time(logger: Optional[structlog.BoundLogger] = None):
    """
    Decorator to log function execution time.

    Args:
        logger: Logger instance to use (creates default if None)
    """

    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            if logger is None:
                log = get_logger(func.__module__)
            else:
                log = logger

            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                execution_time = time.time() - start_time
                log.info(
                    "Function executed successfully",
                    function=func.__name__,
                    execution_time=execution_time,
                    args_count=len(args),
                    kwargs_count=len(kwargs),
                )
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                log.error(
                    "Function execution failed",
                    function=func.__name__,
                    execution_time=execution_time,
                    error=str(e),
                    error_type=type(e).__name__,
                )
                raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            if logger is None:
                log = get_logger(func.__module__)
            else:
                log = logger

            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                log.info(
                    "Function executed successfully",
                    function=func.__name__,
                    execution_time=execution_time,
                    args_count=len(args),
                    kwargs_count=len(kwargs),
                )
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                log.error(
                    "Function execution failed",
                    function=func.__name__,
                    execution_time=execution_time,
                    error=str(e),
                    error_type=type(e).__name__,
                )
                raise

        # Return appropriate wrapper based on function type
        import asyncio

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


class MetricsCollector:
    """
    Placeholder metrics collector for Prometheus integration.
    MVP Week 1: Basic structure for future metrics collection.
    """

    def __init__(self):
        self.metrics: Dict[str, Any] = {}
        self.logger = get_logger(__name__)

    def increment_counter(
        self, name: str, value: float = 1.0, labels: Optional[Dict[str, str]] = None
    ):
        """Increment a counter metric"""
        metric_key = f"{name}_{hash(str(labels)) if labels else 'default'}"
        if metric_key not in self.metrics:
            self.metrics[metric_key] = 0
        self.metrics[metric_key] += value

        self.logger.debug(
            "Counter incremented",
            metric=name,
            value=value,
            labels=labels,
            total=self.metrics[metric_key],
        )

    def record_histogram(
        self, name: str, value: float, labels: Optional[Dict[str, str]] = None
    ):
        """Record a histogram value"""
        metric_key = f"{name}_hist_{hash(str(labels)) if labels else 'default'}"
        if metric_key not in self.metrics:
            self.metrics[metric_key] = []
        self.metrics[metric_key].append(value)

        self.logger.debug(
            "Histogram value recorded",
            metric=name,
            value=value,
            labels=labels,
        )

    def set_gauge(
        self, name: str, value: float, labels: Optional[Dict[str, str]] = None
    ):
        """Set a gauge metric value"""
        metric_key = f"{name}_gauge_{hash(str(labels)) if labels else 'default'}"
        self.metrics[metric_key] = value

        self.logger.debug(
            "Gauge value set",
            metric=name,
            value=value,
            labels=labels,
        )

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of collected metrics"""
        return {
            "total_metrics": len(self.metrics),
            "metrics": self.metrics,
            "timestamp": time.time(),
        }


# Global metrics collector instance
metrics = MetricsCollector()


def track_request_metrics(endpoint: str):
    """Decorator to track request metrics"""

    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                metrics.increment_counter(
                    "requests_total", labels={"endpoint": endpoint, "status": "success"}
                )
                metrics.record_histogram(
                    "request_duration_seconds", duration, labels={"endpoint": endpoint}
                )
                return result
            except Exception as e:
                duration = time.time() - start_time
                metrics.increment_counter(
                    "requests_total", labels={"endpoint": endpoint, "status": "error"}
                )
                metrics.record_histogram(
                    "request_duration_seconds", duration, labels={"endpoint": endpoint}
                )
                raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                metrics.increment_counter(
                    "requests_total", labels={"endpoint": endpoint, "status": "success"}
                )
                metrics.record_histogram(
                    "request_duration_seconds", duration, labels={"endpoint": endpoint}
                )
                return result
            except Exception as e:
                duration = time.time() - start_time
                metrics.increment_counter(
                    "requests_total", labels={"endpoint": endpoint, "status": "error"}
                )
                metrics.record_histogram(
                    "request_duration_seconds", duration, labels={"endpoint": endpoint}
                )
                raise

        import asyncio

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator
