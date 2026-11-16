"""Beş katmanlı min-normalize-ağırlıklı toplam FNN ve vektörlü simülasyon.

Makale denklemleri 1-4'ün açıklamalı yeniden kurulumu; fizik ve eksik
parametreler proje varsayımlarıdır. Her satır bağımsız bir robot koşusudur.
"""
from itertools import product
import numpy as np

RULES = np.array(list(product(range(2), range(2), range(2), range(5), range(2))))
CENTERS = [np.array([0., 1.])]*3 + [np.linspace(-1, 1, 5), np.array([0., 1.])]
WIDTHS = [.42, .42, .42, .30, .55]
N_RULES = len(RULES)
DT, RADIUS, VMAX, WMAX, STEPS, SIZE, GOAL_RADIUS = .2, .18, .8, 1., 250, 10., .3

def wrap(a):
    return (a + np.pi) % (2*np.pi) - np.pi

def memberships(x):
    x = np.atleast_2d(x)
    if not np.isfinite(x).all():
        raise ValueError('Girdiler sonlu olmalı')
    return [np.exp(-((x[:,i,None]-c)/WIDTHS[i])**2) for i,c in enumerate(CENTERS)]

def activation(x):
    mu = memberships(x)
    a = np.minimum.reduce([m[:,RULES[:,i]] for i,m in enumerate(mu)])
    sums = a.sum(axis=1, keepdims=True)
    return np.divide(a, sums, out=np.full_like(a, 1/N_RULES), where=sums>1e-300)

def prior():
    """Uzman kural başlangıcı. Öğrenilmiş parametre diye sunulmaz."""
    w=[]
    for f,l,r,a,d in RULES:
        angle=CENTERS[3][a]
        turn=np.clip(1.8*angle, -1, 1)
        if f==0:
            turn=1. if l>=r else -1.
        speed=.8 if f else .22
        speed*=max(.25, 1-abs(angle)*.7)
        if d==0: speed*=.7
        w.append([speed,turn])
    return np.array(w)

def control(x, weights):
    a=activation(x)
    y=np.einsum('br,brk->bk',a,weights) if weights.ndim==3 else a@weights
    return np.column_stack([np.clip(y[:,0],0,1)*VMAX,np.clip(y[:,1],-1,1)*WMAX])

def segment_clearance(p, q, obs):
    """Süpürülen disk ile doğru parçası boyunca kesin daire çarpışması."""
    v=q-p
    h=np.sum((obs[:,:,:2]-p[:,None,:])*v[:,None,:],axis=2)
    h/=np.maximum(np.sum(v*v,axis=1)[:,None],1e-30)
    closest=p[:,None,:]+np.clip(h,0,1)[:,:,None]*v[:,None,:]
    c=np.min(np.linalg.norm(closest-obs[:,:,:2],axis=2)-obs[:,:,2]-RADIUS,axis=1)
    wall=np.minimum(np.min(np.minimum(p,q),axis=1),SIZE-np.max(np.maximum(p,q),axis=1))-RADIUS
    return np.minimum(c,wall)

def sense(p, theta, goals, obs):
    delta=obs[:,:,:2]-p[:,None,:]
    angles=wrap(np.arctan2(delta[:,:,1],delta[:,:,0])-theta[:,None])
    dist=np.linalg.norm(delta,axis=2)
    surface=np.maximum(0,dist-obs[:,:,2]-RADIUS)
    angular=np.arcsin(np.clip((obs[:,:,2]+RADIUS)/np.maximum(dist,1e-12),0,1))
    sectors=[]
    for center in [0,np.pi/3,-np.pi/3]:
        sees=np.abs(wrap(angles-center)) <= np.pi/6+angular
        sectors.append(np.minimum(3,np.min(np.where(sees,surface,3),axis=1))/3)
    goal_delta=goals-p
    distance=np.linalg.norm(goal_delta,axis=1)
    error=wrap(np.arctan2(goal_delta[:,1],goal_delta[:,0])-theta)
    return np.column_stack(sectors+[error/np.pi,np.minimum(distance,10)/10])

def rollout(weights, maps, trace=False):
    """Bir model/harita çifti için bir satır. Zamanlar simülasyon zamanıdır."""
    n=len(maps)
    p=np.array([m['start'] for m in maps],float)
    goals=np.array([m['goal'] for m in maps],float)
    count=max(len(m['obstacles']) for m in maps)
    obs=np.array([m['obstacles']+[[1e6,1e6,0.]]*(count-len(m['obstacles'])) for m in maps],float)
    theta=np.array([m.get('theta',0.) for m in maps])
    active=np.ones(n,bool); status=np.full(n,'timeout',dtype='<U10')
    length=np.zeros(n); ticks=np.zeros(n,int); qs=np.zeros(n); qv=np.zeros(n)
    minimum=segment_clearance(p,p,obs); safety=np.zeros(n)
    path=[p.copy()] if trace else None
    for _ in range(STEPS):
        if not active.any(): break
        x=sense(p,theta,goals,obs)
        u=control(x,weights)
        nt=wrap(theta+u[:,1]*DT)
        q=p+u[:,0,None]*DT*np.column_stack([np.cos(nt),np.sin(nt)])
        c=segment_clearance(p,q,obs)
        hit=c<=0
        reached=np.linalg.norm(q-goals,axis=1)<=GOAL_RADIUS
        length+=np.linalg.norm(q-p,axis=1)*active
        ticks+=active; qs+=active&~hit; qv+=active&~hit&(np.abs(u[:,1]*DT)<.1)
        minimum=np.where(active,np.minimum(minimum,c),minimum)
        safety+=active*np.maximum(0,(.6-c)/.6)**2
        p=np.where(active[:,None],q,p); theta=np.where(active,nt,theta)
        status[active&hit]='collision'; status[active&~hit&reached]='success'
        active &= ~hit & ~reached
        if trace:path.append(p.copy())
    d=np.linalg.norm(p-goals,axis=1)
    # Eq.9 interpretation: t in frames; unsuccessful run gets t=7000.
    t=np.where(status=='success',ticks,7000)
    fitness=(7000-t)+(1200-60*d)+qv/30+qs/20
    return dict(status=status,length=length,ticks=ticks,time=ticks*DT,minimum=minimum,
                safety=safety/np.maximum(ticks,1),fitness=fitness,distance=d,
                path=np.array(path) if trace else None)

def reachable(m):
    """Muhafazakâr 0.2 m ızgarada 4-komşulu, kenarları doğrulanan BFS."""
    from collections import deque
    obs=np.array(m['obstacles'])[None,:,:]
    start=np.array(m['start']);goal=np.array(m['goal'])
    if segment_clearance(start[None,:],start[None,:],obs)[0]<=0 or segment_clearance(goal[None,:],goal[None,:],obs)[0]<=0:
        return False
    points=np.arange(.2,9.81,.2)
    def key(p): return tuple(np.argmin(abs(points-pi)) for pi in p)
    s,g=key(start),key(goal)
    if segment_clearance(start[None,:],np.array([[points[s[0]],points[s[1]]]]),obs)[0]<=0:return False
    if segment_clearance(goal[None,:],np.array([[points[g[0]],points[g[1]]]]),obs)[0]<=0:return False
    todo=deque([s]);seen={s}
    while todo:
        a=todo.popleft()
        if a==g:return True
        p=np.array([[points[a[0]],points[a[1]]]])
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            b=(a[0]+dx,a[1]+dy)
            if b in seen or min(b)<0 or max(b)>=len(points):continue
            q=np.array([[points[b[0]],points[b[1]]]])
            if segment_clearance(p,q,obs)[0]>.015:
                seen.add(b);todo.append(b)
    return False

def make_map(seed, obstacles=6):
    rng=np.random.default_rng(seed)
    for attempt in range(100):
        start=[.6,float(rng.uniform(.8,9.2))];goal=[9.4,float(rng.uniform(.8,9.2))]
        obs=np.column_stack([rng.uniform(1.7,8.3,obstacles),rng.uniform(.8,9.2,obstacles),rng.uniform(.25,.55,obstacles)])
        m=dict(seed=int(seed),start=start,goal=goal,theta=0.,obstacles=obs.tolist(),attempt=attempt)
        if reachable(m):return m
    raise RuntimeError('Geçilebilir harita üretilemedi')
