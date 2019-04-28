import os
import pathlib as pl


class ModelPaths:  # Quick hack to make struct-like objects in python
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


def initialize_default_paths():
    model_paths = ModelPaths()
    model_paths.test_image_path = os.getcwd() + '/data/kaggle/images_test_rev1/'
    model_paths.train_image_path = os.getcwd() + '/data/kaggle/images_training_rev1/'

    if os.path.isfile(model_paths.test_image_path):
        model_paths.test_image_files = os.listdir(model_paths.test_image_path)
    else:
        model_paths.test_image_files = []

    if os.path.isfile(model_paths.train_image_path):
        model_paths.train_image_files = os.listdir(model_paths.train_image_path)
    else:
        model_paths.train_image_files = []

    model_paths.train_solutions = os.getcwd() + '/data/kaggle/solutions/training_solutions_rev1.csv'
    model_paths.clean_train_solutions = os.getcwd() + '/data/kaggle/solutions/clean_solutions.csv'
    model_paths.augmented_solutions = os.getcwd() + '/data/kaggle/solutions/augmented_solutions.csv'

    model_paths.test_file = os.getcwd() + '/data/kaggle/all_zeros_benchmark.csv'

    model_paths.output_model_file = os.getcwd() + '/data/kaggle/models/galaxy_classifier_model.json'
    model_paths.output_model_weights = os.getcwd() + '/data/kaggle/models/galaxy_classifier_weights.h5'

    model_paths.checkpoint_outer_path = os.getcwd() + "/data/kaggle/models/best_outer_model.hdf5"
    model_paths.checkpoint_overall_path = os.getcwd() + "/data/kaggle/models/best_overall_model.hdf5"

    model_paths.valid_true = os.getcwd() + "/data/kaggle/valid_true.csv"
    model_paths.valid_preds = os.getcwd() + "/data/kaggle/valid_preds.csv"

    pl.Path(model_paths.test_image_path).mkdir(parents=True, exist_ok=True)
    pl.Path(model_paths.train_image_path).mkdir(parents=True, exist_ok=True)
    pl.Path(os.getcwd() + '/data/kaggle/models/').mkdir(parents=True, exist_ok=True)
    pl.Path(os.getcwd() + '/data/kaggle/solutions/').mkdir(parents=True, exist_ok=True)

    return model_paths


def initialize_custom_paths(test_images_p, train_images_p, train_sol, clean_sols, augmented_sols,
                            test_f, output_model_f, output_model_w, checkpoint_p_outer, checkpoint_p_overall, val_true, val_preds):
    model_paths = ModelPaths()
    model_paths.test_image_path = test_images_p
    model_paths.train_image_path = train_images_p

    if os.path.isfile(model_paths.test_image_path):
        model_paths.test_image_files = os.listdir(model_paths.test_image_path)
    else:
        model_paths.test_image_files = []

    if os.path.isfile(model_paths.train_image_path):
        model_paths.train_image_files = os.listdir(model_paths.train_image_path)
    else:
        model_paths.train_image_files = []

    model_paths.train_solutions = train_sol
    model_paths.clean_train_solutions = clean_sols
    model_paths.augmented_solutions = augmented_sols
    model_paths.test_file = test_f
    model_paths.output_model_file = output_model_f
    model_paths.output_model_weights = output_model_w
    model_paths.checkpoint_outer_path = checkpoint_p_outer
    model_paths.checkpoint_overall_path = checkpoint_p_overall
    model_paths.valid_true = val_true
    model_paths.valid_preds = val_preds
    return model_paths
