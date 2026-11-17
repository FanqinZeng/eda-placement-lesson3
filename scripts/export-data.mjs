import {PRESETS,evaluate} from '../site/assets/models.mjs';
import {writeFileSync} from 'node:fs';
writeFileSync('video/data.json',JSON.stringify(Object.fromEntries(Object.entries(PRESETS).map(([k,pins])=>[k,{pins,metrics:evaluate(pins,'A'),hubs:Object.fromEntries(pins.map(p=>[p.id,evaluate(pins,p.id).star]))}])),null,2)+'\n');
