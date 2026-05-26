"""Kiem tra nhanh cac thu vien chinh da cai duoc."""


def test_imports():
    import cv2
    import customtkinter
    import mediapipe
    import numpy
    import pandas
    import PIL
    import sklearn
    import tensorflow

    assert cv2 is not None
    assert customtkinter is not None
    assert mediapipe is not None
    assert numpy is not None
    assert pandas is not None
    assert PIL is not None
    assert sklearn is not None
    assert tensorflow is not None


if __name__ == "__main__":
    test_imports()
    print("All imports are OK")
