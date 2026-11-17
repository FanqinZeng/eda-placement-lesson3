import test from 'node:test';
import assert from 'node:assert/strict';
import {evaluate, PRESETS} from '../site/assets/models.mjs';
import {spawnSync} from 'node:child_process';
test('teacher goldens and asymmetric hub dependence',()=>{
 for(const [key,values] of [['golden',[4,16,8]],['starter',[16,64,32]],['asymmetric',[11,36,16]],['interior',[16,56,24]]]){
  const r=evaluate(PRESETS[key],'A');assert.deepEqual([r.bbox,r.clique,r.star],values);assert.equal(r.pairs.length,6);assert.equal(r.spokes.length,3);
 }
 assert.deepEqual(['A','B','C','D'].map(h=>evaluate(PRESETS.asymmetric,h).star),[16,22,14,20]);
});
test('empty, single, two pins and invalid inputs have explicit behavior',()=>{
 assert.equal(evaluate([]).bbox,0);assert.equal(evaluate([{id:'A',x:2,y:3}],'A').star,0);
 const r=evaluate([{id:'A',x:0,y:1},{id:'B',x:3,y:5}],'A');assert.deepEqual([r.bbox,r.clique,r.star],[7,7,7]);
 for(const pins of [[{id:'A',x:NaN,y:0}],[{id:'A',x:'',y:0}],[{id:'A',x:0,y:0},{id:'A',x:1,y:2}]])assert.throws(()=>evaluate(pins));
 assert.throws(()=>evaluate(PRESETS.golden,'Z'));
});
test('independent Python agrees on 300 deterministic inputs and model invariants',()=>{
 let seed=2603;const rand=()=>{seed=(1664525*seed+1013904223)>>>0;return seed%17-8};
 const inputs=Array.from({length:300},(_,i)=>Array.from({length:1+i%8},(_,j)=>({id:String(j),x:rand(),y:rand()})));
 const p=spawnSync('python3',['site/downloads/reference.py'],{input:JSON.stringify(inputs),encoding:'utf8'});assert.equal(p.status,0,p.stderr);
 const expected=JSON.parse(p.stdout);
 inputs.forEach((pins,i)=>{const r=evaluate(pins,pins[0].id);assert.deepEqual([r.bbox,r.clique,r.star],expected[i]);
  assert.equal(pins.reduce((s,h)=>s+evaluate(pins,h.id).star,0),2*r.clique);
  assert.equal(evaluate(pins.map(p=>({...p,x:p.x+11,y:p.y-5})),pins[0].id).clique,r.clique);
  assert.equal(evaluate(pins.map(p=>({...p,x:p.x*3,y:p.y*3})),pins[0].id).star,3*r.star);
 });
});
