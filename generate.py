"""Original finite-reservoir passive-tracer records. Code MIT; records CC0."""
import argparse,hashlib,hmac,json
from pathlib import Path
import numpy as np
VERSION='3.0.0';N=24;STEPS=240
SAMPLE=np.array([0,1,2,4,7,10,13,16,19,21,23])
def packed(obj):return json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False)
def feed(knots):return np.interp((np.arange(STEPS)+.5)/STEPS,np.linspace(0,1,6),knots)
def forward(diffusivity,opening,supply,initial,volume,flow):
    """Conservative explicit finite volumes; leading dimension batches experiments."""
    d=np.asarray(diffusivity,dtype=float);op=np.asarray(opening,dtype=float);batch=len(d)
    inlet=np.broadcast_to(supply,(batch,STEPS));initial=np.broadcast_to(initial,(batch,8))
    volume=np.broadcast_to(volume,(batch,));flow=np.broadcast_to(flow,(batch,))
    u=np.broadcast_to(initial[:,:,None],(batch,8,N)).copy();bath=inlet[:,0].copy()
    for j in range(STEPS):
        old=u.copy();b=bath.copy();active=np.clip(j+1-op,0,1)
        left=2*d*N*(b[:,None]-old[:,:,0]);right=2*d*N*(b[:,None]-old[:,:,-1])*active
        internal=d[:,:,None]*N*(old[:,:,:-1]-old[:,:,1:])
        u[:,:,:-1]-=internal*N/STEPS;u[:,:,1:]+=internal*N/STEPS
        u[:,:,0]+=left*N/STEPS;u[:,:,-1]+=right*N/STEPS
        bath+=(flow*(inlet[:,j]-b)-(left+right).sum(axis=1))/(STEPS*volume)
    return u[:,:,SAMPLE],bath
def generate(count,key):
    if type(count) is not int or not 1<=count<=100000:raise ValueError('count must be an integer in1..100000')
    if not isinstance(key,bytes) or len(key)<16:raise ValueError('key must contain at least16bytes')
    output=[]
    for start in range(0,count,128):
        batch=[]
        for i in range(start,min(count,start+128)):
            rng=np.random.default_rng(int.from_bytes(hmac.digest(key,('case/'+str(i)).encode(),'sha256'),'big'))
            cid='fb_'+hmac.digest(key,('identifier/'+str(i)).encode(),'sha256').hex()[:24]
            knots=np.round(rng.uniform(.08,.92,6),6);initial=np.round(rng.uniform(.08,.92,8),6)
            volume=round(float(rng.uniform(.35,1.2)),6);flow=round(float(rng.uniform(.3,1.)),6)
            d=rng.uniform(.004,.035,8);opening=rng.choice(np.arange(1,236),8,replace=False)
            noise=rng.normal(0,.004,(8,11));bath_noise=float(rng.normal(0,.004));assays=np.round(d*np.exp(rng.normal(0,.2,8)),6)
            batch.append((cid,knots,initial,volume,flow,d,opening,noise,bath_noise,assays))
        profiles,bath=forward(np.stack([v[5] for v in batch]),np.stack([v[6] for v in batch]),np.stack([feed(v[1]) for v in batch]),np.stack([v[2] for v in batch]),np.array([v[3] for v in batch]),np.array([v[4] for v in batch]))
        for values,p,b in zip(batch,profiles,bath):
            cid,knots,initial,volume,flow,d,opening,noise,bath_noise,assays=values
            output.append({'case_id':cid,'feed_history':knots.tolist(),'initial_concentrations':initial.tolist(),
                'bath_volume':volume,'exchange_rate':flow,'bath_final':round(float(np.clip(b+bath_noise,0,1)),3),
                'diffusivity_assays':assays.tolist(),'profiles':np.round(np.clip(p+noise,0,1),3).tolist(),
                'fracture_ranks':np.argsort(np.argsort(opening)).tolist()})
    return output
def main():
    p=argparse.ArgumentParser();p.add_argument('--count',type=int,default=32);p.add_argument('--key-hex',default='40a8a061b78b3d5240727a44d90fbb2f');p.add_argument('--output',type=Path,default=Path('demo_records.jsonl'));a=p.parse_args()
    rows=generate(a.count,bytes.fromhex(a.key_hex));content=''.join(packed(r)+'\n' for r in rows).encode('utf8');a.output.write_bytes(content)
    print(packed({'version':VERSION,'rows':len(rows),'sha256':hashlib.sha256(content).hexdigest()}))
if __name__=='__main__':main()
