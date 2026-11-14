// Tests of the page's pure functions.  run_tests.py puts the functions'
// source, copied from web/index.html, above this file and runs the two
// together, so this file names them as the page does.  It uses nothing
// beyond the language itself, so it runs in Node and in JavaScriptCore.

const say = typeof print === 'function' ? print : console.log;
let checks = 0;
const failures = [];
function same(what, got, want) {
  checks++;
  const g = JSON.stringify(got), w = JSON.stringify(want);
  if (g !== w) failures.push(`${what}: got ${g}, expected ${w}`);
}
function near(what, got, want) {
  checks++;
  if (!(typeof got === 'number' && Math.abs(got - want) <= 1e-9 * Math.abs(want))) failures.push(`${what}: got ${got}, expected ${want}`);
}

// ---------- parseCSV ----------
same('parseCSV, plain rows', parseCSV('a,b\n1,2\n'), [['a', 'b'], ['1', '2']]);
same('parseCSV, no line break at the end', parseCSV('a,b\n1,2'), [['a', 'b'], ['1', '2']]);
same('parseCSV, Windows line breaks', parseCSV('a,b\r\n1,2\r\n'), [['a', 'b'], ['1', '2']]);
same('parseCSV, old Mac line breaks', parseCSV('a,b\r1,2\r'), [['a', 'b'], ['1', '2']]);
same('parseCSV, a byte order mark is not part of the first name', parseCSV('﻿a,b\n'), [['a', 'b']]);
same('parseCSV, a quoted comma', parseCSV('"Smith, J",2\n'), [['Smith, J', '2']]);
same('parseCSV, a doubled quote', parseCSV('"say ""hi""",2\n'), [['say "hi"', '2']]);
same('parseCSV, a quoted line break', parseCSV('"Intake\nDate",b\n1,2\n'), [['Intake\nDate', 'b'], ['1', '2']]);
same('parseCSV, two spaces in a name are kept', parseCSV('Intake  Date,b\n'), [['Intake  Date', 'b']]);
same('parseCSV, empty fields', parseCSV('a,,c\n,,\n'), [['a', '', 'c'], ['', '', '']]);
same('parseCSV, an empty last field without a line break', parseCSV('a,'), [['a', '']]);
same('parseCSV, an empty line is a row of one empty field', parseCSV('a\n\nb\n'), [['a'], [''], ['b']]);
same('parseCSV, empty text', parseCSV(''), []);
same('parseCSV, a limit on the rows read', parseCSV('a\nb\nc\nd\n', 2), [['a'], ['b']]);

// ---------- checksum ----------
// Values recorded from the function on 2026-11-13. A file the page wrote
// carries such a value in its answers block, so a change to the function
// makes every such file read as edited.
same('checksum, empty text', checksum(''), 'bdcb81aee8d83');
same('checksum, a short text', checksum('date_format: "%m/%d/%Y"\n'), '1ab7ba56864359');
same('checksum, text outside ASCII', checksum('Schäferhund ≤ 2'), 'fcecdfd3194a');
same('checksum, one character changed', checksum('a') === checksum('b'), false);
same('checksum, the order of characters', checksum('ab') === checksum('ba'), false);
same('checksum, a line break at the end', checksum('a') === checksum('a\n'), false);

// ---------- fullYear and validDate ----------
// Two-digit years follow Python's %y, which ShelterDataPrep reads with:
// 69 to 99 are 1969 to 1999, and 00 to 68 are 2000 to 2068.
same('fullYear, 98', fullYear(98), 1998);
same('fullYear, 69', fullYear(69), 1969);
same('fullYear, 68', fullYear(68), 2068);
same('fullYear, 0', fullYear(0), 2000);
same('fullYear, 24', fullYear(24), 2024);
same('fullYear, four digits pass through', [fullYear(1998), fullYear(2024), fullYear(100)], [1998, 2024, 100]);
same('validDate, an ordinary date', validDate(2024, 1, 31), true);
same('validDate, 31 April', validDate(2024, 4, 31), false);
same('validDate, 29 February in a leap year', validDate(2024, 2, 29), true);
same('validDate, 29 February in another year', validDate(2023, 2, 29), false);
same('validDate, 29 February 1900', validDate(1900, 2, 29), false);
same('validDate, 29 February 2000', validDate(2000, 2, 29), true);
same('validDate, month 13', validDate(2024, 13, 1), false);
same('validDate, month 0', validDate(2024, 0, 10), false);
same('validDate, day 0', validDate(2024, 5, 0), false);
same('validDate, a two-digit year', validDate(98, 6, 15), true);
same('validDate, 29 February of the two-digit year 00, read as 2000', validDate(0, 2, 29), true);

// ---------- cutShape ----------
// One intake a day for 200 days from 2020-01-01, each leaving 10 days later.
const day = (n) => addDay('2020-01-01', n);
const steady = [];
for (let k = 0; k < 200; k++) steady.push([day(k), day(k + 10)]);
const shape = cutShape(steady, '2021-01-01');
same('cutShape, the first intake', shape.a, '2020-01-01');
same('cutShape, the first outcome', shape.b, '2020-01-11');
same('cutShape, the last outcome', shape.lastOut, '2020-07-28');
same('cutShape, stays', shape.stays, 200);
same('cutShape, stays with no outcome date', shape.open, 0);
same('cutShape, intakes before the first outcome', shape.before, 10);
same('cutShape, days from the first intake to the first outcome', shape.span, 10);
same('cutShape, intakes in the first 30 days', shape.inEdge, 30);
same('cutShape, outcomes in their first 30 days', shape.outEdge, 30);
// Away from both ends, 2020-02-10 to 2020-06-18, one of each a day: 30 in 30 days.
near('cutShape, the usual intakes in 30 days', shape.inRate, 30);
near('cutShape, the usual outcomes in 30 days', shape.outRate, 30);

// Rows the shape leaves out or counts apart.
const mixed = cutShape([...steady,
  ['2020-03-01', null],            // still in care: an intake, and counted as open
  ['2020-03-02', '?'],             // an outcome date that could not be read: an intake alone
  ['2020-03-03', '2020-03-01'],    // an outcome before the intake: an intake alone
  ['2020-03-04', '2021-06-01'],    // an outcome after today: an intake alone
  ['2021-02-01', '2021-02-05'],    // an intake after today: left out
  [null, '2020-03-05'],            // no intake date: left out
], '2021-01-01');
same('cutShape, stays among mixed rows', mixed.stays, 204);
same('cutShape, open stays among mixed rows', mixed.open, 1);
same('cutShape, the last outcome among mixed rows', mixed.lastOut, '2020-07-28');
near('cutShape, the usual intakes among mixed rows', mixed.inRate, 133 * 30 / 129);
near('cutShape, the usual outcomes among mixed rows', mixed.outRate, 30);

same('cutShape, no rows', cutShape([], '2021-01-01'), null);
same('cutShape, no outcome', cutShape([['2020-01-01', null]], '2021-01-01'), null);
const brief = cutShape(steady.slice(0, 100), '2021-01-01');
same('cutShape, too few days between the ends for a usual pace', [brief.inRate, brief.outRate], [null, null]);
same('cutShape, a short file still has its counts', [brief.stays, brief.inEdge], [100, 30]);

// ---------- verdict ----------
for (const f of failures) say('FAILED ' + f);
say(failures.length ? `${failures.length} of ${checks} checks failed` : `ok: ${checks} checks`);
