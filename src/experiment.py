"""Kontrollü eğitim, doğrulama ve bağımsız test. python -m src.experiment"""
import argparse,csv,json,time,platform
from pathlib import Path
import numpy as np
from .core import *

ROOT=Path(__file__).resolve().parents[1]
def dump(path,obj):
    path=ROOT/path;path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
def train(maps,seed,lam,population,generations):
    rng=np.random.default_rng(seed);start=time.perf_counter()
    # Aynı rastgele dizi, aynı uzman başlangıcı ve aynı bütçe tüm lambda'larda.
    pop=np.clip(prior()+rng.normal(0,.25,(population,N_RULES,2)),-1,1);pop[0]=prior()
    history=[]
    for gen in range(generations):
        out=rollout(np.repeat(pop,len(maps),axis=0),maps*population)
        scores=(out['fitness']-lam*out['safety']).reshape(population,len(maps)).mean(axis=1)
        order=np.argsort(-scores);history.append(dict(generation=gen,best=float(scores.max()),mean=float(scores.mean())))
        if gen==generations-1:break
        children=[pop[order[0]].copy(),pop[order[1]].copy()]
        while len(children)<population:
            parents=[pop[max(rng.choice(population,4,replace=False),key=lambda j:scores[j])] for _ in range(2)]
            a,b=sorted(rng.choice(np.arange(1,N_RULES),2,replace=False))
            child=parents[0].copy();child[a:b]=parents[1][a:b]
            mask=rng.random(child.shape)<.12
            step=.35*(1-gen/generations)+.03
            child+=mask*rng.uniform(-step,step,child.shape)
            children.append(np.clip(child,-1,1))
        pop=np.array(children)
    return pop[order[0]],history,time.perf_counter()-start

def rows_for(weights,maps,seed,method):
    start=time.perf_counter();r=rollout(weights,maps);wall=time.perf_counter()-start
    x=np.tile([.5,.5,.5,0,.5],(1,1)); samples=[]
    for _ in range(200):
        t=time.perf_counter();control(x,weights);samples.append(time.perf_counter()-t)
    return [dict(method=method,training_seed=seed,map_seed=m['seed'],obstacles=len(m['obstacles']),
                 status=str(r['status'][i]),path_m=float(r['length'][i]),sim_s=float(r['time'][i]),
                 min_clearance_m=float(r['minimum'][i]),final_distance_m=float(r['distance'][i]),
                 inference_us=float(np.median(samples)*1e6),batch_wall_s=wall)
            for i,m in enumerate(maps)]

def run(quick=False):
    tag='quick' if quick else 'full';base=Path('results')/tag
    cfg=dict(mode=tag,seeds=[11] if quick else [11,22,33,44,55],population=8 if quick else 20,
             generations=3 if quick else 20,lambdas=[0,100,400,1000],dt=DT,steps=STEPS,
             python=platform.python_version(),numpy=np.__version__,platform=platform.platform())
    trainmaps=[make_map(s) for s in range(100,102 if quick else 108)]
    valmaps=[make_map(s) for s in range(1000,1002 if quick else 1008)]
    testmaps=[make_map(s,[2,4,6,8,10][i%5]) for i,s in enumerate(range(2000,2005 if quick else 2030))]
    dump(base/'config.json',cfg);dump(Path('data')/(tag+'_splits.json'),dict(train=trainmaps,validation=valmaps,test=testmaps))
    candidates={};validation=[];training=[]
    for seed in cfg['seeds']:
        for lam in cfg['lambdas']:
            w,h,seconds=train(trainmaps,seed,lam,cfg['population'],cfg['generations'])
            candidates[seed,lam]=w
            dump(Path('models')/tag/f'seed{seed}_lambda{lam}.json',dict(weights=w.tolist(),seed=seed,lam=lam))
            dump(base/f'convergence_{seed}_{lam}.json',h)
            rows=rows_for(w,valmaps,seed,str(lam));validation.extend(rows)
            training.append(dict(seed=seed,lam=lam,seconds=seconds,evaluations=cfg['population']*cfg['generations']*len(trainmaps)))
            print(f'{tag} seed={seed} lambda={lam}: {sum(r["status"]=="success" for r in rows)}/{len(rows)} validation, {seconds:.1f}s',flush=True)
    # Önceden belirlenmiş leksikografik seçim: başarı, çarpışma, açıklık, düşük lambda.
    def rank(lam):
        r=[r for r in validation if r['method']==str(lam)]
        return (sum(x['status']=='success' for x in r),-sum(x['status']=='collision' for x in r),np.mean([x['min_clearance_m'] for x in r]),-lam)
    selected=max(cfg['lambdas'][1:],key=rank)
    dump(base/'selection.json',dict(selected_lambda=selected,rule='validation: success, fewer collisions, mean minimum clearance, smaller lambda'))
    results=[]
    for seed in cfg['seeds']:
        for method,lam in [('baseline',0),('proposed',selected)]:
            results+=rows_for(candidates[seed,lam],testmaps,seed,method)
    for name,rows in [('raw',results),('validation',validation),('training',training)]:
        path=ROOT/base/(name+'.csv');path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('w',newline='',encoding='utf-8') as f:
            wr=csv.DictWriter(f,fieldnames=list(rows[0]));wr.writeheader();wr.writerows(rows)
    dump(base/'summary.json',summarize(results))
    print(json.dumps(summarize(results),indent=2),flush=True)

def summarize(rows):
    summary={}
    for method in ['baseline','proposed']:
        r=[x for x in rows if x['method']==method];ok=[x for x in r if x['status']=='success']
        seeds=sorted(set(x['training_seed'] for x in r))
        rates=[np.mean([x['status']=='success' for x in r if x['training_seed']==s]) for s in seeds]
        summary[method]=dict(n=len(r),success=len(ok),collision=sum(x['status']=='collision' for x in r),
            timeout=sum(x['status']=='timeout' for x in r),success_rate_seed_mean=float(np.mean(rates)),
            success_rate_seed_sd=float(np.std(rates,ddof=1)) if len(seeds)>1 else None,
            clearance_all_mean=float(np.mean([x['min_clearance_m'] for x in r])),
            successful_path_mean=float(np.mean([x['path_m'] for x in ok])) if ok else None,
            successful_time_mean=float(np.mean([x['sim_s'] for x in ok])) if ok else None)
    pairs={}
    for x in rows:pairs.setdefault((x['training_seed'],x['map_seed']),{})[x['method']]=x
    both=[p for p in pairs.values() if len(p)==2 and all(x['status']=='success' for x in p.values())]
    summary['paired']=dict(n=len(both),proposed_minus_baseline_path=float(np.mean([p['proposed']['path_m']-p['baseline']['path_m'] for p in both])) if both else None)
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--quick',action='store_true');a=p.parse_args();run(a.quick)
