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
FINE_EPOCHS = 50
FINE_LEARNING_RATE = 1e-5
PATIENCE = 3
NUM_LAYERS_TO_UNFREEZE = 25 


path = kagglehub.dataset_download("xhlulu/140k-real-and-fake-faces")
root_dir = "%s/real_vs_fake/real-vs-fake" % path
train_csv = "%s/train.csv" % path
valid_csv = "%s/valid.csv" % path
test_csv  = "%s/test.csv" % path

df_train = pd.read_csv(train_csv)
df_valid = pd.read_csv(valid_csv)

train_datagen = ImageDataGenerator(
    rescale=1./255,
    horizontal_flip=True 
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

model = tf.keras.models.load_model('./exp1/efficientnetb0_final_model.h5')
with open('./exp1/efficientnetb0_history.json', 'r') as f:
    history_pre = json.load(f)


for layer in model.layers[-3-NUM_LAYERS_TO_UNFREEZE:-3]:
    layer.trainable = True

model.compile(
    optimizer=optimizers.Adam(learning_rate=FINE_LEARNING_RATE),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

early_stop_fine = callbacks.EarlyStopping(monitor='val_loss', patience=PATIENCE, restore_best_weights=True)
checkpoint_fine = callbacks.ModelCheckpoint('efficientnetb0_finetuned_model.keras', monitor='val_loss', save_best_only=True)

history_fine = model.fit(
    train_generator,
    epochs=FINE_EPOCHS,
    validation_data=valid_generator,
    callbacks=[early_stop_fine, checkpoint_fine]
)

model.save('./exp2/efficientnetb0_finetuned_model.keras')

with open('./efficientnetb0_finetune_history.json', 'w') as f:
    json.dump(history_fine.history, f)



combined_accuracy = history_pre['accuracy'] + history_fine.history['accuracy']
combined_val_accuracy = history_pre['val_accuracy'] + history_fine.history['val_accuracy']
combined_loss = history_pre['loss'] + history_fine.history['loss']
combined_val_loss = history_pre['val_loss'] + history_fine.history['val_loss']


fine_tuning_start_epoch = len(history_pre['accuracy'])

plt.figure(figsize=(12, 5))
plt.suptitle("EfficientNetB0 Combined Training\n(Pre-training + Fine-tuning)", fontsize=16)

plt.subplot(1, 2, 1)
plt.plot(combined_accuracy, label='Train Accuracy')
plt.plot(combined_val_accuracy, label='Validation Accuracy')
plt.axvline(x=fine_tuning_start_epoch, color='red', linestyle='--', label='Fine-tuning Start')
plt.title('Combined Training Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(combined_loss, label='Train Loss')
plt.plot(combined_val_loss, label='Validation Loss')
plt.axvline(x=fine_tuning_start_epoch, color='red', linestyle='--', label='Fine-tuning Start')
plt.title('Combined Training Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
plt.show()
