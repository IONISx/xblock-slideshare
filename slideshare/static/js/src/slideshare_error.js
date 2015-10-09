function SlideshareXBlock(runtime, element) {
    var iframe = $('iframe', element);
    var exception = $('xblock-slideshare-error-exception', element);
    var slideUrl = iframe.attr('src');
    var eventUrl = runtime.handlerUrl(element, 'publish_event');

    var data = {
            'event_type': 'xblock.slideshare.error',
            url: slideUrl,
            exception: exception,
        };

    $.post(eventUrl, JSON.stringify(data));
}
