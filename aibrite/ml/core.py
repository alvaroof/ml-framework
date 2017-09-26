import numpy as np
from collections import namedtuple


Prediction = namedtuple("Prediction", ["predicted", 'probabilities'])

ScoreReport = namedtuple("ScoreReport", ["labels",
                                         "confusion_matrix", "accuracy", "precision", "recall", "f1", "support", "totals"])


class MlBase:

    def zscore(np_arr):
        avgs = np.sum(np_arr, axis=0, keepdims=True) / np_arr.shape[0]
        return (np_arr - avgs) / np.std(np_arr, axis=0, keepdims=True)

    def hyperbolic_tangent(z):
        return np.tanh(z)

    def relu(data, epsilon=0.1):
        return np.maximum(epsilon * data, data)

    def relu_d(data, epsilon=0.1):
        gradients = 1. * (data > 0)
        gradients[gradients == 0] = epsilon
        return gradients

    def hyperbolic_tangent_d(z):
        return (1 - np.power(z, 2))

    def sigmoid(z):
        """sigmoid"""
        return 1. / (1 + np.exp(-z))

    def sigmoid_d(z):
        return a * (1. - a)

    def softmax(x):
        """Compute softmax values for each sets of scores in x."""
        return np.exp(x) / np.sum(np.exp(x), axis=0)

    def split(arr, *ratios):
        sizes = (np.array(ratios) * len(arr))
        sizes = np.round(sizes).astype(int)
        sizes[0] = sizes[0] + len(arr) - np.sum(sizes)
        assert np.sum(sizes) == len(arr)
        res = []
        for i, v in enumerate(ratios):
            j = 0 if i == 0 else sizes[i - 1]
            res.append(arr[j:sizes[i] + j])
        return res

    def __init__(self):
        pass

    def confusion_matrix(expect, pred, labels=None):
        # expect = np.asarray(expect)
        # pred = np.asarray(pred)
        if (not type(labels) is np.ndarray and labels == None):
            labels = np.union1d(expect, pred)

        m = [[0] * len(labels) for l in labels]
        index = {v: i for i, v in enumerate(labels)}
        for e, p in zip(expect, pred):
            m[index[e]][index[p]] += 1

        return m

    def calc_accuracy(conf_matrix):
        t = sum(sum(l) for l in conf_matrix)
        return sum(conf_matrix[i][i] for i in range(len(conf_matrix))) / t

    def calc_recall(cm):
        tp = [cm[i][i] for i in range(len(cm))]
        sm = [sum(l) for l in cm]
        return [t / s if s > 0 else 0. for t, s in zip(tp, sm)]

    def calc_precision(cm):
        tp = [cm[i][i] for i in range(len(cm))]
        t = [[row[i] for row in cm] for i in range(len(cm[0]))]
        sm = [sum(l) for l in t]
        return [t / s if s > 0 else 0. for t, s in zip(tp, sm)]

    def calc_f1(cm):
        p = np.asarray(MlBase.calc_precision(cm))
        r = np.asarray(MlBase.calc_recall(cm))
        return np.nan_to_num(2 * (r * p) / (r + p))

    def calc_support(cm):
        c = np.sum(cm, axis=1)
        return c

    def score_report(expect, pred, labels=None):
        if (labels == None):
            labels = np.union1d(expect, pred)

        cm = MlBase.confusion_matrix(expect, pred, labels=labels)
        precision = MlBase.calc_precision(cm)
        recall = MlBase.calc_recall(cm)
        f1 = MlBase.calc_f1(cm)
        support = MlBase.calc_support(cm)
        return ScoreReport(
            labels=labels,
            confusion_matrix=cm,
            accuracy=MlBase.calc_accuracy(cm),
            precision=precision,
            recall=recall,
            f1=f1,
            support=support,
            totals=(np.average(precision, weights=support), np.average(recall, weights=support), np.average(f1, weights=support), sum(support)))

    def format_score_report(report):

        title = "{label:<10}{precision:>10}{recall:>10}{f1:>10}{support:>10}\n\n"
        content = ""
        for i, v in enumerate(report.precision):
            content += "{label:<10}{precision:10.2f}{recall:10.2f}{f1:10.2f}{support:>10}\n".format(label=report.labels[i],
                                                                                                    precision=report.precision[i],
                                                                                                    recall=report.recall[i],
                                                                                                    f1=report.f1[i],
                                                                                                    support=report.support[i])
        footer = "\n{label:<10}{precision: 10.2f}{recall: 10.2f}{f1: 10.2f}{support:>10}\n".format(label="avg/total",
                                                                                                   precision=report.totals[0],
                                                                                                   recall=report.totals[1],
                                                                                                   f1=report.totals[2],
                                                                                                   support=report.totals[3])
        footer += "Accuracy: {accuracy:5.2f}".format(accuracy=report.accuracy)
        return title.format(label="label", precision="precision", recall="recall", f1="f1", support="support") + content + footer
