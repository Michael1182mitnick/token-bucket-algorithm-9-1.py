# Token_Bucket_Algorithm
# Implement a rate limiter that limits the number of API requests a user can make within a specified time window. Use different algorithms like the Token Bucket or Leaky Bucket.
# The bucket holds tokens that are added at a constant rate (tokens per second).
# Each request consumes one token.
# If the bucket contains tokens, the request is allowed; otherwise, it is denied.

import time
from threading import Lock


class TokenBucket:
    def __init__(self, rate, capacity):
        """
        Initialize the token bucket.

        :param rate: Tokens are added to the bucket per second.
        :param capacity: The maximum number of tokens the bucket can hold.
        """
        self.rate = rate  # Rate at which tokens are added (tokens per second)
        self.capacity = capacity  # Maximum tokens in the bucket
        self.tokens = capacity  # Start with a full bucket
        self.last_checked = time.time()  # Last time tokens were updated
        self.lock = Lock()  # To handle concurrency

    def allow_request(self):
        """
        Returns True if the request is allowed, otherwise False.
        """
        with self.lock:
            current_time = time.time()
            elapsed_time = current_time - self.last_checked

            # Add tokens based on the time elapsed
            self.tokens += elapsed_time * self.rate
            # Cap at the bucket capacity
            self.tokens = min(self.tokens, self.capacity)
            self.last_checked = current_time

            if self.tokens >= 1:
                self.tokens -= 1
                return True
            else:
                return False


# Example Usage
if __name__ == "__main__":
    rate_limiter = TokenBucket(rate=1, capacity=5)  # 1 token/sec, max 5 tokens

    for _ in range(10):
        if rate_limiter.allow_request():
            print("Request allowed")
        else:
            print("Request denied")
        time.sleep(0.5)
