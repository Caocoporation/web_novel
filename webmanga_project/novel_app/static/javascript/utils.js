$(document).ready(function(){
    var chapter_id = "";
    var csrf_token = $("meta[name='data']").data("csrfToken");

    console.log($(".chapters").children());

    $(".chapter-remove-btn").on({
        click: function(){
            $(".modal-bg").addClass("modal-bg-hidden");
            chapter_id = $(this).data("chapterId");
            console.log(chapter_id);
            console.log($(".chapters").children());
        }
    })

    $(".cancel-btn").click(function(){
        $(".modal-bg").removeClass("modal-bg-hidden");
    })
    $(".chapter-confirm-btn").click(function(){
        $.ajax( 
            { 
                type:"POST", 
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
                    xhr.setRequestHeader('X-CSRFToken', csrf_token);
            },
            
            url: `/delete_chapter/${chapter_id}`, 
            data: {test: 'test'},
            success: function(data){ 
                console.log(data);
                $(`.chapters #content-${chapter_id}`).remove();
                $(".modal-bg").removeClass("modal-bg-hidden");
            }
        });  
    })
})

$(document).ready(function(){
    $(".novel-item").click(function(){
        var novel_id = $(this).attr("id");
        window.location.href = `/chapters/${novel_id}`;    
    });
})

$(document).ready(function(){
    var csrf_token = $("meta[name='data']").data("csrfToken");

    $(".search-box").on({
        keyup: function(){
            var get_value = $(".search-box").val();
            var content = "";
            $(".search-results").empty();
            
            if(get_value.length > 0){
                $.ajax( 
                    { 
                        type:"POST", 
                        beforeSend: function (xhr) {
                            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
                            xhr.setRequestHeader('X-CSRFToken', csrf_token);
                    },
                    
                    url: `/search/${get_value}`, 
                    data: {"test": 'test'},
                    success: function(data){ 
                        for(const [key, value] of Object.entries(data)){
                            if(key.length === 0){
                                content = "";
                            }else{
                                var end_point =  (value["title"].toLowerCase()).indexOf(get_value.toLowerCase());
                                var first_sub = "";
                                var second_sub = "";
                                var highlight_key = "";
                                var temp = "";
                               
                                first_sub = value["title"].substring(0, (end_point));
                                highlight_key = value["title"].substring(end_point, (end_point + get_value.length));
                                second_sub = value["title"].substring((end_point + get_value.length), value["title"].length);
    
                                var highlight = `<span class="let-highlight" style="font-weight: 800; background-color: yellow;">${highlight_key}</span>`;
                                temp = `<div class="searched-novel" id="${value["id"]}">${first_sub}${highlight}${second_sub}</div>`
                               
                                content = content + temp;
                                
                            }
                        }
    
                        $(".search-results").append(content);

                        $(".search-results").on({
                            click: function(){
                                window.location.href = `/chapters/${novel_id}`;    
                            },

                            mouseenter: function(){
                                $(this).css("background-color", "gray");
                            },

                            mouseleave: function(){
                                $(this).css("background-color", "");
                            },

                        }, ".searched-novel");
                    }
                });  
            }
        }  
    })
});



