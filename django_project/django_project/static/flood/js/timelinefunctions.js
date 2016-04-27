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

function displayRiverLevels(riverlevels){
    //var substr = location.search.substr(1); //search url for input
    //var dates = substr.split("+"); //get dates seperated by + in url
    for (river in riverlevels) {

        var dateTaken = new Date(river.date_taken); //get the date_taken of river level
        if (dateTaken >= new Date(dates[0]) && dateTaken <= new Date(dates[1])) { //check river level date corresponds to dates requested
            //console.log("{{ river.place }}")
            //console.log("{{ river.river_level }}")
            if (river.place == "Leeds") { //populate leeds graph with relevant data
                traceLeeds.x.push(river.date_taken);
                traceLeeds.y.push(river.river_level);
            }
            else if (river.place == "Kirkstall") { //populat kirkstall graph with relevant data
                traceKirk.x.push(river.date_taken);
                traceKirk.y.push(river.river_level);
            }
            else if (river.place == "castleford") { //populate castleford graph
                traceCastl.x.push(river.date_taken);
                traceCastl.y.push(river.river_level);
            }
            else if (river.place == "tadcaster") { //populate tadcaster graph
                traceTad.x.push(river.date_taken);
                traceTad.y.push(river.river_level);
            }
            else if (river.place == "mytholmroyd") { //populate mytholmroyd graph
                traceMyth.x.push(river.date_taken);
                traceMyth.y.push(river.river_level);
            }
        }
        else if (dates[0] == "") { //no dates selected by user so no dates present in url.
            if (river.place.toLowerCase() == "leeds") { //populate leeds graph with relevant data
                traceLeeds.x.push(river.date_taken);
                traceLeeds.y.push(river.river_level);
            }
            else if (river.place.toLowerCase() == "kirkstall") { //populat kirkstall graph with relevant data
                traceKirk.x.push(river.date_taken);
                traceKirk.y.push(river.river_level);
            }
            else if (river.place.toLowerCase() == "castleford") { //populate castleford graph
                traceCastl.x.push(river.date_taken);
                traceCastl.y.push(river.river_level);
            }
            else if (river.place.toLowerCase() == "tadcaster") { //populate tadcaster graph
                traceTad.x.push(river.date_taken);
                traceTad.y.push(river.river_level);
            }
            else if (river.place.toLowerCase() == "mytholmroyd") { //populate mytholmroyd graph
                traceMyth.x.push(river.date_taken);
                traceMyth.y.push(river.river_level);
            }
        }
    }
}