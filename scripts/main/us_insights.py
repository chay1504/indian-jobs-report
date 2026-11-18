import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
d = [x for x in d if x["jobs"] and x["exposure"] is not None]
J = sum(x["jobs"] for x in d); W = sum(x["jobs"]*(x["pay"] or 0) for x in d)
print("occupations", len(d), "jobs", J, "wages $T", round(W/1e12,2))
print("job-weighted exposure", round(sum(x["exposure"]*x["jobs"] for x in d)/J,2))
print("wage-weighted exposure", round(sum(x["exposure"]*x["jobs"]*(x["pay"] or 0) for x in d)/W,2))
for t in (7,8):
    g=[x for x in d if x["exposure"]>=t]
    print(f">= {t}: jobs {sum(x['jobs'] for x in g)/J:.1%}, wages {sum(x['jobs']*(x['pay'] or 0) for x in g)/W:.1%}")
# top-paid 10% of jobs: exposure
s = sorted(d, key=lambda x: -(x["pay"] or 0)); acc=0; grp=[]
for x in s:
    if acc >= 0.10*J: break
    grp.append(x); acc += x["jobs"]
print("top-paid ~10% of jobs avg exposure", round(sum(x["exposure"]*x["jobs"] for x in grp)/acc,2), "share of wages", round(sum(x["jobs"]*x["pay"] for x in grp)/W,3))
cats={}
for x in d:
    c=cats.setdefault(x["category"],[0,0,0]); c[0]+=x["jobs"]; c[1]+=x["jobs"]*x["exposure"]; c[2]+=x["jobs"]*(x["pay"] or 0)
for k,v in sorted(cats.items(), key=lambda kv:-kv[1][0]):
    print(f"  {k:40s} {v[0]/1e6:6.1f}M  exp {v[1]/v[0]:.1f}  pay ${v[2]/v[0]:,.0f}")
print("top 15 largest occupations:")
for x in sorted(d,key=lambda x:-x["jobs"])[:15]: print(f"  {x['title'][:45]:45s} {x['jobs']/1e6:5.2f}M exp {x['exposure']} pay ${x['pay'] or 0:,}")
