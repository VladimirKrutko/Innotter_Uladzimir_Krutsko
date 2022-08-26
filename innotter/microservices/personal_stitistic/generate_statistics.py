from typing import List, Dict, Tuple

import psycopg2 as psycopg


class GetStatistics:
    HOST = 'localhost'
    DATABASE = 'innotter_db'
    USERNAME = 'innotter'
    PASSWORD = '1458'
    POST_STATISTIC = (
        " SELECT count(*) "
        " FROM post_post pp "
        " JOIN page_page p ON p.id = pp.page_id_id"
        " WHERE exists( "
        " SELECT 1 "
        " FROM user_user uu "
        " WHERE p.owner_id = uu.id AND "
        " uu.email = '{}' "
        " ); "
    )
    LIKES_STATISTIC = (
        " SELECT coalesce(count(*), 0) "
        " FROM post_post_likes pp "
        " WHERE exists( "
        " SELECT 1"
        " FROM user_user uu "
        " WHERE pp.user_id = uu.id AND "
        " uu.email = '{}'"
        ");"
    )

    def connection(self):
        conn = psycopg.connect(
            host=self.HOST,
            database=self.DATABASE,
            user=self.USERNAME,
            password=self.PASSWORD,
        )
        return conn

    def _query_render(self, query_result: List[tuple], keys: Tuple[str, ...]) -> List[Dict]:
        """
        Function to transform list of tuples to list of dicts
        """
        json_query = [
            {key: value for key, value in zip(keys, row)} for row in query_result
        ]

        return json_query

    def execute_query(self, query):
        with self.connection() as conn:

            with conn.cursor() as cur:
                cur.execute(query)
                query_result = cur.fetchall()

        return query_result

    def generate_statistic(self, email):
        post_count = self.execute_query(
            self.POST_STATISTIC.format(email))
        likes_count = self.execute_query(self.LIKES_STATISTIC.format(email))
        result = {"post_count": post_count[0], "likes_count": likes_count}
        return result
