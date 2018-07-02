var fetchPieceResults = function() {
    fetchInitialResults('piece', 1, '#pieces');
};

var fetchRelationshipResults = function() {
    fetchInitialResults('relationship', 1, '#relationships');
};

var fetchFacets = function() {
    qstr = window.location.search.replace("?", "");

    $.ajax({
        url: '/search/results/facet',
        data: qstr,
        success: function(data) {
            $('#facets').empty();
            $('#facets').append(data);

            qstr_params = $.parseParams(qstr);
            jQuery.each(qstr_params, function(param, val) {
                if (typeof val == "object") {
                    $.each(val, function(num, v) {
                        $("input[name='" + param + "'][value='" + v + "']").attr('checked', true);
                    });
                } else {
                    $("input[name='" + param + "'][value='" + val + "']").attr('checked', true);
                }
            });
        }
    });
};

var attachFacetActions = function() {
    $('.facet-refine').on({
        'click': function(event) {
            qstr = window.location.search.replace("?", "");
            var p = $(this).attr('name');
            var v = $(this).attr('value');
            if ($(this).is(':checked')) {
                qstr_add = "&" + p + "=" + v;
                window.location.search = qstr + qstr_add;
            } else {
                console.log("Unchecked!");
                qstr_remove = qstr.replace('&' + p + "=" + encodeURI(v), "");
                console.log(qstr_remove);
                window.location.search = qstr_remove;
            }
        }
    });
};

var fetchInitialResults = function(searchtype, page, target) {
    var qstr = window.location.search.replace("?", "");
    if (searchtype == 'piece') {
        if (window.location.search.match(/piece_page/g) === null) {
            qstr = qstr + "&piece_page=" + page;
        }
    }

    if (searchtype == 'relationship') {
        if (window.location.search.match(/relationship_page/g) === null) {
            qstr = qstr + "&relationship_page=" + page;
        }
    }

    $.ajax({
        url: '/search/results/' + searchtype,
        data: qstr,
        success: function(data) {
            $(target).empty();
            $(target).append(data);
        }
    });
};

var searchPageCallback = function(href) {
    var searchtype;
    var target;
    if (href.match('relationship_page')) {
        searchtype = "relationship";
        target = "#relationships";
    } else if (href.match('piece_page')) {
        searchtype = "piece";
        target = "#pieces";
    } else {
        searchtype = "piece";
        target = "#pieces";
    }

    href = href.replace("?", "");

    $.ajax({
        url:'/search/results/' + searchtype,
        data: decodeURIComponent(href),
        success: function(data) {
            $(target).empty();
            $(target).append(data);
        }
    });
    // return false;
};

var attachPagerActions = function() {
    $('.pagination a').on({
        'click': function(event) {
            searchPageCallback($(this).attr('href'));
            return false;
        }
    });
};
