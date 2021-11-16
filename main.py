from fer import FER
from fer import Video
import matplotlib.pyplot as plt


def emotions_from_image(image):
    """
    Zwraca tablicę obiektów zawierającą szczegóły dotyczące każdej wykrytej twarzy

    :param image: np. wynik funkcji plt.imread("./sciezka/do/pliku")
    """
    detector = FER(mtcnn=True)
    emotions = detector.detect_emotions(image)

    return emotions


def emotions_from_video(video):
    """

    :param video: np. wynik funkcji Video(video_filename)
    :return:
    """
    detector = FER(mtcnn=True)
    raw_data = video.analyze(detector, save_frames=False, save_video=False)
    df = video.to_pandas(raw_data)

    return df


def test_emotions_extraction():
    test_image_one = plt.imread("./test_images/polska.jpg")

    captured_emotions = emotions_from_image(test_image_one)

    print(captured_emotions)
    plt.imshow(test_image_one)


def test_emotions_video_extraction():
    path = "./test_images/inception_shortened.mp4"
    print("Przetwarzanie filmu %s", path)

    test_video = Video(path)

    captured_emotions = emotions_from_video(test_video)

    print(captured_emotions)


test_emotions_video_extraction()