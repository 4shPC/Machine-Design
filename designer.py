"""
The program can be used to design knuckle joints
[
    PARAMETERS = Axial load,
                 Factor of Safety (not given will be assumed to be 5)
                 Yield Strength of the Material  (Compressive yield and Tensile Yield will be assumed equal)
]
"""
import math

def roundup(x, y):
    """ehe te nandayo!"""
    return int(math.ceil(x/y))*y

def standard(x):
    """Returns the standard sizes of shaft diameters"""
    if x<25: return roundup(x, 0.5)
    elif x<=60 and x>25: return roundup(x,5)
    elif x>60 and x<110: return roundup(x,10)
    elif x>110 and x<140: return roundup(x,15)
    elif x>140 and x<500: return roundup(x,20)
    else: return roundup(x,5)

class Knuckle:
    def __init__(self, load, yield_strength, fos=None, tensile_stress=None, crushing_stress=None, shear_stress=None):
        self.load = load
        self.fos = 5 if fos==None else fos
        self.yield_strength = yield_strength

        # Permissible Stresses
        self.tensile_stress = (self.yield_strength/self.fos) if tensile_stress==None else tensile_stress
        self.crushing_stress = (self.yield_strength/self.fos) if crushing_stress==None else crushing_stress 
        self.shear_stress = (self.yield_strength/self.fos)/2 if shear_stress==None else shear_stress
        

    def dimensions(self):
        self.d = standard((math.sqrt((4*self.load)/(math.pi*self.tensile_stress))))

        self.d1 = self.d
        self.d2 = 2*self.d
        self.d3 = 1.5*self.d
        self.t = 1.25*self.d
        self.t1 = 0.75*self.d
        self.t2 = 0.5*self.d
        return self.d, self.d1, self.d2, self.d3, self.t, self.t1, self.t2

    def pin_failure_in_shear(self):
        self.d1_ = math.sqrt((2*self.load)/(math.pi*self.shear_stress))
        return True if self.d1_<=self.d1 else False

    def rod_end_failure_in_tension(self):
        self.sigma_t1 = self.load/((self.d2 - self.d1)*self.t)
        return True if self.sigma_t1 <= self.tensile_stress else False
        
    def rod_end_failure_in_shear(self):
        self.tau1 = self.load/((self.d2 - self.d1)*self.t)
        return True if self.tau1 <= self.shear_stress else False

    def rod_end_failure_in_crushing(self):
        self.sigma_c1 = self.load/(self.d1*self.t)
        return True if self.sigma_c1 <= self.crushing_stress else False
     
    def forked_end_failure_in_tension(self):
        self.sigma_t2 = self.load/(2*(self.d2 - self.d1)*self.t1)
        return True if self.sigma_t2 <= self.tensile_stress else False

    def forked_end_failure_in_shear(self):
        self.tau2 = self.load/(2*(self.d2 - self.d1)*self.t1)
        return True if self.tau2 <= self.shear_stress else False

    def forked_end_failure_in_crushing(self):
        self.sigma_c2 = self.load/(2*self.d1*self.t1)
        return True if self.sigma_c2 <= self.tensile_stress else False


