import zmq
import cv2
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

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.bind("tcp://*:{}".format(server_port))

    g_run = True
    num_frames = 0
    topic = "image"
    len_topic = len(topic.encode())
    socket.setsockopt_string(zmq.SUBSCRIBE, topic)

    image_wrapper = ImageWrapper()

    while g_run:

        try:
            data = socket.recv()
            image_bytes = data[len_topic:]

            image_wrapper.image_pb.ParseFromString(image_bytes)

            success, image = image_wrapper.get_open_cv_image()
            if success:
                # 显示时间戳
                cv2.putText(image, str(image_wrapper.image_pb.timestamp), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(image, str(image_wrapper.image_pb.channel_id), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow("display", image)
                key = cv2.waitKey(1)
                if key == 'q':
                    g_run = False

        except KeyboardInterrupt:
            print("Interrupt received, stopping...")
            g_run = False

    socket.close()
    context.term()


if __name__ == "__main__":
    main()
