# -*- coding: utf-8 -*-
# %% [markdown]
# # Train ANN phân loại tư thế làm việc từ landmark MediaPipe Pose
#
# **Đề tài:** Xây dựng ứng dụng phát hiện lỗi tư thế làm việc qua webcam sử dụng Computer Vision.
#
# Notebook này huấn luyện mô hình ANN để phân loại:
#
# - `0`: Correct posture / tư thế đúng
# - `1`: Incorrect posture / tư thế sai
#
# Dữ liệu đầu vào là file `posture_data.csv`, gồm:
#
# - 99 cột đặc trưng landmark: `33 landmark x 3 tọa độ x, y, z`
# - 1 cột nhãn: `label`
#
# **Lưu ý:** Notebook này không sử dụng CNN, YOLO, ảnh gốc, hoặc mô hình pre-trained classification. Mô hình chỉ học từ vector landmark 99 chiều.

# %% [markdown]
# ## PHẦN 1: Import thư viện
#
# Import các thư viện cần thiết cho xử lý dữ liệu, chia tập dữ liệu, chuẩn hóa, huấn luyện ANN, đánh giá và lưu mô hình.

# %%
import os
import io
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)
from sklearn.utils.class_weight import compute_class_weight

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

# Thiết lập seed để kết quả ổn định hơn giữa các lần chạy.
SEED = 42
np.random.seed(SEED)
tf.random.set_seed(SEED)

print("TensorFlow version:", tf.__version__)

# %% [markdown]
# ## PHẦN 2: Load dataset
#
# Trên Kaggle, dataset thường nằm trong thư mục `/kaggle/input/...`. Cell dưới đây tự động tìm file `posture_data.csv` bằng `os.walk`.
#
# Nếu không tìm thấy file, notebook sẽ báo lỗi rõ ràng để người dùng kiểm tra lại phần Add Data của Kaggle Notebook.

# %%
DATASET_FILENAME = "posture_data.csv"
KAGGLE_INPUT_DIR = "/kaggle/input"

csv_path = None

for root, dirs, files in os.walk(KAGGLE_INPUT_DIR):
    if DATASET_FILENAME in files:
        csv_path = os.path.join(root, DATASET_FILENAME)
        break

if csv_path is None:
    raise FileNotFoundError(
        f"Không tìm thấy file {DATASET_FILENAME} trong {KAGGLE_INPUT_DIR}. "
        "Hãy kiểm tra lại bạn đã Add Data vào Kaggle Notebook chưa."
    )

print("CSV path:", csv_path)

df = pd.read_csv(csv_path)

print("Dataset shape:", df.shape)
display(df.head())

print("\nThông tin dataframe:")
df.info()

missing_values = df.isnull().sum()
total_missing = int(missing_values.sum())
print("\nTổng số missing values:", total_missing)

if total_missing > 0:
    print("\nCác cột có missing values:")
    print(missing_values[missing_values > 0])
else:
    print("Không có missing values.")

print("\nLabel distribution:")
print(df["label"].value_counts().sort_index() if "label" in df.columns else "Không tìm thấy cột label")

# %% [markdown]
# ## PHẦN 3: Kiểm tra dữ liệu
#
# Ở bước này ta kiểm tra:
#
# - Dataset có cột `label` hay không.
# - Số lượng feature có đúng bằng 99 hay không.
# - Nhãn chỉ gồm hai giá trị `0` và `1`.
# - Nếu có missing values thì loại bỏ các dòng bị thiếu.
#
# Sau đó tách dữ liệu thành:
#
# - `X`: ma trận đặc trưng landmark
# - `y`: vector nhãn

# %%
if "label" not in df.columns:
    raise ValueError("Dataset phải có cột 'label'.")

num_features = df.drop("label", axis=1).shape[1]
if num_features != 99:
    raise ValueError(f"Số feature không đúng. Kỳ vọng 99 feature, nhưng nhận được {num_features}.")

unique_labels = sorted(df["label"].dropna().unique().tolist())
if set(unique_labels) != {0, 1}:
    raise ValueError(f"Label chỉ được gồm 0 và 1. Giá trị hiện có: {unique_labels}")

rows_before = len(df)

if df.isnull().sum().sum() > 0:
    df = df.dropna().reset_index(drop=True)
    rows_after = len(df)
    print(f"Đã loại bỏ {rows_before - rows_after} dòng có missing values.")
else:
    print("Không cần xử lý missing values.")

X = df.drop("label", axis=1).astype(np.float32)
y = df["label"].astype(int)

print("X shape:", X.shape)
print("y shape:", y.shape)
print("Số feature:", X.shape[1])

print("\nPhân bố label theo phần trăm:")
print((y.value_counts(normalize=True).sort_index() * 100).round(2).astype(str) + "%")

# %% [markdown]
# ## PHẦN 4: Chia train/validation/test
#
# Dataset được chia thành:
#
# - Train: 70%
# - Validation: 15%
# - Test: 15%
#
# Sử dụng `stratify` để giữ tỷ lệ nhãn tương đối giống nhau giữa các tập. Điều này quan trọng vì dữ liệu hiện có sự lệch nhẹ giữa lớp đúng và sai.

# %%
X_train_temp, X_test, y_train_temp, y_test = train_test_split(
    X,
    y,
    test_size=0.15,
    random_state=SEED,
    stratify=y
)

validation_size = 0.15 / 0.85

X_train, X_val, y_train, y_val = train_test_split(
    X_train_temp,
    y_train_temp,
    test_size=validation_size,
    random_state=SEED,
    stratify=y_train_temp
)

print("X_train shape:", X_train.shape)
print("X_val shape:", X_val.shape)
print("X_test shape:", X_test.shape)

def print_label_distribution(name, labels):
    counts = labels.value_counts().sort_index()
    percentages = (labels.value_counts(normalize=True).sort_index() * 100).round(2)
    print(f"\n{name} label distribution:")
    for label in counts.index:
        print(f"Label {label}: {counts[label]} mẫu ({percentages[label]}%)")

print_label_distribution("Train", y_train)
print_label_distribution("Validation", y_val)
print_label_distribution("Test", y_test)

# %% [markdown]
# ## PHẦN 5: Chuẩn hóa dữ liệu bằng StandardScaler
#
# Dữ liệu landmark được chuẩn hóa bằng `StandardScaler`.
#
# **Nguyên tắc quan trọng:** chỉ `fit` scaler trên tập train, sau đó dùng scaler đó để `transform` validation và test. Cách này tránh data leakage, tức tránh việc thông tin từ validation/test bị đưa vào quá trình huấn luyện.

# %%
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

print("Mean của X_train_scaled:", np.mean(X_train_scaled).round(6))
print("Std của X_train_scaled:", np.std(X_train_scaled).round(6))

print("\nShape sau scaling:")
print("X_train_scaled:", X_train_scaled.shape)
print("X_val_scaled:", X_val_scaled.shape)
print("X_test_scaled:", X_test_scaled.shape)

# %% [markdown]
# ## PHẦN 6: Xây dựng ANN model
#
# Mô hình ANN được sử dụng để phân loại tư thế làm việc dựa trên vector đặc trưng landmark được trích xuất từ MediaPipe Pose. Mỗi mẫu dữ liệu gồm 99 đặc trưng tương ứng với tọa độ x, y, z của 33 điểm mốc cơ thể. Dữ liệu được chuẩn hóa bằng StandardScaler trước khi đưa vào mô hình nhằm giúp quá trình huấn luyện ổn định hơn. Mô hình sử dụng hàm sigmoid ở lớp đầu ra để dự đoán xác suất tư thế sai.
#
# Kiến trúc được giữ ở mức vừa phải vì dataset hiện có khoảng hơn 5 nghìn mẫu. Các lớp `Dropout` và `BatchNormalization` giúp mô hình ổn định hơn và giảm overfitting.

# %%
input_dim = X_train_scaled.shape[1]

model = Sequential([
    # Lớp ẩn đầu tiên học các quan hệ phi tuyến từ 99 đặc trưng landmark.
    Dense(128, activation="relu", input_shape=(input_dim,)),
    BatchNormalization(),
    Dropout(0.3),

    # Lớp ẩn thứ hai tiếp tục rút trích biểu diễn ở mức nhỏ hơn.
    Dense(64, activation="relu"),
    BatchNormalization(),
    Dropout(0.25),

    # Lớp ẩn cuối giúp gom thông tin trước khi phân loại nhị phân.
    Dense(32, activation="relu"),
    Dropout(0.2),

    # Output sigmoid trả về xác suất mẫu thuộc lớp 1: incorrect posture.
    Dense(1, activation="sigmoid")
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# %% [markdown]
# ## PHẦN 7: Callback khi train
#
# Sử dụng ba callback:
#
# - `EarlyStopping`: dừng sớm khi validation loss không cải thiện.
# - `ModelCheckpoint`: lưu model tốt nhất theo `val_loss`.
# - `ReduceLROnPlateau`: giảm learning rate khi mô hình bị chững.

# %%
OUTPUT_DIR = "/kaggle/working"
os.makedirs(OUTPUT_DIR, exist_ok=True)

best_model_path = os.path.join(OUTPUT_DIR, "ann_best.keras")

callbacks = [
    EarlyStopping(
        monitor="val_loss",
        patience=15,
        restore_best_weights=True
    ),
    ModelCheckpoint(
        filepath=best_model_path,
        monitor="val_loss",
        save_best_only=True,
        mode="min",
        verbose=1
    ),
    ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=5,
        min_lr=1e-6,
        verbose=1
    )
]

print("Best model path:", best_model_path)

# %% [markdown]
# ## PHẦN 8: Xử lý lệch lớp nếu cần
#
# Dataset hiện tại hơi lệch lớp:
#
# - Correct posture ít hơn
# - Incorrect posture nhiều hơn
#
# Mức lệch này không quá nặng, nhưng `class_weight` giúp mô hình không bị thiên lệch quá nhiều về lớp có số mẫu lớn hơn.

# %%
classes = np.array([0, 1])

class_weights = compute_class_weight(
    class_weight="balanced",
    classes=classes,
    y=y_train
)

class_weight_dict = {
    int(label): float(weight)
    for label, weight in zip(classes, class_weights)
}

print("Class weight:")
print(class_weight_dict)

# %% [markdown]
# ## PHẦN 9: Train model
#
# Huấn luyện mô hình ANN với:
#
# - `EPOCHS = 100`
# - `BATCH_SIZE = 32`
# - Có sử dụng validation set
# - Có truyền `class_weight`

# %%
EPOCHS = 100
BATCH_SIZE = 32

history = model.fit(
    X_train_scaled,
    y_train,
    validation_data=(X_val_scaled, y_val),
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    callbacks=callbacks,
    class_weight=class_weight_dict,
    verbose=1
)

# %% [markdown]
# ## PHẦN 10: Vẽ biểu đồ training
#
# Vẽ hai biểu đồ:
#
# - Training Loss và Validation Loss
# - Training Accuracy và Validation Accuracy
#
# Các biểu đồ này giúp quan sát hiện tượng overfitting hoặc underfitting.

# %%
plt.figure(figsize=(8, 5))
plt.plot(history.history["loss"], label="Training Loss")
plt.plot(history.history["val_loss"], label="Validation Loss")
plt.title("Training Loss và Validation Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# %%
plt.figure(figsize=(8, 5))
plt.plot(history.history["accuracy"], label="Training Accuracy")
plt.plot(history.history["val_accuracy"], label="Validation Accuracy")
plt.title("Training Accuracy và Validation Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# %% [markdown]
# ## PHẦN 11: Đánh giá trên tập test
#
# Tập test chỉ được sử dụng sau khi huấn luyện xong để đánh giá khách quan.
#
# Với bài toán này:
#
# - Positive class = `1` = incorrect posture / tư thế sai
# - Recall của lớp incorrect rất quan trọng vì hệ thống cần phát hiện được các trường hợp ngồi sai.
#
# Confusion matrix có dạng:
#
# ```text
# [[TN, FP],
#  [FN, TP]]
# ```
#
# Trong đó:
#
# - `TN`: tư thế đúng, model dự đoán đúng
# - `FP`: tư thế đúng nhưng model báo sai
# - `FN`: tư thế sai nhưng model báo đúng
# - `TP`: tư thế sai và model báo sai

# %%
if os.path.exists(best_model_path):
    model = tf.keras.models.load_model(best_model_path)
    print("Đã load best model từ:", best_model_path)
else:
    print("Không tìm thấy best model checkpoint. Sử dụng model hiện tại.")

y_prob = model.predict(X_test_scaled)
y_pred = (y_prob >= 0.5).astype(int).ravel()

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, pos_label=1, zero_division=0)
recall = recall_score(y_test, y_pred, pos_label=1, zero_division=0)
f1 = f1_score(y_test, y_pred, pos_label=1, zero_division=0)
cm = confusion_matrix(y_test, y_pred, labels=[0, 1])

report = classification_report(
    y_test,
    y_pred,
    labels=[0, 1],
    target_names=["0 - Correct", "1 - Incorrect"],
    zero_division=0
)

print("Test Accuracy:", round(accuracy, 4))
print("Test Precision:", round(precision, 4))
print("Test Recall:", round(recall, 4))
print("Test F1-score:", round(f1, 4))

print("\nConfusion matrix [[TN, FP], [FN, TP]]:")
print(cm)

print("\nClassification report:")
print(report)

# %% [markdown]
# ## PHẦN 12: Vẽ confusion matrix
#
# Confusion matrix được vẽ bằng `matplotlib`, không dùng seaborn.

# %%
fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(cm, cmap="Blues")

class_names = ["0 - Correct", "1 - Incorrect"]

ax.set_xticks(np.arange(len(class_names)))
ax.set_yticks(np.arange(len(class_names)))
ax.set_xticklabels(class_names)
ax.set_yticklabels(class_names)

ax.set_xlabel("Predicted label")
ax.set_ylabel("True label")
ax.set_title("Confusion Matrix")

for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        text_color = "white" if cm[i, j] > cm.max() / 2 else "black"
        ax.text(j, i, cm[i, j], ha="center", va="center", color=text_color, fontsize=12)

fig.colorbar(im)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## PHẦN 13: Kiểm tra một vài mẫu dự đoán
#
# In thử 10 mẫu đầu tiên trong tập test để quan sát:
#
# - Nhãn thật
# - Nhãn dự đoán
# - Xác suất model cho lớp `incorrect posture`

# %%
num_samples_to_show = min(10, len(y_test))

for i in range(num_samples_to_show):
    true_label = int(y_test.iloc[i]) if hasattr(y_test, "iloc") else int(y_test[i])
    pred_label = int(y_pred[i])
    prob_incorrect = float(y_prob[i][0])
    print(
        f"Sample {i + 1} | "
        f"True: {true_label} | "
        f"Pred: {pred_label} | "
        f"P(incorrect): {prob_incorrect:.4f}"
    )

# %% [markdown]
# ## PHẦN 14: Lưu model, scaler và kết quả đánh giá
#
# Sau khi huấn luyện, notebook lưu các artifact cần thiết:
#
# - `/kaggle/working/ann_best.keras`
# - `/kaggle/working/scaler.pkl`
# - `/kaggle/working/metrics.txt`
# - `/kaggle/working/classification_report.txt`
# - `/kaggle/working/confusion_matrix.csv`
#
# Khi triển khai local app, cần dùng cùng scaler đã fit trên train set để chuẩn hóa dữ liệu realtime trước khi đưa vào ANN.

# %%
scaler_path = os.path.join(OUTPUT_DIR, "scaler.pkl")
metrics_path = os.path.join(OUTPUT_DIR, "metrics.txt")
report_path = os.path.join(OUTPUT_DIR, "classification_report.txt")
cm_path = os.path.join(OUTPUT_DIR, "confusion_matrix.csv")

# Đảm bảo model tốt nhất tồn tại. Nếu checkpoint chưa tạo vì lý do nào đó, lưu model hiện tại.
if not os.path.exists(best_model_path):
    model.save(best_model_path)

joblib.dump(scaler, scaler_path)

cm_df = pd.DataFrame(
    cm,
    index=["true_0_correct", "true_1_incorrect"],
    columns=["pred_0_correct", "pred_1_incorrect"]
)
cm_df.to_csv(cm_path)

with open(report_path, "w", encoding="utf-8") as f:
    f.write(report)

summary_buffer = io.StringIO()
model.summary(print_fn=lambda line: summary_buffer.write(line + "\n"))
model_summary_text = summary_buffer.getvalue()

metrics_text = f"""
Posture Detection ANN Metrics
=============================

Dataset path: {csv_path}
Dataset shape: {df.shape}

Train shape: {X_train.shape}
Validation shape: {X_val.shape}
Test shape: {X_test.shape}

Class distribution:
{df["label"].value_counts().sort_index().to_string()}

Class weight:
{class_weight_dict}

Test Accuracy: {accuracy:.6f}
Test Precision: {precision:.6f}
Test Recall: {recall:.6f}
Test F1-score: {f1:.6f}

Confusion matrix [[TN, FP], [FN, TP]]:
{cm}

Classification report:
{report}

Model architecture summary:
{model_summary_text}
"""

with open(metrics_path, "w", encoding="utf-8") as f:
    f.write(metrics_text)

print("Đã lưu model:", best_model_path)
print("Đã lưu scaler:", scaler_path)
print("Đã lưu metrics:", metrics_path)
print("Đã lưu classification report:", report_path)
print("Đã lưu confusion matrix:", cm_path)

# %% [markdown]
# ## PHẦN 15: Hướng dẫn tải file về
#
# Sau khi train xong trên Kaggle, vào phần Output của notebook và tải các file sau:
#
# - `ann_best.keras`
# - `scaler.pkl`
# - `metrics.txt`
# - `classification_report.txt`
# - `confusion_matrix.csv`
#
# Để chạy trong project local, hai file quan trọng nhất cần copy về là:
#
# - `ann_best.keras` → `models/ann_best.keras`
# - `scaler.pkl` → `models/scaler.pkl`
#
# Trong app realtime, pipeline dự đoán nên là:
#
# `Webcam frame -> MediaPipe Pose -> 99 landmark features -> scaler.transform -> ANN model -> xác suất tư thế sai -> cảnh báo`

# %%
output_files = [
    "ann_best.keras",
    "scaler.pkl",
    "metrics.txt",
    "classification_report.txt",
    "confusion_matrix.csv"
]

print("Các file output đã tạo trong /kaggle/working:")
for filename in output_files:
    path = os.path.join(OUTPUT_DIR, filename)
    print(f"- {path} | exists: {os.path.exists(path)}")

print("\nSau khi train xong, hãy tải về:")
print("- /kaggle/working/ann_best.keras -> models/ann_best.keras")
print("- /kaggle/working/scaler.pkl -> models/scaler.pkl")
