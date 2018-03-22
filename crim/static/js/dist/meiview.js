/***
* meiview.js
* Author: Zoltan Komives
* Contributor: Raffaele Viglianti
* 
* Copyright © 2013 Zoltan Komives, Raffaele Viglianti
* University of Maryland
* 
* Licensed under the Apache License, Version 2.0 (the "License"); you
* may not use this file except in compliance with the License.  You may
* obtain a copy of the License at
* 
*    http://www.apache.org/licenses/LICENSE-2.0
* 
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
* implied.  See the License for the specific language governing
* permissions and limitations under the License.
***/


// the default line thickness is 2, but this renders poorly with meiView's scaling
if (typeof Vex !== 'undefined') Vex.Flow.STAVE_LINE_THICKNESS = 1;

meiView = {};

// Define the list of supplied staff types we will be using.
// (Perhaps this could be automated in the future.)
meiView.VarTypeList = {
  'reconstruction':
      { 'title': 'editor',
        'attr': 'resp', 
        'el': 'rdg',
        'parent': 'app',
      },
  'concordance':
      { 'title': 'source[type="concordance"]',
        'attr': 'source', 
        'el': 'rdg',
        'parent': 'app',
      },
  'blank':
      { 'title': null,
        'attr': null,
        'el': 'rdg',
        'parent': 'app',
      },
}

meiView.Util = {};

meiView.Util.loadXMLDoc = function(filename) {
  if (window.XMLHttpRequest) {
    // code for IE7+, Firefox, Chrome, Opera, Safari
    xmlhttp=new XMLHttpRequest();
  } else {
    // code for IE6, IE5
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
  xmlhttp.open("GET",filename,false);
  xmlhttp.send();
  if (!xmlhttp.responseXML) throw filename + ' cannot be loaded.';
  return xmlhttp.responseXML;
}

meiView.SelectedSuppliedPartList = function(type_name) {
  this.init(type_name);
}

meiView.SelectedSuppliedPartList.prototype.init = function (type_name){
  this.origins = {};
  this.var_type = type_name;
}

meiView.SelectedSuppliedPartList.prototype.toggleSuppliedPart = function(origin) {
  this.origins[origin] = !this.origins[origin];
}

meiView.SelectedSuppliedPartList.prototype.originsList = function() {
  var res = [];
  $.each(this.origins, function(i, e) {
    if (e) {
      res.push(i);
    }
  });
  return res;
}

meiView.Viewer = function(options) {
  this.init(options);
}

meiView.DISPLAY_MEASURE_NUMBERS = {
  NONE: 0,
  ALL: 1,
/*TODO:  
  EVERY_5: 5,
  EVERY_10: 5,
  SYSTEM: 'SYSTEM',
*/
}


/**
 * Constructor of the MEI Viewer.
 * 
 * @options.param MEI the rich MEI document (XML DOM object)
 * @options.width the width of the canvas in pixels
 * @options.height the height of the canvas in pixels
 * @options.pano {Boolean} whether the display should be panoramic, or system-breaking
 * @options.rich {Boolean} whether to display rich features (grren dots, selectable staevs, etc.) or display 
 *       the lemma flat, without any interactive controls
 */
meiView.Viewer.prototype.init = function(options){

  var randomID = function() {
    return ("0000" + (Math.random()*Math.pow(36,4) << 0).toString(36)).substr(-8)
  }

  this.id = options.id || randomID();
  this.MEI = options.MEI;
  this.MEI.initSectionView();
  this.display_measure_numbers = options.display_measure_numbers;
  if (options.pages) {
    this.pages = options.pages;
  } else {
    this.pages = new meiView.Pages();
    if (this.parsePages) {
      this.parsePages(this.MEI);
    }
  }
  this.scoreWidth = options.width || 1200; // 1000
  this.scoreHeight = options.height || 1000;
  this.createSourceList(this.MEI.ALTs);
  
  // Create an object of supplied parts. Reconstructions, concordances,
  // and any other supplied parts can be added to this object.
  this.SuppliedPartLists = {};
  for (var var_type in meiView.VarTypeList) {
    this.SuppliedPartLists[var_type] = this.createSuppliedPartList(var_type);
  }

  // Create dictionary of selected part lists, matching the
  // part lists which have been created
  this.selectedSuppliedPartLists = {};
  for (var var_type in meiView.VarTypeList) {
    this.selectedSuppliedPartLists[var_type] = new meiView.SelectedSuppliedPartList(var_type);
  }

  this_viewer = this;
  this.UI = new meiView.UI({
    viewer: this_viewer,
    maindiv: options.maindiv,
    title: options.title,
  });
}

meiView.Viewer.prototype.toggleSuppliedPart = function(var_type, origin) {
  this.selectedSuppliedPartLists[var_type].toggleSuppliedPart(origin);
  this.selectSuppliedParts();
}

meiView.Viewer.prototype.createSuppliedPartList = function(var_type) {
  var title = (meiView.VarTypeList[var_type])['title'];
  var attr = (meiView.VarTypeList[var_type])['attr'];
  var el = (meiView.VarTypeList[var_type])['el'];
  var result = {};
  var me = this;

  if (attr) {
    var origins = $(this.MEI.rich_head).find('fileDesc').find(title);
    $(origins).each(function(i) {
      var orig_id = $(this).attr('xml:id');
      if (!orig_id) {
        throw ("Origin ID is undefined");
      }
      if ($(me.MEI.rich_score).find(el + '[' + attr + '="#' + orig_id + '"]').length > 0) {
        result[orig_id] = this;
      }
    });
  }
  else {
    if ($(me.MEI.rich_score).find(el + '[type="' + var_type + '"]').length > 0) {
      result[var_type] = var_type;
    }
  }
  return result;
}

meiView.Viewer.prototype.createSourceList = function(Apps) {
  this.Sources = {};
  this.Emendations = {};
  this.Report = {};
  for(appID in Apps) {
    var app = Apps[appID];
    var measure_n = $($(app.elem).closest('measure')[0]).attr('n');
    if (app.tagname === 'choice' || (app.tagname === 'app' && $(app.elem).attr('type') !== 'reconstruction' && $(app.elem).attr('type') !== 'concordance')) {
      if (typeof this.Report[measure_n] === 'undefined') {
        this.Report[measure_n] = [];
      }
      this.Report[measure_n].push(Apps[appID]);
    }
    var resultList;
    if (app.tagname === 'app') {
      resultList = this.Sources;
    } else if (app.tagname === 'choice') {
      resultList = this.Emendations
    }
    for(varXMLID in app.altitems) {
      var altitem = app.altitems[varXMLID];
      var tagname = altitem.tagname;
      if ((tagname === 'rdg' && $(altitem.elem).attr('type') !== 'concordance') || tagname === 'corr') {
        var source_resp;
        if (tagname === 'rdg') { 
          source_resp = altitem.source;
        } else {
          source_resp = altitem.resp
        }
        if (source_resp) {
          var srcIDs = source_resp.split(' ');
          for (var k=0; k<srcIDs.length; k++) {
            var srcID = srcIDs[k];
            if (!resultList[srcID]) {
              resultList[srcID] = [];
            }
            resultList[srcID].push( { appID:app.xmlID, measureNo:measure_n } );
          } 
        }
      } else if (tagname === 'lem' || tagname === 'sic') {
        if (!resultList[tagname]) {
          resultList[tagname] = [];
        }
        resultList[tagname].push( { appID:app.xmlID, measureNo:measure_n } );
      }
    }
  }
}

meiView.Viewer.prototype.selectingState = { 
  
  enter: function(appID, selectedvarXmlID) {
    this.ON = true;
    this.appID = appID;
    this.selectedVarXmlID = selectedvarXmlID;
  },
  
  select: function(xmlID) {
    this.selectedVarXmlID = xmlID;
  },
  
  exit: function() {
    this.ON = false;
  },
  
};


meiView.Page = function(start, end) {
  this.startMeasureN = start;
  this.endMeasureN = end;
}

meiView.Pages = function(options) {
  options = options || {};
  if (options.pages) {
    this.pages = options.pages;
  } else {
    this.pages = [];
    var length = (typeof options.length !== 'undefined') ? options.length : 0;
    var mpp = +(typeof options.mpp !== 'undefined') ? options.mpp : 5;
    if (mpp > 0) {
      for (var i=0; i*mpp<length; ++i) {
        this.pages.push(new meiView.Page(i*mpp+1, Math.min(i*mpp+mpp, length)));
      }
    }
  }
  this.currentPageIndex = -1;
}

meiView.Pages.prototype.AddPage = function(start, end) {
  this.pages.push(new meiView.Page(start, end));
}

meiView.Pages.prototype.nextPage = function() {
  if (this.currentPageIndex<this.pages.length-1) {
    this.currentPageIndex++;
  }
}

meiView.Pages.prototype.jumpTo = function(pageNo) {
  if (0<=pageNo && pageNo<this.pages.length) {
    this.currentPageIndex = pageNo;
  }
}

meiView.Pages.prototype.jumpToMeasure = function(measureNo) {
  this.jumpTo(this.whichPage(measureNo));
}


meiView.Pages.prototype.prevPage = function() {
  if (this.currentPageIndex>0) {
    this.currentPageIndex--;
  }
}

meiView.Pages.prototype.whichPage = function(measureNo) {
  var result = -1;
  $.each(this.pages, function(i, page) {
    if (page.startMeasureN <= measureNo && measureNo <= page.endMeasureN) {
      result = i;
    }
  });
  return result;
}

meiView.Pages.prototype.currentPage = function() {
  return this.pages[this.currentPageIndex];
}

meiView.Pages.prototype.totalPages = function() {
  return this.pages.length;
}

meiView.Viewer.prototype.nextPage = function(){
  this.pages.nextPage();
  this.displayCurrentPage();
  this.UI.dlg && this.UI.dlg.hide();
  // setTimeout(function(){this.UI.fabrCanvas.renderAll()}, 0);
}

meiView.Viewer.prototype.prevPage = function(){
  this.pages.prevPage();
  this.displayCurrentPage();
  this.UI.dlg && this.UI.dlg.hide();
  // setTimeout(function(){this.UI.fabrCanvas.renderAll()}, 0);
}

meiView.Viewer.prototype.jumpTo = function(i) {
  this.pages.jumpTo(i);
  this.displayCurrentPage();
}

meiView.Viewer.prototype.jumpToMeasure = function(i) {
  this.pages.jumpToMeasure(i);
  this.displayCurrentPage();
}

meiView.Viewer.prototype.displayCurrentPage = function() {
  var pageXML = this.getPageXML(this.pages.currentPage());
  var isFirstPage = (this.pages.currentPageIndex === 0);
  this.UI.renderPage(pageXML, {
    labelMode: (isFirstPage) ? 'full' : 'abbr',
    systemLeftMar: (isFirstPage) ? 100 : 25,
    page_margin_top: 30,
    staveSpacing: 70,
    systemSpacing: 90,
    staff: {
      bottom_text_position: 8,
      fill_style: "#000000"
    },
    vexWidth:this.scoreWidth, 
    vexHeight:this.scoreHeight
  });
  this.UI.displayDots();
  this.UI.showTitle(isFirstPage);
  this.UI.fabrCanvas.calcOffset();
  this.UI.updatePageLabels(this.pages.currentPageIndex+1, this.pages.totalPages())

}

meiView.Viewer.prototype.selectSuppliedParts = function(var_type) {
  var sectionplaneUpdate = {};
  for (var var_type in this.selectedSuppliedPartLists) {
    var attr = (meiView.VarTypeList[var_type])['attr'];
    var el = (meiView.VarTypeList[var_type])['el'];
    var parent = (meiView.VarTypeList[var_type])['parent'];

    var origins = this.selectedSuppliedPartLists[var_type].origins
    var all_apps = $(this.MEI.rich_score).find(parent);
    for (originID in origins) {
      var i;
      for (i=0; i<all_apps.length; i++) {
        var app = all_apps[i];
        var app_xml_id=$(app).attr('xml:id');
        if (attr) {
          var rdgs = $(app).find(el + '[' + attr + '="#'+originID+'"]');
        }
        else {
          var rdgs = $(app).find(el + '[type' + '="'+originID+'"]');
        }
        var j;
        for (j=0; j<rdgs.length; j++) {
          var rdg_xml_id = $(rdgs[j]).attr('xml:id');
          if (sectionplaneUpdate[app_xml_id] && origins[originID]) {
            sectionplaneUpdate[app_xml_id].push(rdg_xml_id);
          } else if (!sectionplaneUpdate[app_xml_id] && origins[originID]) {
            sectionplaneUpdate[app_xml_id] = [rdg_xml_id];
          } else if (!sectionplaneUpdate[app_xml_id] && !origins[originID]){
            sectionplaneUpdate[app_xml_id] = [];
          }
        }
      }
    }
  }

  this.MEI.updateSectionView(sectionplaneUpdate);
  this.displayCurrentPage();
}

meiView.Viewer.prototype.voiceNames = function(mei) {
  // Return an associative object that contains the voice names indexed
  // by staff/@n
  var result = {};
  var scoreDefs;
  if (mei.localName === 'score') {
    scoreDefs = $(mei).find('scoreDef');
  } else {
    scoreDefs = $(mei).find('score').find('scoreDef');
  }
  if (scoreDefs.length > 0) {
    var staffDefs = $(scoreDefs[0]).find('staffDef');
    $(staffDefs).each(function() {
      var staff_n = $(this).attr('n') || "1";
      result[staff_n] = $(this).attr('label') || "N/A";
    });
  }
  return result;
}

meiView.Viewer.prototype.stavesToDisplay = function(plain_mei) {
  var result = [];
  staffNs = {};
  staffDefs = $(plain_mei).find('staffDef');
  var i;
  for (i=0; i<staffDefs.length; i++) {
    sd = staffDefs[i];
    N = +$(sd).attr('n') || 1;
    if ($(plain_mei).find('staff[n="' + N + '"]').length > 0) {
      if (result.indexOf(N) === -1) {
        result.push(Number(N));
      }
    }
  }  
  return result;
}


meiView.Viewer.prototype.selectVariant = function(varXmlID) {
  /* assuming meiView.selectingState.on === true */
  this.selectingState.select(varXmlID);

  /* update variant path according to new selection */
  var sectionplaneUpdate = {};
  sectionplaneUpdate[this.selectingState.appID] = varXmlID;
  this.MEI.updateSectionView(sectionplaneUpdate);
}

/**
 * @param page {mewView.Page} to specify measure numbers.
 * @return XML {XML DOM object}
 */
meiView.Viewer.prototype.getPageXML = function(page) {
  var noMeter = (page.startMeasureN !== 1);
  staves = this.stavesToDisplay(this.MEI.sectionview_score);
  return this.MEI.getSectionViewSlice({start_n:page.startMeasureN, end_n:page.endMeasureN, noMeter:noMeter, staves:staves});
}

meiView.Viewer.prototype.loadXMLString = function(txt) {
  var xmlDoc;
  if (window.DOMParser)
  {
    parser=new DOMParser();
    xmlDoc=parser.parseFromString(txt,"text/xml");
  }
  else // Internet Explorer
  {
    xmlDoc=new ActiveXObject("Microsoft.XMLDOM");
    xmlDoc.async=false;
    xmlDoc.loadXML(txt); 
  }
  return xmlDoc;
}
;/***
* meiview-ui.js
* Author: Zoltan Komives
* Contributor: Raffaele Viglianti
* 
* Copyright © 2013 Zoltan Komives, Raffaele Viglianti
* University of Maryland
* 
* Licensed under the Apache License, Version 2.0 (the "License"); you
* may not use this file except in compliance with the License.  You may
* obtain a copy of the License at
* 
*    http://www.apache.org/licenses/LICENSE-2.0
* 
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
* implied.  See the License for the specific language governing
* permissions and limitations under the License.
***/

meiView.UI = function(options) {
  this.init(options);
};

meiView.UI.prototype.init = function(options) {
  this.viewer = options.viewer;
  this.maindiv = options.maindiv;
  this.main_id = 'meiview-main-' + this.viewer.id;
  this.canvas_id = 'meiview-canvas-' + this.viewer.id;
  this.score_id = 'meiview-score-' + this.viewer.id;
  this.base_html = '<div class="meiview-main" id="' + this.main_id + '" style="margin: 10px 20px auto">\
    <div id="' + this.score_id + '" align="center" class="ui-widget-content meiview-scorediv meiview-sized-scorediv">\
    	<button class="ui-widget-content ui-corner-all"onclick="meiView.UI.callback(\'' + this.viewer.id + '\', \'prevPage\')"><span class="ui-icon ui-icon-triangle-1-w"/></button>\
    	<span id="pageNumber-top" width="10">0/0</span>\
    	<button class="ui-widget-content ui-corner-all" onclick="meiView.UI.callback(\'' + this.viewer.id + '\', \'nextPage\')"><span class="ui-icon ui-icon-triangle-1-e"/></button>\
    	<div id="titlediv"><h4><span id="title" class="title" property="dc:title"></span></h4></div>\
    	<canvas class="canvas" id="' + this.canvas_id + '" width="780" height="700"></canvas>\
    	<button class="ui-widget-content ui-corner-all"onclick="meiView.UI.callback(\'' + this.viewer.id + '\', \'prevPage\')"><span class="ui-icon ui-icon-triangle-1-w"/></button>\
    	<span id="pageNumber-bottom" width="10">0/0</span>\
    	<button class="ui-widget-content ui-corner-all" onclick="meiView.UI.callback(\'' + this.viewer.id + '\', \'nextPage\')"><span class="ui-icon ui-icon-triangle-1-e"/></button>\
    </div>\
    <div id="sidebar">\
    	<div id="accordion"> \
    	</div>\
    	<div id="legend" >\
    		<p>\
    			<ul>\
    				<li><h5>Click on the green dots to view the differences between the sources!</h5></li>\
    				<li class=".meiview-source-has-variant-on">\
    					When a  <text style="color: rgb(190,0,0)">Source is highlighted</text> it means some of its \
    					variants are currently displayed in the score.\
    				</li>\
    				<li>\
    					When a <text style="color: rgb(185,0,0);">Variant is highlighted</text> it means that variant is currently \
    					displayed in the score.\
    				</li>\
    			</ul>\
    		</p>\
    	</div>\
    </div> \
  </div>';
  $(this.maindiv).append(this.base_html);
  this.titleDiv = $(this.maindiv).find('.titlediv');
  this.dots = {};
  this.measure_n_texts = {};
  meiView.UI.addObject(this.viewer.id, this.viewer);
  meiView.UI.addObject(this.viewer.id + '-ui', this);
  // console.log($(this.maindiv).find('#' + this.score_id))

  // attach the sidebar to the score div
  // NOTE: aligning the 'top' property is buggy in jquery-ui, so it has to be done manually
  //       TODO: padding is hard-coded
	$(this.maindiv).find('#sidebar').position({
		my: 'left',
		at: 'right+10',
		of: $('#' + this.score_id)
	});
	var sH = $('#' + this.score_id).height();
	var H = Number(sH)
	$(this.maindiv).find('#sidebar').css('top', -1*H-20);
  $(this.maindiv).css('height', this.maxHeight() + 20);
  $('#' + this.main_id).css('height', this.maxHeight() + 20);
  
  var titleElem = $(this.maindiv).find('span.title')[0];
	$(titleElem).html(options.title);

	this.fillSideBar($(this.maindiv).find('#accordion'), 'meiview-sidebar');
	$(this.maindiv).find('#accordion').accordion({
		collapsible: true,
		heightStyle: "content",
		active: false
	});
				
	this.fabrCanvas = this.initCanvas(this.canvas_id);
  this.initSidebarHighlight();
  
}

meiView.UI.prototype.maxHeight = function() {
  //TODO: calculate max height of accordion/sidebar
	var str_scoreH = $('#' + this.score_id).height();
	var scoreH = Number(str_scoreH);
	var sideH = 0;
  var side = $(this.maindiv).find('#sidebar')[0];
  if (side) {
    str_sideH = $(side).height();
  	sideH = Number(str_sideH);
  }
  
  return Math.max(scoreH, sideH);
}

meiView.UI.prototype.toCSSId = function(identifierString) {
  return identifierString.replace(/#/g, '').replace(/\./g, '_');
}

meiView.UI.prototype.liID = function(sourceID, appID) {
  return this.toCSSId(sourceID) + '-' + this.toCSSId(appID);
}

meiView.UI.prototype.srcID2srcLabel = function(src) {
  if (src === 'lem') {
    return 'Base text'
  } else {
    return 'Source ' + src.replace(/^#/, '');
  }
}

meiView.UI.prototype.originID2originLabel = function(src) {
  if (src === 'sic') {
    return 'Sic (mistakes in base text)'
  } else {
    return 'Corrected by ' + src.replace(/^#/, '');
  }
}


meiView.UI.prototype.choiceItem2choiceItemLabel = function(altitem) {
  var label = '';
  if (altitem.localName === 'sic') {
    label = 'sic';
  } else  if (altitem.localName === 'corr') {
    label = 'corr. by ' + $(altitem).attr('resp').replace(/^#/, '');
  }
  return label;
}

meiView.UI.prototype.shortVoiceLabel = function(elem) {
  var staff_l = '';
  var staff = $(elem).closest('staff');
  if (staff.length>0) {
    var staff_n = staff.attr('n') || '1';
    var staffDefs = $(elem).closest('score').find('staffDef[n="' + staff_n + '"]');
    var i;
    for (i=0; i<staffDefs.length; ++i) {
      staff_l = $(staffDefs[i]).attr('label.abbr') || $(staffDefs[i]).attr('label') || staff_l;
    }
    if (staff_l.length > 4) staff_l = staff_l.substr(0,1);
  }
  return staff_l;
}

meiView.UI.prototype.appID2appLabel = function(appID) {
  var app = $(this.viewer.MEI.rich_score).find('app[xml\\:id="' 
    + appID + '"], choice[xml\\:id="' + appID + '"]');
  var measure = app.closest('measure');

  var label = 'M' + measure.attr('n');
  var staff = app.closest('staff');
  if (staff.length>0) {
    var staff_n = staff.attr('n') || '1';
    var staffDefs = app.closest('score').find('staffDef[n="' + staff_n + '"]');
    var i;
    var staff_l = '';
    for (i=0; i<staffDefs.length; ++i) {
      staff_l = $(staffDefs[i]).attr('label.abbr') || $(staffDefs[i]).attr('label') || staff_l;
    }
    if (staff_l.length > 4) staff_l = staff_l.substr(0,1);
  }
  label += '.' + this.shortVoiceLabel(app);
  return label;
}

meiView.UI.prototype.showTitle = function(show) {
  if (this.titleDiv && this.titleElem) {
    if (show) {
      $(this.titleDiv).append(this.titleElem);
    } else {
      $(this.titleElem).remove();
    }  
  }
}

meiView.UI.prototype.updatePageLabels = function(current, total) {
  $(this.maindiv).find('#pageNumber-top, #pageNumber-bottom')
    .html((current).toString() + '/' + total);
}

meiView.UI.prototype.onClickSideBarMarkup = function(me, measure_n, altID) {
  var result = 'onclick="meiView.UI.callback('
    + '\'' + me.viewer.id + '-ui\', \'onClickSidebarItem\', { measure_n: '
    + measure_n + ', altID: \'' +  altID
    + '\'})"';
  return result;
}

meiView.UI.prototype.fillSideBar = function(sidebardiv, sidebar_class) {
  // Create a capitalized, plural form of a var name
  // e.g. 'reconstruction' -> 'Reconstructions'
  cap_plural = function(string) {
    return string.charAt(0).toUpperCase() + string.slice(1) + 's';
  }
  // Supplied part lists: reconstructions and concordances
  for (var var_type in this.viewer.SuppliedPartLists) {
    for (originID in this.viewer.SuppliedPartLists[var_type]) {
      var listElem = sidebardiv.find('ul[id="' + var_type + '"]');
      if (listElem.length === 0) {
        sidebardiv.append('<h3 class="' + sidebar_class + 
            '">' + cap_plural(var_type) + '</h3><div class="' + sidebar_class +
            '"><ul id="' + var_type + '"></ul></div>');
        listElem = sidebardiv.find('ul[id="' + var_type + '"]');
      }
      listElem.append('<li class="meiview-sidebar-item"\
          onclick="meiView.UI.callback(\'' + 
          this.viewer.id + '-ui\', \'onSuppliedPartClick\', { ' +
          'originID: \'' + originID + '\',' +
          'var_type: \'' + var_type + '\',' + '})">' + 
          // Just a hack to make a better message than 'blank'
          // for showing blank staves
          (originID == 'blank' ? 'Show missing staves' : originID) +
          '</li>');
    }
  }

  var emendations = this.viewer.Emendations;
  var choices = $(this.viewer.MEI.rich_score).find('choice');
  if (choices.length > 0) {
    sidebardiv.append('<h3 class="' + sidebar_class 
      + '">Emendations</h3>\
        <div class="' + sidebar_class + '">\
          <ul class="emendations-list"></ul>\
        </div>');
    var emendListElem = sidebardiv.find('ul.emendations-list');
    var i=0;
    for (var i;i<choices.length; i++) {
      var choice = choices[i]
      var measure_n = $($(choice).closest('measure')[0]).attr('n');
      var choiceID = $(choice).attr('xml:id');
      var liID = this.toCSSId(choiceID);

      // resplist <- list of editors who have entered corrections
      var resplist = '';
      var corrs = $(choice).find('corr');
      var altlabel_open = '(corr. by ';
      var altlabel_close = ')';
      var j = 0;
      for (var j; j<corrs.length; j++) {
        var corr = corrs[j];
        resplist += ( j > 0 ? ', ' : '') + $(corr).attr('resp').replace(/^#/, '');
      }

      emendListElem.append('<li id="' + liID + '" class="meiview-sidebar-item" '
        + this.onClickSideBarMarkup(this, measure_n, choiceID) + '>'
        + this.appID2appLabel(choiceID) + altlabel_open + resplist + altlabel_close
        + '</li>'
      );
      var liItem = $(emendListElem).find('li#' + liID);
    }
  }

  var sources = this.viewer.Sources;
  for(src in sources){
    var source = sources[src];
    sidebardiv.append('<h3 class="' + sidebar_class + '">'
      + this.srcID2srcLabel(src)
      + '</h3><div class="'
      + sidebar_class
      + '"><ul id="' + src + '"></ul></div>'
    );
    var listElem = sidebardiv.find('ul[id="'+src+'"]');
    for (var i=0; i<source.length; i++) {
      var appID = source[i].appID;
      var measure_n = source[i].measureNo;
      listElem.append('<li id="' + this.liID(src, appID)
        + '" class="' +  this.toCSSId(appID)
        + ' meiview-sidebar-item" '
        + this.onClickSideBarMarkup(this, measure_n, appID) + '>'
        + this.appID2appLabel(appID)
        + '</li>'
      );
    }
  }

}

meiView.UI.callback = function(id, fname, params) {
  meiView.UI.objects[id][fname](params);
}

meiView.UI.prototype.onSuppliedPartClick = function(params) {
  this.viewer.toggleSuppliedPart(params.var_type, params.originID);
}

meiView.UI.objects = {};
meiView.UI.addObject = function(id, obj) {
  meiView.UI.objects[id] = obj;
};

meiView.UI.prototype.onClickSidebarItem = function(params) {
  this.viewer.jumpToMeasure(params.measure_n);
  this.ShowSelectorPanel(this.dots[params.altID].info);
}

meiView.UI.prototype.renderMei2Canvas = function(score, options) {
  options = options || {};
  var paddingX = options.paddingX || 0;
  var paddingY = options.paddingY || 0;

  var tempCanvas = new fabric.StaticCanvas();
  tempCanvas.setDimensions({width:options.vexWidth, height:options.vexHeight});
  var score_width = options.vexWidth;
  var score_height = options.vexHeight;
  this.L('Rendering MEI... ');
  MEI2VF.render_notation(score, tempCanvas.getElement(), score_width, score_height, null, options);
  this.rendered_measures = MEI2VF.rendered_measures;
  this.L('Done rendering MEI');
  return tempCanvas;  
}

meiView.UI.prototype.displayDots = function() {
  for (appID in this.dots) {
    if (this.dots[appID])
    { 
      this.fabrCanvas.remove(this.dots[appID].circle);
      delete this.dots[appID];
    }
  }
  for (appID in this.viewer.MEI.ALTs) {
    this.dots[appID] = this.displayDotForAPP(appID);
  }
}

meiView.UI.prototype.displayDotForAPP = function(appID) {

  // In order to know what coordiantes to display the dot at, we have to
  // get the coordinates of the VexFlow staff object. VexFlow staff objects are 
  // exposed by MEI2VF via the MEI2VF.rendered_measures:
  // MEI2VF.rendered_measures is indexed by the measure number and staff number.
  // so, in order to retreive the right measure we have to know the measure number and the 
  // staff number:

  // get the meausure number first,
  var app = this.viewer.MEI.ALTs[appID].elem; 
  var parent_measure = $(app).parents('measure');
  var measure_n = parent_measure.attr('n');

  // then the staff number...
  var parent_staff = $(app).parents('staff');
  var staff_n;
  if (parent_staff.length === 0) {
    var child = $(app).find('[staff]')
    staff_n = $(child).attr('staff');
  } else {
    staff_n = parent_staff.attr('n');
  }

  // ...then display the dot at the coordinates specified by the
  // properties of MEI2VF.rendered_measures[measure_n][staff_n];
  var vexStaffs = MEI2VF.rendered_measures[measure_n];
  if (vexStaffs) {
    var vexStaff = vexStaffs[staff_n];
    if (vexStaff) {
      var dotInfo = {
        appXmlID: appID, 
        measure_n: Number(measure_n),
        measure_top: vexStaff.y,
        measure_left: vexStaff.x,
        measure_width: vexStaff.width,
        staff_n: Number(staff_n),
      }
      return { circle:this.displayDotForMeasure(vexStaff), info:dotInfo };
    }
  }
}

meiView.UI.prototype.displayDotForMeasure = function(vexStaff) { 
  if (vexStaff) {
    var left = (vexStaff.x + vexStaff.width - 12) * this.scale;
    // var top = (vexStaff.y + 30) * this.scale;
    var top = (vexStaff.y + 25) * this.scale;

    var circle = new fabric.Circle({
      radius: 5, 
      fill: 'green', 
      left:left, 
      top:top, 
      lockMovementX: true,
      lockMovementY: true,
      lockScalingX: true,
      lockScalingY: true,
      lockRotation: true,
      hasControls: false,
      hasBorders: false,
    });
    circle.meiViewID = appID;
    this.fabrCanvas.add(circle);
    return circle;
  }
}



meiView.UI.prototype.displayMeasureNos = function() {
//  console.log('meiView.UI.prototype.displayMeasureNos()')
  for (n in this.measure_n_texts) {
    if (this.measure_n_texts[n])
    { 
      this.fabrCanvas.remove(this.measure_n_texts[n]);
      delete this.measure_n_texts[n];
    }
  }
  var rendered_measures = this.rendered_measures
  var ui_scale = this.scale;
  var ui_canvas = this.fabrCanvas;
  var ui_measure_n_texts = this.measure_n_texts;
  $.each(rendered_measures, function(n, measure) {
//    console.log('meiView.UI.prototype.displayMeasureNos() n:' + n);
    if (measure) {
      var i, vexStaff = measure[1], skip = false;
      for (i=0; i<vexStaff.modifiers.length; i++) {
        var modifier = vexStaff.modifiers[i];

        // TODO: Detect collision between measure number and modifier
        // (perhaps by detecting collision with modifier.modifier_context)
        //
        // For now: if modifier is a volta, do not render measure number.
        if (modifier.volta == Vex.Flow.Volta.type.BEGIN || 
            modifier.volta == Vex.Flow.Volta.type.BEGIN_END) {
          skip = true;
        }
      }
      if (!skip) {
//        console.log('meiView.UI.prototype.displayMeasureNos() vexStaff:');
//        console.log(vexStaff);
        var left = (vexStaff.x + 8) * ui_scale;
        var top = (vexStaff.y + 15) * ui_scale;
        var text = new fabric.Text(n.toString(), {
          fontSize: Math.round(16 * ui_scale),
          fill: 'grey',
          left:left, 
          top:top, 
          lockMovementX: true,
          lockMovementY: true,
          lockScalingX: true,
          lockScalingY: true,
          lockRotation: true,
          hasControls: false,
          hasBorders: false,
        });
        ui_canvas.add(text);
        ui_measure_n_texts[n] = text;
      }
    }
  });
}

meiView.UI.prototype.renderMei2Img = function(meixml, options) {
  var tempCanvas = this.renderMei2Canvas(meixml, options);
  var img = new Image;
  img.src = tempCanvas.toDataURL();
  return img;
}

meiView.UI.prototype.renderPage = function(pageXML, options) { 
  options = options || {};
  options.paddingX = 20;
  options.paddingY = 20;
  options.vexWidth = options.vexWidth || $(this.fabrCanvas.getElement()).attr('width');
  options.vexHeight = options.vexHeight || $(this.fabrCanvas.getElement()).attr('height');
  
  
  
  var img = this.renderMei2Img(pageXML, options);
  if (this.scoreImg) {
     this.fabrCanvas.remove(this.scoreImg);    
  }
  this.scale = this.fabrCanvas.width/options.vexWidth;
  var W = this.fabrCanvas.width;
  var H = options.vexHeight * this.scale;
  this.scoreImg = new fabric.Image(img, {
    width:W,height:H, left:W/2, top:H/2,
    lockMovementX: true,
    lockMovementY: true,
    lockScalingX: true,
    lockScalingY: true,
    lockRotation: true,
    hasControls: false,
    hasBorders: false,
    selectable: false,
  });
  this.fabrCanvas.add(this.scoreImg);
  if (this.viewer.display_measure_numbers) {
    this.displayMeasureNos();
  }
  this.fabrCanvas.renderAll_Hack();
}

meiView.UI.prototype.initCanvas = function(canvasid) {

  var dimensions = { width: $('#'+canvasid).width(), height: $('#'+canvasid).height() }
  var me = this;

  var canvas = new fabric.Canvas(canvasid);
  canvas.setDimensions(dimensions)
  canvas.hoverCursor = 'pointer';
  var this_ui = this;

  canvas.renderAll_Hack = function() {
    setTimeout(function(){canvas.renderAll()}, 1000);
  }

  canvas.findTarget = (function(originalFn) {
    return function() {
      var target = originalFn.apply(this, arguments);
      if (target) {
        if (this._hoveredTarget !== target) {
          canvas.fire('object:over', { target: target });
          if (this._hoveredTarget) {
            canvas.fire('object:out', { target: this._hoveredTarget });
          }
          this._hoveredTarget = target;
        }
      }
      else if (this._hoveredTarget) {
        canvas.fire('object:out', { target: this._hoveredTarget });
        this._hoveredTarget = null;
      }
      return target;
    };
  })(canvas.findTarget);
  
  canvas.on('object:over', function(e) {
    if (e.target && e.target.meiViewID) {
      e.target.setFill('red');
      canvas.renderAll();
    }
  });

  canvas.on('object:out', function(e) {
    if (e.target && e.target.meiViewID) {
      e.target.setFill('green');
      canvas.renderAll();
    }
  });

  canvas.on('mouse:down', function(e) {
    
    if (e.target) {
      var dotInfo = 
        e.target.meiViewID && 
        this_ui.dots[e.target.meiViewID] && 
        this_ui.dots[e.target.meiViewID].info;
      if (dotInfo) {
        this_ui.ShowSelectorPanel(dotInfo);
      } else if (e.target.selectItem>=0) {
        this_ui.dlg && this_ui.dlg.select(e.target.selectItem);
      } else {
        this_ui.HideSelectorPanel();
      }
      me.L(e.target);
      me.L(e.target.meiViewID  + ': x:' + e.target.left + ', y:' + e.target.top);
    }
  });
  
  canvas.allowTouchScrolling = true;
  
  return canvas;
  
}

meiView.UI.prototype.onSelectorDraw = function(args) {
  this.viewer.selectingState.enter(args.appID, this.viewer.MEI.sectionplane[args.appID].xmlID);
  this.updateSidebar();
}

meiView.UI.prototype.onSelectorSelect = function(args) {

  if (this.viewer.selectingState.ON) {

    var oldVarID = this.viewer.selectingState.selectedVarXmlID;
    this.viewer.selectVariant(args.varXmlID);

    /* re-draw current page [TODO: only re-draw if the change happened on the current page] */

    this.viewer.displayCurrentPage();
    if (this.dlg) { 
      this.dlg.bringToFront();
    }
    
    this.updateSidebar(this.viewer.selectingState.appID, oldVarID);
  }
}

meiView.UI.prototype.onSelectorHide = function() {
  this.viewer.selectingState.exit();
  this.updateSidebar();
}

meiView.UI.prototype.addHightlightClasses = function(appID) {
  var source = this.viewer.MEI.sectionplane[appID].source;
  var sources = source ? source.split(' ') : ['lem'];
  for (var i=0;i<sources.length; i++) {
    var liID = this.liID(sources[i], appID);
    $(this.maindiv).find('#' + liID)
      .addClass('meiview-variant-on')
      .closest('div.meiview-sidebar').prev().addClass('meiview-source-has-variant-on');
  }
}

meiView.UI.prototype.initSidebarHighlight = function() {
  if (!this.viewer.MEI.sectionview_socre) return;
  for (appID in this.viewer.MEI.ALTs) {
    this.addHightlightClasses(appID);
  } 
}

meiView.UI.prototype.updateSidebarHighlight = function(appID, oldVarID) {
  this.addHightlightClasses(appID);
  if (oldVarID) {
    source = this.viewer.MEI.ALTs[appID].altitems[oldVarID].source;
    var sources = source ? source.split(' ') : ['lem'];
    for (var i=0;i<sources.length; i++) {
      var liID = this.liID(sources[i], appID);
      $(this.maindiv).find('#' + liID)
      .removeClass('meiview-variant-on');
    }
    $(this.maindiv).find('div.meiview-sidebar')
      .not(':has(li.meiview-variant-on)')
      .prev('.meiview-source-has-variant-on')
      .removeClass('meiview-source-has-variant-on');
  }
}

meiView.UI.prototype.updateSidebar = function(appID, oldVarID) {
  if (appID) {
    this.updateSidebarHighlight(appID, oldVarID);
  }
  if (this.viewer.selectingState.ON) {
    /* Disable sources without variants at the currently selected <app> */
    $(this.maindiv).find('div.meiview-sidebar')
      .not(':has(li.' + this.toCSSId(this.viewer.selectingState.appID) + ')')
      .prev()
      .addClass('meiview-source-disabled');
    /* Close up variant list the source is disbaled */
    if ($(this.maindiv).find('.meiview-source-disabled.ui-accordion-header-active').length>0) { 
      $(this.maindiv).find("#accordion").accordion( "option", "active", false);
    }
    /* Disable clicking on sources */
    $(this.maindiv).find('#accordion').on('accordionbeforeactivate', function(event, ui) {
      event.preventDefault();
    });
  } else {
    /* Enable all sources */
    $(this.maindiv).find('h3.meiview-source-disabled').removeClass('meiview-source-disabled');
    /* Enable clicking on sources */
    $(this.maindiv).find('#accordion').off();
  }
}

meiView.UI.prototype.ShowSelectorPanel = function(dotInfo) {
  var variantSlice = this.viewer.MEI.getRichSlice({start_n:dotInfo.measure_n, end_n:dotInfo.measure_n, staves:[dotInfo.staff_n], noClef:true, noKey:true, noMeter:true, noConnectors:true});
  var panelItemParamList = [];
  var appID = dotInfo.appXmlID;
  var altitems = this.viewer.MEI.ALTs[appID].altitems;

  if (this.dlg) {
    this.dlg.hide();
  }
  this.dlg = new meiView.SelectorPanel({
    left: dotInfo.measure_left*this.scale, 
    top: dotInfo.measure_top*this.scale, 
    measureWidth: 500*this.scale, 
    //measureWidth: 300*this.scale, 
    canvas: this.fabrCanvas,
    scale: 0.7,
    appID: appID,
    UI: this,
  });
  
  self = this;
  this.dlg.onDraw = function(args) { self.onSelectorDraw(args) };
  this.dlg.onSelect = function (args) { self.onSelectorSelect(args) };
  this.dlg.onHide = function () { self.onSelectorHide() };

  variantSlice.initSectionView();
  for (xmlID in altitems) {
    var altitem = altitems[xmlID];
    var tagname = altitem.tagname;
    var source = altitem.source;
    var resp = altitem.resp;
    var replacements = {};
    replacements[appID] = xmlID;
    variantSlice.updateSectionView(replacements);
    var text = '';
    if (tagname == 'lem') {
      text = 'Lemma';
    }
    else if (tagname == 'sic') {
      text = 'Original';
    }
    else if (tagname == 'corr') {
      if (resp) {
        text = 'Corrected (' + resp.replace(/#/g, '').replace(/ /g, ', ') + ')';
      }
      else {
        text = 'Corrected'
      }
    }
    else if (source) {
      text = source.replace(/#/g, '').replace(/ /g, ', ');
    }
    else if (resp) {
      text = resp.replace(/#/g, '').replace(/ /g, ', ');
    }
    var selected = (this.viewer.MEI.sectionplane[appID] === altitem);
    this.dlg.addItem(text+':', variantSlice.sectionview_score, selected, xmlID);
  }
  this.dlg.draw();
}

meiView.UI.prototype.HideSelectorPanel = function() {
  if (this.dlg) {
    this.dlg.hide();
  }
}

meiView.DO_LOG = true;

meiView.UI.prototype.L = function() {
  if (meiView.DO_LOG) Vex.L("meiView", arguments);
}

meiView.SelectorItem = function(options) {
  this.text = options.text;
  this.imgData = options.imgData;
  this.xmlID = xmlID;
}

meiView.SelectorPanel = function (options) {
  this.measureWidth = options.measureWidth || 300;
  this.measureHeight = options.measureHeight || 125;
  this.scale = options.scale || 0.8;
  this.marginWE = options.marginWE || 5;
  this.marginNS = options.marginNS || this.marginWE;
  this.itemSpacing = options.itemSpacing || 5;
  this.width = this.measureWidth * this.scale;
  this.height = 0;
  this.selectedIndex = options.currentSelection || -1;

  this.left = options.left || this.width/2;
  this.top = options.top || this.height/2;

  this.canvas = options.canvas;
  this.UI = options.UI;
  
  this.contentWidth = this.width - 2*(this.marginWE);
  this.imgW = this.contentWidth;
  this.imgH = this.imgW * this.measureHeight/this.measureWidth;

  this.contentTop = this.top - this.height/2 + this.marginNS;

  this.contentScale = options.contentScale || 0.7;
  
  this.items = [];
  this.objects = [];
  if (!options.appID) throw "appID isn't defined for SelectorPanel.";
  this.appID = options.appID;

  this.onDraw = function(args) {};
  this.onSelect = function(args) {};
  this.onHide = function(args) {};
}

meiView.SelectorPanel.prototype.setCanvas = function(fabricCanvas) {
  this.canvas = fabricCanvas;
}

meiView.SelectorPanel.prototype.addItem = function(text, singleVarSliceXML, selected, xmlID) {
  var imgData = this.UI.renderMei2Img(singleVarSliceXML, {
    labelMode: 'full',
    systemLeftMar: 100,
    page_margin_top: 20,
    staveSpacing: 70,
    systemSpacing: 90,
    staff: {
      bottom_text_position : 8,
      fill_style : "#000000"
    },
    vexWidth:this.measureWidth, 
    vexHeight:this.measureHeight 
  });
  var newItem = new meiView.SelectorItem({text:text, imgData:imgData, xmlID:xmlID});
  this.items.push(newItem);
  if (selected) {
    this.select(this.items.length-1);
  }
}

meiView.SelectorPanel.prototype.addObjectsForItem = function(item, itemIndex) {
  var text = new fabric.Text(item.text, {
    fontSize: 17*this.scale,
    selectable: false,
    left: this.left,
  });
  
  if (text.width > this.contentWidth) {
    this.contentWidth = text.width;
    this.width = this.contentWidth + 2*(this.marginWE);
  }
  
  var img = new fabric.Image(item.imgData, {
    width:this.imgW, 
    height:this.imgH,
    left: this.left,
    lockMovementX: true,
    lockMovementY: true,
    lockScalingX: true,
    lockScalingY: true,
    lockRotation: true,
    hasControls: false,
    hasBorders: true,
    selectable: false,
  });

  var br = text.getBoundingRect();

//  text.left = this.contentLeft + br.width/2;
  text.top = this.contentTop + this.nextItemTop + br.height/2

  img.top = text.top + br.height/2 + img.height/2;
  // img.left = this.contentLeft + img.width/2;

  var vertIncr = text.height + img.height;
  item.height =  vertIncr;
  this.nextItemTop += vertIncr + this.itemSpacing;
  var heightIncr = itemIndex===0 ? vertIncr + this.marginNS : vertIncr + this.itemSpacing;
  this.height += heightIncr;
  this.top += heightIncr/2;
  
  var smW = this.contentWidth;
  var smH = this.imgH+text.height;
  item.selectorMask =  new fabric.Rect({
    fill: 'green',
    width:smW, 
    height:smH,
    left: this.left,
    lockMovementX: true,
    lockMovementY: true,
    lockScalingX: true,
    lockScalingY: true,
    lockRotation: true,
    hasControls: false,
    selectable: true,
  });
  
  item.selectorMask.top = item.selectorMask.height/2 + text.top - text.height/2;

  // some custom members for selectorMask:
  //  * remember the index to know which item it is attached to,
  //  * define how to highlight when selected
  item.selectorMask.selectItem = itemIndex;
  item.selectorMask.highlight = function(value) {
    this.opacity = value ? 0.35 : 0;
  };
  
  item.selectorMask.highlight(itemIndex === this.selectedIndex);

  this.objects.push(text);
  this.objects.push(img);
  this.objects.push(item.selectorMask);
 
}

/**
 * Calculate delta_x and delta_y to shift the panel so it fits inside the specified box;
 */
meiView.SelectorPanel.prototype.shiftXY = function(box) {
  var pHeight = 0;
  var items = this.items;
  for (var i=0;i<items.length;i++) {
    pHeight += items[i].height + (i === 0 ? this.marginNS : this.itemSpacing);
  }
  if (items.length>0) pHeight += this.marginNS;
  var pWidth = this.width;
  var Wc = box.width;
  var Hc = box.height;
  var Xc = box.x;
  var Yc = box.y;
  
  var curr_x = this.panel.left;
  var curr_y = this.panel.top;
  
  var min_x = Xc - Wc/2 + pWidth/2;
  var max_x = Xc + Wc/2 - pWidth/2;
  var delta_x = 0;
  if (curr_x > max_x ) delta_x = max_x - curr_x;
  if (curr_x < min_x) delta_x = min_x - curr_x;
 
  var min_y = Yc  - Hc/2 + pHeight/2;
  var max_y = Yc  + Hc/2 - pHeight/2;
  var delta_y = 0;
  if (curr_y > max_y) delta_y = max_y - curr_y;
  if (curr_y < min_y) delta_y = min_y - curr_y;

  return {x:delta_x, y:delta_y};
}

meiView.SelectorPanel.prototype.draw = function(box) {
  this.objects = [];
  this.nextItemTop = 0;

  if (!this.panel) {
      this.panel = new fabric.Rect({
        fill: 'grey',
        selectable: false
      });
  }
  this.objects.push(this.panel);

  var items = this.items;
  for (var i=0;i<items.length;i++) {
    this.addObjectsForItem(items[i], i);
  }

  this.panel.width = this.width;
  this.panel.height = this.height+this.marginNS;

  this.panel.left = this.left;
  this.panel.top = this.top+this.marginNS/2;
  
  var delta = this.shiftXY({
    x: this.canvas.width/2, 
    y: this.canvas.height/2, 
    width: this.canvas.width,
    height: this.canvas.height
  });

  var objects = this.objects;
  for (var i=0;i<objects.length;i++) {
    var obj = objects[i];
    obj.left += delta.x;
    obj.top += delta.y;
    this.canvas.add(obj);
  }
  this.canvas.renderAll_Hack();
  this.onDraw({appID:this.appID});
}

meiView.SelectorPanel.prototype.hide = function() {
  this.canvas.remove(this.panel);
  var objects = this.objects;
  for (var i=0;i<objects.length;i++) {
    this.canvas.remove(objects[i]);
  }
  this.onHide();
  delete this;
}

meiView.SelectorPanel.prototype.select = function(i) {

  if (0<=i && i<this.items.length) {
    
    //switch off highlight on prviously selected item
    if (this.selectedIndex>=0 && this.items[this.selectedIndex].selectorMask) {
      this.items[this.selectedIndex].selectorMask.highlight(false);
    }
    
    //switch off highlight on new selection
    if (this.items[i].selectorMask) {
      this.items[i].selectorMask.highlight(true);
    }
    
    this.selectedIndex = i;

    this.onSelect({ varXmlID: this.items[i].xmlID});
    
  }
  
}

meiView.SelectorPanel.prototype.bringToFront = function() {
  var objects = this.objects;
  for (var i=0;i<objects.length;i++) {
    objects[i].bringToFront();
  }
}

;/***
* meiview.js
* Author: Zoltan Komives
* 
* Copyright © 2013 Zoltan Komives
* 
* Licensed under the Apache License, Version 2.0 (the "License"); you
* may not use this file except in compliance with the License.  You may
* obtain a copy of the License at
* 
*    http://www.apache.org/licenses/LICENSE-2.0
* 
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
* implied.  See the License for the specific language governing
* permissions and limitations under the License.
***/


/**
 * MeiFilter is responsible to transform an 'arbitrary' MEI file into an 
 * MEI file that can be presented with meiView
 *
 */
meiView = (typeof meiView == "undefined")? {} : meiView;

meiView.substituteLonga = function(music) {
  var longs = $(music).find('note[dur="long"]');
  $(longs).each(function(){
    //TODO: for now we simply replace longas with breve
    // much better would be to introduce long in VexFlow
    $(this).attr('dur', 'breve');
  })
}

meiView.filterMei = function(meiXml, options) {
  var options = options || {};
  /**
   * Propagate relevant attribute values from scoreDef into staffDef elements
   */
  var propagateScoreDefAttrs = function(scoreDef) {
    
    var propagateAttrValue = function(attrname, descendant, ancestor) {
      var desc_attr_val = $(descendant).attr(attrname);
      var anc_attr_val = $(ancestor).attr(attrname);
      if (!desc_attr_val && anc_attr_val) {
        $(descendant).attr(attrname, anc_attr_val);
      }
    }
    
    var staffDefs = $(scoreDef).find('staffDef');
    $(staffDefs).each(function() {
      propagateAttrValue('meter.count', this, scoreDef);
      propagateAttrValue('meter.unit', this, scoreDef);
      propagateAttrValue('meter.rend', this, scoreDef);
      propagateAttrValue('key.pname', this, scoreDef);
      propagateAttrValue('key.accid', this, scoreDef);
      propagateAttrValue('key.mode', this, scoreDef);
      propagateAttrValue('key.sig.show', this, scoreDef);
    });
  }

  var eliminateAccidElements = function(music) {

    var eliminateAccid = function(accid) {

      var place_val = $(accid).attr('place');
      var func_val = $(accid).attr('func');

      if ( place_val == 'above' && func_val == 'edit' ) {

        var parent_note_id = $(accid).parent('supplied').parent('note').attr('xml:id');
        if (!parent_note_id) {
//          console.log('parent note xml:id is needed in order to attach ficta. Ficta will be ignored.');
        } else {
          var dir = meiXml.createElementNS('http://www.music-encoding.org/ns/mei', 'dir');
          $(dir).attr('startid', parent_note_id);
          var accid_val = $(accid).attr('accid');
          if (accid_val == 's') {
            $(dir).append('♯');
          } else if (accid_val == 'n') {
            $(dir).append('♮');
          } else if (accid_val == 'f') {
            $(dir).append('♭');
          }
          $(accid).closest('staff').get(0).parentNode.appendChild(dir);
        }

      } else {
        $(accid).parent('note').attr('accid', $(accid).attr('accid'));
      }

      accid.parentNode.removeChild(accid);
    }

    var accids = $(music).find('accid');
    $(accids).each(function() {
      eliminateAccid(this);
    });

  }
  
  var music = meiXml.getElementsByTagNameNS("http://www.music-encoding.org/ns/mei", 'music')[0];

  // Remove page break elements (<pb>)
  $(music).find('pb').remove();

  // Propagate meter and key signatures from score def to staff def
  var scoreDefs = $(music).find('scoreDef');
  $(scoreDefs).each(function() {
    propagateScoreDefAttrs(this);
  });

  // Remove system breaks if not needed.
  if (options.noSysBreak) {
    $(music).find('sb').remove();
  }
  
  // Remove elements that may cause the renderer to choke
  $(music).find('meterSig').remove();
  $(music).find('annot[type="bracket"]').remove();

  // Substitute longas with breves
  meiView.substituteLonga(music);

  eliminateAccidElements(music);

  return meiXml;
}

;meiView.Mode = {
  SINGLE_PAGE: 0,
  PLAIN: 1,
  SIDEBAR_ONLY: 2,
  CRITREP_ONLY: 3,
  FULL: 4,
}

meiView.Merge = function(destination, source) {
    for (var property in source)
        destination[property] = source[property];
    return destination;
};

meiView.Inherit = (function () {
  var F = function () {};
  return function (C, P, O) {
    F.prototype = P.prototype;
    C.prototype = new F();
    C.superclass = P.prototype;
    C.prototype.constructor = C;
    meiView.Merge(C.prototype, O);
    return C;
  };
}());

meiView.CompactViewer = function(options) {
  this.init(options);
}

meiView.Inherit(meiView.CompactViewer, meiView.Viewer, {
  init: function(options) {

    var randomID = function() {
      return ("0000" + (Math.random()*Math.pow(36,4) << 0).toString(36)).substr(-8)
    }

    this.mode = (typeof options.mode === 'undefined') ? meiView.Mode.FULL : options.mode;
    this.id = (typeof $(options.maindiv).attr('id') == 'undefined') ? randomID() : $(options.maindiv).attr('id');
    this.MEI = options.MEI;
    this.MEI.initSectionView();
    this.display_measure_numbers = (typeof options.display_measure_numbers == 'undefined') ? 
      1 : options.display_measure_numbers;
    if (options.pages) {
      this.pages = options.pages;
    } else {
      this.pages = new meiView.Pages();
      if (this.parsePages) {
        this.parsePages(this.MEI);
      }
    }
    if (options.pxpMeasure) {
      this.pxpMeasure = options.pxpMeasure;
    } else {
      this.scoreWidth = options.width || 1200;
    }
    this.scoreHeight = options.height || 1000;
    this.createSourceList(this.MEI.ALTs);
    
    // Create an object of supplied parts. Reconstructions, concordances,
    // and any other supplied parts can be added to this object.
    this.SuppliedPartLists = {}
    for (var var_type in meiView.VarTypeList)
      this.SuppliedPartLists[var_type] = this.createSuppliedPartList(var_type);

    // Create dictionary of selected part lists, matching the
    // part lists which have been created
    this.selectedSuppliedPartLists = {};
    for (var var_type in meiView.VarTypeList) {
      this.selectedSuppliedPartLists[var_type] = new meiView.SelectedSuppliedPartList(var_type);
    }

    this_viewer = this;
    this.UI = new meiView.CompactUI({
      viewer: this_viewer,
      maindiv: options.maindiv,
      title: options.title,
      scale: options.scale,
    });

    if (this.mode == meiView.Mode.FULL) {
      // this.UI.showCritRep();
      // this.UI.showSideBar();
    } else if (this.mode == meiView.Mode.CRITREP_ONLY) {
      this.UI.hideSideBar();
    } else if (this.mode == meiView.Mode.SIDEBAR_ONLY) {
      this.UI.hideCritRep();
    } else if(this.mode == meiView.Mode.PLAIN) {
      this.UI.hideSideBar();
      this.UI.hideCritRep();
    } else if (this.mode == meiView.Mode.SINGLE_PAGE) {
      this.UI.hideSideBar();
      this.UI.hideCritRep();
      this.UI.hidePagination();
    }

    if (this.UI.sideBarLength() == 0) {
      this.UI.hideSideBar();
    }

    if (options.displayFirstPage) {
      this.nextPage();
    }

  },

  getScoreWidth: function(score) {
    if (this.pxpMeasure) {
      var no_of_measures = $(score).find('measure').length;
      return this.pxpMeasure * no_of_measures;
    } else {
      return this.scoreWidth;
    }
  },

  toggleCritRep: function() {
    if (this.UI.critRepOn()) {
      this.UI.hideCritRep();
    } else {
      this.UI.showCritRep();
    }
  },

  getPageXML_ContentPart: function(page) {
    var noMeter = (page.startMeasureN !== 1);
    var staves = this.stavesToDisplay(this.MEI.sectionview_score);
    var contentxml = this.MEI.getSectionViewSlice({
      start_n:page.startMeasureN,
      end_n:page.endMeasureN,
      noMeter:noMeter,
      noKey:true,
      noClef:true,
      staves:staves
    });
    // Remove stave connectors
    var scoredefs = $(contentxml).find('scoreDef');
    if (scoredefs[0]) {
      $(scoredefs[0]).find('staffGrp').attr('symbol', 'none');
    }
    return contentxml;
  },

  getPageXML_ClefPart: function(page) {
    var me = this, staves, clefxml, score,
        scoredefs, scoredef, section, measure, staff_n;
//    console.log('getPageXML_ClefPart() {start}');
    staves = me.stavesToDisplay(this.MEI.sectionview_score);
    clefxml = me.MEI.getSectionViewSlice({
      start_n:'-1',
      noMeter:true,
      noKey:false,
      noClef:false,
      staves:staves
    });
    score = clefxml;
    if (score) {
//      console.log('getPageXML_ClefPart() {I}');
    
      scoredefs = $(score).find('scoreDef');
      scoredef = scoredefs[0];

      section = $(score).find('section').get(0);

      // in some browsers JQuery.append() didn't seem to work,
      // the measure wouldn't get inserted to the section; using
      // native XML DOM methods instead.
      measure = me.MEI.xmlDoc.createElementNS("http://www.music-encoding.org/ns/mei", "measure");
      measure.setAttribute('n', '1');
      measure.setAttribute('right', 'invis');
      if (scoredef) {
        $(scoredefs[0]).find('staffDef').each(function(i, std) {
          var staff, layer;
          if (section) {
            staff_n = $(std).attr('n');
              staff = me.MEI.xmlDoc.createElementNS("http://www.music-encoding.org/ns/mei", "staff");
              staff.setAttribute('n', staff_n);
              layer = me.MEI.xmlDoc.createElementNS("http://www.music-encoding.org/ns/mei", "layer");
              staff.appendChild(layer);
              measure.appendChild(staff);
          }
        });
        section.appendChild(measure);
      }
    }
    return clefxml;
  },

  displayCurrentPage: function () {
    this.displayCurrentPage_TwoParts();
  },

  displayCurrentPage_TwoParts: function() {
    var pageXML_ContentPart = this.getPageXML_ContentPart(this.pages.currentPage());
    var pageXML_ClefPart = this.getPageXML_ClefPart(this.pages.currentPage());
    this.UI.renderContentPart(pageXML_ContentPart, {vexWidth:this.getScoreWidth(pageXML_ContentPart), vexHeight:this.scoreHeight});
    this.UI.rendered_measures = MEI2VF.rendered_measures;
    this.UI.content_dims = MEI2VF.Converter.getStaffArea();
    this.UI.updateMainHeight();
    var clefoptions = {}
    clefoptions.page_margin_right = 0;
    clefoptions.page_margin_left = 10;
    clefoptions.scale = this.UI.scale;
    clefoptions.vexHeight = this.scoreHeight;
    this.UI.renderClefPart(pageXML_ClefPart, clefoptions);
    this.UI.rendered_clefmeasures = MEI2VF.rendered_measures;
    this.UI.resizeElements();
    this.UI.displayDots();
    this.UI.showTitle(this.pages.currentPageIndex === 0);
    this.UI.updatePageLabels(this.pages.currentPageIndex+1, this.pages.totalPages())
    this.UI.displayVoiceNames(pageXML_ClefPart, { x: clefoptions.page_margin_left + 20});
    this.UI.fabrCanvas.calcOffset();
  },

  nextPage: function(){
    this.pages.nextPage();
    this.displayCurrentPage_TwoParts();
    this.UI.dlg && this.UI.dlg.hide();
    // setTimeout(function(){this.UI.fabrCanvas.renderAll()}, 0);
  },

  prevPage: function(){
    this.pages.prevPage();
    this.displayCurrentPage_TwoParts();
    this.UI.dlg && this.UI.dlg.hide();
    // setTimeout(function(){this.UI.fabrCanvas.renderAll()}, 0);
  },

  jumpTo: function(i) {
    this.pages.jumpTo(i);
    this.displayCurrentPage_TwoParts();
    this.UI.dlg && this.UI.dlg.hide();
  },

  jumpToMeasure: function(i) {
    this.pages.jumpToMeasure(i);
    this.displayCurrentPage_TwoParts();
    this.UI.dlg && this.UI.dlg.hide();
  },
});
;meiView.CompactUI = function(options) {
  this.init(options);
}

meiView.Inherit(meiView.CompactUI, meiView.UI, {

  init: function(options) {
    this.options = options || {};
    this.viewer = options.viewer;
    this.maindiv = options.maindiv;
    this.canvas_id = 'meiview-canvas-' + this.viewer.id;
    this.canvas_clef_id = 'meiview-canvas-clef-' + this.viewer.id;
    $(this.maindiv).attr('id', this.viewer.id);
    $(this.maindiv).addClass('meiview-main');
    $(this.maindiv).addClass('ui-widget-content');

    var pageTurnButton = function(dir, id) {
      return '<button class="ui-widget-content ui-corner-all" onclick="meiView.UI.callback(\''
        + id + '\', \'' + dir + 'Page\')">\
        <span class="ui-icon ui-icon-triangle-1-'
        + ((dir !== 'next') ? ((dir !== 'prev') ? '' : 'w') : 'e')
        + '"/></button>';
    }
    this.base_html = '\
    <div class="main-area">\
      <div class="pagination-div" align="center">'
        + pageTurnButton('prev', this.viewer.id)
        + '<span id="pageNumber-top" width="10">0/0</span>'
        + pageTurnButton('next', this.viewer.id)
      + '</div>\
      <div class="meiview-canvas-container">\
        <div class="clef-canvas-div">\
          <canvas class="clef-canvas" id="' + this.canvas_clef_id + '"></canvas>\
        </div>\
        <div class="main-canvas-div" onscroll="meiView.UI.callback(\'' 
          + this.viewer.id + '-ui\', \'onScrollMainCanvas\', {})">\
          <canvas class="main-canvas" id="' + this.canvas_id + '"></canvas>\
        </div>\
      </div>\
      <div class="critrep-div ui-widget-content ui-corner-top" onclick="toggleCritRep()">\
      </div>\
      <div class="pagination-div" align="center">'
        + pageTurnButton('prev', this.viewer.id)
        + '<span id="pageNumber-top" width="10">0/0</span>'
        + pageTurnButton('next', this.viewer.id)
      + '</div>\
      <div class="sidebar ui-widget-content ui-corner-left" id="sidebar">\
        <div id="accordion">\
        </div>\
      </div>\
    </div>\
    '
    $(this.maindiv).append(this.base_html);

    this.main_area = $(this.maindiv).find('.main-area');
    this.options.sidebar_ratio = (typeof this.options.sidebar_ratio == 'undefined') ? 0.2 : this.options.sidebar_ratio;
    this.titleDiv = $(this.maindiv).find('.titlediv');
    this.dots = {};
    this.measure_n_texts = {};
    meiView.UI.addObject(this.viewer.id, this.viewer);
    meiView.UI.addObject(this.viewer.id + '-ui', this);
  
    var titleElem = $(this.maindiv).find('span.title')[0];
    $(titleElem).html(options.title);

    this.fillSideBar($(this.maindiv).find('#accordion'), 'meiview-sidebar');
    $(this.maindiv).find('#accordion').accordion({
      collapsible: true,
      heightStyle: "fill",
      active: false
    });
    if ($(this.maindiv).find('#accordion h3').length === 0) {
      this.hideSideBar();
    }

    this.fillCritReport();

    this.scale = options.scale || 1.0;

    this.fabrCanvas = this.initCanvas(this.canvas_id);
    this.canvasClef = $(this.maindiv).find('.clef-canvas').get();
    var dimensions = { width: $(this.canvasClef).width(), height: $(this.canvasClef).height() }
    this.fabrCanvasClef = new fabric.StaticCanvas(this.canvas_clef_id);
    this.fabrCanvasClef.setDimensions(dimensions)
    this.initSidebarHighlight();

    var me = this;
    $(window).on('resize', function(event){
//      console.log('window resized');
      me.resizeElements();
    });

  },

  updateMainHeight: function() {
    var h3s = $(this.maindiv).find('#accordion h3');
    var sidebar = $(this.maindiv).find('.sidebar');
    var minSidebarContentHeight = 100;
    var minSidebarDivHeight = h3s.length * h3s.height() + minSidebarContentHeight;

    //150 is an ugly constant to accommodate selector panels that may pop up
    var main_height = Math.max((this.content_dims.height + 150) * this.scale, minSidebarDivHeight);
    $(this.maindiv).find('.main-canvas-div').height(main_height);
    this.fabrCanvas.setDimensions({height: main_height});
    this.fabrCanvasClef.setDimensions({height: main_height});
     this.resizeElements();
  },

  maxCritRep: function() {
    $(this.maindiv).find('.critrep-div').removeClass('critrep-min');
    $(this.maindiv).find('.critrep-div').addClass('critrep-max');
    this.resizeElements();
  },

  minCritRep: function() {
    $(this.maindiv).find('.critrep-div').removeClass('critrep-max');
    $(this.maindiv).find('.critrep-div').addClass('critrep-min');
    this.resizeElements();
  },

  critRepState: function () {
    if ($(this.maindiv).find('critrep-div').hasClass('critrep-min')) {
      return "critrep-min";
    } else if ($(this.maindiv).find('critrep-div').hasClass('critrep-max')){
      return "critrep-max";
    }
    ;
  },

  showCritRep: function() {
    $(this.maindiv).find('.critrep-div').css('display', 'block');
    this.resizeElements();
  },

  hideCritRep: function() {
    $(this.maindiv).find('.critrep-div').css('display', 'none');
    this.resizeElements();
  },

  critRepOn: function () {
    return $(this.maindiv).find('.critrep-div').css('display') !== 'none';
  },

  showPagination: function() {
    $(this.maindiv).find('.pagination-div').css('display', 'block');
    this.resizeElements();
  },

  hidePagination: function() {
    $(this.maindiv).find('.pagination-div').css('display', 'none');
    this.resizeElements();
  },

  paginationOn: function () {
    return $(this.maindiv).find('.pagination-div').css('display') !== 'none';
  },

  onScrollMainCanvas: function() {
    this.fabrCanvas.calcOffset();
  },

  showSideBar: function() {
    $(this.maindiv).find('.sidebar').css('display', 'block');
    this.resizeElements();
  },

  hideSideBar: function() {
    $(this.maindiv).find('.sidebar').css('display', 'none');
    this.resizeElements();
  },

  sideBarLength: function() {
    return $(this.maindiv).find('.sidebar').find('h3.meiview-sidebar').length;
  },

  sideBarOn: function () {
    return $(this.maindiv).find('.sidebar').css('display') !== 'none';
  },

  renderContentPart: function(pageXML, options) {
    options = options || {};
    //TODO: set left padding and left margin to 0
    options.page_margin_left = 0;
    options.page_margin_right = 20;
    options.vexWidth = options.vexWidth || $(this.fabrCanvas.getElement()).attr('width');
    options.vexHeight = options.vexHeight || $(this.fabrCanvas.getElement()).attr('height');
    var img = this.renderMei2Img(pageXML, options);
    if (this.scoreImg) {
       this.fabrCanvas.remove(this.scoreImg);    
    }
    this.fabrCanvas.setDimensions({width:options.vexWidth * this.scale});
    var W = options.vexWidth * this.scale;
    var H = options.vexHeight * this.scale;
    this.scoreImg = new fabric.Image(img, {
      width:W,height:H, left:W/2, top:H/2,
      lockMovementX: true,
      lockMovementY: true,
      lockScalingX: true,
      lockScalingY: true,
      lockRotation: true,
      hasControls: false,
      hasBorders: false,
      selectable: false,
    });
    this.fabrCanvas.add(this.scoreImg);
    if (this.viewer.display_measure_numbers) {
      this.displayMeasureNos();
    }
    this.fabrCanvas.renderAll_Hack();
  },

  renderClefMei: function(staticCanvas, score, options) {
    options = options || {};

    options.vexWidth = options.vexWidth || $(this.fabrCanvas.getElement()).attr('width');
    options.vexHeight = options.vexHeight || $(this.fabrCanvas.getElement()).attr('height');
    options.scale = options.scale || 1.0;
    var score_width = options.vexWidth;
    var score_height = options.vexHeight;
    staticCanvas.setDimensions({width:options.vexWidth, height:options.vexHeight});
    this.L('Rendering clef part MEI... ');
    MEI2VF.render_notation(score, staticCanvas.getElement(), score_width, score_height, null, options);
    this.L('Done rendering clef part MEI');

  },

  alignCanvases: function () {
    $(this.maindiv).find('.main-canvas-div').position({
       my: 'left top',
       at: 'right top',
       of: $(this.maindiv).find('.clef-canvas-div'),
       collision: 'none'
     });
   },

  alignSidebar: function() {
    $(this.maindiv).find('.sidebar').position({
      my: 'left top',
      at: 'right top',
      of: $(this.maindiv).find('.meiview-canvas-container'),
      collision: 'none'
    });
  },

  resizeElements: function () {
      var viewerObj = this.viewer;
      var maindiv = this.maindiv;
      var view_main_width = $(maindiv).width();
      var main_canvas_div_height = $(maindiv).find('.main-canvas-div').height();
      canvas_container_width = view_main_width * (1 - this.options.sidebar_ratio);
      if ($(maindiv).find('.sidebar').css('display') === 'none') {
        canvas_container_width = view_main_width - 18;
      }
      var canvas_container_height = main_canvas_div_height;
      var clef_canvas_height = main_canvas_div_height;
      var sidebar_width = view_main_width - canvas_container_width;
      var sidebar_height = main_canvas_div_height;
      var clef_canvas_div_width = $(maindiv).find('.clef-canvas-div').width();
      var main_canvas_div_width = canvas_container_width - clef_canvas_div_width + 18;
      var pagination_heigh = (this.paginationOn()) ? $(maindiv).find('.pagination-div').height() : 0;
      var critrep_heigh = (this.critRepOn()) ? $(maindiv).find('.critrep-div').height() : 0;
      var main_area_height = main_canvas_div_height + 2 * pagination_heigh + critrep_heigh;
      $(maindiv).find('.clef-canvas-div').css('height', main_canvas_div_height);
      $(maindiv).find('.view').css('width', view_main_width);
      $(maindiv).find('.main-area').css('width', view_main_width);
      $(maindiv).find('.main-area').css('height', main_area_height);
      $(maindiv).find('.meiview-canvas-container').css('width', canvas_container_width);
      $(maindiv).find('.meiview-canvas-container').css('height', canvas_container_height);
      $(maindiv).find('.sidebar').css('width', sidebar_width);
      $(maindiv).find('.sidebar').css('height', sidebar_height);
      $(maindiv).find('.main-canvas-div').css('width', main_canvas_div_width);
      this.alignCanvases();
      this.alignSidebar();
      $(maindiv).find('#accordion').accordion('refresh');
    },


  renderClefPart: function(clefxml, options) {
    options = options || {};
    options.scale = options.scale || 1.0;
    options.vexWidth = options.vexWidth || $(this.canvasClef).attr('width');
    options.vexHeight = options.vexHeight || $(this.canvasClef).attr('height');

    var tempCanvas = this.renderClefMei(this.fabrCanvasClef, clefxml, options);
    var img = new Image;
    var vexStaffs = MEI2VF.rendered_measures[1];
    var w_max = 0;
    if (vexStaffs) {
      var i;
      $(vexStaffs).each(function(){
        if (this.getModifierXShift) {
          var w = this.getModifierXShift();
          if (w > w_max) {
            w_max = w;
          }
        }
      });
    }
//    console.log('max measure width: ' + w_max.toString());
//    console.log('scale: ' + options.scale.toString());
  
    $(this.maindiv).find('.clef-canvas-div').css('width', w_max * options.scale);
    $(this.canvasClef).css('width', $(this.canvasClef).width() * options.scale);
    $(this.canvasClef).css('height', $(this.canvasClef).height() * options.scale);

  },
  
  displayVoiceNames: function(score, base_offset) {
    base_offset.x = (typeof base_offset.x !== 'undefined') ? base_offset.x : 10;
    base_offset.y = (typeof base_offset.y !== 'undefined') ? base_offset.y : 20;
    var voiceNames = this.viewer.voiceNames(score);
    var this_UI = this;
    //1. Hide all voicename-divs
    $(this.maindiv).find('.voicename-div').hide();
    for (staff_n in voiceNames) {
      //2. display voiceNames[staff_n] in a voicename-div
      //corresponding to staff_n
      var voicename_div = this_UI.getVoiceNameDiv(staff_n);
      //3. position them according layout logic
      var measure = $(score).find('measure')[0];
      if (measure) {
        var measure_n = $(measure).attr('n') || "1";
        var vexStaffs = this.rendered_clefmeasures[measure_n];
        if (vexStaffs) {
          var vexStaff = vexStaffs[staff_n];
          if (vexStaff) {
            var canvas_offset = $(this.maindiv).find('canvas.clef-canvas').offset();
            var main_area_offset = $(this.main_area).offset();
            var dx = canvas_offset.left - main_area_offset.left;
            var dy = canvas_offset.top - main_area_offset.top;
            $(voicename_div).show();
            $(voicename_div).css('top', (vexStaff.y + base_offset.y + dy) * this_UI.scale);
            $(voicename_div).css('left', (vexStaff.x + base_offset.x + dx) * this_UI.scale);
            $(voicename_div).find('span').html(voiceNames[staff_n]);
            $(voicename_div).find('span').css('font-size', (this_UI.scale * 100).toString() + '%');
          }
        }
      }
    }
  },

  getVoiceNameDiv: function() {
    var voicename_div = $(this.maindiv).find('.voicename-div.staff-n-' + staff_n);
    if (voicename_div.length === 0) {
      $(this.main_area).append('<div class="voicename-div staff-n-' + staff_n +'">'
        + '<span></span></div>');
      return $(this.maindiv).find('.voicename-div.staff-n-' + staff_n);
    } else {
      return voicename_div;
    }
  },

  onSelectorSelect: function(args) {

    if (this.viewer.selectingState.ON) {

      var oldVarID = this.viewer.selectingState.selectedVarXmlID;
      this.viewer.selectVariant(args.varXmlID);

      /* re-draw current page [TODO: only re-draw if the change happened on the current page] */

      this.viewer.displayCurrentPage_TwoParts();
      if (this.dlg) { 
        this.dlg.bringToFront();
      }
    
      this.updateSidebar(this.viewer.selectingState.appID, oldVarID);
    }
  },


  displayDotForAPP: function(appID) {

    // In order to know what coordiantes to display the dot at, we have to
    // get the coordinates of the VexFlow staff object. VexFlow staff objects are 
    // exposed by MEI2VF via the MEI2VF.rendered_measures:
    // MEI2VF.rendered_measures is indexed by the measure number and staff number.
    // so, in order to retreive the right measure we have to know the measure number and the 
    // staff number:

    // get the meausure number first,
    var app = this.viewer.MEI.ALTs[appID].elem; 
    var parent_measure = $(app).parents('measure');
    var measure_n = parent_measure.attr('n');

    // then the staff number...
    var parent_staff = $(app).parents('staff');
    var staff_n;
    if (parent_staff.length === 0) {
      var child = $(app).find('[staff]')
      staff_n = $(child).attr('staff');
    } else {
      staff_n = parent_staff.attr('n');
    }

    // ...then display the dot at the coordinates specified by the
    // properties of MEI2VF.rendered_measures[measure_n][staff_n];
    var vexStaffs = this.rendered_measures[measure_n];
    if (vexStaffs) {
      var vexStaff = vexStaffs[staff_n];
      if (vexStaff) {
        var dotInfo = {
          appXmlID: appID, 
          measure_n: Number(measure_n),
          measure_top: vexStaff.y,
          measure_left: vexStaff.x,
          measure_width: vexStaff.width,
          staff_n: Number(staff_n),
        }
        return { circle:this.displayDotForMeasure(vexStaff), info:dotInfo };
      }
    }
  },
  
  fillCritReport: function() {

    var getTableBody = function(maindiv) {
      var table = $(maindiv).find('.critrep-div table.critrep tbody');
      if (table.length === 0) {
        $(maindiv).find('.critrep-div').append('<table class="critrep">'
          + '<tbody>'
            + '<tr>'
              + '<th>Measure</th>'
              + '<th>Voice</th>'
              + '<th>Type</th>'
              + '<th>Source/Responsibility</th>'
            + '</tr>'
          + '</tbody></table>');
        return $(maindiv).find('.critrep-div table.critrep tbody');
      } else {
        return table;
      }
    }

    // measure by measure
    var me = this;
//    console.log("Critical Report:")
//    console.log(this.viewer.Report);
    var tbody = getTableBody(this.maindiv);
    for (measure_n in this.viewer.Report) {
      var altlist = this.viewer.Report[measure_n];
      var i, j;
      for (i=0, j=altlist.length; i<j; ++i) {
        var alt = altlist[i];
        var measure_n = $(alt.elem).closest('measure').attr('n');
        var comma = '';
        var sourceresp = (alt.tagname == 'app') ? 'in ' : 'by ';
        for (altid in alt.altitems) {
          var listitem = '';
          if (alt.altitems[altid].tagname == 'rdg' && $(alt.altitems[altid].elem).attr('type') == 'variant') {
            listitem = alt.altitems[altid].source;
          } else if (alt.altitems[altid].tagname == 'corr') {
            listitem = alt.altitems[altid].resp;
          }
          if (listitem) {
            sourceresp += comma + listitem.replace(/#/g, '').replace(/ /g, ', ');
            if (comma == '') {
              comma = ', ';
            }
            $(me.maindiv).find('.critrep-div ul').append('<li>' + alt.xmlID + '</li>');
            $(tbody).append('<tr class="meiview-sidebar-item meiview-critrep-item"' 
              + me.onClickSideBarMarkup(me, measure_n, alt.xmlID) + '>'
              + '<td class="critrep-field critrep-measureno">' + 'M' + measure_n.toString() + '</td>'
              + '<td class="critrep-field critrep-voice">' + this.shortVoiceLabel(alt.elem) + '</td>'
              + '<td class="critrep-field critrep-type">' + ((alt.tagname == 'app') ? 'Variant' : 'Emendation') + '</td>'
              + '<td class="critrep-field critrep-sources">' + sourceresp +'</td>'
            + '</tr>');
          }
        }
      }
    }
    if ($(tbody).find('.meiview-critrep-item').length == 0) {
      this.hideCritRep();
    }
  },

});


