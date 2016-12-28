import population as pop
import random
import matplotlib.pyplot as plt
import matplotlib.collections as mc
import matplotlib.animation as animation
import multiprocessing

def go():
    l=[]
    
    for i in range(40):
        x=random.randrange(70)
        y=random.randrange(70)
        l.append([x,y])
   
    t = pop.Tour(l)
    now = pop.Population(t,200)
    ret = now.getfittest()
    print("at first")
    ret.print_on_file()

    print((ret).getdistance())
    print("start!!")
    ga = pop.GeneticAlgorithm(t,mutationrate=0.02,tournamentsize=8)
    for x in range(100):
        next = ga.evolve(now)
        ret = next.getfittest()
        ret.print()
        ret.print_on_file()
        print((next.getfittest()).getdistance())
        now = next
    print("finish")

def make():
    fig = plt.figure()
    ax1=fig.add_subplot(1,1,1)

    def animate(i):
        graph_data=open('data.txt','r').read()
        graph=graph_data.split('\n')
        xs=[]
        ys=[]
        lines=[]
        for line in graph:
            if len(line)>1:
                x,y=line.split(',')
                xs.append(x)
                ys.append(y)
        n = len(xs)
        for now in range(len(xs)):
            next = (now+1)%n
            lines.append([(xs[now],ys[now]),(xs[next],ys[next])])
        ax1.clear()
        ax1.set_title('solving TSP with genetic algorithm')
        ax1.scatter(xs,ys)
        lc = mc.LineCollection(lines)
        ax1.add_collection(lc)
        ss=open("data2.txt","r").read()
        plt.text(1,4.1,ss,fontsize=30)
    ani = animation.FuncAnimation(fig,animate,interval=100)
    plt.show()

if __name__=="__main__":
    p1 = multiprocessing.Process(target=go)
    p2 = multiprocessing.Process(target=make)
    open('data.txt','w')
    open('data2.txt','w')
    p1.start()
    p2.start()
    p1.join()
    p2.join()


