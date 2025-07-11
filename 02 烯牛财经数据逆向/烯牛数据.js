// npm install crypto-js
const CryptoJS = require('crypto-js');

const _keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
const _p = "W5D80NFZHAYB8EUI2T649RT2MNRMVE2O";

function e1(e) {
    if (e == null) return null;
    let t, n, r, o, i, a, u;
    let c = "",
    l = 0;
    while (l < e.length) {
        t = e.charCodeAt(l++);
        o = t >> 2;
        n = e.charCodeAt(l++);
        i = ((3 & t) << 4) | (n >> 4);
        r = e.charCodeAt(l++);
        a = ((15 & n) << 2) | (r >> 6);
        u = 63 & r;
        if (isNaN(n)) {
            a = u = 64;
        } else if (isNaN(r)) {
            u = 64;
        }
        c += _keyStr.charAt(o) + _keyStr.charAt(i) + _keyStr.charAt(a) + _keyStr.charAt(u);
    }
    return c;
}

function _u_e(e) {
    if (e == null) return null;
    e = e.replace(/\r\n/g, "\n");
    let t = "";
    for (let n = 0; n < e.length; n++) {
        let r = e.charCodeAt(n);
        if (r < 128) {
            t += String.fromCharCode(r);
        } else if (r < 2048) {
            t += String.fromCharCode((r >> 6) | 192);
            t += String.fromCharCode((r & 63) | 128);
        } else {
            t += String.fromCharCode((r >> 12) | 224);
            t += String.fromCharCode(((r >> 6) & 63) | 128);
            t += String.fromCharCode((r & 63) | 128);
        }
    }
    return t;
}

function e2(e) {
    e = _u_e(e);
    if (e == null) return null;
    let t = "";
    for (let n = 0; n < e.length; n++) {
        let r = _p.charCodeAt(n % _p.length);
        t += String.fromCharCode(e.charCodeAt(n) ^ r);
    }
    return t;
}

function sig(e) {
    return CryptoJS.MD5(e + _p).toString().toUpperCase();
}

function d1(e) {
    let t,
    n,
    r,
    o,
    i,
    a;
    let u = "",
    c = 0;
    e = e.replace(/[^A-Za-z0-9\+\/\=]/g, "");
    while (c < e.length) {
        t = _keyStr.indexOf(e.charAt(c++)) << 2;
        o = _keyStr.indexOf(e.charAt(c++));
        n = ((15 & o) << 4) | (_keyStr.indexOf(e.charAt(c++)) >> 2);
        r = ((3 & _keyStr.indexOf(e.charAt(c - 1))) << 6) | _keyStr.indexOf(e.charAt(c++));
        u += String.fromCharCode(t | (o >> 4));
        if (64 != _keyStr.indexOf(e.charAt(c - 2))) u += String.fromCharCode(n);
        if (64 != _keyStr.indexOf(e.charAt(c - 1))) u += String.fromCharCode(r);
    }
    return u;
}

function _u_d(e) {
    let t = "",
    n = 0;
    while (n < e.length) {
        let r = e.charCodeAt(n);
        if (r < 128) {
            t += String.fromCharCode(r);
            n++;
        } else if (r > 191 && r < 224) {
            let o = e.charCodeAt(n + 1);
            t += String.fromCharCode(((r & 31) << 6) | (o & 63));
            n += 2;
        } else {
            let o = e.charCodeAt(n + 1);
            let i = e.charCodeAt(n + 2);
            t += String.fromCharCode(((r & 15) << 12) | ((o & 63) << 6) | (i & 63));
            n += 3;
        }
    }
    return t;
}

function d2(e) {
    let t = "";
    for (let n = 0; n < e.length; n++) {
        let r = _p.charCodeAt(n % _p.length);
        t += String.fromCharCode(e.charCodeAt(n) ^ r);
    }
    return _u_d(t);
}
function get_content(dd) {
    let d = d1(dd);
    let y = JSON.parse(d2(d));
    return y;
}
function get_list(n) {
    let s = n;
    let f = e1(e2(JSON.stringify(s.payload)));
    let p = sig(f);
    return [f, p];
}