$(window).on("load", function(){
    if($(window).width() < 768){
        $(".main-body").css({
            "padding-right": "0px",
            "padding-left": "0px"
        });

        $(".popular-novel-list").css({
            "width": $(window).width(),
        });
    }

    $("#cog-icon").click(function(){
        $(this).toggleClass("fa-spin");

        if($(window).width() <= 768){
            $(".search-section").toggle()
        }  
    });


    $(window).resize(function(){
        if($(window).width() > 768){
            $(".search-section").css("display", "flex");       
            $(".main-body").css({
                "padding-right": "100px",
                "padding-left": "100px"
            });

            $(".popular-novel-list").css({
                "width": "auto",
            });

        }else{
            $(".search-section").css("display", "none");    
            $(".main-body").css({
                "padding-right": "0px",
                "padding-left": "0px"
            });

            $(".popular-novel-list").css({
                "width": $(window).width(),
            });
        }
    }); 
});

$(document).ready(function(){
    var novel_id = "";
    var csrf_token = "";

    $(".novel-delete-btn").click(function(){
        $(".modal-bg").addClass("modal-bg-hidden");
        novel_id = $(this).data("novelId");
        csrf_token = $(this).data("csrfToken");
        console.log(csrf_token);
    })

    $(".cancel-btn").click(function(){
        $(".modal-bg").removeClass("modal-bg-hidden");
    })

    $(".novel-confirm-btn").click(function(){
        console.log(novel_id);

        $.ajax( 
            { 
                type:"POST", 
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
                    xhr.setRequestHeader('X-CSRFToken', csrf_token);
            },
            
            url: `/delete_novel/${novel_id}`, 
            data: {test: 'test'},
            success: function(data){ 
               console.log(data);
               $(".novel-content").remove(`#novel-${novel_id}`);
               $(".modal-bg").removeClass("modal-bg-hidden");
            }
        });
    })
});

$(document).ready(function (){
    $(".novel-thumbnail").click(function (e){
        var get_novel_id = 0;
        if(! isNaN($(this).attr("id"))){
            get_novel_id = $(this).attr("id");
            window.location.href = `/chapters/${get_novel_id}`
        }
    })
})

$(document).ready(function(){
    $(".novel-item").on({
        mouseover: function(){
            var item_id = $(this).attr("id");
            $(`.p-novel-title#${CSS.escape(item_id)}`).css("background-color", "#d3d0d0");
        },

        mouseleave: function(){
            var item_id = $(this).attr("id");
            $(`.p-novel-title#${CSS.escape(item_id)}`).css("background-color", "");
        }
    });

    var list_novel_items = $(".ranking");
    console.log(list_novel_items);

    for( var item of list_novel_items){
        if($(item).attr("id") == 1){
            $(item).css({
                "background-color": "#f52525",
                "color": "white"
            })
        }

        else if($(item).attr("id") == 2){
            $(item).css({
                "background-color": "#00bcd1",
                "color": "white"
            })
        }

        else if($(item).attr("id") == 3){
            $(item).css({
                "background-color": "#c4a400",
                "color": "white"
            })
        }
    }
});


$(document).ready(function(){
    $(".user-avatar").click(function(){
        $(".user-avatar-nav").toggle();
    }); 

    $(".popular-novel-list").mousewheel(function(event, delta){
        this.scrollLeft -= (delta * 30);
        event.preventDefault();
    });
})


// testing section
$(document).ready(function(){
    var csrf_token = $("meta[name='data']").data("csrfToken");
    $(".testing-btn").click(function(){
        $.ajax( 
            { 
                type:"GET", 
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
                    xhr.setRequestHeader('X-CSRFToken', csrf_token);
            },
            
            url: `/api/novels/novel_thumbnail_api`, 
            data: {test: 'test'},
            success: function(data){ 
               console.log(data);
            }
        });
    })
})



