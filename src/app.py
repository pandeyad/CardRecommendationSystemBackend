from src import create_app, scheduled_job_runner, load_config
import threading
import sys
import signal

from src.llm import dynamically_register_all_models


def signal_handler(sig, frame):
    """Gracefully handle shutdown on SIGINT"""
    print('Cleaning up and shutting down gracefully...')
    sys.exit(0)

# Register the signal handler for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

def main():
    config = load_config()
    dynamically_register_all_models('src/llm/models/') # To dynamically load all llm models
    # Start the scheduled jobs in a separate thread
    scheduler_thread = threading.Thread(target=scheduled_job_runner)
    scheduler_thread.daemon = True  # Allow the thread to exit when the main program exits
    scheduler_thread.start()
    app = create_app()
    app.run(
        debug=config["app"]["debug"],
        host=config["app"]["host"],
        port=config["app"]["port"]
    )

if __name__ == "__main__":
    main()