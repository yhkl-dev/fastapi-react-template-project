from .tasks import test_task


class AccountMonitorService:
    @staticmethod
    def run_task():
        t = test_task.delay()
        return t.id

    @staticmethod
    def detect_new_accounts():
        print("detect new accounts: ")
