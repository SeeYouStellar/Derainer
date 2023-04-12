import cv2
# import _thread as thread
import time
import threading

mutex = threading.Lock()
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
def opencap():
    print("thread1 is begin")
    while True:
        mutex.acquire()
        if cap.isOpened():
            ret, frame = cap.read()
            print("cap is opening")
        else:
            break
        mutex.release()
        time.sleep(1)

def closecap():
    print("thread2 is begin")
    time.sleep(5)
    mutex.acquire()
    if cap.isOpened():
        cap.release()
        cv2.destroyAllWindows()
        print("cap is close")
    mutex.release()
if __name__ == "__main__":
    t1 = threading.Thread(target=opencap)
    t2 = threading.Thread(target=closecap)
    t1.start()
    t2.start()

    t1.join()
    t2.join()
