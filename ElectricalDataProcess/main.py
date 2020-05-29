import tensorflow as tf
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

record_default = [[0.0]] * 338
ds = tf.data.experimental.CsvDataset(['group_output.csv', 'tag_data_output.csv'], record_default, header=True)
ds = ds.map(lambda *items: tf.stack(items[2:]))
dataset  = tf.data.Dataset.zip((ds, ds)).batch(1).repeat()
ts = tf.data.experimental.CsvDataset('validate.csv', record_default, header=True)
ts = ts.map(lambda *items: tf.stack(items[2:]))
testset  = tf.data.Dataset.zip((ts, ts)).batch(1).repeat()

inputsize = 336
hiddensize = 168
outputsize = 336

x = tf.keras.layers.Input(shape=(inputsize,))
h = tf.keras.layers.Dense(hiddensize, activation='relu')(x)
y = tf.keras.layers.Dense(outputsize, activation='sigmoid')(h)

model = tf.keras.Model(inputs=x, outputs=y)
model.compile(optimizer='adam', loss='mse')

histroy = model.fit(dataset,
                    epochs=20,
                    steps_per_epoch=50000,
                    validation_steps=12000,
                    validation_data=testset
)

