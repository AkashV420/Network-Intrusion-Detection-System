def accCheck(statistics):
    labels = ['normal','tcpsynflood','icmpflood','udpflood','ipsweep','portscan','pingofdeath']
    print(statistics)
    tpr={}
    fpr={}
    precision={}
    f1score={}
    for i in labels:
        fp = tn = fn = 0
        tp = statistics[i][i]
        for j in labels:
            if i != j:
                fn += statistics[i][j]
                fp += statistics[j][i]
                for k in statistics[j].keys():
                    if k != i:
                        tn += statistics[j][k]
        tpr[i] = tp / (tp + fn)
        fpr[i] = fp / (fp + tn)
        precision[i] = tp / (tp + fp)
        f1score[i] = 2/(1/tpr[i] + 1/precision[i])
    print('TPR: \n ' + str(tpr))
    print('FRP:\n ' + str(fpr))
    print('Precision:\n ' + str(precision))
    print('F1-score: \n' + str(f1score))
