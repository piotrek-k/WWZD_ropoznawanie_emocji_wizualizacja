from fer import FER
import matplotlib.pyplot as plt


def emotions_from_image(image):
    """
    Zwraca tablicę obiektów zawierającą szczegóły dotyczące każdej wykrytej twarzy

    :param image: np. wynik funkcji plt.imread("./sciezka/do/pliku")
    """
    detector = FER(mtcnn=True)
    emotions = emo_detector.detect_emotions(image)

    return emotions


def test_emotions_extraction():
    test_image_one = plt.imread("./test_images/polska.jpg")
    print(captured_emotions)
    plt.imshow(test_image_one)
