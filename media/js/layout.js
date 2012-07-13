// lightbox for every image link
$(function () {
    $('a[href$=".jpg"]')
    .add($('a[href$=".jpeg"]'))
    .add($('a[href$=".png"]'))
    .add($('a[href$=".gif"]')).lightBox(
        {
            fixedNavigation:    true,
            imageLoading:       '/media/jquery-lightbox/images/lightbox-ico-loading.gif',
            imageBtnPrev:       '/media/jquery-lightbox/images/lightbox-btn-prev.gif',
            imageBtnNext:       '/media/jquery-lightbox/images/lightbox-btn-next.gif',
            imageBtnClose:      '/media/jquery-lightbox/images/lightbox-btn-close.gif',
            imageBlank:         '/media/jquery-lightbox/images/lightbox-blank.gif'
        }
    );
});

// catalog widget categories expanding/collapsing
$(function () {
    $('ul.category_tree li.expandable.collapsing_toggler').click(function () {
        var $li = $(this);
        $li.toggleClass('expanded').toggleClass('collapsed');
        return false;
    }).find('a').click(function (event) {
            event.stopPropagation();
        });
});

$(function () {
    $('.dropdown-toggle').attr('href', '#');
});

$(function handle_color_list_hovering () {
    function swap_colors () {
        var $node = $(this);
        var tmp = $node.css('color');
        $node.css('color', $node.css('background-color'));
        $node.css('background-color', tmp);
        $node.css('border-color', tmp);
    }
    $('.compact_color_list li').hover(swap_colors, swap_colors)
});