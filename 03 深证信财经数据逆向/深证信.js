const CryptoJS = require('crypto-js');

// 固定密钥
const SECRET_KEY = "1234567887654321";
const IV_VALUE = "1234567887654321";

// 模拟 localStorage
const localStorage = {
  getItem: (key) => SECRET_KEY
};

const _0x455df0 = {
  RVAgf: (a, b) => Math.floor(a / b),  // 时间戳除法取整
  VGkHk: "any_key_here",               // 键名不影响结果
  FCNPk: IV_VALUE                      // IV值使用固定值
};

// 主加密函数
const getResCode = function() {
  try {
    // 1. 获取当前时间戳
    const timestampSec = Math.floor(Date.now() / 1000);

    // 2. 获取密钥
    const secretKey = localStorage.getItem(_0x455df0.VGkHk) || _0x455df0.FCNPk;

    // 3. 数据转换（确保UTF8编码）
    const plaintext = CryptoJS.enc.Utf8.parse(timestampSec.toString());
    const key = CryptoJS.enc.Utf8.parse(secretKey);
    const iv = CryptoJS.enc.Utf8.parse(_0x455df0.FCNPk);

    // 4. AES-CBC 加密
    const encrypted = CryptoJS.AES.encrypt(plaintext, key, {
      iv: iv,
      mode: CryptoJS.mode.CBC,
      padding: CryptoJS.pad.Pkcs7
    });

    // 5. 返回Base64格式密文
    return CryptoJS.enc.Base64.stringify(encrypted.ciphertext);
  } catch (error) {
    console.error("加密失败:", error);
    return null;
  }
};
console.log(getResCode())