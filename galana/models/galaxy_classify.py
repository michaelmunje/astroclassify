from keras.models import Model
from keras.models import Sequential
from keras_preprocessing.image import ImageDataGenerator as IDG
from keras.layers import Dense, Activation, Flatten, Dropout, BatchNormalization, Input
from keras.layers import Conv2D, MaxPooling2D
from keras import regularizers, optimizers
import pandas as pd
import numpy as np
import os


test_image_path = os.getcwd() + '/data/kaggle/images_test_rev1/'
test_image_files = os.listdir(test_image_path)
train_image_path = os.getcwd() + '/data/kaggle/images_training_rev1/'
train_image_files = os.listdir(train_image_path)
train_solutions = os.getcwd() + '/data/kaggle/training_solutions_rev1.csv'
test_file = os.getcwd() + '/data/kaggle/all_zeros_benchmark.csv'

df_headers = list()
model = Model()


def read_galaxy_zoo(filepath):
    df = pd.read_csv(filepath, dtype=str)
    df.drop(columns=['Class1.1', 'Class1.2', 'Class2.1', 'Class3.1', 'Class3.2', 'Class4.1',
            'Class4.2', 'Class5.2', 'Class5.3', 'Class5.4', 'Class7.1', 'Class7.2',
            'Class7.3', 'Class8.1', 'Class8.2', 'Class8.3', 'Class8.4', 'Class8.5',
            'Class8.6', 'Class8.7', 'Class9.1', 'Class9.2', 'Class9.3', 'Class10.1',
            'Class10.2', 'Class10.3', 'Class11.1', 'Class11.2', 'Class11.3', 'Class11.4',
            'Class11.5', 'Class11.6'])
    df.rename(index=str, columns={"Class1.3": "Star", "Class2.2": "Spiral", "Class6.1": "Irregular",
                                  "Class6.2": "Elliptical"})
    return df


def append_ext(fn):
    return fn + ".jpg"


def generator_wrapper(generator):
    for batch_x, batch_y in generator:
        yield (batch_x, [batch_y[:, i] for i in range(len(df_headers)-1)])


def construct_model(df_headers):
    # inp = Input(shape=(424,424,3))
    # x = Conv2D(32, (3, 3), padding = 'same')(inp)
    # x = Activation('relu')(x)
    # x = Conv2D(32, (3, 3))(x)
    # x = Activation('relu')(x)
    # x = MaxPooling2D(pool_size = (2, 2))(x)
    # x = Dropout(0.25)(x)
    # x = Conv2D(64, (3, 3), padding = 'same')(x)
    # x = Activation('relu')(x)
    # x = Conv2D(64, (3, 3))(x)
    # x = Activation('relu')(x)
    # x = MaxPooling2D(pool_size = (2, 2))(x)
    # x = Dropout(0.25)(x)
    # x = Flatten()(x)
    # x = Dense(512)(x)
    # x = Activation('relu')(x)
    # x = Dropout(0.5)(x)
    #
    # outputs = []
    # losses = ['binary_crossentropy']*(len(df_headers)-1)
    # for _ in range(len(df_headers)-1):
    #     outputs.append(Dense(1, activation='sigmoid')(x))
    # model = Model(inp, outputs)
    # model.compile(optimizers.rmsprop(lr=0.0001,
    #                                  decay=1e-6),
    #               loss=losses,
    #               metrics=["accuracy"])
    #
    # return model

    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=[424, 424, 3]),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(32, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Flatten(),
        Dense(64, activation='relu'),
        Dropout(0.5),
        Dense(37, activation='softmax')
    ])

    model.compile(loss='categorical_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])
    
    return model


def train_model():

    traindf = read_galaxy_zoo(train_solutions)
    testdf = read_galaxy_zoo(test_file)

    traindf["GalaxyID"] = traindf["GalaxyID"].apply(append_ext)
    testdf["GalaxyID"] = testdf["GalaxyID"].apply(append_ext)
    df_headers = list(traindf.columns)
    test_headers = list(testdf.columns)

    datagen = IDG(rescale=1./255., validation_split=0.25)
    test_datagen = IDG(rescale=1./255.)

    # Create generators
    train_generator=datagen.flow_from_dataframe(
        dataframe=traindf,
        directory=train_image_path,
        x_col=df_headers[0],
        y_col=df_headers[1:],
        subset="training",
        batch_size=32,
        seed=42,
        shuffle=True,
        class_mode="other",
        target_size=(424, 424))

    valid_generator=datagen.flow_from_dataframe(
        dataframe=traindf,
        directory=train_image_path,
        x_col=df_headers[0],
        y_col=df_headers[1:],
        subset="validation",
        batch_size=32,
        seed=42,
        shuffle=True,
        class_mode="other",
        target_size=(424, 424))

    test_generator = test_datagen.flow_from_dataframe(
        dataframe=testdf,
        directory=test_image_path,
        x_col=test_headers[0],
        y_col=test_headers[1:],
        batch_size=32,
        seed=42,
        shuffle=False,
        class_mode=None,
        target_size=(424, 424))

    model = construct_model(df_headers)

    # Train the model
    STEP_SIZE_TRAIN = train_generator.n//train_generator.batch_size
    STEP_SIZE_VALID = valid_generator.n//valid_generator.batch_size
    STEP_SIZE_TEST = test_generator.n//test_generator.batch_size
    model.fit_generator(generator=generator_wrapper(train_generator),
                        use_multiprocessing=True,
                        steps_per_epoch=STEP_SIZE_TRAIN,
                        validation_data=generator_wrapper(valid_generator),
                        validation_steps=STEP_SIZE_VALID,
                        epochs=1,
                        verbose=2)

    # Predict Model
    test_generator.reset()
    pred = model.predict_generator(test_generator,
                                  steps=STEP_SIZE_TEST,
                                  verbose=1)


