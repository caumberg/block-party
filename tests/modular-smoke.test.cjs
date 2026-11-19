// Run: node --test tests/modular-smoke.test.cjs
// Static smoke tests only. They do not replace browser, Android, or Supabase tests.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const scripts = [...html.matchAll(/<script\b[^>]*\bsrc=["'](js\/[^"']+)["']/g)].map(m => m[1]);
const styles = [...html.matchAll(/<link\b[^>]*\bhref=["'](css\/[^"']+)["']/g)].map(m => m[1]);
const app = scripts.map(s => fs.readFileSync(path.join(root, s), 'utf8')).join('\n');

test('all 13 scripts are referenced and exist', () => {
 assert.equal(scripts.length, 13);
 for (const file of scripts) assert.ok(fs.existsSync(path.join(root, file)), file);
});
test('all 42 stylesheets are referenced and exist', () => {
 assert.equal(styles.length, 42);
 for (const file of styles) assert.ok(fs.existsSync(path.join(root, file)), file);
});
test('Level 150 does not require a four-block match', () => {
 assert.match(app, /requiresFourMatch=l\.n>=151/);
 assert.match(app, /won=left<=6&&\(!requiresFourMatch\|\|fourMatchMade\)/);
});
test('campaign result is sent to the server and returned stars are displayed', () => {
 assert.match(app, /bp_campaign_complete/);
 assert.match(app, /p_won:!!result\.won/);
 assert.match(app, /d\.earned_stars/);
 assert.match(app, /bpShowCampaignStars\?\.\(a\.level,earned/);
});
test('server response is used to refresh campaign progress', () => {
 assert.match(app, /unlocked=Math\.max\(unlocked,Number\(d\.unlocked_level\)/);
 assert.match(app, /stars=d\.stars\|\|stars;selected=a\.level;render\(\)/);
});
