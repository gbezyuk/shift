function fetch_sidebar_height() {
    var $sidebar = $('.catalog_widget');
    $sidebar.height($sidebar.parent().height());
}

$(function () {
    $(window).resize(fetch_sidebar_height);
    fetch_sidebar_height();
});