# src/main.py

from scheduler import Scheduler

if __name__ == "__main__":
    scheduler = Scheduler()
    print("Scheduler started")
    scheduler.start()