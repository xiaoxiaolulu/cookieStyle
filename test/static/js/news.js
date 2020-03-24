$(function () {
    let csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $("#newsFormModal").on('shown.bs.modal', function () {
        $('#newsInput').trigger('focus')
    });

    $("#postNews").click(function () {
        if ($("#newsInput").val() === '') {
            alert("请输入新闻动态的内容");
            return;
        }
        if (currentUser === "") {
            alert("请登录后在发布状态");
            return;
        } else {
            $.ajax({
                url: '/news/post-news/',
                data: $("#postNewsForm").serialize(),
                type: 'POST',
                cache: false,
                success: function (data) {
                    $("ul.stream").prepend(data);
                    $("#newsInput").val("");
                    $("#newsFormModal").modal("hide");
                    // hide_stream_update();
                },
                error: function (data) {
                    alert(data.responseText);
                },
            });
        }
    });

    $("ul.stream").on("click", ".like", function () {
        // Ajax call on action on like button.
        var li = $(this).closest("li");
        var news = $(li).attr("news-id");
        var payload = {
            'news': news,
            'csrf_token': csrftoken
        };
        $.ajax({
            url: '/news/like/',
            data: payload,
            type: 'POST',
            cache: false,
            success: function (data) {
                $(".like .like-count", li).text(data.likes);
                if ($(".like .heart", li).hasClass("fa fa-heart")) {
                    $(".like .heart", li).removeClass("fa fa-heart");
                    $(".like .heart", li).addClass("fa fa-heart-o");
                } else {
                    $(".like .heart", li).removeClass("fa fa-heart-o");
                    $(".like .heart", li).addClass("fa fa-heart");
                }
            }
        });
        return false;
    });

    $('#replayFormModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var recipient = button.data('who');
        var newsid = button.data('newsid');
        var modal = $(this);
        modal.find('.modal-title').text('新的回复 ' + recipient);
        modal.find('.modal-body input#recipient-name').val(recipient);
        modal.find('.modal-body input#newsid').val(newsid)
    });

    $("#postReply").click(function () {
        if ($("#reply-content").val() === '') {
            alert("请输入提问内容");
            return;
        }
        if (currentUser === "") {
            alert("请登录后在发布评论");
            return;
        } else {
            $.ajax({
                url: '/news/post-reply/',
                data: $("#postReplyForm").serialize(),
                type: 'POST',
                cache: false,
                success: function (data) {
                    let li = $('[news-id=' + data.newsid + ']');
                    $(".reply .reply-count", li).text(data.replies_count);
                    $("#reply-content").val("");
                    $("#replayFormModal").modal("hide");
                },
                error: function (data) {
                    alert(data.responseText);
                },
            });
        }
    });

    $("ul.stream").on("click", ".reply", function () {
        var li = $(this).closest("li");
        var newsId = $(li).attr("news-id");
        $.ajax({
            url: '/news/get-relies/',
            data: {'newsId': newsId},
            cache: false,
            success: function (data) {
                $("#replyListModal .modal-body").html(data.replies);
            }
        });
    });
});
