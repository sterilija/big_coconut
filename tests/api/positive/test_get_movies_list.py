from faker import Faker
import  math
fake = Faker()

def test_get_movies_list_no_query(api_manager_su):
    api_manager_su.movies_api.get_movies_list(query={})

def test_get_movies_list(api_manager_su):
    #pagination check
    page_n = fake.random_int(max=12, min=1)
    page_size = fake.random_int(max=10, min=1)
    response = api_manager_su.movies_api.get_movies_list({
        'page': page_n,
        'pageSize': page_size
    })
    current_page = response.json()
    expect_page_count = math.ceil(current_page.get("count") / current_page.get("pageSize"))
    #   Проверяем что вернуло правильное кол-во страниц по формуле
    assert current_page.get("page") == page_n, \
        f"vagination page is{current_page.get('page')}, expected {page_n}"
    #   Проверяем что вернуло правильный размер страницы
    assert current_page.get("pageSize") == len(current_page.get("movies")), \
        f"vagination response has pageSize and len(movies) are not equal"
    #   Проверяем что вернуло правильный размер страницы
    assert current_page.get("pageSize") == page_size, \
        f"vagination pageSize is {current_page.get('pageSize')}, expected {page_size}"
    #   Проверяем что в массиве столько же элементов, сколько мы запросили
    assert len(current_page.get("movies")) == page_size, \
        f"vagination: length of movies is {len(current_page.get('movies'))}, expected {page_size}"
    #   Проверяем что вернуло правильное кол-во страниц по факту
    assert current_page.get("pageCount") == expect_page_count, \
        f"vagination pageCount is {current_page.get('pageCount')}, expected {expect_page_count}"
