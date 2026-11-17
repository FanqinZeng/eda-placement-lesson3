import {evaluate} from './models.mjs';
export function diagram(pins,kind,hub='A',limit=Infinity,interactive=false){
 const r=evaluate(pins,hub),xy=p=>[40+p.x*30,290-p.y*30],find=id=>pins.find(p=>p.id===id),color={bbox:'#ddbd78',clique:'#86a9e0',star:'#76cbb5'}[kind];
 let marks='';for(let i=0;i<=8;i++){marks+=`<path d="M40 ${290-i*30}H280 M${40+i*30} 50V290" stroke="#253a42" stroke-width=".6"/>`;marks+=`<text x="${40+i*30}" y="310" class="tick">${i}</text><text x="24" y="${294-i*30}" class="tick">${i}</text>`;}
 if(kind==='bbox'){const a=xy({x:r.box.minX,y:r.box.maxY}),b=xy({x:r.box.maxX,y:r.box.minY});marks+=`<rect x="${a[0]}" y="${a[1]}" width="${b[0]-a[0]}" height="${b[1]-a[1]}" fill="${color}" fill-opacity=".06" stroke="${color}" stroke-width="2" stroke-dasharray="6 4"/>`;}
 else for(const [i,e] of (kind==='clique'?r.pairs:r.spokes).entries()){if(i>=limit)break;const a=xy(find(e.from)),b=xy(find(e.to));marks+=`<path d="M${a[0]} ${a[1]}H${b[0]}V${b[1]}" stroke="${color}" stroke-opacity="${i===limit-1?1:.65}" stroke-width="${i===limit-1?3:1.5}" fill="none"/>`;}
 for(const p of pins){const [x,y]=xy(p);marks+=`<g ${interactive?`class="pin" data-pin="${p.id}" tabindex="0" role="button" aria-label="引脚 ${p.id}，坐标 ${p.x},${p.y}，方向键移动"`:''}><circle cx="${x}" cy="${y}" r="${kind==='star'&&p.id===hub?12:9}" fill="#0b2029" stroke="${kind==='star'&&p.id===hub?color:'#eeeadd'}" stroke-width="2"/><text x="${x+13}" y="${y-11}" fill="#eeeadd" font-size="14">${p.id}</text></g>`;}
 return `<svg viewBox="0 0 330 335" role="img" aria-label="${kind}模型，原点左下，x和y范围0至8"><title>${kind} 网络模型；点坐标见下方输入表</title>${marks}<text x="300" y="294" class="tick">x</text><text x="36" y="30" class="tick">y</text></svg>`;
}
