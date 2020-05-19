class ApiRequestGetter:
    ApiRequestGetters_list = []

    def __init__(self, api_url, headers, method, post_data):
        self.api_url = api_url
        self.headers = headers
        self.method = method
        self.post_data = post_data
        ApiRequestGetter.ApiRequestGetters_list.append(self)
