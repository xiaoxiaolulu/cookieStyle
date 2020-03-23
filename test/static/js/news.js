$(function () {
    $("#newsFormModal").on('shown.bs.modal', function () {
        $('#newsInput').trigger('focus')
    });

    $("#postNews").click(function () {
        if ($("#newsInput").val() === ''){
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
    })
});
