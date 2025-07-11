(function() {
    // 启用严格模式，帮助捕获常见错误
    'use strict';

    // 临时变量，用于存储indexcode的值
    var cookieTemp = "";

    // 使用Object.defineProperty来定义/修改window对象的indexcode属性
    Object.defineProperty(window, 'indexcode', {
        // setter函数，当设置indexcode属性时触发
        set: function(val) {
            console.log('Hook捕获到window设置indexcode->', val);
            debugger;
            // 将值存储在临时变量中
            cookieTemp = val;
            return val;
        },
        // getter函数，当获取indexcode属性时触发
        get: function() {
            // 返回临时变量中存储的值
            return cookieTemp;
        }
    });
})();