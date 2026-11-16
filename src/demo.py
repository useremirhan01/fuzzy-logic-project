"""Tkinter canlı demo: python -m src.demo. Aynı core.py denetleyicisini çalıştırır."""
import json, tkinter as tk
from tkinter import ttk,messagebox
from pathlib import Path
import numpy as np
from .core import *

ROOT=Path(__file__).resolve().parents[1]
class Demo:
    def __init__(self):
        self.root=tk.Tk();self.root.title('Bulanık Robot | Emirhan Efe Demir')
        self.root.configure(bg='#101c2c');self.running=False;self.ready=False
        bar=ttk.Frame(self.root);bar.pack(fill='x')
        self.seed=tk.StringVar(value='2000');self.method=tk.StringVar(value='baseline');self.edit=tk.StringVar(value='Engel ekle')
        ttk.Label(bar,text='Harita tohumu').pack(side='left');ttk.Entry(bar,textvariable=self.seed,width=8).pack(side='left')
        ttk.Combobox(bar,textvariable=self.method,values=['baseline','proposed'],state='readonly',width=10).pack(side='left')
        for name,fn in [('Harita yükle',self.load),('Başlat',self.start),('Duraklat',self.pause),('Sıfırla',self.reset)]:ttk.Button(bar,text=name,command=fn).pack(side='left')
        ttk.Combobox(bar,textvariable=self.edit,values=['Başlangıç','Hedef','Engel ekle','Engel sil'],state='readonly',width=13).pack(side='left')
        self.canvas=tk.Canvas(self.root,width=650,height=650,bg='#f5f8fc',highlightthickness=0);self.canvas.pack(side='left');self.canvas.bind('<Button-1>',self.click)
        self.info=tk.Text(self.root,width=42,height=38,font=('Consolas',10),bg='#101c2c',fg='#e1edf9');self.info.pack(side='right',fill='both')
        self.load();self.root.after(40,self.tick)
    def load(self):
        try:
            seed=int(self.seed.get())
            source=ROOT/'data/full_splits.json'
            saved=json.loads(source.read_text())['test'] if source.exists() else []
            self.map=next((m for m in saved if m['seed']==seed),None)
            if self.map is None:self.map=make_map(seed,6)
            self.reset()
        except Exception as e:messagebox.showerror('Harita yüklenemedi',str(e))
    def pause(self):self.running=False
    def reset(self):
        self.running=False;self.p=np.array(self.map['start'],float);self.theta=0.;self.path=[self.p.copy()]
        self.steps=0;self.length=0.;self.minimum=float('inf');self.status='Hazır';self.draw()
    def start(self):
        try:
            if not reachable(self.map):raise ValueError('Başlangıç/hedef geçersiz veya doğrulanmış geçiş bulunamadı.')
            tag='full' if (ROOT/'results/full/selection.json').exists() else 'quick'
            sel=json.loads((ROOT/f'results/{tag}/selection.json').read_text())['selected_lambda']
            lam=0 if self.method.get()=='baseline' else sel
            obj=json.loads((ROOT/f'models/{tag}/seed11_lambda{lam}.json').read_text())
            self.weights=np.array(obj['weights']);self.label=f'{tag}, eğitim tohumu 11, λ={lam}'
            if self.status in ['Başarı','Çarpışma','Zaman aşımı']:self.reset()
            self.running=True;self.status='Çalışıyor'
        except Exception as e:messagebox.showerror('Başlatılamadı',str(e))
    def click(self,event):
        self.running=False;p=[event.x/65,10-event.y/65];m=dict(self.map);m['obstacles']=[o[:] for o in m['obstacles']]
        mode=self.edit.get()
        if mode=='Başlangıç':m['start']=p
        elif mode=='Hedef':m['goal']=p
        elif mode=='Engel ekle':m['obstacles'].append(p+[.4])
        else:
            if len(m['obstacles'])<=1:return
            j=int(np.argmin([np.linalg.norm(np.array(o[:2])-p) for o in m['obstacles']]))
            m['obstacles'].pop(j)
        if not reachable(m):messagebox.showwarning('Geçersiz düzenleme','Robot boyutuna uygun geçiş doğrulanamadı.');return
        self.map=m;self.reset()
    def draw(self):
        c=self.canvas;c.delete('all')
        def disk(p,r,col):
            x,y=p[0]*65,(10-p[1])*65;c.create_oval(x-r*65,y-r*65,x+r*65,y+r*65,fill=col,outline='')
        for x in range(11):c.create_line(x*65,0,x*65,650,fill='#e0e6ef');c.create_line(0,x*65,650,x*65,fill='#e0e6ef')
        for x,y,r in self.map['obstacles']:disk([x,y],r,'#62738b')
        disk(self.map['goal'],GOAL_RADIUS,'#12a88b');disk(self.map['start'],.12,'#e7a63d')
        if len(self.path)>1:c.create_line(*[z for p in self.path for z in (p[0]*65,(10-p[1])*65)],fill='#126ec9',width=3)
        disk(self.p,RADIUS,'#126ec9')
        c.create_line(self.p[0]*65,(10-self.p[1])*65,(self.p[0]+.4*np.cos(self.theta))*65,(10-self.p[1]-.4*np.sin(self.theta))*65,fill='#092544',width=3)
    def tick(self):
        if self.running:
            obs=np.array(self.map['obstacles'])[None,:,:];goal=np.array([self.map['goal']]);p=self.p[None,:]
            x=sense(p,np.array([self.theta]),goal,obs);u=control(x,self.weights)[0]
            self.theta=float(wrap(self.theta+u[1]*DT));q=self.p+u[0]*DT*np.array([np.cos(self.theta),np.sin(self.theta)])
            clearance=segment_clearance(p,q[None,:],obs)[0]
            self.minimum=min(self.minimum,clearance);self.length+=float(np.linalg.norm(q-self.p));self.steps+=1;self.p=q;self.path.append(q.copy())
            if clearance<=0:self.status='Çarpışma';self.running=False
            elif np.linalg.norm(q-goal[0])<=GOAL_RADIUS:self.status='Başarı';self.running=False
            elif self.steps>=STEPS:self.status='Zaman aşımı';self.running=False
            a=activation(x)[0];top=np.argsort(-a)[:5];mu=memberships(x)
            lines=[self.label,self.status,f'Süre: {self.steps*DT:.1f} s',f'Yol: {self.length:.2f} m',f'En az açıklık: {self.minimum:.3f} m',f'v={u[0]:.3f} m/s, ω={u[1]:.3f} rad/s','', 'Normalize girdiler:']
            for name,value in zip(['Ön','Sol','Sağ','Açı','Hedef uzaklığı'],x[0]):lines.append(f'{name}: {value:.3f}')
            lines+=['','Üyelikler:']+[np.array2string(v[0],precision=2) for v in mu]
            lines+=['','En etkin kurallar:']+[f'{i}: {RULES[i].tolist()} α={a[i]:.3f}' for i in top]
            self.info.delete('1.0','end');self.info.insert('1.0','\n'.join(lines));self.draw()
        self.root.after(40,self.tick)

if __name__=='__main__':Demo().root.mainloop()
