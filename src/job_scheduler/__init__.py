from apscheduler.schedulers.background import BackgroundScheduler
from src.llm import RecommendationApp
from src.runner import RunnerFactory
from src.utils.python_util import load_config, get_nested


class JobIntervalScheduler(BackgroundScheduler):

    def __init__(self, **options):
        super().__init__(**options)
        self.config = load_config()
        # Expose the singleton instance globally
        self.runner_factory = RunnerFactory()

    def schedule(self):
        self.runner_factory.run_all()
        RecommendationApp.refresh_model_data()
        # Add scheduled jobs with simplified configuration fetching
        self.add_job(self.runner_factory.run_all, 'interval',
                     seconds=int(get_nested(self.config, 'scheduler.data_crawl.interval', 900)))
        self.add_job(RecommendationApp.refresh_model_data, 'interval',
                     seconds=int(get_nested(self.config, 'scheduler.data_train.interval', 600)))
        self.start()
