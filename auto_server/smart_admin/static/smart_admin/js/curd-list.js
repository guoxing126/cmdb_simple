/**
 * Created by xing on 2018/1/25.
 */

(function (jq) {

    var requestUrl;

    var GLOBAL_CHOICE_DICT = {
        // 'status_choices':[{0:'xxx'},{1:'xxx'},]
    };

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            //在请求头中设置crsftoken
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
            }
        }
    });

    function getChoiceNameById(choice_name, id) {
        var val;
        var status_choices_list = GLOBAL_CHOICE_DICT[choice_name];
        $.each(status_choices_list, function (kkkk, choice) {
            if (id == choice[0]) {
                val = choice[1];
            }
        });
        return val
    }

    String.prototype.format = function (args) {
        return this.replace(/\{(\w+)\}/g, function (s, i) {
            return args[i];
        });
    };

    function initTableName(response) {
        $('#tableName').text(response.table_name);
    }

    function init(pageNum) {
        var conditions = getSearchCondition();
        $.ajax({
            url: requestUrl,
            type: 'GET',
            traditional: true,
            data: {
                'pageNum': pageNum,
                'conditions': JSON.stringify(conditions)
            },
            dataType: 'JSON',
            success: function (response) {
                /*填写表名*/
                initTableName(response);
                /* 处理choice*/
                initChoices(response);
                /* 处理搜索条件*/
                initSearchConfig(response);
                /*处理表头*/
                initTableHead(response);
                /*定制表格内容*/
                initTableBody(response);
                /* 处理表分页*/
                initPageHtml(response);
            }
        })
    }

    function bindSearchConditionEvent() {
        /*改变下拉框内容时，触发事件*/
        $('#searchCondition').on('click', 'li', function () {
            $(this).parent().prev().prev().text($(this).text());
            $(this).parent().parent().next().remove();
            var name = $(this).find('a').attr('name');
            var type = $(this).find('a').attr('type');
            if (type == 'select') {
                var choices_name = $(this).find('a').attr('choices_name');
                /*生产select标签*/
                var tag = document.createElement('select');
                tag.setAttribute('name', name);
                tag.className = 'form-control no-radius';
                $.each(GLOBAL_CHOICE_DICT[choices_name], function (i, item) {
                    var op = document.createElement('option');
                    op.innerHTML = item[1];
                    op.setAttribute('value', item[0]);
                    tag.appendChild(op);
                })
            } else {
                /*生产input标签*/
                var tag = document.createElement('input');
                // $(tag).addClass('form-control no-radius')
                tag.className = 'form-control no-radius';
                tag.setAttribute('placeholder', '请输入条件');
                tag.setAttribute('name', name);
                tag.setAttribute('type', 'text');
            }
            $(this).parent().parent().after(tag);
        })
        /*添加搜索条件*/
        $('#searchCondition .add-condition').click(function () {
            var $condition = $(this).parent().parent().clone();
            $condition.find('.add-condition').removeClass('add-condition').addClass('del-condition');
            $condition.find('i').attr('class', 'fa fa-minus-square');
            // $(this).parent().parent().parent().append($condition);
            $condition.appendTo($('#searchCondition'))
        });
        /*删除搜索条件*/
        $('#searchCondition').on('click', '.del-condition', function () {
            $(this).parent().parent().remove();
        })
        /*点击搜索按钮*/
        $('#doSearch').click(function () {
            init(1);
        })

    }

    function tdIntoEditMode($td) {
        if ($td.attr('edit-type') == 'select') {
            //处理select
            //先取choices-key
            var choicesKey = $td.attr('choices-key');
            var origin = $td.attr('origin');
            var tag = document.createElement('select');
            $.each(GLOBAL_CHOICE_DICT[choicesKey], function (k, val) {
                var op = document.createElement('option');
                op.innerHTML = val[1];
                op.value = val[0];
                if (val[0] == origin) {
                    op.setAttribute('selected', 'selected');
                }
                tag.appendChild(op);
            });
            tag.className = 'form-control';
            $td.html(tag);

        } else if ($td.attr('edit-type') == 'input') {
            //处理input
            var text = $td.text();
            var tag = document.createElement('input');
            tag.setAttribute('type', 'text');
            tag.value = text;
            tag.className = 'form-control';
            $td.html(tag);
        }

    }

    function tdOutEditMode($td) {
        var editstatus = false;
        var origin = $td.attr('origin');
        if ($td.attr('edit-type') == 'select') {
            var val = $td.find('select').val();
            // var text=$td.find('select')[0].selectedOptions[0].innerText;
            var text = $td.find('select option[value="' + val + '"]').text();
            $td.attr('new-value', val);
            $td.html(text);
        } else if ($td.attr('edit-type') == 'input') {
            var val = $td.find('input').val();
            $td.html(val);
        }
        if (origin != val) {
            editstatus = true;
        }
        return editstatus;
    }

    function trIntoEditMode($tr) {
        // $(this)当前需要进入编辑的td标签
        $tr.addClass('success');
        $tr.find('td[edit="true"]').each(function () {
            // $(this)当前需要进入编辑的td标签
            tdIntoEditMode($(this));
        })
    }

    function trOutEditMode($tr) {
        $tr.removeClass('success');
        $tr.find('td[edit="true"]').each(function () {
            // $(this)当前需要进入编辑的td标签
            if (tdOutEditMode($(this))) {
                $tr.attr('edit-status', 'true')
            }
        })
    }

    function bindEditModeEvent() {
        // 单独的checkbox绑定事件
        $('#tBody').on('click', ':checkbox', function () {
            if ($('#editModeStatus').hasClass('btn-warning')) {
                if ($(this).prop('checked')) {
                    //进入编辑模式
                    //如果后台配置文件：edit=true,方可进入
                    var $tr = $(this).parent().parent();
                    $tr.addClass('success');
                    trIntoEditMode($tr);
                } else {
                    //退出编辑模式
                    var $tr = $(this).parent().parent();
                    $tr.removeClass('success');
                    trOutEditMode($tr);
                }
            }
            // $(this),点击当前CheckBox标签，触发事件

        })
    }

    //按钮组在绑定事件
    function bindBtnGroupEvent() {
        //进入和退出编辑模式
        $('#editModeStatus').click(function () {
            if ($(this).hasClass('btn-warning')) {
                //要退出编辑模式
                $(this).removeClass('btn-warning');
                $(this).text('进入编辑模式');
                $('#tBody :checked').each(function () {
                    var $tr = $(this).parent().parent();
                    trOutEditMode($tr);
                })
            } else {
                //要进入编辑模式
                $(this).addClass('btn-warning');
                $(this).text('退出编辑模式');
                $('#tBody :checked').each(function () {
                    var $tr = $(this).parent().parent();
                    trIntoEditMode($tr);
                })
            }
        });

        //全选
        $('#checkAll').click(function () {
            $('#tBody :checkbox').each(function () {
                if (!$(this).prop('checked')) {
                    //选中
                    $(this).prop('checked', 'true');
                    //判断editModeStatus状态，进入编辑模式
                    if ($('#editModeStatus').hasClass('btn-warning')) {
                        var $tr = $(this).parent().parent();
                        trIntoEditMode($tr);
                    }
                }
            })
        });

        //取消
        $('#checkCancel').click(function () {
            $('#tBody :checked').each(function () {
                $(this).prop('checked', false);
                if ($('#editModeStatus').hasClass('btn-warning')) {
                    var $tr = $(this).parent().parent();
                    trOutEditMode($tr);
                }
            })
        });

        //反选
        $('#checkReverse').click(function () {
            $('#tBody :checkbox').each(function () {
                if ($(this).prop('checked')) {
                    $(this).prop('checked', false);
                    //判断editModeStatus状态，进入编辑模式
                    if ($('#editModeStatus').hasClass('btn-warning')) {
                        var $tr = $(this).parent().parent();
                        trOutEditMode($tr);
                    }
                } else {
                    $(this).prop('checked', 'true');
                    //判断editModeStatus状态，进入编辑模式
                    if ($('#editModeStatus').hasClass('btn-warning')) {
                        var $tr = $(this).parent().parent();
                        trIntoEditMode($tr);
                    }
                }
            })
        });

        //删除
        $('#delMulit').click(function () {
            //显示模态对话框
            //给确定按钮绑定事件
            var delIds = [];
            $('#tBody :checked').each(function () {
                delIds.push($(this).val());
                $(this).parent().parent().remove();
            });
            $.ajax({
                url: requestUrl,
                type: 'delete',
                // data: {'delIds': delIds},
                data: JSON.stringify(delIds),
                traditional: true,
                dataType: 'JSON',
                success: function (arg) {
                    if (arg.status) {
                        //显示正确信息
                        $('#handleStatus').text('执行成功');
                        setTimeout(function () {
                            $('#handleStatus').empty()
                        }, 2000)
                    } else {
                        //显示错误信息
                        $('#handleStatus').text(arg.msg);
                    }
                }
            })
        });

        //保存
        $('#saveMulit').click(function () {
            var update_dict = [];
            $('#tBody tr[edit-status="true"]').each(function () {
                //$(this)是每一个改动的tr标签
                tmp = {};
                tmp['id'] = $(this).children().first().attr('id');
                $(this).children('[edit="true"]').each(function () {
                    //对标签内所有可编辑的td进行循环
                    var origin = $(this).attr('origin');
                    var name = $(this).attr('name');
                    if ($(this).attr('edit-type') == 'select') {
                        var newVal = $(this).attr('new-value');
                    } else if ($(this).attr('edit-type') == 'input') {
                        var newVal = $(this).text();
                    }
                    if (origin != newVal) {
                        tmp[name] = newVal;
                    }
                });
                update_dict.push(tmp);
            });
            //数据用put发送到后台
            $.ajax({
                url: requestUrl,
                type: 'put',
                data: JSON.stringify(update_dict),
                traditional: true,
                dataType: 'JSON',
                success: function (arg) {
                    if (arg.status) {
                        //显示正确信息
                        $('#handleStatus').text('执行成功');
                        setTimeout(function () {
                            $('#handleStatus').empty()
                        }, 2000)
                    } else {
                        //显示错误信息
                        $('#handleStatus').text(arg.msg);
                    }
                }
            });
            $('#editModeStatus').removeClass('btn-warning');
            $('#editModeStatus').text('进入编辑模式');
            $('#tBody :checked').each(function () {
                var $tr = $(this).parent().parent();
                trOutEditMode($tr);
            });
        })

    }


    // 给表格中的下拉框绑定change事件
    ctrlStatus = false;
    window.onkeydown = function (event) {
        if (event && event.keyCode == 17) {
            ctrlStatus = true;
        }
    };
    window.onkeyup = function (event) {
        if (event && event.keyCode == 17) {
            ctrlStatus = false;
        }
    };
    function bindSelectChangeEvent() {
        $('#tBody').on('change', 'select', function () {
            if (ctrlStatus) {
                var v = $(this).val();
                var $tr = $(this).parent().parent();
                var index = $(this).parent().index();
                $tr.nextAll().each(function () {
                    if ($(this).find(':checkbox').prop('checked')) {
                        $(this).children().eq(index).children().val(v);
                    }
                });
            }
        })
    }

    function initSearchConfig(response) {
        if (!$('#searchCondition').attr('init')) {
            var ul = $('#searchCondition :first').find('ul');
            ul.empty();
            initDefaultSearchCondition(response.search_config[0]);
            $.each(response.search_config, function (i, item) {
                var li = document.createElement('li');
                var a = document.createElement('a');
                a.innerHTML = item.title;
                a.setAttribute('name', item.name);
                a.setAttribute('type', item.type);
                if (item.type == 'select') {
                    a.setAttribute('choices_name', item.choices_name)
                }
                $(li).append(a);
                ul.append(li);
            })
            $('#searchCondition').attr('init', 'true')
        }
    }

    function initDefaultSearchCondition(item) {
        if (item.type == 'input') {
            /*生产input标签*/
            var tag = document.createElement('input');
            // $(tag).addClass('form-control no-radius')
            tag.className = 'form-control no-radius';
            tag.setAttribute('placeholder', '请输入条件');
            tag.setAttribute('name', item.name);
            tag.setAttribute('type', 'text');
        } else {
            var choices_name = $(this).find('a').attr('choices_name');
            /*生产select标签*/
            var tag = document.createElement('select');
            tag.className = 'form-control no-radius';
            tag.setAttribute('name', item.name);
            $.each(GLOBAL_CHOICE_DICT[item.choices_name], function (i, row) {
                var op = document.createElement('option');
                op.innerHTML = row[1];
                op.setAttribute('value', row[0]);
                tag.appendChild(op);
            });
        }
        $('#searchCondition').find('.input-group').append(tag);
        $('#searchCondition').find('.input-group label').text(item.title);
    }

    function initPageHtml(response) {
        $('#pagination').empty().append(response.page_html);

    }

    function initChoices(response) {
        GLOBAL_CHOICE_DICT = response.global_choices_dict
    }

    function initTableHead(response) {
        $('#tHead tr').empty();
        $.each(response.table_config, function (k, conf) {
            if (conf.display) {
                var th = document.createElement('th');
                th.innerHTML = conf.title;
                $('#tHead tr').append(th);
            }
        });
    }

    function initTableBody(respnse) {

        $("#tBody").empty();

        $.each(respnse.data_list, function (k, server_info) {
            var tr = document.createElement('tr');
            $.each(respnse.table_config, function (kk, conf) {
                if (conf.display) {
                    var td = document.createElement('td');
                    //处理td内容
                    td.innerHTML = server_info[conf.q];
                    var format_dict = {};
                    $.each(conf.text.kwargs, function (kkk, words) {
                        if (words.substring(0, 2) == "@@") {
                            var name = words.substring(2, words.length);
                            var val = getChoiceNameById(name, server_info[conf.q]);
                            format_dict[kkk] = val;
                        }
                        else if (words[0] == "@") {
                            var name = words.substring(1, words.length);
                            format_dict[kkk] = server_info[name]
                        } else {
                            format_dict[kkk] = words
                        }
                    });
                    td.innerHTML = conf.text.tpl.format(format_dict);
                    //处理td属性
                    $.each(conf.attr, function (attrName, attrVal) {
                        if (attrVal[0] == '@') {
                            attrVal = server_info[attrVal.substring(1, attrVal.length)];
                        }
                        td.setAttribute(attrName, attrVal);
                    });
                    $(tr).append(td)
                }
            });
            $('#tBody').append(tr)

        })
    }

    function getSearchCondition() {
        /*找到所有的input和select标签*/
        var result = {};
        $('#searchCondition').find('input,select').each(function () {
            var name = $(this).attr('name');
            var val = $(this).val();
            if (result[name]) {
                result[name].push(val)
            } else {
                result[name] = [val]
            }
        });
        return result
    }

    jq.extend({
        'curdList': function (url) {
            requestUrl = url;
            init(1);
            bindSearchConditionEvent();
            bindEditModeEvent();
            bindBtnGroupEvent();
            bindSelectChangeEvent();
        },
        'changePage': function (pageNum) {
            init(pageNum);
        }
    })

})(jQuery);


