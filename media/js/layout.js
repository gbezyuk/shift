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

// catalog widget categories extending/collapsing
$(function () {
    $('.catalog_widget ul li.extendable.collapsing_toggler').click(function () {
        var $li = $(this);
        $li.toggleClass('extended').toggleClass('collapsed');
        return false;
    }).find('a').click(function (event) {
            event.stopPropagation();
        });
});