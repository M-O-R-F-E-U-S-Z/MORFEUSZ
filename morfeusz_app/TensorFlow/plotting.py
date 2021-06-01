import numpy as np
import matplotlib.pyplot as plt
import csv

EXTENSION = '.pdf'
FONT = 30
XTICK = 20
YTICK = 20

plt.rcParams.update({
        'font.size': FONT,
        'xtick.labelsize': XTICK,
        'ytick.labelsize': YTICK })

def single_plot(name, E, W, L, const=0):
    plt_name = 'Plot-eff_{}'.format(name)
    fig = plt.figure(figsize=(14,8))
    ax = plt.gca()
    plt.plot(E, W[0]*100, 'b', linewidth=2, label='Train')
    plt.plot(E, W[1]*100, 'r', linewidth=2, label='Test')
    if const!=0: plt.plot(E, const*np.ones(len(E)), 'k--')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])
    plt.legend(loc='lower left', bbox_to_anchor=(1, -0.025), fontsize=22)
    plt.xlabel('Epoch')
    plt.ylabel('Efficiency [%]')
    plt.xticks(np.arange(0, E[-1]+1, 5))
    plt.xlim([0, E[-1]+1])
    plt.ylim([50, 90])
    plt.text(s='{:.2f}%'.format(np.mean(W[0][-1:])*100), color='b', alpha=1.0, x=E[-1]+1.2, y=np.mean(W[0][-1:])*100+0.6, va='center', ha='left', fontsize=30)
    plt.text(s='{:.2f}%'.format(np.mean(W[1][-1:])*100), color='r', alpha=1.0, x=E[-1]+1.2, y=np.mean(W[1][-1:])*100-0.6, va='center', ha='left', fontsize=30)
    plt.savefig('Plots/'+plt_name+EXTENSION)
    plt.close()
    plt_name = 'Plot-loss_{}'.format(name)
    fig = plt.figure(figsize=(14,8))
    ax = plt.gca()
    plt.semilogy(E, L[0], 'b', linewidth=2, label='Train')
    plt.semilogy(E, L[1], 'r', linewidth=2, label='Test')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])
    plt.legend(loc='lower left', bbox_to_anchor=(1, -0.025), fontsize=22)
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.xticks(np.arange(0, E[-1]+1, 5))
    plt.xlim([0, E[-1]+1])
    plt.ylim([0.2, 2])
    plt.savefig('Plots/'+plt_name+'.pdf')
    plt.close()

def all_plots():

    if not os.path.exists('Plots'):
        os.makedirs('Plots')

    layer_sizes = [128]
    conv_layers = [3,4,5]
    dense_layers = [1,2,3]
    names = []
    for layer_size in layer_sizes:
        for conv_layer in conv_layers:
            for dense_layer in dense_layers:
                names.append('run-{}nodes-{}conv-{}dense'.format(layer_size,conv_layer,dense_layer))

    W_tren = []
    W_test = []
    L_tren = []
    L_test = []
    for name in names:
        A = []
        for sheet in ['_train-tag-epoch_accuracy',
                      '_validation-tag-epoch_accuracy',
                      '_train-tag-epoch_loss',
                      '_validation-tag-epoch_loss']:

            with open('CSV/'+name+sheet+'.csv') as file:
                reader = csv.reader(file)
                i = next(reader)
                A1 = [row for row in reader]
                A.append(np.asfarray(A1,float))

        A = np.array(A)
        E = A[0,:,1]+1
        W_tren.append(A[0,:,2])
        W_test.append(A[1,:,2])
        L_tren.append(A[2,:,2])
        L_test.append(A[3,:,2])

    W_test_all = []
    L_test_all = []

    for i in range(len(names)):
        SinglePlot(str(i+1)+'-'+names[i],
                   E,
                   [W_tren[i], W_test[i]],
                   [L_tren[i], L_test[i]])

        W_test_all.append(np.mean(W_test[i][-1:])*100)
        L_test_all.append(np.mean(L_test[i][-1:]))


    W_all = np.reshape(W_test_all,(len(conv_layers),len(dense_layers)))
    L_all = np.reshape(L_test_all,(len(conv_layers),len(dense_layers)))

    if not os.path.exists('Maps'):
        os.makedirs('Maps')    

    W = (W_all[:,:]).T
    L = (L_all[:,:]).T
    
    folder = 'Maps/'
    plt_name = 'Plot-map-eff'
    fig = plt.figure(figsize=(10,10))
    ax = plt.gca()
    ax.imshow(W, cmap='YlGn', vmin=np.min(W_all), vmax=np.max(W_all))
    plt.xlabel('Convolutional layers')
    plt.ylabel('Dense layers')
    ax.set_xticks(np.arange(len(conv_layers)))
    ax.set_yticks(np.arange(len(dense_layers)))
    ax.set_xticklabels(conv_layers)
    ax.set_yticklabels(dense_layers)

    for i in range(len(conv_layers)):
        for j in range(len(dense_layers)):
            if (W[j, i]-np.min(W_all))/(np.max(W_all)-np.min(W_all)) < 0.3:
                col = "k"
            else:
                col = "w"
            text = ax.text(i, j, str(round(W[j, i], 2))+' %',
                           ha="center", va="center", color=col)
    
    plt.savefig(folder+plt_name+EXTENSION)
    plt.close()
    plt_name = 'Plot-map-loss'
    fig = plt.figure(figsize=(10,10))
    ax = plt.gca()
    ax.imshow(L, cmap='OrRd', vmin=np.min(L_all), vmax=np.max(L_all))
    plt.xlabel('Convolutional layers')
    plt.ylabel('Dense layers')
    ax.set_xticks(np.arange(len(conv_layers)))
    ax.set_yticks(np.arange(len(dense_layers)))
    ax.set_xticklabels(conv_layers)
    ax.set_yticklabels(dense_layers)

    for i in range(len(conv_layers)):
        for j in range(len(dense_layers)):
            if (L[j, i]-np.min(L_all))/(np.max(L_all)-np.min(L_all)) < 0.3:
                col = "k"
            else:
                col = "w"
            text = ax.text(i, j, round(L[j, i], 4),
                           ha="center", va="center", color=col)
    
    plt.savefig(folder+plt_name+EXTENSION)
    plt.close()
