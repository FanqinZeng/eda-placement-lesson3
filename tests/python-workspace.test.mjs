import {test} from 'node:test';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {EXAMPLES,RUN_TIMEOUT_MS,LIVE_DEBOUNCE_MS} from '../site/python/examples.mjs';
function python(code) {return spawnSync('python3',['-c',code],{encoding:'utf8',timeout:5000})}
test('reference executes actual Python and calculates all golden metrics',()=>{
 const result=python(EXAMPLES.reference);assert.equal(result.status,0,result.stderr);assert.equal(result.stdout,'BBox = 4\nClique = 16\nStar = 8\n');
});
test('editing pins changes calculated results',()=>{
 const result=python(EXAMPLES.asymmetric);assert.equal(result.status,0,result.stderr);assert.equal(result.stdout,'BBox = 11\nClique = 36\nStar = 16\n');
});
test('reference handles empty nets and alternative hub',()=>{
 const result=python(EXAMPLES.reference+'\nassert (bbox([]),clique([]),star([])) == (0,0,0)\nassert star([(0,0),(6,0),(1,2),(2,5)], 1)==22\n');assert.equal(result.status,0,result.stderr);
});
test('exercise provides executable feedback and guardrail constants are finite',()=>{
 assert.match(python(EXAMPLES.exercise).stderr,/NotImplementedError/);assert.equal(RUN_TIMEOUT_MS,5000);assert.equal(LIVE_DEBOUNCE_MS,700);
});
