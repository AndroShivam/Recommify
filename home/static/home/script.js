// hide loading gif and add to playlist button until button is pressed
$("#loading-img").hide();
$("#add_to_playlist_btn").hide();

// Setup plyr player
document.addEventListener('DOMContentLoaded', () => {
    const player = Plyr.setup('#js-player');
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
            document.getElementById("result").innerHTML = `${result.tracks.map(tracksTemplate).join('')}`
        }
    }); 
}


// Javascript template literals to show result cards
function tracksTemplate(track){
    return `
    <div class="card mb-3">
    <div class="row no-gutters">
      <div class="col-md-4">
        <img src = ${track.album.images[0].url} class="card-img" alt="Error loading image">
      </div>
      <div class="col-md-8">
        <div class="card-body">
          <h5 class="card-title font-weight-bold">${ track.name }</h5>
          <p class="card-text">${ track.artists[0].name }</p>
          <p class="card-text"><small>Released On : ${ track.album.release_date }</small></p>
        </div>
      </div>
    </div>
  </div>
  `
}