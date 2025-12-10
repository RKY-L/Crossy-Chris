import matplotlib.pyplot as plt
import math
plt.ion()

def plot(scores, mean_scores,above_halfway_percent,avg_ma_100):
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    if len(scores) != 0:
        plt.plot(scores,alpha=0.3,label ='Scores',color='powderblue')
        plt.plot(above_halfway_percent,label ='% Score Above 13: ' + f'{(above_halfway_percent[-1]/26):.2%}',color = "green")
        plt.plot(avg_ma_100,label ='MA 100: ' + str(avg_ma_100[-1]),color="red")
        plt.plot(mean_scores,label ='Mean Scores',color="orange")

        plt.legend(loc='upper left')
        plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
        plt.show(block=False)
        plt.pause(.1)