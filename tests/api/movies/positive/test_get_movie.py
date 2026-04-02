from datetime import datetime

from math import ceil
from http import HTTPStatus
from typing import Any
from faker import Faker

fake = Faker()


class TestPositiveGet:

    def test_get_movies_list_no_query(self, api_manager_su):
        api_manager_su.movies_api.get_movies_list(query={})

    def test_get_movies_list(self, api_manager_su):
        page_number = fake.random_int(max=30, min=1)
        page_size = fake.random_int(max=20, min=1)
        response = api_manager_su.movies_api.get_movies_list({
            'page': page_number,
            'pageSize': page_size
        })
        current_page = response.json()
        pages_count = current_page.get("count")
        current_size = current_page.get("pageSize")
        expect_page_count = ceil(pages_count / current_size)
        movies_list = current_page.get('movies')

        assert current_page.get("page") == page_number, \
            f"vagination page is{current_page.get('page')}, expected {page_number}"

        assert current_size == len(movies_list), \
            f"vagination response has pageSize and len(movies) are not equal"

        assert current_size == page_size, \
            f"vagination pageSize is {current_size}, expected {page_size}"

        assert len(movies_list) == page_size, \
            f"vagination: length of movies is {len(movies_list)}, expected {page_size}"

        assert current_page.get("pageCount") == expect_page_count, \
            f"vagination pageCount is {pages_count}, expected {expect_page_count}"

    def test_get_movies_list_positive_boundaries(self, api_manager_su):
        api_manager_su.movies_api.get_movies_list({
            'page': 1,
            'pageSize': 1
        }, expected_status=HTTPStatus.OK)

        api_manager_su.movies_api.get_movies_list({
            'page': fake.random_int(max=20, min=1),
            'pageSize': 20
        }, expected_status=HTTPStatus.OK)

    def test_get_movies_list_sort(self, api_manager_su):
        def check_date_times_sort(movies_list: list[dict[str, Any]], reverse: bool=False):
            date_times = [
                datetime.fromisoformat(item['createdAt'].replace('Z', '+00:00'))
                for item in movies_list
            ]
            assert date_times == sorted(date_times, reverse=reverse), 'Сортировка выполнена неверно'

        response = api_manager_su.movies_api.get_movies_list({
            "createdAt": "asc"
        })
        movies = response.json().get("movies")
        check_date_times_sort(movies)

        response = api_manager_su.movies_api.get_movies_list({
            "createdAt": "desc"
        })
        movies = response.json().get("movies")
        check_date_times_sort(
            movies_list=movies,
            reverse=True
        )
