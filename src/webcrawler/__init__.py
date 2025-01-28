from src.utils.python_util import load_config


class BaseCrawler:

    def __init__(self):
        self.config = load_config()

    def crawl_data(self, **kwargs):
        raise Exception("Unsupported method. Please extend this method.")


    def get_base_data_path(self):
        return self.config['data']['base_path']