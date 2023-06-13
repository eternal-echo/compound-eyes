import zmq
import cv2
from wrappers import ImageWrapper

def main():
    video = cv2.VideoCapture(0)

    if not video.isOpened():
        video.open(0)

    context = zmq.Context()
    socket = context.socket(zmq.PUB)

    print("Collecting images from server...")
    socket.connect("tcp://localhost:5555")

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
                image_wrapper.copy_from_cv_image(image)

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
