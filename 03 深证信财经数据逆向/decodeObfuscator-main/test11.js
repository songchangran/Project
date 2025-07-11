const { spawn } = require('child_process');

// spawn('node -e console.log("Hello world!");', (error, stdout, stderr) => {
//   if (error) {
//     console.error(`执行失败：${error}`);
//     return;
//   }
//   console.log(`stdout: ${stdout}`);
//   console.error(`stderr: ${stderr}`);
// });
// var ggg = 123
// const child = spawn('node', ['-e', 'console.log("Hello world!");']);
// child.stdout.on('data', (data) => {
//   //console.log(1111111111,`${data}`.replace(/^\s+|\s+$/g, ''))
//   //console.log(1111111111,`${data}`.trim())
//   var output = `${data}`.trim()
//   console.log(output)
// });
// console.log(11111111,output)
// console.log(output)
// child.on('close', () => {
//   const result = eval('console.log("Hello world!");');
//   // console.log(output + result); // 输出 "Hello world!undefined"
// });

// const helllo = eval('console.log("Hello world!");'); // helllo 的值为 undefined

// 暂存原始的 console.log 方法
const originalLog = console.log;

// 重写 console.log 方法
console.log = function wrapper() {
  const result = [];
  for (let i = 0; i < arguments.length; i++) {
    result.push(arguments[i]);
  }
  originalLog.apply(console, arguments); // 执行原始的 console.log 方法

  // 返回打印的值
  if (result.length === 1) {
    return result[0];
  }
  return result;
};
 'var KGI = AJgjJ.EMf()[12][18];for (; KGI !== AJgjJ.EMf()[12][15];) {
  switch (KGI) {
    case AJgjJ.EMf()[12][18]:
      console.log("var t = 0;KGI = AJgjJ.EMf()[4][17];break;");
      KGI = AJgjJ.EMf()[4][17]
      break;

    case AJgjJ.EMf()[12][17]:
      console.log("if (e) {\n  t = parseInt(e);\n\n  if (t !== t) {\n    t = 0;\n  }\n}KGI = AJgjJ.EMf()[4][16];break;");
      KGI = AJgjJ.EMf()[4][16]
      break;

    case AJgjJ.EMf()[12][16]:
      return t;
      break;
  }
}'
var hello = eval(
              'console.log("return yhkl(59) in body[yhkl(70)] || yhkl(29) in body[yhkl(70)] || xmaS(25) in body[xmaS(70)] || yhkl(1) in body[xmaS(70)];break;")'
    )
console.log(hello)
// 使用已重写的 console.log 方法
// const greeting = 'Hello, world!';
// const result = console.log('The greeting is', greeting);
// console.log('The result is:', result);

// 恢复原始的 console.log 方法
// console.log = originalLog;

// 使用未重写的 console.log 方法
// console.log('This message will not return any value.');

