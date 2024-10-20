import queue


class AutoRemoveQueue(queue.Queue):
    def put(self, item, block=True, timeout=None):
        while self.full():
            try:
                # Remove old items
                self.get_nowait()
            except queue.Empty:
                break

        # Add the new item to the queue
        super().put(item, block, timeout)
