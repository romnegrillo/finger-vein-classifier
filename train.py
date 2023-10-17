import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2

# Path to your dataset
TRAIN_DIR = "dataset_split/train"
VALIDATION_DIR = "dataset_split/validation"

# Image settings
IMG_SIZE = (224, 224)  # MobileNetV2 default input size
BATCH_SIZE = 32

# Data Augmentation
train_datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    fill_mode="nearest",
)

validation_datagen = ImageDataGenerator(rescale=1.0 / 255)

# Data Loading
train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",  # or 'categorical' if more than 2 classes
)

validation_generator = validation_datagen.flow_from_directory(
    VALIDATION_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",  # or 'categorical' if more than 2 classes
)

# Model: MobileNetV2
base_model = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet",
)

# Freezing base model
base_model.trainable = False

# Adding custom layers
model = tf.keras.Sequential(
    [
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(
            1, activation="sigmoid"
        ),  # or Dense(num_classes, activation='softmax')
    ]
)

# Compile the model
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",  # or 'categorical_crossentropy'
    metrics=["accuracy"],
)

# Training
EPOCHS = 10
history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=validation_generator,
)

# Save the model
model.save("vein_classifier_mobilenetv2.h5")
