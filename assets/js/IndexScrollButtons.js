var TriggeredWo;
var TriggeredCard;

function mOver(MouseOver_id){
    TriggeredWo = "Wo" + MouseOver_id;
    TriggeredCard = MouseOver_id;
    document.getElementById(TriggeredWo).style.display= "block";
    document.getElementById(TriggeredCard).style.height= "17em";
    document.getElementById(TriggeredCard).style.transform= "scale(1.05) translateY(0.7em)";
    document.getElementById(TriggeredCard).style.boxShadow= "0 2px 5px 0 rgba(0,0,0,0.2),0 2px 10px 0 rgba(0,0,0,0.2)";
}
function mOut(MouseOut_id){
    document.getElementById(TriggeredWo).style.display= "none";
    document.getElementById(TriggeredCard).style.height= "10em";
    document.getElementById(TriggeredCard).style.transform= "scale(1)";
    document.getElementById(TriggeredCard).style.boxShadow= "0 2px 5px 0 rgba(0,0,0,0.16),0 2px 10px 0 rgba(0,0,0,0.12)";
}

function leftScroll(ScrollButton_Id){
    var elmnt = document.getElementById('Carusell' + ScrollButton_Id);
    elmnt.scrollLeft -= 332;
}
function rightScroll(ScrollButton_Id){
    var elmnt = document.getElementById('Carusell' + ScrollButton_Id);
    elmnt.scrollLeft += 332;
}