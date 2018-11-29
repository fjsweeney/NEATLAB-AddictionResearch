from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np


def transform(data, n_components):
    pca = PCA(n_components=n_components)
    return pca.fit_transform(data)


def plot(data, labels):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel('Principal Component 1')
    ax.set_ylabel('Principal Component 2')
    ax.set_title('2 component PCA')

    # Printing bag stats. This could be removed, it's just for testing.
    unique, counts = np.unique(labels, return_counts=True)
    v_pct = float(counts[1]) / float(len(labels))
    nv_pct = float(counts[0]) / float(len(labels))
    print("Predicted Vulnerable: %.2f | Predicted Not Vulnerable: %.2f" %
          (v_pct, nv_pct))

    pos_instances = []
    neg_instances = []
    for i, label in enumerate(labels):
        if label == 0:
            neg_instances.append(data[i])
        else:
            pos_instances.append(data[i])

    pos_instances = np.asarray(pos_instances)
    neg_instances = np.asarray(neg_instances)

    ax.scatter(x=neg_instances[:,0], y=neg_instances[:,1], color='r',
               label="Vulnerable")
    ax.scatter(x=pos_instances[:, 0], y=pos_instances[:, 1], color='b',
               label="Not Vulnerable")
    ax.legend(loc="lower right")

    ax.grid
    plt.show()