import time

class Time:
    time_started: int = time.time_ns()
    
    @staticmethod
    def get_time() -> float:
        return (time.time_ns() - Time.time_started) * 1e-9

