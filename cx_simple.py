from brian import *
#import math

taum = 20 * ms          # membrane time constant
taue = 5 * ms          # excitatory synaptic time constant
taui = 10 * ms          # inhibitory synaptic time constant
Vt = -50 * mV          # spike threshold
Vr = -60 * mV          # reset value
El = -49 * mV          # resting potential
we = (60 * 0.27 / 10) * mV # excitatory synaptic weight
wi = (20 * 4.5 / 10) * mV # inhibitory synaptic weight

n = 40

eqs = Equations('''
      dV/dt  = (ge-gi-(V-El))/taum : volt
      dge/dt = -ge/taue         : volt
      dgi/dt = -gi/taui         : volt
      ''')

spiketimes = [(0, 1 * ms),(0, 10 * ms)]


G_TL2 = SpikeGeneratorGroup(2, spiketimes)
G_CL1a = NeuronGroup(N=16, model=eqs, threshold=Vt, reset=Vr)
G_CL1b = NeuronGroup(N=16, model=eqs, threshold=Vt, reset=Vr)
G_TB1 = NeuronGroup(N=16, model=eqs, threshold=Vt, reset=Vr)
G_CPU1 = NeuronGroup(N=16, model=eqs, threshold=Vt, reset=Vr)

C_LAL_CBL_1 = Connection(G_TL2, G_CL1a, 'ge')
C_CBL_PB = Connection(G_CL1a, G_TB1, 'ge', weight=we)
C_PB_PB_1 = Connection(G_TB1, G_TB1, 'gi', weight=wi)
C_PB_CBL = Connection(G_TB1, G_CL1b, 'gi', weight=wi)
C_PB_CBL = Connection(G_CL1b, G_CL1a, 'gi', weight=wi)

