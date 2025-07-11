const fs               = require('fs');
const usefulPlugins    = require("./tools/usefulPlugins");
const decodeObfuscator = require("./tools/decodeOb");


//js混淆代码读取
process.argv.length > 2 ? encodeFile = process.argv[2]: encodeFile ="./input/crypto-js.js";
process.argv.length > 3 ? decodeFile = process.argv[3]: decodeFile ="./output/crypto-js.js";

//将源代码解析为AST
let sourceCode = fs.readFileSync(encodeFile, {encoding: "utf-8"});
let ast    = parser.parse(sourceCode);

console.time("处理完毕，耗时");

//traverse(ast, Demo1);
//traverse(ast, Demo2);
//traverse(ast, Demo3);
//traverse(ast, Demo4);
//traverse(ast, Demo5);
/*
traverse(ast, mytest1);
traverse(ast, get_name_Array);
traverse(ast, replace_name_Array);
traverse(ast, Del_Dai);
traverse(ast, replace_unicode);
*/


//字面量解混淆
console.log("traverse Hex or Unicode String.......");
traverse(ast, simplifyLiteral);

console.log("constantFold.......");

traverse(ast, constantFold);

console.log("delete Repeat Define.......");

traverse(ast, deleteRepeatDefine);

traverse(ast, SimplifyIfStatement);

traverse(ast, standardLoop);

console.log("resolve Sequence.......");

traverse(ast, resolveSequence);

console.log("traverse CallExpress To ToLiteral.......");

traverse(ast, CallExpressToLiteral);

console.log("constantFold.......");

traverse(ast, constantFold);


//object key值Literal
console.log("Object Preconditioning .......");

traverse(ast, keyToLiteral);

traverse(ast, preDecodeObject);

//处理object

// console.log("Object Decode .......");
//
//
// traverse(ast, decodeObject);


console.log("Control Flow Decoding.......\n");

traverse(ast, decodeControlFlow);

console.log("constantFold.......");

traverse(ast, constantFold);

console.log("remove Dead Code.......\n");

traverse(ast, removeDeadCode);

ast = parser.parse(generator(ast).code);

traverse(ast, removeDeadCode);

traverse(ast, simplifyLiteral);


//可能会误删一些代码，可屏蔽

traverse(ast, deleteObfuscatorCode);


console.timeEnd("处理完毕，耗时");


// traverse(ast, replace_DAi);
// traverse(ast, replace_Array_DAi);
//traverse(ast, solve_Switch_Case_new);
// traverse(ast, relace_Unicode);
//traverse(ast, spa13)
let {code} = generator(ast,opts = {jsescOption:{"minimal":true}});

fs.writeFile(decodeFile, code, (err) => {});