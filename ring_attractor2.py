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


G_input = SpikeGeneratorGroup(2, spiketimes)
G_ring = NeuronGroup(N=n, model=eqs, threshold=Vt, reset=Vr)

C1 = Connection(G_input, G_ring, 'ge')
CE = Connection(G_ring, G_ring, 'ge', weight=we)
CI = Connection(G_ring, G_ring, 'gi', weight=wi)

C_ring_i = Connection(G_ring, G_ring, 'ge')


C1[0, 0] = 3 * mV

for i in range(0,n):
    for j in range(0,n):
        con_strength = (math.cos(2 * math.pi / n * (i - j)) + 1) / 2
        CE[i, j] = con_strength * 3 * mV
        CI[i, j] = con_strength * 3 * mV
        #print i, j

print CE.W
x = arange(n)
y = arange(n)
X, Y = meshgrid(x, y)
#figure()
#contourf(X, Y, CE.W)
#show()


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
#plot(MV.times / ms, MV[10] / mV)
subplot(224)
plot(Mge.times / ms, Mge[0] / mV)
show()