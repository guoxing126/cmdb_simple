(function (jQuery) {
    var requestUrl = "";
    var GLOBAL_CHOCICES = {};

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            // 请求头中设置一次csrf-token
            if(!csrfSafeMethod(settings.type)){
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            }
        }
    });

    function getChoiceNameById(choice_name, id) {
        var val;
        var status_choices_list = GLOBAL_CHOCICES[choice_name];
        $.each(status_choices_list, function (kkkk, vvvv) {
            if (id == vvvv[0]) {
                val = vvvv[1];
            }
        });
        return val;
    }

    String.prototype.format = function (args) {
        return this.replace(/\{(\w+)\}/g, function (s, i) {
            return args[i];
        });
    };

    function init() {
        $('#loading').removeClass('hide');
        $.ajax({
            url: requestUrl,
            type: 'GET',
            data: {},
            dataType: 'JSON',
            success: function (response) {
                // 处理choices
                initChoices(response.global_choice_dict);
                // 处理表头
                initTableHead(response.table_config);
                // 处理表内容
                initTableBody(response.data_list, response.table_config);
                $('#loading').addClass('hide');

            },
            error: function () {
                $('#loading').addClass('hide');
            }
        })
    }

    function initChoices(global_choice_dict) {
        GLOBAL_CHOCICES = global_choice_dict;
    }

    function initTableHead(table_config) {
        $('#tHead tr').empty();
        $.each(table_config, function (k, conf) {
            if (conf.display) {
                var th = document.createElement('th');
                th.innerHTML = conf.title;
                $('#tHead tr').append(th)
            }
        })
    }

    function initTableBody(data_list, table_config) {
        $.each(data_list, function (k, row_dict) {
            //{'hostname':'xx','sn':'xx','os_platform':'xx'},
            //{'hostname':'xx','sn':'xx','os_platform':'xx'},
            var tr = document.createElement('tr');
            $.each(table_config, function (kk, vv) {
                if (vv.display) {
                    var td = document.createElement('td');
                    //td.innerHTML=row_dict[vv.q];
                    //td.innerHTML=vv.text.tpl;
                    // 处理tD内容
                    var format_dict = {};
                    $.each(vv.text.kwargs, function (kkk, vvv) {
                        //'q':'hostname',
                        //'title':'主机名',
                        //'text': {'tpl': '{a1}-{a2}','kwargs':{'a1':'@hostname','a2':'666'}},
                        if (vvv.substring(0, 2) == "@@") {
                            var name = vvv.substring(2, vvv.length);
                            var val = getChoiceNameById(name, row_dict[vv.q]);
                            format_dict[kkk] = val;
                        }
                        else if (vvv[0] == "@") {
                            var name = vvv.substring(1, vvv.length);
                            format_dict[kkk] = row_dict[name];
                        } else {
                            format_dict[kkk] = vvv
                        }
                    });
                    //td.innerHTML=vv.text.tpl.format(vv.text.kwargs);
                    td.innerHTML = vv.text.tpl.format(format_dict);
                    // 处理tD属性
                    $.each(vv.attr, function (attrName, attrVal) {
                        if (attrVal[0] == "@") {
                            attrVal = row_dict[attrVal.substring(1, attrVal.length)]
                        }
                        td.setAttribute(attrName, attrVal);
                    });
                    $(tr).append(td);
                }
            });
            $('#tBody').append(tr)
        });
    }


    function tdIntoEditMode($td) {
        //替换标签
        if ($td.attr('edit-type') === 'select') {
            var choicekey = $td.attr('choice-key');
            var origin = $td.attr('origin');
            var tag = document.createElement('select');
            $.each(GLOBAL_CHOCICES[choicekey], function (k, value) {
                var opt = document.createElement('option');
                opt.innerHTML = value[1];
                opt.value = value[0];
                if (value[0] == origin) {
                    //当select循环option时，有selecetd那默认选择该项，没有则选第一个
                    opt.setAttribute('selected', 'selected');
                }
                tag.appendChild(opt);
            });
            $td.html(tag);

        } else {
            var text = $td.text();
            var tag = document.createElement('input');
            tag.setAttribute('type', 'text');
            tag.className = 'form-control';
            tag.value = text;
            $td.html(tag);
        }
    }

    function tdOuttoEditMode($td) {
        var editStatus = false;
        var origin = $td.attr('origin');
        if ($td.attr('edit-type') === 'select') {
            var val = $td.find('select').val();
            // var text=$td.find('select')[0].selectedOptions[0].innerText;
            var text = $td.find('select option[value="' + val + '"]').text();
            $td.attr('new-value', val);
            $td.html(text);
        } else {
            var val = $td.find('input').val();
            $td.html(val);
        }
        if (origin != val) {
            editStatus = true;
        }
        return editStatus;
    }

    function trIntoEditMode($tr) {
        $tr.addClass('success');
        $tr.find('td[edit="true"]').each(function () {
            tdIntoEditMode($(this));
        })
    }

    function trOutEditMode($tr) {
        $tr.removeClass('success');
        $tr.find('td[edit="true"]').each(function () {
            if (tdOuttoEditMode($(this))) {
                $tr.attr('edit-status', 'true')
            }
        })
    }

    // 单独的checkbox绑定事件
    function bindEditModeEvent() {
        $('#tBody').on('click', ':checkbox', function () {
            if ($('#editModeStatus').hasClass('btn-warning')) {
                if ($(this).prop('checked')) {
                    //进入编辑模式
                    var $tr = $(this).parent().parent();
                    $tr.addClass('success');
                    $tr.find('td[edit="true"]').each(function () {
                        tdIntoEditMode($(this));
                    })
                } else {
                    //退出编辑模式
                    var $tr = $(this).parent().parent();
                    $tr.removeClass('success');
                    $tr.find('td[edit="true"]').each(function () {
                        if (tdOuttoEditMode($(this))) {
                            $tr.attr('edit-status', 'true')
                        }
                    })
                }
            }
        })
    }

    // 按钮组绑定事件
    function bindBtnGroupEvent() {
        // 全选
        $('#checkAll').click(function () {
            $('#tBody :checkbox').each(function () {
                if (!$(this).prop('checked')) {
                    //选中
                    $(this).prop('checked', true);
                    // 进入编辑模式
                    if ($('#editModeStatus').hasClass('btn-warning')) {
                        var $tr = $(this).parent().parent();
                        trIntoEditMode($tr);
                    }
                }
            })
        });
        // 取消
        $('#checkCancel').click(function () {
            $('#tBody :checked').each(function () {
                if ($(this).prop('checked')) {
                    //取消
                    $(this).prop('checked', false);
                    // 退出编辑模式
                    if ($('#editModeStatus').hasClass('btn-warning')) {
                        var $tr = $(this).parent().parent();
                        trOutEditMode($tr);
                    }
                }
            })
        });
        // 删除
        $('#delMulti').click(function () {
            // 弹出模态对话框
            // 给确定按钮绑定事件
            var ids=[];
            $('#tBody :checked').each(function () {
                ids.push($(this).val());
            });
            // 发送delete请求
            $.ajax({
                url:requestUrl,
                type:'delete',
                data:{'ids_list':ids},
                headers:{'x-':$.cookie('csrftoken')},
                success:function (arg) {
                    console.log(arg);
                }
            })
        });
        // 进入和退出编辑模式
        $('#editModeStatus').click(function () {
            if ($(this).hasClass('btn-warning')) {
                // 退出编辑模式
                $(this).removeClass('btn-warning');
                $(this).text('进入编辑模式')
                $('#tBody :checked').each(function () {
                    var $tr = $(this).parent().parent();
                    trOutEditMode($tr)
                })
            } else {
                // 进入编辑模式
                $(this).addClass('btn-warning');
                $(this).text('退出编辑模式');
                $('#tBody :checked').each(function () {
                    var $tr = $(this).parent().parent();
                    trIntoEditMode($tr)
                })
            }
        })

    }

    jQuery.extend({
        "js_showhtml": function (url) {
            requestUrl = url;
            init();
            //此处写分页函数
            bindEditModeEvent();
            bindBtnGroupEvent();
        }
    });

})(jQuery);
