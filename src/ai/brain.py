import numpy,random
from scipy.special import expit
import rhythm
    

def sigmoid(x):
    """
    Effecient numpy implementation of sigmoid function
    :param x:
    :return    sigmoid(x):
    """
    return expit(numpy.clip(x,-500,500))

   
def rand_matrix(nrow,ncol,range=[-1,1]):
    low=range[0]    # /ncol
    scale=(range[1]-range[0])  # /ncol
    return numpy.matrix(low+numpy.random.rand(nrow,ncol)*scale)


class Layer:
    
    def __init__(self,nin,nout,func,matrix=None):
        
        self.nin = nin
        self.nout = nout
        
        if matrix == None:
            self.matrix = rand_matrix(nrow=nout,ncol=nin)
        else:
            self.matrix = numpy.matrix(matrix)
        
        self.func=func
        
        self.input=numpy.zeros(nin)
        self.z=numpy.zeros(nout)
        self.output=numpy.zeros(nout)
    
        
    def fire(self):
        self.z[:] = numpy.dot(self.matrix, self.input)

        self.output[:] = self.func(self.z)
        return self.output
    
    def radomize(self):
        self.matrix = rand_matrix( nrow=self.nout,ncol=self.nin)
        
        
    
            
class ElmanNet:

    def __init__(self,nin,nhid,nout,feedback=0.0):
        
        self.nin=nin
        self.nhid=nhid
        self.nout=nout
        self.layer1=Layer(nin+nhid+1,nhid,sigmoid)
        self.layer2=Layer(nhid+1,nout,sigmoid)
        self.feedback=feedback

    
    def fire(self,input):
        self.layer1.input[:self.nin]=input
        
 #  feed back output of layer1 (which should be stored as input to layer2
        self.layer1.input[self.nin:-1]=  self.layer2.input[:self.nhid]+self.layer1.input[self.nin:-1]*self.feedback
        
        self.layer1.input[-1]=1.0
        
        self.layer2.input[:-1]=self.layer1.fire()
        self.layer2.input[-1]=1.0
  
        self.layer2.fire()
        return self.layer2.output          
# 

class Brain:
    """
    client is fed the output state every tick
    
    """
    
    def __init__(self,nin,output):

        #  numpy.random.seed(1)
        self.nin=nin
        self.nout=output.size()

        self.input=numpy.zeros(self.nin)

        self.output=output
        self.net=None

            
    def random_net(self,nhid):
        self.nhid=nhid
        self.net=ElmanNet(self.nin,self.nhid,self.nout)

    def quit(self):
        self.seq.quit()
        

        
    def tick(self,state):
        """
        brain is driven by calling this with state

        :param state:   activation
        :return:
        """
        if self.net == None:
            return False
        
        assert len(state) == self.nin

        self.input[:len(state)]=state

        self.out=self.net.fire(self.input)
        return True

            
    def freewheel(self,ncycle):
        
        for _ in range(ncycle):
            out=self.net.fire(self.input)
        
        if self.output != None:
            self.output.process(out,mute=True)
    


if __name__ == "__main__":

    def test():
        el.fire(input)

    def noise():
        return random.random()

    nin = 10
    nhid = 1000
    nout = 1000
    noise = None
    el=ElmanNet(nin,nhid,nout)

    input=numpy.zeros(nin)

    import timeit

    print timeit.timeit("test()",setup="from __main__ import test",number=1000)


