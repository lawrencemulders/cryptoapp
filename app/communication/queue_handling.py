import queue

# Logic to ensure maximum of 1 item pending to be sent.


class AutoRemoveQueue(queue.Queue):
    def put(self, item, block=True, timeout=None):
        # Check if the queue is full
        while self.full():
            try:
                # Remove an item from the queue
                self.get_nowait()
            except queue.Empty:
                break
        # Add the new item to the queue
        super().put(item, block, timeout)
