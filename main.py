from src.transaction_tracker import TransactionTracker
import time

def main():
    tracker = TransactionTracker('config/config.json')
    
    print("Starting Solana transaction tracking...")
    
    while True:
        try:
            tracker.track_transactions()
            time.sleep(10)  # Check for new transactions every 10 seconds
        except KeyboardInterrupt:
            print("\nStopping transaction tracking...")
            break
        except Exception as e:
            print(f"Error in main loop: {str(e)}")
            time.sleep(5)

if __name__ == "__main__":
    main()
