import cv2
import numpy as np
from PIL import Image
import onnxruntime as ort
import torchvision.transforms as transforms

ort_session = ort.InferenceSession("captcha_crnn.onnx")

CHAR_SET = "2346789ACDEFGHJKLNPQRTUVXYZ"
char_to_idx = {char: idx for idx, char in enumerate(CHAR_SET)}
idx_to_char = {idx: char for char, idx in char_to_idx.items()}

transform = transforms.Compose(
    [
        transforms.Grayscale(),
        transforms.ToTensor(),
    ]
)


def clean_image(image: cv2.typing.MatLike, show_steps=False):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    opened = cv2.morphologyEx(
        blurred, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
    )
    eroded = cv2.erode(
        opened, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1
    )
    dilated = cv2.dilate(
        eroded, cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2)), iterations=1
    )
    closed = cv2.morphologyEx(
        dilated,
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1)),
        iterations=2,
    )
    blurred = cv2.GaussianBlur(closed, (5, 5), 0)
    opened = cv2.morphologyEx(
        blurred, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    )
    _, binary = cv2.threshold(opened, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    mask_for_large_objects = np.zeros_like(gray)
    for contour in contours:
        if len(contour) > 0:
            area = cv2.contourArea(contour)
            if np.isscalar(area) and area >= 100:
                cv2.drawContours(mask_for_large_objects, [contour], -1, 255, cv2.FILLED)
    cleaned_binary = cv2.bitwise_and(binary, binary, mask=mask_for_large_objects)
    if show_steps:
        cv2.imshow("Original", image)
        cv2.imshow("Binary", cleaned_binary)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return binary


def ocr_captcha_onnx(img_mat):
    cleaned_img = clean_image(img_mat)
    cleaned_img = cv2.cvtColor(cleaned_img, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(cleaned_img).convert("RGB")
    input_tensor = transform(image).unsqueeze(0)

    input_numpy = input_tensor.numpy().astype(np.float32)

    outputs = ort_session.run(None, {"input": input_numpy})

    predicted_indices = np.argmax(outputs[0], axis=2).squeeze(0)
    predicted_string = "".join([idx_to_char[idx] for idx in predicted_indices])

    return predicted_string
