from fer import FER
from fer import Video
import matplotlib.pyplot as plt
import hashlib


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
    raw_data = video.analyze(
        detector,
        output="csv",
        save_frames=False,
        save_video=False,
        annotate_frames=False,
    )
    df = video.to_pandas(raw_data)

    return df


def load_video_then_analise(path):
    """

    :param path:
    :return:
    """
    video_file = Video(path)

    captured_emotions = emotions_from_video(video_file)

    return captured_emotions


def test_emotions_extraction():
    test_image_one = plt.imread("./test_images/polska.jpg")

    captured_emotions = emotions_from_image(test_image_one)

    print(captured_emotions)
    plt.imshow(test_image_one)


def test_emotions_video_extraction(path):
    # path = "./test_images/inception_shortened.mp4"
    _path = "././" + path
    print("Przetwarzanie filmu %s", _path)

    test_video = Video(_path)

    captured_emotions = emotions_from_video(test_video)

    print(captured_emotions)
    return captured_emotions


def generate_sha(file):
    sha = hashlib.sha1()
    file.seek(0)
    while True:
        buf = file.read(104857600)
        if not buf:
            break
        sha.update(buf)
    sha1 = sha.hexdigest()
    file.seek(0)

    return sha1


def sha256sum(filename):
    """
    Zwraca hash pliku. Przydatne do cache'owania
    :param filename:
    :return:
    """
    h = hashlib.sha256()
    b = bytearray(128 * 1024)
    mv = memoryview(b)
    with open(filename, "rb", buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()


# test_emotions_video_extraction()
