/**
 * Created by mike on 08/04/2016.
 */

function up(id){
    var scr = document.getElementById(id).innerHTML;
    console.log(scr);
    var finalScr = parseInt(scr) + 1;
    console.log(finalScr);
    document.getElementById(id).innerHTML = finalScr;
    window.location.replace("upvote/"+id);
}

function down(id){
    var scr = document.getElementById(id).innerHTML;
    console.log(scr);
    var finalScr = parseInt(scr) - 1;
    console.log(finalScr);
    document.getElementById(id).innerHTML = finalScr;
    window.location.replace("downvote/"+id);
}