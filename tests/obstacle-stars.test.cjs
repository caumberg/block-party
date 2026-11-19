const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname,'../js/script-04.js'),'utf8');
const handler = source.match(/const left=Number\(e\.data\.remaining\)\|\|0;[^\n]+/);
assert.ok(handler, 'Obstacle finish handler not found');
const logic = handler[0];
const compute = new Function('remaining','level','fourMatchMade', `
  const e={data:{remaining,fourMatchMade}};
  const l={n:level};
  ${logic}
  return {won,score:won?Math.max(1,1000-left):0};
`);
const stars = score => score>=1000?3:score>=997?2:score>=994?1:0;
for(const [left, expected] of [[0,3],[1,2],[3,2],[4,1],[6,1]]) {
 test(`Level 150 with ${left} blocks awards ${expected} star(s) without four-match`,()=>{
  const r=compute(left,150,false);
  assert.equal(r.won,true);
  assert.equal(stars(r.score),expected);
 });
}
test('Level 150 with seven blocks is a loss',()=>{
 const r=compute(7,150,false);
 assert.equal(r.won,false);
 assert.equal(stars(r.score),0);
});
test('Level 151 requires a four-match',()=>{
 assert.equal(compute(0,151,false).won,false);
 assert.equal(compute(0,151,true).won,true);
});
