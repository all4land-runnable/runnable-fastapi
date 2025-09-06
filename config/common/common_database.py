from abc import ABC, abstractmethod

class CommonDatabase(ABC):
    """
    프로젝트에서 데이터베이스 구현을 위해 준수해야 할 필수 인터페이스

    데이터베이스 드라이버를 구현할 시, 꼭 다음 함수를 이용해주세요.
    """
    @abstractmethod
    def get_connection(self):
        """
        데이터베이스 Connection을 반환하는 함수입니다.
        """
        pass

    @abstractmethod
    def get_cursor(self):
        """
        Connection의 Cursor를 반환하는 함수입니다.
        """
        pass

    @abstractmethod
    def execute_update(self, sql: str, values: tuple=()) -> None:
        """
        create, insert, update, delete sql 구현에 사용하는 함수입니다.

        Parameters:
            sql(str): 구현할 SQL입니다.
            values(tuple): SQL에 포함될 데이터입니다.
        """
        pass

    @abstractmethod
    def execute_query(self, sql: str, values: tuple=()):
        """
        select sql 구현에 사용하는 함수입니다.

        Parameters:
            sql(str): 구현할 SQL입니다.
            values(tuple): SQL에 포함될 데이터입니다.
        """
        pass