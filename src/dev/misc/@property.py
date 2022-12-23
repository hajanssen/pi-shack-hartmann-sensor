    @property
    def ZernikeFunctions(self):
        z1 = lambda x,y : x
        z2 = lambda x,y : y
        z3 = lambda x,y : -1*x**2 + y**2
        z4 = lambda x,y : 2*x*y
        z5 = lambda x,y : -1 + 2*x**2 + 2+y**2
        z6 = lambda x,y : -3*x**2*y + y**3
        z7 = lambda x,y : -1*x**3 + 2*x*y**2
        Z = [z1,z2,z3,z4,z5,z6,z7]
        
        return Z[:self.NZernike]
    
    @property
    def ZernikeFunctionsDx(self):
        z1dx = lambda x,y : np.ones_like(x)
        z2dx = lambda x,y : np.zeros_like(x)
        z3dx = lambda x,y : -2*x
        z4dx = lambda x,y : 2*y
        z5dx = lambda x,y : 4*x
        z6dx = lambda x,y : -6*x*y
        z7dx = lambda x,y : -4*x**2
        Zdx = [z1dx,z2dx,z3dx,z4dx,z5dx,z6dx,z7dx]
        return Zdx[:self.NZernike]
    
    @property
    def ZernikeFunctionsDy(self):
        z1dy = lambda x,y : np.zeros_like(x)
        z2dy = lambda x,y : np.ones_like(x)
        z3dy = lambda x,y : 2*y
        z4dy = lambda x,y : 2*x
        z5dy = lambda x,y : 2*y
        z6dy = lambda x,y : 2*y**2
        z7dy = lambda x,y : 4*x*y
        Zdy = [z1dy,z2dy,z3dy,z4dy,z5dy,z6dy,z7dy]
        return Zdy[:self.NZernike]
