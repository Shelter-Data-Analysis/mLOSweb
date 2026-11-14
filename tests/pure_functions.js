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

// ---------- timeShape and readDate ----------
// The four formats of step 4 and the time shapes that may follow a date.
// The shape is the place in TIMES: 0 none, 1 hours:minutes, 2 with seconds,
// 3 hours:minutes AM or PM, 4 with seconds and AM or PM; -1 is not read.
same('the formats, in the order step 4 prefers them', FORMATS.map(f => f.py), ['ISO8601', '%m/%d/%Y', '%d/%m/%Y', '%m/%d/%y']);
same('the time shapes, as ShelterDataPrep patterns', TIMES.map(t => t.py), ['', ' %H:%M', ' %H:%M:%S', ' %I:%M %p', ' %I:%M:%S %p']);
const [ISO, MDY, DMY, MDY2] = FORMATS;
const shapes = (v) => FORMATS.map(f => timeShape(v, f));
same('timeShape, a bare month/day/year', shapes('1/31/2024'), [-1, 0, -1, -1]);
same('timeShape, a date either order reads', shapes('5/6/2024'), [-1, 0, 0, -1]);
same('timeShape, a two-digit year', shapes('1/31/24'), [-1, -1, -1, 0]);
same('timeShape, hours and minutes', shapes('1/31/2024 0:00'), [-1, 1, -1, -1]);
same('timeShape, hours, minutes, and seconds', shapes('1/31/2024 14:30:59'), [-1, 2, -1, -1]);
same('timeShape, AM or PM', shapes('1/31/2024 1:05 PM'), [-1, 3, -1, -1]);
same('timeShape, AM or PM in small letters, with seconds', shapes('1/31/2024 12:00:00 am'), [-1, 4, -1, -1]);
same('timeShape, a time after a two-digit year', shapes('6/15/98 0:00'), [-1, -1, -1, 1]);
same('timeShape, day/month/year with a time', shapes('31/1/2024 14:30'), [-1, -1, 1, -1]);
same('timeShape, two spaces before the time', timeShape('1/31/2024  0:00', MDY), 1);
same('timeShape, hour 24', timeShape('1/31/2024 24:00', MDY), -1);
same('timeShape, minute 60', timeShape('1/31/2024 9:60', MDY), -1);
same('timeShape, hour 13 with PM', timeShape('1/31/2024 13:05 PM', MDY), -1);
same('timeShape, hour 0 with AM', timeShape('1/31/2024 0:05 AM', MDY), -1);
same('timeShape, no space before PM', timeShape('1/31/2024 1:05PM', MDY), -1);
same('timeShape, a T before the time', timeShape('1/31/2024T0:00', MDY), -1);
same('timeShape, a fraction of a second', timeShape('1/31/2024 0:00:00.000', MDY), -1);
same('timeShape, text after the date', timeShape('1/31/2024x', MDY), -1);
same('timeShape, a date that does not exist, with a time', timeShape('2/30/2024 0:00', MDY), -1);
same('timeShape, year-month-day', shapes('2024-01-31'), [0, -1, -1, -1]);
same('timeShape, year-month-day with a time has no shape of its own', [timeShape('2024-01-31 14:30', ISO), timeShape('2024-01-31T14:30:00', ISO)], [0, 0]);
same('timeShape, a year-month-day date that does not exist', timeShape('2024-02-30', ISO), -1);
same('readDate, the date beside a time', readDate('1/31/2024 14:30', MDY, 1), '2024-01-31');
same('readDate, a value of another time shape is not read', [readDate('1/31/2024 14:30', MDY, 0), readDate('1/31/2024', MDY, 1)], [null, null]);
same('readDate, day/month/year', readDate('5/6/2024 7:08', DMY, 1), '2024-06-05');
same('readDate, month/day/year of the same value', readDate('5/6/2024 7:08', MDY, 1), '2024-05-06');
same('readDate, a two-digit year before 2000', readDate('6/15/98 0:00', MDY2, 1), '1998-06-15');
same('readDate, year-month-day with a time', readDate('2024-1-5 08:00', ISO, 0), '2024-01-05');

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
