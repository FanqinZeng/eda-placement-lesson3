import test from 'node:test';
import assert from 'node:assert/strict';
import {mapPlaybackTime} from '../site/assets/player.mjs';
const zh=[{start:0,end:10},{start:10,end:30},{start:30,end:40}];
const en=[{start:0,end:15},{start:15,end:25},{start:25,end:45}];
test('voice switching preserves scene and fraction despite different narration lengths',()=>{
 assert.equal(mapPlaybackTime(5,zh,en),7.5);
 assert.equal(mapPlaybackTime(20,zh,en),20);
 assert.equal(mapPlaybackTime(35,zh,en),35);
 assert.equal(mapPlaybackTime(10,zh,en),15);
});
test('start/end and round trip are stable; invalid times fall back to start',()=>{
 assert.equal(mapPlaybackTime(-1,zh,en),0);assert.equal(mapPlaybackTime(NaN,zh,en),0);
 assert.equal(mapPlaybackTime(40,zh,en),45);assert.equal(mapPlaybackTime(99,zh,en),45);
 for(const t of [0,2,9.9,10,16,29.99,30,39.9])assert.ok(Math.abs(mapPlaybackTime(mapPlaybackTime(t,zh,en),en,zh)-t)<1e-8);
 assert.equal(mapPlaybackTime(5,[],en),0);
});
