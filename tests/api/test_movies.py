import requests

from constants import AUTH_SU_CREDENTIALS


class TestMoviesAPI:

    def test_delete(self, api_manager_su):
        print (api_manager_su.movies_api.get_session().headers)