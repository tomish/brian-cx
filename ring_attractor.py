from brian import *

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


G_input = SpikeGeneratorGroup(2, spiketimes)
G_ring = NeuronGroup(N=n, model=eqs, threshold=Vt, reset=Vr)

C1 = Connection(G_input, G_ring, 'ge')
C2 = Connection(G_ring, G_ring, 'ge')

C_ring_i = Connection(G_ring, G_ring, 'ge')


C1[0, 0] = 3 * mV

for i in range(0,n):
    C2[i, (i+1)%n] = 3 * mV

M = SpikeMonitor(G_ring)
MV = StateMonitor(G_ring, 'V', record=True)
Mge = StateMonitor(G_ring, 'ge', record=True)

G_ring.V = Vr + (Vt - Vr) * rand(len(G_ring))

run(1000 * ms)

figure()
subplot(211)
raster_plot(M, title='The ring attractor network', newfigure=False)
subplot(223)
plot(MV.times / ms, MV[0] / mV)
plot(MV.times / ms, MV[10] / mV)
subplot(224)
plot(Mge.times / ms, Mge[0] / mV)
show()







#subplot(211)
#plot(Mv.times, Mv[0])
#subplot(212)
#plot(Mge.times, Mge[0])
#show()

#raster_plot(Mb, title='The Ring network')
#show()