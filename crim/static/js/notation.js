function attachPhraseClickEvents() {
    $('.view-phrase').on({
        'click': function(event) {
            var is_analysis;
            if ($(this).data('phrasenum')) {
                is_analysis = false;
            }
            else {
                is_analysis = true;
            }

            $("#phrase-modal").remove();
            var modal = $("<div />", {
                "id": "phrase-modal",
            }).appendTo("body");

            // Distinguish between Phrase and Analysis slices
            var title_string;
            if (is_analysis) {
                title_string = ($(this).data('pieceid') + ', measures ' +
                    $(this).data('start') + '–' + $(this).data('stop'))
            }
            else {
                title_string = $(this).data('pieceid') + ', phrase ' +
                    $(this).data('phrasenum')
            }

            $("#phrase-modal").dialog({
                'height': 520,
                'width': 980,
                'modal': true,
                'title': title_string,
            });
            $("<div />", {
                "class": "phrase-modal-body"
            }).appendTo(modal);

            ajaxRenderPhrase(
                $(this).data('meilink'),
                $(this).data('start'),
                $(this).data('stop'),
                is_analysis
            );
            return false;
        }
    });
}

function ajaxRenderPhrase(mei_link, start, end, is_analysis) {
    var loadedXML = meiView.Util.loadXMLDoc(mei_link);
    var filteredXml = meiView.filterMei(loadedXML, { noSysBreak:true });
    var meiDoc = new MeiLib.MeiDoc(filteredXml);

    var pagination = new meiView.Pages();

    /* If you want scrolling: */
    pagination.AddPage(start, end);

    /* If you want pagination rather than scrolling:

    // Throughout, -1 appears because measures are not counted "logically"
    var max_m = start;

    while (max_m < end) {
        if (end - (max_m - 1) < 8) {
            // Less than 8 measures left: fit it all in
            pagination.AddPage(max_m, end);
            max_m = end;
        }
        else if (end - (max_m - 1) < 12) {
            // To avoid uneven cramming at the end, consider pages of 5
            pagination.AddPage(max_m, max_m + 4);
            max_m += 5;
        }
        else {
            pagination.AddPage(max_m, max_m + 3);
            max_m += 4;
        }
    }
    */

    var modal_viewer = new meiView.CompactViewer({
        maindiv: $('.phrase-modal-body'),
        MEI: meiDoc,
        pages: pagination,
        title: "",
        displayFirstPage: true,
        scale: 0.8,
        mode: meiView.Mode.SINGLE_PAGE,
        pxpMeasure: 280,
    });

    var modal = $("#phrase-modal");
}
