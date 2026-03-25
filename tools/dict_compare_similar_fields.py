def dict_compare_similar_fields(payload, response_json):
    for k, v in payload.items():
        assert response_json[k] == v