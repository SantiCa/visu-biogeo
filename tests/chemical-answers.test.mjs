import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {answerMatches} from '../engine.mjs';

const catalog=JSON.parse(readFileSync(new URL('../data/species.json',import.meta.url)));
const entry=id=>catalog.find(x=>x.id==='molecula-'+id);

test('chemical names accept documented short answers without accepting a different form',()=>{
 for(const [id,yes,no] of [
  ['vitamina-b3-niacina','ácido nicotínico','nicotinamida'],
  ['vitamina-a-retinol','retinol','retinal'],
  ['vitamina-b6-piridoxina','piridoxina','piridoxal'],
  ['vitamina-d','colecalciferol','ergocalciferol'],
  ['vitamina-k-fitomenadiona','filoquinona','menaquinona'],
  ['nadh','NADH','NAD+'],
  ['atp','adenosintrifosfato','ADP'],
 ]){
  const item=entry(id);assert.ok(item,id);
  assert.ok(answerMatches(yes,item),`${id}: ${yes}`);
  assert.ok(!answerMatches(no,item),`${id} must reject ${no}`);
 }
});
