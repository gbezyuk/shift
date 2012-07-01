function fetch_sidebar_height() {
    var $sidebar = $('.catalog_widget');
    var $rest = $sidebar.parent();//$('.rest');
    var rest_height = $rest.height();
    $sidebar.height(rest_height);
}

$(function () {
    $(window).resize(fetch_sidebar_height);
    fetch_sidebar_height();
    setInterval(fetch_sidebar_height, 500);
});