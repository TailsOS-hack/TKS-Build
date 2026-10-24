#!/usr/bin/env python3
"""Plot anonymous cohort-mean native Grad-CAM maps from authorized saved arrays; no inference."""
import argparse,ast,csv,hashlib,json,struct
from pathlib import Path

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def npy(p):
 b=p.read_bytes(); assert b[:6]==b'\x93NUMPY'; major=b[6]; k=2 if major==1 else 4; n=int.from_bytes(b[8:8+k],'little'); h=ast.literal_eval(b[8+k:8+k+n].decode().strip()); assert h['shape']==(7,7) and not h['fortran_order']; dtype=h['descr']; assert dtype in ('<f4','<f8'); values=struct.unpack('<'+('f' if dtype=='<f4' else 'd')*49,b[8+k+n:]); assert min(values)>=0 and sum(values)>0; return [x/sum(values) for x in values]
def main():
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);a=p.parse_args();s=a.source;r=a.root
 manifest=json.loads((s/'SHA256SUMS.json').read_text()); rows=list(csv.DictReader((s/'per_case.csv').open())); out={}
 for model in ('old_baseline','candidate_3'):
  selected=[x for x in rows if x['model']==model and x['role']=='reused_original100']; assert len(selected)==100
  maps=[]
  for x in selected:
   rel='maps/'+model+'_'+x['case_id']+'.npy'; f=s/rel; assert sha(f)==manifest[rel]; maps.append(npy(f))
  out[model]=[sum(v[i] for v in maps)/100 for i in range(49)]
 payload={'scope':'Cohort mean of 100 reused original100 native maps per model; each map normalized by its sum before averaging. No MRI images, case identifiers or new inference.','n_per_model':100,'grid_shape':[7,7],'source_manifest_sha256':sha(s/'SHA256SUMS.json'),'mean_score_mass':out}
 (r/'results/mean_native_gradcam.json').write_text(json.dumps(payload,indent=2)+'\n')
 maxv=max(max(v) for v in out.values());svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="620" viewBox="0 0 1000 620"><rect width="1000" height="620" fill="white"/><g font-family="sans-serif" fill="#162536"><text x="32" y="35" font-size="24">Actual saved Grad-CAM: cohort-mean native 7×7 maps</text><text x="32" y="64" font-size="15">100 reused original100 maps per model · per-map sum normalization · common color scale</text>']
 for panel,(model,values) in enumerate(out.items()):
  left=45+panel*485;svg.append(f'<text x="{left}" y="108" font-size="20">{model}</text>')
  for i,v in enumerate(values):
   t=v/maxv; rgb=(int(244-213*t),int(249-133*t),int(254-74*t));x=left+(i%7)*60;y=125+(i//7)*60
   svg.append(f'<rect x="{x}" y="{y}" width="60" height="60" fill="rgb{rgb}" stroke="white"/><text x="{x+30}" y="{y+35}" text-anchor="middle" font-size="12" fill="'+('white' if t>.6 else '#162536')+f'">{v*100:.2f}%</text>')
 svg+=['<text x="32" y="580" font-size="15">Cell labels: mean normalized score mass. Coarse, overlapping receptive fields; no anatomical or causal claim.</text>','<text x="32" y="604" font-size="14">Derived from actual archived arrays, not synthetic examples. These aggregate maps do not display individual MRI scans.</text></g></svg>']
 (r/'figures/mean_native_gradcam.svg').write_text(''.join(svg))
 print('Verified and aggregated 200 saved arrays; no individual records exported.')
if __name__=='__main__':main()
