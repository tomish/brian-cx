from brian import *
from brian.library.IF import *
#import math

taum = 20 * ms          # membrane time constant
taue = 5 * ms          # excitatory synaptic time constant
taui = 10 * ms          # inhibitory synaptic time constant
Vt = -50 * mV          # spike threshold
Vr = -60 * mV          # reset value
El = -49 * mV          # resting potential
we = (60 * 0.27 / 10) * mV # excitatory synaptic weight
wi = (20 * 4.5 / 10) * mV # inhibitory synaptic weight

we = 1.5 * mV
wi = 4.5 * mV

n = 40

eqs=Izhikevich(a=0.02/ms,b=0.2/ms)

#eqs = Equations('''
#      dV/dt  = (ge-gi-(V-El))/taum      : volt
#      dge/dt = -ge/taue                 : volt
#      dgi/dt = -gi/taui                 : volt
#      ''')


spiketimes = [(6, 1 * ms),(6, 10 * ms),(10, 500 * ms),(10, 505 * ms),(10, 510 * ms),(10, 515 * ms),(10, 520 * ms),(10, 525 * ms)]

#Groups
#G_TL2 = SpikeGeneratorGroup(30, spiketimes)

#For adding some spikes in to CPU1 neuron output
#G_CBU_Activity = SpikeGeneratorGroup(30, spiketimes)

G_CL1a = SpikeGeneratorGroup(16, spiketimes)


#G_CL1a = NeuronGroup(N=16, model=eqs, threshold=Vt, reset=Vr)
G_CL1b = NeuronGroup(N=16, model=eqs, threshold=Vt, reset=Vr)
G_TB1 = NeuronGroup(N=8, model=eqs, threshold=Vt, reset=Vr)

#Background spiking of 20 - 40 Hz (Heinze & Homberg, Science, 2007)
G_CPU1 = NeuronGroup(N=16, model=eqs, threshold=Vt, reset=Vr)

#Connections
#C_LAL_CBL_1 = Connection(G_TL2, G_CL1a, 'ge')
#C_PB_CBL = Connection(G_TB1, G_CL1b, 'gi', weight=wi)
#C_PB_CBL = Connection(G_CL1b, G_CL1a, 'gi', weight=wi)
#C_TB1_TB1 = Connection(G_TB1, G_TB1, 'gi', weight=wi)


# times two
#TB1_TB1_array = array([[0,0,0.5,1,1,0.5,0,0,0,0,0.5,1,1,0.5,0,0],
#                       [0,0,0,0.5,1,1,0.5,0,0,0,0,0.5,1,1,0.5,0],
#                       [0.5,0,0,0,0.5,1,1,0.5,0,0,0,0,0.5,1,1,0.5],
#                       [1,0.5,0,0,0,0.5,1,1,0.5,0,0,0,0,0.5,1,1],
#                       [1,1,0.5,0,0,0,0,0.5,1,1,0.5,0,0,0,0.5,1],
#                       [0.5,1,1,0.5,0,0,0,0,0.5,1,1,0.5,0,0,0,0.5],
#                       [0,0.5,1,1,0.5,0,0,0,0,0.5,1,1,0.5,0,0,0],
#                       [0,0,0.5,1,1,0.5,0,0,0,0,0.5,1,1,0.5,0,0]])

#leftmost column is neuron with vericose arborisations in L1 and R8
TB1_TB1_array = array([[0   ,0   ,0.25,1   ,1   ,0.5 ,0   ,0   ],
                       [0   ,0   ,0   ,0.5 ,1   ,1   ,0.5 ,0   ],
                       [0.25,0   ,0   ,0   ,0.5 ,1   ,1   ,0.5 ],
                       [0.75,0.25,0   ,0   ,0   ,0.5 ,1   ,1   ],
                       [1   ,1   ,0.5 ,0   ,0   ,0   ,0.25,0.75],
                       [0.5 ,1   ,1   ,0.5 ,0   ,0   ,0   ,0.25],
                       [0   ,0.5 ,1   ,1   ,0.5 ,0   ,0   ,0   ],
                       [0   ,0   ,0.5 ,1   ,1   ,0.5 ,0   ,0   ]]) * wi

C_TB1_TB1 = Connection(G_TB1, G_TB1, 'gi')
C_TB1_TB1.connect(G_TB1, G_TB1, TB1_TB1_array)


#CL1a neurons are numbers from L to R across the CBU
CL1a_TB1_array = array([[1,0,0,0,0,0,0,0],
                        [1,0,0,0,0,0,0,0],
                        [0,1,0,0,0,0,0,0],
                        [0,1,0,0,0,0,0,0],
                        [0,0,1,0,0,0,0,0],
                        [0,0,1,0,0,0,0,0],
                        [0,0,0,1,0,0,0,0],
                        [0,0,0,1,0,0,0,0],
                        [0,0,0,0,1,0,0,0],
                        [0,0,0,0,1,0,0,0],
                        [0,0,0,0,0,1,0,0],
                        [0,0,0,0,0,1,0,0],
                        [0,0,0,0,0,0,1,0],
                        [0,0,0,0,0,0,1,0],
                        [0,0,0,0,0,0,0,1],
                        [0,0,0,0,0,0,0,1]]) * we

C_CL1a_TB1 = Connection(G_CL1a, G_TB1, 'ge')
C_CL1a_TB1.connect(G_CL1a, G_TB1, CL1a_TB1_array)


#these are inhibitory connections from TB1 cels to CPU1.
#we number CPU 1 cells from L to R on the PB
TB1_CPU1_array = array([[1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
                        [0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
                        [0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0],
                        [0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0],
                        [0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0],
                        [0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0],
                        [0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0],
                        [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1]]) * wi

#CBU_CPU1_array = 


print C_TB1_TB1.W
print TB1_TB1_array
print CL1a_TB1_array

print we
print wi



M_TB1_spikes = SpikeMonitor(G_TB1)
MV = StateMonitor(G_TB1, 'V', record=True)
Mge = StateMonitor(G_TB1, 'ge', record=True)
Mgi = StateMonitor(G_TB1, 'gi', record=True)

G_TB1.V = Vr + (Vt - Vr) * rand(len(G_TB1))
run(1000 * ms)

figure()
#plotting spikes of TB 1 cells on raster plot.
subplot(411)
raster_plot(M_TB1_spikes, title='TB1 spikes', newfigure=False)

#observation_list = [0,1,2,3,4,5,6,7]
observation_list = [3,5]


#plotting voltage on TB1 cells
subplot(412)
title('V')
for i in observation_list:
    plot(MV.times / ms, MV[i] / mV)

subplot(413)
title('ge')
for i in observation_list:
    plot(Mge.times / ms, Mge[i] / mV)

subplot(414)
title('gi')
for i in observation_list:
    plot(Mge.times / ms, Mgi[i] / mV)


show()