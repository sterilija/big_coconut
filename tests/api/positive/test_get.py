from tools.is_sorted_by_created_at import is_sorted_by_created_at
import math
from models.http_status_codes import HTTPStatusCodes

class TestPositiveGet:

    def test_get_movies_list_no_query(self, api_manager_su):
        api_manager_su.movies_api.get_movies_list(query={})

    def test_get_movies_list(self, api_manager_su, faker_fxtr):
        page_n = faker_fxtr.random_int(max=30, min=1)
        page_size = faker_fxtr.random_int(max=20, min=1)
        response = api_manager_su.movies_api.get_movies_list({
            'page': page_n,
            'pageSize': page_size
        })
        current_page = response.json()
        pages_count = current_page.get("count")
        current_size = current_page.get("pageSize")
        expect_page_count = math.ceil(pages_count / current_size)
        movies_list = current_page.get('movies')

        assert current_page.get("page") == page_n, \
            f"vagination page is{current_page.get('page')}, expected {page_n}"

        assert current_size == len(movies_list), \
            f"vagination response has pageSize and len(movies) are not equal"

        assert current_size == page_size, \
            f"vagination pageSize is {current_size}, expected {page_size}"

        assert len(movies_list) == page_size, \
            f"vagination: length of movies is {len(movies_list)}, expected {page_size}"

        assert current_page.get("pageCount") == expect_page_count, \
            f"vagination pageCount is {pages_count}, expected {expect_page_count}"

    def test_get_movies_list_positive_boundaries(self, api_manager_su, faker_fxtr):
        api_manager_su.movies_api.get_movies_list({
            'page': 1,
            'pageSize': 1
        }, expect_status=HTTPStatusCodes.Success)

        api_manager_su.movies_api.get_movies_list({
            'page': faker_fxtr.random_int(max=20, min=1),
            'pageSize': 20
        }, expect_status=HTTPStatusCodes.Success)

    def test_get_movies_list_sort(self, api_manager_su):
        response = api_manager_su.movies_api.get_movies_list({
            "createdAt": "asc"
        })
        movies = response.json().get("movies")
        assert is_sorted_by_created_at(items=movies, asc=True)

        response = api_manager_su.movies_api.get_movies_list({
            "createdAt": "desc"
        })
        movies = response.json().get("movies")
        assert is_sorted_by_created_at(items=movies, asc=False)
