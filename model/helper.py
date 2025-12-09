import matplotlib.pyplot as plt
plt.ion()

def plot(scores, mean_scores,above_halfway_percent):
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.plot(above_halfway_percent)
    plt.text(len(above_halfway_percent)-1, above_halfway_percent[-1], str(above_halfway_percent[-1]/26))
    plt.show(block=False)
    plt.pause(.1)