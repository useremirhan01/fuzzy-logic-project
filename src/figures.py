"""Ham sonuçlardan grafik ve tabloları yeniden üret."""
import csv,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .core import rollout
from .experiment import ROOT

def main():
    out=ROOT/'results/figures';out.mkdir(parents=True,exist_ok=True)
    tables=ROOT/'results/tables';tables.mkdir(parents=True,exist_ok=True)
    rows=list(csv.DictReader((ROOT/'results/full/raw.csv').open()))
    summary=json.loads((ROOT/'results/full/summary.json').read_text())
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(figsize=(8,4));x=np.arange(2);bottom=np.zeros(2)
    for key,label,color in [('success','Başarı','#168a76'),('collision','Çarpışma','#cf4c52'),('timeout','Zaman aşımı','#e3b450')]:
        y=np.array([summary[m][key] for m in ['baseline','proposed']]);ax.bar(x,y,bottom=bottom,color=color,label=label)
        for i,v in enumerate(y):
            if v>2:ax.text(i,bottom[i]+v/2,str(v),ha='center',va='center',color='white')
        bottom+=y
    ax.set_xticks(x,['Temel sistem','Güvenli mesafe']);ax.set_ylabel('Koşu sayısı / 150');ax.legend(loc='upper center',bbox_to_anchor=(.5,1.16),ncol=3);fig.tight_layout();fig.savefig(out/'outcomes.png',dpi=170);plt.close(fig)
    fig,axs=plt.subplots(1,2,figsize=(10,4))
    for method,color in [('baseline','#2569ad'),('proposed','#168a76')]:
        r=[x for x in rows if x['method']==method]
        vals=[[float(x['min_clearance_m']) for x in r if int(x['obstacles'])==n] for n in [2,4,6,8,10]]
        axs[0].plot([2,4,6,8,10],[np.mean(v) for v in vals],'-o',label=method,color=color)
        axs[1].plot([2,4,6,8,10],[np.mean([x['status']=='success' for x in r if int(x['obstacles'])==n])*100 for n in [2,4,6,8,10]],'-o',label=method,color=color)
    axs[0].set_ylabel('Ortalama minimum açıklık (m)');axs[1].set_ylabel('Başarı (%)')
    for ax in axs:ax.set_xlabel('Engel sayısı');ax.legend()
    fig.tight_layout();fig.savefig(out/'density.png',dpi=170);plt.close(fig)
    sel=json.loads((ROOT/'results/full/selection.json').read_text())['selected_lambda']
    fig,ax=plt.subplots(figsize=(8,4))
    for lam,color in [(0,'#2569ad'),(sel,'#168a76')]:
        a=np.array([[x['best'] for x in json.loads((ROOT/f'results/full/convergence_{s}_{lam}.json').read_text())] for s in [11,22,33,44,55]])
        ax.plot(a.mean(0),color=color,label=f'λ={lam}');ax.fill_between(range(a.shape[1]),a.mean(0)-a.std(0,ddof=1),a.mean(0)+a.std(0,ddof=1),color=color,alpha=.15)
    ax.set_xlabel('Nesil');ax.set_ylabel('En iyi uygunluk, ortalama ± SS');ax.legend();fig.tight_layout();fig.savefig(out/'convergence.png',dpi=170);plt.close(fig)
    # Sabit seçim: ilk test haritası. İkinci panel ilk temel sistem başarısızlığı.
    maps=json.loads((ROOT/'data/full_splits.json').read_text())['test']
    failure=next((int(x['map_seed']) for x in rows if x['method']=='baseline' and x['training_seed']=='11' and x['status']!='success'),2001)
    chosen=[maps[0],next(m for m in maps if m['seed']==failure)]
    fig,axs=plt.subplots(1,2,figsize=(10,5))
    for ax,m in zip(axs,chosen):
        for x,y,r in m['obstacles']:ax.add_patch(plt.Circle((x,y),r,color='#8795a8'))
        for method,lam,color in [('baseline',0,'#2569ad'),('proposed',sel,'#168a76')]:
            w=np.array(json.loads((ROOT/f'models/full/seed11_lambda{lam}.json').read_text())['weights'])
            r=rollout(w,[m],True);p=r['path'][:,0,:];ax.plot(p[:,0],p[:,1],color=color,label=f'{method}: {r["status"][0]}')
        ax.plot(*m['start'],'ko');ax.plot(*m['goal'],'r*',markersize=12);ax.set(xlim=(0,10),ylim=(0,10),aspect='equal',title=f'Harita {m["seed"]}',xlabel='x (m)',ylabel='y (m)');ax.legend(fontsize=8)
    fig.tight_layout();fig.savefig(out/'trajectories.png',dpi=170);plt.close(fig)
    val=list(csv.DictReader((ROOT/'results/full/validation.csv').open()));fig,ax=plt.subplots(figsize=(8,4))
    ls=[0,100,400,1000];v=[sum(x['status']=='success' for x in val if x['method']==str(l)) for l in ls]
    ax.bar([str(x) for x in ls],v,color=['#2569ad' if l==0 else '#168a76' for l in ls]);ax.set(xlabel='Güvenli mesafe katsayısı λ',ylabel='Doğrulamada başarı / 40',ylim=(0,40));fig.tight_layout();fig.savefig(out/'ablation.png',dpi=170);plt.close(fig)
    with (tables/'summary.csv').open('w',newline='',encoding='utf-8') as f:
        wr=csv.writer(f);wr.writerow(['method','success','collision','timeout','n','clearance_mean','seed_success_rate_sd'])
        for m in ['baseline','proposed']:
            s=summary[m];wr.writerow([m,s['success'],s['collision'],s['timeout'],s['n'],s['clearance_all_mean'],s['success_rate_seed_sd']])
    print('5 figures and summary.csv generated')
if __name__=='__main__':main()
