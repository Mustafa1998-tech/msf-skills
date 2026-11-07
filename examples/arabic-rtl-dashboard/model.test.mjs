import test from 'node:test';
import assert from 'node:assert/strict';
import { rows, selectRows, counts } from './model.mjs';

test('finds a shipment by either language and its isolated reference', () => {
  for (const query of ['الرياض', 'riyadh', 'MC-4182']) {
    assert.equal(selectRows(rows, {query}).some(row => row.id === 'MC-4182'), true);
  }
});
test('combines hub, status and search without mutating the original order', () => {
  const snapshot = rows.map(row => row.id);
  const found = selectRows(rows, {query:'ال', hub:'ruh', status:'moving', sort:'asc'});
  assert.ok(found.length > 0);
  assert.ok(found.every(row => row.hub === 'ruh' && row.status === 'moving'));
  assert.deepEqual(rows.map(row => row.id), snapshot);
});
test('calculates independent totals from the example dataset', () => {
  const totals = counts(rows);
  assert.equal(totals.total, rows.length);
  assert.equal(totals.moving + totals.delivered + totals.delayed, totals.total);
});
