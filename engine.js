// Bitrate Math engine - recording size, capacity and average bitrate arithmetic.
// Mirrored by oracle.py; keep the op order identical.
// Decimal units: 1 MB = 1,000,000 bytes, 1 GB = 1000 MB, 1 kbps = 1000 bits per second.

function _whole(x, lo, hi, msg) {
  if (!Number.isInteger(x) || x < lo || x > hi) throw new Error(msg);
  return x;
}

function _kbps(x) { return _whole(x, 1, 1000000, "bitrate must be a whole number of kbps from 1 to 1000000"); }
function _min(x) { return _whole(x, 1, 100000, "minutes must be a whole number from 1 to 100000"); }
function _gb(x) { return _whole(x, 1, 100000, "capacity must be a whole number of GB from 1 to 100000"); }

function _hund(x, msg) {
  if (!isFinite(x) || x <= 0 || x > 1000000) throw new Error(msg);
  return Math.floor(x * 100 + 0.5);
}

function _fixed2(h) {
  var whole = Math.floor(h / 100), frac = h % 100;
  return whole + "." + (frac < 10 ? "0" : "") + frac;
}

function _fmt(h) {
  var whole = Math.floor(h / 100), frac = h % 100;
  if (frac === 0) return String(whole);
  var f = (frac < 10 ? "0" : "") + frac;
  if (f.charAt(1) === "0") f = f.charAt(0);
  return whole + "." + f;
}

function _plural(n, word) {
  return n + " " + word + (n === 1 ? "" : "s");
}

// The size truth: how big a recording at a bitrate and length is.
function sizeTruth(kbps, minutes) {
  var k = _kbps(kbps);
  var m = _min(minutes);
  var x = k * m;
  var mb = Math.floor((3 * x + 2) / 4);
  var gb = Math.floor((3 * x + 2000) / 4000);
  return k + " kbps for " + _plural(m, "minute") + ": " + _fixed2(mb) + " MB, " + _fixed2(gb) + " GB.";
}

// The fit truth: how many whole minutes a capacity holds at a bitrate.
function fitTruth(capacityGb, kbps) {
  var c = _gb(capacityGb);
  var k = _kbps(kbps);
  var mins = Math.floor(c * 400000 / (k * 3));
  var h = Math.floor(mins / 60), r = mins % 60;
  return "Capacity " + c + " GB at " + k + " kbps holds " + _plural(mins, "minute") + ", which is " +
    _plural(h, "hour") + " " + _plural(r, "minute") + ".";
}

// The rate truth: the average bitrate of a file of a known size and length.
function rateTruth(sizeMb, minutes) {
  var s = _hund(sizeMb, "size must be between 0 and 1000000 MB, over 0");
  var m = _min(minutes);
  var t = Math.floor((80 * s + 3 * m) / (6 * m));
  var whole = Math.floor(t / 10), frac = t % 10;
  var text = frac === 0 ? String(whole) : whole + "." + frac;
  return _fmt(s) + " MB over " + _plural(m, "minute") + " averages " + text + " kbps.";
}
