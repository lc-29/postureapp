"""
Test nhanh xem các thư viện chính đã cài được chưa.
"""

def test_imports():
    import cv2
    import mediapipe
    import numpy
    import pandas
    import sklearn
    import tensorflow
    import customtkinter
    import PIL

    print("All imports are OK")


if __name__ == "__main__":
    test_imports()
