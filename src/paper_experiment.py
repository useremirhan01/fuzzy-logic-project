"""Şekil 6'nın engel sayısı taramasının yaklaşık tekrarı, ayrı değerlendirme."""
import csv,time
from pathlib import Path
import numpy as np
from .core import make_map,rollout
from .experiment import train,dump,ROOT

def main():
    rows=[];maps=[]
    for count in [0,2,4,6,8,10]:
        m=make_map(4000+count,count);maps.append(m)
        for seed in [11,22,33,44,55]:
            w,h,seconds=train([m],seed,0,20,20)
            r=rollout(w,[m])
            rows.append(dict(obstacles=count,seed=seed,train_seconds=seconds,status=r['status'][0],path_m=r['length'][0]))
    p=ROOT/'results/full/paper_approximation.csv'
    with p.open('w',encoding='utf-8',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=list(rows[0]));wr.writeheader();wr.writerows(rows)
    dump(Path('data/paper_approximation.json'),maps)
    print('30 approximately reconstructed runs completed; different hardware and definitions prevent direct timing equivalence.')
if __name__=='__main__':main()
