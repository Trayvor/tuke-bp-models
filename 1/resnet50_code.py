import os
import json
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers, callbacks
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import kagglehub

IMG_HEIGHT = 256
IMG_WIDTH = 256
BATCH_SIZE = 16
EPOCHS = 100
TRAIN_IMAGE_COUNT = 100000   
DROPOUT_RATE = 0.5
PATIENCE = 3
NUM_CLASSES = 1  

# dataset download
path = kagglehub.dataset_download("xhlulu/140k-real-and-fake-faces")
root_dir = "%s/real_vs_fake/real-vs-fake" % path
train_csv = "%s/train.csv" % path
valid_csv = "%s/valid.csv" % path
test_csv  = "%s/test.csv" % path

df_train = pd.read_csv(train_csv)
df_valid = pd.read_csv(valid_csv)
df_test  = pd.read_csv(test_csv)

if len(df_train) > TRAIN_IMAGE_COUNT:
    df_train = df_train.sample(n=TRAIN_IMAGE_COUNT, random_state=42)

train_datagen = ImageDataGenerator(
    rescale=1./255,
    horizontal_flip=True  # + flip images 
)
valid_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_dataframe(
    dataframe=df_train,
    directory=root_dir,
    x_col="path",
    y_col="label",
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='raw',  
    shuffle=True
)
valid_generator = valid_datagen.flow_from_dataframe(
    dataframe=df_valid,
    directory=root_dir,
    x_col="path",
    y_col="label",
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='raw',
    shuffle=False
)


base_model = tf.keras.applications.ResNet50(
    weights='imagenet', # pretrained on imagenet
    include_top=False,
    input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)
)
base_model.trainable = False  

x = base_model.output
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(DROPOUT_RATE)(x)
outputs = layers.Dense(1, activation='sigmoid')(x)
model = models.Model(inputs=base_model.input, outputs=outputs)

model.compile(
    optimizer=optimizers.Adam(learning_rate=1e-4),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# early stop + checkpoints 
early_stop = callbacks.EarlyStopping(monitor='val_loss', patience=PATIENCE, restore_best_weights=True)
checkpoint = callbacks.ModelCheckpoint('resnet50_model.h5', monitor='val_loss', save_best_only=True)

history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=valid_generator,
    callbacks=[early_stop, checkpoint]
)

# history save
history_dir = './'
if not os.path.exists(history_dir):
    os.makedirs(history_dir)

with open(os.path.join(history_dir, 'resnet50_history.json'), 'w') as f:
    json.dump(history.history, f)
    
model.save('./resnet50_final_model.h5')

# graphs
plt.figure(figsize=(12, 5))

# acc
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('ResNet50 Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

# loss
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('ResNet50 Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
plt.show()
