import zmq
import cv2
import multiprocessing
import time
from datetime import datetime
from wrappers import ImageWrapper
import logging
import json

# 创建日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)

# 图像采集进程
def image_capture_worker(channel_id, camera_id, worker_url, context=None):
    video = cv2.VideoCapture(camera_id)

    if not video.isOpened():
        video.open(camera_id)

    context = context or zmq.Context.instance()

    socket = context.socket(zmq.PUB)

    print("Collecting images from server: {}".format(worker_url))
    socket.connect(worker_url)

    read = True
    num_frames = 0
    topic = "image".encode()

    while read:

        try:
            success, image = video.read()

            if success:
                num_frames += 1

                # initialize new protobuf image
                image_wrapper = ImageWrapper()
                # image_wrapper.copy_from_cv_image(image_gray)
                image_wrapper.copy_from_cv_image(image, channel_id=channel_id, timestamp=datetime.now().timestamp())

                # serial to string, pack into message
                msg = topic+image_wrapper.image_pb.SerializeToString()

                # Send message
                socket.send(msg)

        except KeyboardInterrupt:
            print("Interrupt received, stopping...")
            read = False

    video.release()
    socket.close()

def main():
    multiprocessing.freeze_support()
    # 读取配置文件
    with open('config.json', 'r') as f:
        config = json.load(f)

    # 解析配置信息
    camera_config = config['camera_config']
    server_address = config['server_address']
    server_port = config['server_port']

    context = zmq.Context()
    worker_url = "tcp://{}:{}".format(server_address, server_port)

    # 创建图像读取进程
    processes = []
    for camera_info in camera_config:
        channel_id = camera_info['channel_id']
        camera_id = camera_info['camera_id']
        p = multiprocessing.Process(target=image_capture_worker, args=(channel_id, camera_id, worker_url, context))
        processes.append(p)
        p.start()

    context.term()

if __name__ == "__main__":
    main()
