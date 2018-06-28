var fetchWorkResults = function() {
    fetchInitialResults('work', 1, '#works');
};

var fetchElementResults = function() {
    fetchInitialResults('element', 1, '#elements');
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
    if (searchtype == 'work') {
        if (window.location.search.match(/wpage/g) === null) {
            qstr = qstr + "&wpage=" + page;
        }
    }

    if (searchtype == 'element') {
        if (window.location.search.match(/epage/g) === null) {
            qstr = qstr + "&epage=" + page;
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
    if (href.match('epage')) {
        searchtype = "element";
        target = "#elements";
    } else if (href.match('wpage')) {
        searchtype = "work";
        target = "#works";
    } else {
        searchtype = "work";
        target = "#works";
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

