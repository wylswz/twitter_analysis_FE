import tensorflow as tf
import numpy as np

bins = [1, 2, 3, 4, 6, 8, 10, 12, 14, 16, 20, 24, 28, 30]

def cnn_model_fn(features, labels, mode, params):
    device_name = "/cpu:0"
    print(tf.test.is_gpu_available)
    print("Session: =======================================")

    if tf.test.is_gpu_available():
        device_name = "/gpu:0"
    with tf.device(device_name):
        input_layer = features["feature_1"]
        input_layer_ = features["feature_2"]


        conv1 = tf.layers.conv2d(
            name="conv1",
            inputs=input_layer,
            filters=32,
            kernel_size=(5, 5),
            padding='same',
            activation=tf.nn.relu,
        )

        conv1_ = tf.layers.conv2d(
            name="conv1",
            inputs=input_layer_,
            filters=32,
            kernel_size=(5, 5),
            padding='same',
            activation=tf.nn.relu,
            reuse=True
        )

        pool1 = tf.layers.max_pooling2d(inputs=conv1,
                                        pool_size=(2, 2),
                                        strides=2,
                                        )
        pool1_ = tf.layers.max_pooling2d(inputs=conv1_,
                                        pool_size=(2, 2),
                                        strides=2,
                                        )

        conv2 = tf.layers.conv2d(
            name="conv2",
            inputs=pool1,
            filters=32,
            kernel_size=(5, 5),
            padding='same',
            activation=tf.nn.relu
        )

        conv2_ = tf.layers.conv2d(
            name="conv2",
            inputs=pool1_,
            filters=32,
            kernel_size=(5, 5),
            padding='same',
            activation=tf.nn.relu,
            reuse=True
        )

        pool2 = tf.layers.max_pooling2d(
            inputs=conv2,
            pool_size=(2, 2),
            strides=2
        )

        pool2_ = tf.layers.max_pooling2d(
            inputs=conv2_,
            pool_size=(2, 2),
            strides=2
        )

        dense = tf.layers.dense(
            name="dense",
            inputs=pool2,
            units=1024,
            activation=tf.nn.relu
        )
        dense_ = tf.layers.dense(
            name="dense",
            inputs=pool2_,
            units=1024,
            activation=tf.nn.relu,
            reuse=True
        )


        dropout = tf.layers.dropout(
            inputs=dense,
            rate=0.4,
            training=mode == tf.estimator.ModeKeys.TRAIN)

        dropout_ = tf.layers.dropout(
            inputs=dense_,
            rate=0.4,
            training=mode == tf.estimator.ModeKeys.TRAIN)
        logits = tf.layers.dense(name="logits", inputs=dropout, units=10)
        logits_ = tf.layers.dense(name="logits", inputs=dropout_, units=10, reuse=True)
        print(input_layer, input_layer_, features)
        loss = (1.0-labels) * 0.5 * tf.square(tf.norm(logits-logits_)) +\
               labels * 0.5 * tf.square(tf.maximum(0.0, 1.0-tf.norm(logits - logits_)))

        optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.0001)
        train_op = optimizer.minimize(
            loss=loss,
            global_step=tf.train.get_global_step())
        return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)



def double_cnn_model_fn(feature, labels, mode):
    pass



if __name__ == '__main__':
    pass