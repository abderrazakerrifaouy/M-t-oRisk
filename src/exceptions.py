class PipelineError(Exception):
    """Base exception for expected pipeline failures."""


class ExtractionError(PipelineError):
    """Raised when source files or weather API extraction fails."""


class TransformationError(PipelineError):
    """Raised when weather data cannot be transformed or validated."""


class LoadingError(PipelineError):
    """Raised when transformed data cannot be persisted."""


class AnalyticsError(PipelineError):
    """Raised when analytics queries cannot be executed."""
