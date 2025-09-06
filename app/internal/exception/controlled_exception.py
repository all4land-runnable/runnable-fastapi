from app.internal.exception.error_message import ErrorMessage


class ControlledException(RuntimeError):
    """
    예측 가능한 에러를 관리하기 위한 Exception Class
    """
    def __init__(self, error_code: ErrorMessage):
        self.error_code = error_code