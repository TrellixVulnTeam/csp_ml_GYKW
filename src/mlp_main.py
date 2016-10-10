from src.tools.dataset_helper import DatasetHelper, DatasetLoader
from src.tools import xml_tools
from src.tools.perftools import *
from src.ml import mlp
import os
from src.tools.simulator_data_parser import DatParser


def __self_test():
    mlperc = mlp.MultilayerPerceptron(494, 2, 64, 16)

    # training_set, training_labels, test_set, test_labels = DatasetLoader.load_archives(
    #     "res/datasets/set_5/healthy_training.tar.gz",
    #     "res/datasets/set_5/healthy_test.tar.gz",
    #     "res/datasets/set_5/stroke_training.tar.gz",
    #     "res/datasets/set_5/stroke_test.tar.gz")

    # mlperc.train(training_set, training_labels, 400)
    # mlperc.save("res/saved_nns/symmetry_64_16_2_multi_slice_4_and_5.dat")
    #
    #       symmetry_64_16.dat                      ###   97% accuracy, 1.125% false alarm, trained on set_4
    #       symmetry_64_16_multi_slice.dat          ###   98% accuracy, 0 false alarm,      trained on set_5
    #       symmetry_64_16_multi_slice_4_and_5.dat  ###   trained on (set 4 and 5)

    mlperc.load("res/saved_nns/symmetry_64_16_multi_slice_4_and_5.dat")

    print("evaluating...")

    stroke_test_set = DatasetHelper.load_archive("res/datasets/set_3/stroke_test.tar.gz", 1)
    healthy_test_set = DatasetHelper.load_archive("res/datasets/set_3/healthy_test.tar.gz", 1)
    # stroke_test_set = DatasetHelper.load_data("res/datasets/set_2/stroke/test", 1)
    # healthy_test_set = DatasetHelper.load_data("res/datasets/set_2/healthy/test", 1)

    test_mlp(mlperc, healthy_test_set, stroke_test_set)


def train_new(root, name, healthy_training, stroke_training, epochs, symmetry, *hidden_layers):
    training_set, training_labels = DatasetLoader.load_archives_training(
        healthy_training, stroke_training, symmetry)
    input_layer_size = training_set.shape[1]
    mlperc = mlp.MultilayerPerceptron(input_layer_size, 2, *hidden_layers)

    mlperc.train(training_set, training_labels, epochs)
    try:
        os.mkdir("{}userspace/saved_nns/{}/".format(root, name))
    except FileExistsError:
        print("Folder already exists")
    xml_tools.create_topology_xml(root, name, symmetry, [input_layer_size, 2], *hidden_layers)
    mlperc.save("{}userspace/saved_nns/{}/{}.dat".format(root, name, name))


# TODO Guarda simmetria e implementa
def test_existing(root, name, healthy_test, stroke_test):
    dir = "static/"
    files = os.listdir(dir)

    for file in files:
        if file.endswith(".png"):
            os.remove(os.path.join(dir, file))

    mlperc = mlp.MultilayerPerceptron.load_folder("{}userspace/saved_nns/{}".format(root, name))

    stroke_test_set = DatasetHelper.load_archive(stroke_test, mlperc.uses_symmetry_features())
    healthy_test_set = DatasetHelper.load_archive(healthy_test, mlperc.uses_symmetry_features())
    mlperc.destroy()

    return test_mlp(mlperc, healthy_test_set, stroke_test_set)




def classify(nn_filepath, sample_filepath):
    mlperc = mlp.MultilayerPerceptron.load_folder(nn_filepath)
    symmetry = mlperc.uses_symmetry_features()
    sample = DatParser.parse_file(sample_filepath, symmetry)
    out = mlperc.classify(sample, 1)
    mlperc.destroy()
    return out

# __self_test()

# train_new("test", [494, 2], [64, 16, 2],
#           "res/datasets/set_5/healthy_training.tar.gz",
#           "res/datasets/set_5/healthy_test.tar.gz",
#           "res/datasets/set_5/stroke_training.tar.gz",
#           "res/datasets/set_5/stroke_test.tar.gz",
#           2
#           )

# mlp.MultilayerPerceptron.load_folder("userspace/saved_nns/test")
