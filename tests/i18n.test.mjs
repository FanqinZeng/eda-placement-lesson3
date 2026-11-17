import test from 'node:test';
import assert from 'node:assert/strict';
import {translate,getLanguage} from '../site/assets/i18n.mjs';
test('English lesson values preserve mathematical meaning',()=>{
 assert.equal(translate('学习记录 · 3 / 12 已完成','en'),'Progress · 3 / 12 completed');
 assert.equal(translate('第 2/6 对：A–C = 2。当前累计 2 + 2 = 4。','en'),'Pair 2/6: A–C = 2. Running sum: 2 + 2 = 4.');
 assert.match(translate('当前单个 ABCD net：HPWL 4，Clique 16，Star-from-A 8。它们的数值口径不同，不能直接据此给模型排名。','en'),/^Current ABCD net: HPWL 4, Clique 16, Star-from-A 8\./);
});
test('Composite exercise feedback and accessible pin names are translated',()=>{
 assert.equal(translate('再想一想：当前模型值是 16。六项为 2、2、4、4、2、2，总和 16。','en'),'Try again: The current model value is 16. The six terms are 2, 2, 4, 4, 2, and 2; their sum is 16.');
 assert.equal(translate('引脚 A，坐标 2,4，方向键移动','en'),'Pin A, coordinates 2,4, move with arrow keys');
 assert.equal(translate('HPWL 的“半”是什么意思？','zh'),'HPWL 的“半”是什么意思？');
 assert.equal(getLanguage(),'zh');
});
