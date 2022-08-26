from fastapi import FastAPI
from generate_statistics import GetStatistics


statistics_class = GetStatistics()
app = FastAPI()


@app.get('/get_user_stat/{email}')
def get_user_statistic(email: str):
    user_stat = statistics_class.generate_statistic(email)
    return user_stat

