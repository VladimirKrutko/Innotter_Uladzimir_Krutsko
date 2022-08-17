from typing import List, Dict, Tuple
import psycopg2 as psycopg
from innotter.settings import DATABASES
from exceptions import IncorrectFormat


class GetStatistics:
    HOST = DATABASES['default']['HOST']
    DATABASE = DATABASES['default']['NAME']
    USERNAME = DATABASES['default']['USER']
    PASSWORD = DATABASES['default']['PASSWORD']

    def connection(self):
        conn = psycopg.connect(
            host=self.HOST,
            database=self.DATABASE,
            user=self.USERNAME,
            password=self.PASSWORD
        )
        return conn

    def _query_render(self, query_result: List[tuple], keys: Tuple[str, ...]) -> List[Dict]:
        """
        Function to transform list of tuples to list of dicts
        """
        json_query = [{key: value for key, value in zip(keys, row)}
                      for row in query_result]

        return json_query

    def get_user_statistics_by_date(self, date) -> list[Dict]:
        """
        Get dict with users that registration in system after date
        """
        split_date = date.split('-')
        if len(split_date) == 3:
            if len(split_date[0]) != 4 or len(split_date[1]) != 2 or len(split_date[2]) != 2:
                raise IncorrectFormat('Incorrect date format, should be \'YYYY-MM-DD\'')
        else:
            raise IncorrectFormat('Incorrect date format, should be \'YYYY-MM-DD\'')

        query = 'select email, username, create_data, create_data, last_login, ' \
                ' is_blocked, is_active, is_staff, is_admin, image_s3_path ' \
                ' from user_user ' \
                f' where \'{date}\' < create_data; '

        with self.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                user_data = cur.fetchall()

        json_data = self._query_render(query_result=user_data,
                                       keys=('email', 'username', 'create_data', 'create_data', 'last_login',
                                             'is_blocked', 'is_active', 'is_staff', 'is_admin', 'image_s3_path'))

        return json_data

