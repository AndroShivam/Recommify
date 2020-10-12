// hide loading gif and add to playlist button until button is pressed
$("#loading-img").hide();
$("#add_to_playlist_btn").hide();

// Setup plyr player
document.addEventListener('DOMContentLoaded', () => {
    const player = Plyr.setup('.js-player');
});

// Form submission
$('#home-form').on('submit', function(event){
    event.preventDefault();
    create_post();
});

// Get response using ajax
function create_post(){
    $("#loading-img").show();
    $.ajax({
        url : "get_response/",
        type : "POST",
        data : {
            artists : $('#id_artists').val(),
            genres : $('#id_genres').val(),
            tracks : $('#id_tracks').val(),
            csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken]').val()
        },
        complete:function(){
            $("#loading-img").hide();
        },
        success : function(result){
            $("#add_to_playlist_btn").show();
            document.getElementById("demo").innerHTML = `
            ${result.tracks.map(tracksTemplate).join('')}
            `
        }
    }); 
}

// Javascript template literals
function tracksTemplate(track){
    return `
    <div class = "card-bg">
        <img class = "card-photo" src = "${track.album.images[0].url}"> 
        <h3 class = "font-weight-bold">${ track.name }</h3>
        <p>${ track.artists[0].name }</p>
        <p class = "text-muted"><small>Released On : ${ track.album.release_date }</small></p>
        ${track.preview_url ? `
        <audio class="js-player">
            <source src="${ track.preview_url }" type="audio/mp3">
        </audio>
        ` : `
        <p class = "text-muted" >Audio not available</p>
        `}
    </div>
      `
}
