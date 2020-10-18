import tensorflow.compat.v1 as tf
import cv2 as cv2
import numpy as np

INPUT_TENSOR_NAME = 'input.1:0'
OUTPUT_TENSOR_NAME = 'add_4:0'
IMAGE_PATH = "images/parnas3.jpg"
PB_PATH = "./saved_model.pb"

img = cv2.imread(IMAGE_PATH)
img = np.dot(img[..., :3], [0.299, 0.587, 0.114])
img = cv2.resize(img, dsize=(28, 28), interpolation=cv2.INTER_AREA)
img.resize((1, 1, 28, 28))
def openGraph(path):
    graph = tf.Graph()
    graphDef = tf.GraphDef()
    with open(path, "rb") as graphFile:
        graphDef.ParseFromString(graphFile.read())

        with graph.as_default():
            tf.import_graph_def(graphDef)

    return graph


graph_def = openGraph(PB_PATH)
# with tf.gfile.FastGFile(PB_PATH, 'rb') as f:
#     graph_def = tf.GraphDef()
#     graph_def.ParseFromString(f.read())

with tf.Graph().as_default() as graph:
    tf.import_graph_def(graph_def, name="")

input_tensor = graph.get_tensor_by_name(INPUT_TENSOR_NAME)
output_tensor = graph.get_tensor_by_name(OUTPUT_TENSOR_NAME)

with tf.Session(graph=graph) as sess:
    output_vals = sess.run(output_tensor, feed_dict={input_tensor: img})  #

prediction = int(np.argmax(np.array(output_vals).squeeze(), axis=0))
print(prediction)