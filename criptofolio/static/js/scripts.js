let shownExchanges = 10;
function showMore() {
    let exchanges = document.getElementById("exchange-list").children;
    for (let i = shownExchanges; i < shownExchanges + 10; i++) {
        exchanges[i].style.display = "block";
    }
    shownExchanges += 10;
}
