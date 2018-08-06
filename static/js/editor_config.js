var E = window.wangEditor;
    var editor = new E('#div1');
    var $text1 = $('#text1');
    // 自定义菜单配置
    editor.customConfig.menus = [
        'head',
        'bold',
        'italic',
        'underline',
        'emoticon',
        'code'
    ];
    editor.customConfig.onchange = function (html) {
        // 监控变化，同步更新到 textarea
        $text1.val(html)
    };
    editor.create();
    // 初始化 textarea 的值
    $text1.val(editor.txt.html());

