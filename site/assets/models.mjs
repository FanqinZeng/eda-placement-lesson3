/** Unit-weight Manhattan net models; no routing or legality claim. */
export const PRESETS={
 golden:[[2,2],[4,2],[2,4],[4,4]],starter:[[0,0],[8,0],[0,8],[8,8]],
 asymmetric:[[0,0],[6,0],[1,2],[2,5]],interior:[[0,0],[8,0],[0,8],[4,4]]
};
for(const key of Object.keys(PRESETS))PRESETS[key]=PRESETS[key].map(([x,y],i)=>({id:'ABCD'[i],x,y}));
export function evaluate(pins,hub=pins?.[0]?.id){
 if(!Array.isArray(pins))throw new TypeError('引脚必须是数组');
 const ids=new Set();
 for(const p of pins){if(!p||typeof p.id!=='string'||!p.id||ids.has(p.id)||!Number.isFinite(p.x)||!Number.isFinite(p.y))throw new TypeError('引脚名称不可重复，坐标必须是有限数值');ids.add(p.id);}
 if(pins.length&&!ids.has(hub))throw new TypeError('中心必须是当前引脚');
 const box=pins.length?{minX:Math.min(...pins.map(p=>p.x)),maxX:Math.max(...pins.map(p=>p.x)),minY:Math.min(...pins.map(p=>p.y)),maxY:Math.max(...pins.map(p=>p.y))}:{minX:0,maxX:0,minY:0,maxY:0};
 const edge=(a,b)=>({from:a.id,to:b.id,value:Math.abs(a.x-b.x)+Math.abs(a.y-b.y)});
 const pairs=[];for(let i=0;i<pins.length;i++)for(let j=i+1;j<pins.length;j++)pairs.push(edge(pins[i],pins[j]));
 const h=pins.find(p=>p.id===hub),spokes=pins.filter(p=>p.id!==hub).map(p=>edge(h,p));
 return {bbox:box.maxX-box.minX+box.maxY-box.minY,clique:pairs.reduce((s,e)=>s+e.value,0),star:spokes.reduce((s,e)=>s+e.value,0),box,pairs,spokes};
}
