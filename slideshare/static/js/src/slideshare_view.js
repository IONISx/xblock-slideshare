function SlideshareXBlock(runtime, element) {
    var iframe = $('iframe', element);
    var slideUrl = iframe.attr('src');
    var eventUrl = runtime.handlerUrl(element, 'publish_event');

    var data = {
            'event_type': 'xblock.slideshare.loaded',
            url: slideUrl,
        };

    $.post(eventUrl, JSON.stringify(data));
}
