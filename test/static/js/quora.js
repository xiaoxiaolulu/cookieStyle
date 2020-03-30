$(function () {
    let csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $(".question-vote").click(function () {
        let span = $(this);
        let questionId = $(this).closest(".question").attr("question-id");
        let vote = null;
        if($(this).hasClass('up-vote')){
            vote = "U";
        } else {
            vote = "D";
        }
        $.ajax({
            url: "/quora/question/vote/",
            data: {
                'questionId': questionId,
                'value': vote
            },
            type: 'post',
            cache: false,
            success: function (data) {
                $(".vote", span).removeClass('voted');
                if(vote === "U"){
                    $(span).addClass('voted');
                }
                if(vote === "D"){
                     $(span).addClass('voted');
                }
                $("#questionVotes").text(data.votes);
            }
        })
    });

    $(".answer-vote").click(function () {
        let span = $(this);
        let answer = $(this).closest(".answer").attr("answer-id");
        let vote = null;
        if($(this).hasClass('up-vote')){
            vote = "U";
        } else {
            vote = "D";
        }
        $.ajax({
            url: "/quora/answer/vote/",
            data: {
                'answerId': answer,
                'value': vote
            },
            type: 'post',
            cache: false,
            success: function (data) {
                $(".vote", span).removeClass('voted');
                if(vote === "U"){
                    $(span).addClass('voted');
                }
                if(vote === "D"){
                     $(span).addClass('voted');
                }
                $("#answerVotes-" + answer).text(data.votes);
            }
        })
    });

    $(".acceptAnswer").click(function () {
        var span = $(this);
        var answer = $(this).closest(".answer").attr("answer-id");
        $.ajax({
            url: '/quora/accept_answer/',
            data: {
                'answerId': answer
            },
            type: 'post',
            cache: false,
            success: function (data) {
                $("#acceptAnswer-" + answer).removeClass('accepted');
                $("#acceptAnswer-" + answer).prop("title", "点击接受回答");
                $("#acceptAnswer-" + answer).addClass("accepted");
                $("#acceptAnswer-" + answer).prop("title", "该回答已被采纳");
            }
        })
    })
});
