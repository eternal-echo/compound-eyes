import zmq
import cv2
import time
from datetime import datetime
from wrappers import ImageWrapper
import json

def main():
    # 读取配置文件
    with open('config.json', 'r') as f:
        config = json.load(f)

    # 解析配置信息
    camera_config = config['camera_config']
    server_address = config['server_address']
    server_port = config['server_port']

    video = cv2.VideoCapture(0)

    if not video.isOpened():
        video.open(0)

    context = zmq.Context()
    socket = context.socket(zmq.PUB)

    print("Collecting images from server...")
    socket.connect("tcp://%s:%s" % (server_address, server_port))

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
                image_wrapper.copy_from_cv_image(image, channel_id=1, timestamp=datetime.now().timestamp())

                # serial to string, pack into message
                msg = topic+image_wrapper.image_pb.SerializeToString()

                # Send message
                socket.send(msg)

        except KeyboardInterrupt:
            print("Interrupt received, stopping...")
            read = False

    video.release()
    socket.close()
    context.term()

if __name__ == "__main__":
    main()
