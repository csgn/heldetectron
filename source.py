import cv2

class Source:
    def __init__(self, source_path):
        try:
            self.cap = cv2.VideoCapture(int(source_path))
        except ValueError:
            self.cap = cv2.VideoCapture(source_path)

        self.status = self.cap.isOpened()
        if not self.status: 
            raise Exception(f"`{source_path}` is not exist or corrupted")

        print("Capture Status: ", self.status)

    def __del__(self):
        if self.status:
            self.cap.release()
    
    def frames(self):
        while True:
            yield self.cap.read()