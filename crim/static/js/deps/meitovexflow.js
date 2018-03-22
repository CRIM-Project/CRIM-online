/*
* meilib.js
*
* Author: Zoltan Komives Created: 05.07.2013
*
* Copyright © 2012, 2013 Richard Lewis, Raffaele Viglianti, Zoltan Komives,
* University of Maryland
*
* Licensed under the Apache License, Version 2.0 (the "License"); you may not
* use this file except in compliance with the License. You may obtain a copy of
* the License at
*
* http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
* WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
* License for the specific language governing permissions and limitations under
* the License.
*/

/**
 * @class MeiLib
 * MeiLib - General purpose JavaScript functions for processing MEI documents.
 * @singleton
 */
var MeiLib = {};

/**
 * @class MeiLib.RuntimeError
 *
 * @constructor
 * @param {String} errorcode
 * @param {String} message
 */
MeiLib.RuntimeError = function(errorcode, message) {
  this.errorcode = errorcode;
  this.message = message;
}
/**
 * @method toString
 * @return {String} the string representation of the error
 */
MeiLib.RuntimeError.prototype.toString = function() {
  return 'MeiLib.RuntimeError: ' + this.errorcode + ': ' + this.message ? this.message : "";
}
/**
 * @class MeiLib
 * @singleton
 */

/**
 * @method createPseudoUUID
 */
MeiLib.createPseudoUUID = function() {
  return ("0000" + (Math.random() * Math.pow(36, 4) << 0).toString(36)).substr(-4)
}
/**
 * @class MeiLib.EventEnumerator
 * Enumerate over the children events of node (node is a layer, beam or tuplet).
 * @constructor
 * @param {Object} node an XML DOM object
 */
MeiLib.EventEnumerator = function(node, proportion) {
  this.init(node, proportion);
}
/**
 * @method init
 * @param {} node
 */
MeiLib.EventEnumerator.prototype.init = function(node, proportion) {
  if (!node)
    throw new MeiLib.RuntimeError('MeiLib.EventEnumerator.init():E01', 'node is null or undefined');
  this.node = node;
  this.next_evnt = null;
  this.EoI = true;
  // false if and only if next_evnt is valid.
  this.children = $(this.node).children();
  this.i_next = -1;
  this.proportion = proportion || {
    num: 1,
    numbase: 1
  };
  this.outputProportion = proportion || {
    num: 1,
    numbase: 1
  };
  this.read_ahead();
}
/**
 * @method nextEvent
 * @return
 */
MeiLib.EventEnumerator.prototype.nextEvent = function() {
  if (!this.EoI) {
    var result = this.next_evnt;
    this.read_ahead();
    return result;
  }
  throw new MeiLib.RuntimeError('MeiLib.LayerEnum:E01', 'End of Input.')
}
/**
 * @method read_ahead
 * @return
 */
MeiLib.EventEnumerator.prototype.read_ahead = function() {
  if (this.beam_enumerator) {
    if (!this.beam_enumerator.EoI) {
      this.next_evnt = this.beam_enumerator.nextEvent();
      this.EoI = false;
    } else {
      this.EoI = true;
      this.beam_enumerator = null;
      this.step_ahead()
    }
  } else {
    this.step_ahead()
  }
}
/**
 * @method step_ahead
 */
MeiLib.EventEnumerator.prototype.step_ahead = function() {++this.i_next;
  if (this.i_next < this.children.length) {
    this.next_evnt = this.children[this.i_next];
    var node_name = $(this.next_evnt).prop('localName');
    if (node_name === 'note' || node_name === 'rest' || node_name === 'mRest' || node_name === 'chord') {
      this.EoI = false
    } else if (node_name === 'beam') {
      this.beam_enumerator = new MeiLib.EventEnumerator(this.next_evnt);
      if (!this.beam_enumerator.EoI) {
        this.next_evnt = this.beam_enumerator.nextEvent();
        this.EoI = false;
      } else {
        this.EoI = true;
      }
    } else if (node_name === 'tuplet') {
      
      var proportion = {
        num: this.proportion.num * +this.next_evnt.getAttribute('num') || 3,
        numbase: this.proportion.numbase * +this.next_evnt.getAttribute('numbase') || 2        
      };

      this.beam_enumerator = new MeiLib.EventEnumerator(this.next_evnt, proportion);
      if (!this.beam_enumerator.EoI) {
        this.outputProportion = this.beam_enumerator.outputProportion;
        this.next_evnt = this.beam_enumerator.nextEvent();
        this.EoI = false;
      } else {
        this.outputProportion = this.proportion;
        this.EoI = true;
      }
    }
  } else {
    this.EoI = true;
  }
}
/**
 * @class MeiLib
 * @singleton
 */

/**
 * @method durationOf
 * Calculate the duration of an event (number of beats) according to the given
 * meter.
 *
 * Event refers to musical event such as notes, rests, chords. The MEI element
 * <b>space</b> is also considered an event.
 *
 * @param evnt an XML DOM object
 * @param meter the time signature object { count, unit }
 */
MeiLib.durationOf = function(evnt, meter) {

  IsSimpleEvent = function(tagName) {
    return (tagName === 'note' || tagName === 'rest' || tagName === 'space');
  }
  var durationOf_SimpleEvent = function(simple_evnt, meter) {
    var dur = $(simple_evnt).attr('dur');
    if (!dur)
      throw new MeiLib.RuntimeError('MeiLib.durationOf:E04', '@dur of <b>note</b>, <b>rest</b> or <b>space</b> must be specified.');
    return MeiLib.dotsMult(simple_evnt) * MeiLib.dur2beats(Number(dur), meter);
  }
  var durationOf_Chord = function(chord, meter, layer_no) {
    if (!layer_no)
      layer_no = "1";
    var dur = $(chord).attr('dur');
    var dotsMult = MeiLib.dotsMult(chord);
    if (dur)
      return dotsMult * MeiLib.dur2beats(Number(dur), meter);
    $(chord).find('note').each(function() {
      lyr_n = $(this).attr('layer');
      if (!lyr_n || lyr_n === layer_no) {
        var dur_note = $(this).attr('dur');
        var dotsMult_note = MeiLib.dotsMult(chord);
        if (!dur && dur_note) {
          dur = dur_note;
          dotsMult = dotsMult_note;
        } else if (dur && dur != dur_note) {
          throw new MeiLib.RuntimeError('MeiLib.durationOf:E05', 'duration of <chord> is ambiguous.');
        }
      }
    });
    if (dur)
      return dotsMult * MeiLib.dur2beats(Number(dur), meter);
    throw new MeiLib.RuntimeError('MeiLib.durationOf:E06', '@dur of chord must be specified either in <chord> or in at least one of its <note> elements.');
  }
  var durationOf_Beam = function(beam, meter) {
    var acc = 0;
    $(beam).children().each(function() {
      var dur_b;
      var dur;
      var tagName = this.localName;
      if (IsSimpleEvent(tagName)) {
        dur_b = durationOf_SimpleEvent(this, meter);
      } else if (tagName === 'chord') {
        dur_b = durationOf_Chord(this, meter);
      } else if (tagName === 'beam') {
        dur_b = durationOf_Beam(this, meter);
      } else if (tagName === 'tuplet') {
        dur_b = durationOf_Tuplet(this, meter);
      } else {
        throw new MeiLib.RuntimeError('MeiLib.durationOf:E03', "Not supported element '" + tagName + "'");
      }
      acc += dur_b;
    });
    return acc;
  }
  var durationOf_Tuplet = function(tuplet, meter) {
    // change the meter unit according to the ratio in the tuplet, the get the duration as if the tuplet were a beam 
    var num = +tuplet.getAttribute('num') || 3;
    var numbase = +tuplet.getAttribute('numbase') || 2;
    var acc = durationOf_Beam(tuplet, {
      count : meter.count,
      unit : meter.unit * numbase / num
    });
    return acc;
  }
  var evnt_name = $(evnt).prop('localName');
  if (IsSimpleEvent(evnt_name)) {
    return durationOf_SimpleEvent(evnt, meter);
  }
  if (evnt_name === 'mRest') {
    return meter.count;
  }
  if (evnt_name === 'chord') {
    return durationOf_Chord(evnt, meter);
  }
  if (evnt_name === 'beam') {
    return durationOf_Beam(evnt, meter);
  }
  if (evnt_name === 'tuplet') {
    return durationOf_Tuplet(evnt, meter);
  }
  throw new MeiLib.RuntimeError('MeiLib.durationOf:E05', "Not supported element: '" + evnt_name + "'");

}
/**
 * @method tstamp2id
 * Find the event with the minimum distance from of the given timestamp.
 *
 * @param {String} tstamp the timestamp to match against events in the given
 * context. Local timestamp only (without measure part).
 * @param {Object} layer an XML DOM object, contains all events in the given
 * measure.
 * @param {Object} meter the effective time signature object { count, unit } in
 * the measure containing layer.
 * @return {String} the xml:id of the closest element, or
 * undefined if <b>layer</b> contains no events.
 */
MeiLib.tstamp2id = function(tstamp, layer, meter) {
  var ts = Number(tstamp);
  var ts_acc = 0;
  // total duration of events before current event
  var c_ts = function() {
    return ts_acc + 1;
  }// tstamp of current event
  var distF = function() {
    return ts - c_ts();
  }// signed distance between tstamp and tstamp of current event;
  var eventList = new MeiLib.EventEnumerator(layer);
  var evnt;
  var dist;
  var prev_evnt;
  // previous event
  var prev_dist;
  // previous distance
  while (!eventList.EoI && (dist === undefined || dist > 0)) {
    prev_evnt = evnt;
    prev_dist = dist;
    evnt = eventList.nextEvent();
    dist = distF();
    ts_acc += MeiLib.durationOf(evnt, meter) 
      * eventList.outputProportion.numbase 
      / eventList.outputProportion.num;
    m = meter;
    e = evnt;
  }

  if (dist === undefined)
    return undefined;
  var winner;
  if (dist < 0) {
    if (prev_evnt && prev_dist < Math.abs(dist)) {
      winner = prev_evnt;
    } else {
      winner = evnt;
    }
  } else {
    winner = evnt;
  }
  var xml_id;
  xml_id = $(winner).attr('xml:id');
  if (!xml_id) {
    xml_id = MeiLib.createPseudoUUID();
    $(winner).attr('xml:id', xml_id);
  }
  return xml_id;
}
/**
 * @method XMLID
 * returns the xml:id attribute of an element; if there is none, the function
 * created a pseudo id, adds it to the element and returns that id.
 * @param {XMLElement} elem the element to process
 * @return {String} the xml:id of the element
 */
MeiLib.XMLID = function(elem) {
  xml_id = $(elem).attr('xml:id');
  if (!xml_id) {
    xml_id = MeiLib.createPseudoUUID();
    $(elem).attr('xml:id', xml_id);
  }
  return xml_id;
}
/**
 * @method id2tstamp
 * Calculates a timestamp value for an event in a given context. (Event refers
 * to musical events such as notes, rests and chords).
 *
 * @param eventid {String} the xml:id of the event
 * @param context {Array} of contextual objects {layer, meter}. Time signature
 * is mandatory for the first one, but optional for the rest. All layers belong
 * to a single logical layer. They are the layer elements from some consequtive
 * measures.
 * @return {String} the MEI timestamp value (expressed in beats relative to the
 * meter of the measure containing the event) of all events that happened before
 * the given event in the given context. If the event is not in the first
 * measure (layer) the timestamp value contains a 'measure part', that is for
 * example 2m+2 if the event is at the second beat in the 3rd measure.
 */
MeiLib.id2tstamp = function(eventid, context) {
  var meter;
  var found = false;
  for (var i = 0; i < context.length && !found; ++i) {
    if (context[i].meter)
      meter = context[i].meter;
    if (i === 0 && !meter)
      throw new MeiLib.RuntimeError('MeiLib.id2tstamp:E001', 'No time signature specified');

    var result = MeiLib.sumUpUntil(eventid, context[i].layer, meter);
    if (result.found) {
      found = true;
      return i.toString() + 'm' + '+' + (result.beats + 1).toString();
    }
  }
  throw new MeiLib.RuntimeError('MeiLib.id2tstamp:E002', 'No event with xml:id="' + eventid + '" was found in the given MEI context.');
};

/**
 * @method dur2beats
 * Convert absolute duration into relative duration (nuber of beats) according
 * to time signature.
 *
 * @param dur {Number} reciprocal value of absolute duration (e.g. 4->quarter
 * note, 8->eighth note, etc.)
 * @param {Object} meter the time signature object { count, unit }
 * @return {Number}
 */
MeiLib.dur2beats = function(dur, meter) {
  return (meter.unit / dur);
}
/**
 * @method beats2dur
 * Convert relative duration (nuber of beats) into absolute duration (e.g.
 * quarter note, eighth note, etc) according to time signature.
 *
 * @param beats {Number} duration in beats @param meter time signature object {
 * count, unit } @return {Number} reciprocal value of absolute duration (e.g. 4
 * -> quarter note, 8 -> eighth note, etc.)
 */
MeiLib.beats2dur = function(beats, meter) {
  return (meter.unit / beats);
}
/**
 * @method dotsMult
 * Converts the <b>dots</b> attribute value into a duration multiplier.
 *
 * @param node XML DOM object containing a node which may have <code>dots</code>
 * attribute
 * @return {Number} The result is 1 if no <code>dots</code> attribute is present.
 * For <code>dots="1"</code> the result is 1.5, for <code>dots="2"</code> the
 * result is 1.75, etc.
 */
MeiLib.dotsMult = function(node) {
  var dots = $(node).attr('dots');
  dots = Number(dots || "0");
  var mult = 1;
  for (; dots > 0; --dots) {
    mult += (1 / Math.pow(2, dots))
  };
  return mult;
}
/**
 * @method sumUpUntil
 * For a given event (such as note, rest chord or space) calculates the combined
 * legth of preceding events, or the combined lenght of all events if the given
 * event isn't present.
 *
 * @param {String} eventid the value of the xml:id attribute of the event
 * @param {Object} layer an XML DOM object containing the MEI <b>Layer</b>
 * element
 * @param {Object} meter the time signature object { count, unit }
 * @return {Object} an object { beats:number, found:boolean }. 1. 'found' is true
 * and 'beats' is the total duration of the events that happened before the event
 * 'eventid' within 'layer', or 2. 'found' is false and 'beats is the total
 * duration of the events in 'layer'.
 */
MeiLib.sumUpUntil = function(eventid, layer, meter) {

  var sumUpUntil_inNode = function(node_elem) {
    var beats, children, found, dur, dots, subtotal, chord_dur, i;
    var node = $(node_elem);
    var node_name = node.prop('localName');
    if (node_name === 'note' || node_name === 'rest') {
      if (node.attr('xml:id') === eventid) {
        return {
          beats : 0,
          found : true
        };
      } else {
        dur = Number(node.attr('dur'));
        if (!dur)
          throw new MeiLib.RuntimeError('MeiLib.sumUpUntil:E001', "Duration is not a number ('breve' and 'long' are not supported).");
        dots = node.attr('dots');
        dots = Number(dots || "0");
        beats = MeiLib.dotsMult(node) * MeiLib.dur2beats(dur, meter);

        return {
          beats : beats,
          found : false
        };
      }
    } else if (node_name === 'mRest') {
      if (node.attr('xml:id') === eventid) {
        found = true;
        return {
          beats : 0,
          found : true
        };
      } else {
        return {
          beats : meter.count,
          found : false
        };
        // the duration of a whole bar expressed in number of beats.
      }
    } else if (node_name === 'layer' || node_name === 'beam' || node_name === 'tuplet') {

      // sum up childrens' duration
      beats = 0;
      children = node.children();
      found = false;
      for ( i = 0; i < children.length && !found; ++i) {
        subtotal = sumUpUntil_inNode(children[i]);
        beats += subtotal.beats;
        found = subtotal.found;
      }
      return {
        beats : beats,
        found : found
      };
    } else if (node_name === 'chord') {
      chord_dur = node.attr('dur');
      if (node.attr('xml:id') === eventid) {
        return {
          beats : 0,
          found : true
        };
      } else {
        // ... or find the longest note in the chord ????
        chord_dur = node.attr('dur');
        if (chord_dur) {
          if (node.find("[xml\\:id='" + eventid + "']").length) {
            return {
              beats : 0,
              found : true
            };
          } else {
            return {
              beats : MeiLib.dur2beats(chord_dur, meter),
              found : found
            };
          }
        } else {
          children = node.children();
          found = false;
          for ( i = 0; i < children.length && !found; ++i) {
            subtotal = sumUpUntil_inNode(children[i]);
            beats = subtotal.beats;
            found = subtotal.found;
          }
          return {
            beats : beats,
            found : found
          };
        }
      };
    }
    return {
      beats : 0,
      found : false
    };
  }

  return sumUpUntil_inNode(layer);
}

/**
 * @method SliceMEI
 * Returns a slice of the MEI. The slice is specified by the number of the
 * starting and ending measures.
 *
 * About the <code>staves</code> parameter: it specifies a list of staff
 * numbers. If it is defined, only the listed staves will be kept in the
 * resulting slice. The following elements will be removed from:
 *
 * 1. <b>staffDef</b> elements (@staff value is matched against the specified list)
 * 2. <b>staff</b> elements (@n value is matched against the specified list)
 * 3. any other child element of measures that has
 *
 * @staff specified AND it is not listed.
 *
 * Note that <b>staff</b> elements without @n will be removed.
 *
 * @param {Object} params like { start_n:NUMBER, end_n:NUMBER, noKey:BOOLEAN,
 *            noClef:BOOLEAN, noMeter:BOOLEAN, noConnectors, staves:[NUMBER] },
 *            where <code>noKey</code>, <code>noClef</code> and
 *            <code>noMeter</code> and <code>noConnectors</code> are
 *            optional. taves is optional. If staves is set, it is an array of
 *            staff numbers. Only the staves specified in the list will be
 *            included in the resulting MEI.
 * @return XML DOM object
 */
MeiLib.SliceMEI = function(MEI, params) {

  var setVisibles = function(elements, params) {
    $.each(elements, function(i, elem) {
      if (params.noClef)
        $(elem).attr('clef.visible', 'false');
      if (params.noKey)
        $(elem).attr('key.sig.show', 'false');
      if (params.noMeter)
        $(elem).attr('meter.rend', 'false');
    });
  }
  var paramsStaves = params.staves;
  if (paramsStaves) {
    var staffDefSelector = '';
    var staffNSelector = '';
    var commaspace = '';
    for (var i = 0; i < paramsStaves.length; i++) {
      staffDefSelector += commaspace + '[n="' + paramsStaves[i] + '"]';
      staffNSelector += commaspace + '[staff="' + paramsStaves[i] + '"]'
      if (i === 0)
        commaspace = ', ';
    }
  }

  var slice = MEI.cloneNode(true);
  var scoreDefs;
  if (paramsStaves)
    $(slice).find('staffDef').remove(':not(' + staffDefSelector + ')');
  if (params.noClef || params.noKey || params.noMeter) {
    scoreDef = $(slice).find('scoreDef')[0];
    var staffDefs = $(scoreDef).find('staffDef');
    setVisibles($(scoreDef), params);
    setVisibles(staffDefs, params);
  }
  if (params.noConnectors) {
    $(slice).find('staffGrp').removeAttr('symbol');
  }
  var section = $(slice).find('section')[0];
  var inside_slice = false;

  /**
   * Keep or remove child from section depending whether it's inside the section or not.
   * If it's kept, remove unwanted staves
   */
  var keepOrRemove = function(elem, inside_slice, staffNSelector, params) {
    if (!inside_slice) {
      if (elem.localName === 'measure' && Number($(elem).attr('n')) === params.start_n) {
        inside_slice = true;
      } else {
        elem.parentNode.removeChild(elem);
      }
    }

    if (inside_slice) {
      // remove unwanted staff
      if (params.staves) {
        $(elem).find('[staff]').remove(':not(' + staffNSelector + ')');
        var staves = $(elem).find('staff');
        $(staves).each(function() {
          var staff = this;
          if ($.inArray(Number($(staff).attr('n')), params.staves) === -1) {
            var parent = this.parentNode;
            parent.removeChild(this);
          }
        })
      }

      // finish inside_slice state if it's the end of slice.
      if (elem.localName === 'measure' && Number($(elem).attr('n')) === params.end_n) {
        inside_slice = false;
      }
    }
    return inside_slice;
  }

  /*
   * Iterate through each child of the section and remove everything outside
   * the slice. Remove
   */
  var section_children = section.childNodes;

  $(section_children).each(function() {

    if (this.localName === 'ending') {
      var ending_children = this.childNodes;
      $(ending_children).each(function() {
        inside_slice = keepOrRemove(this, inside_slice, staffNSelector, params);
      });
      if ($(this).find('measure').length === 0) {
        this.parentNode.removeChild(this);
      }
    } else {
      inside_slice = keepOrRemove(this, inside_slice, staffNSelector, params);
    }

  });

  return slice;
}
/**
 * Represents an MEI <b>app</b> or <b>choice</b> element.
 *
 * @class MeiLib.Alt
 * @constructor
 * @param {String} xmlID the xml:id attribute value of the <b>app</b> or
 * <b>choice</b> element.
 * @param {String} parentID the xml:id attribute value of the direct parent
 * element of the <b>app</b> or <b>choice</b> element.
 */
MeiLib.Alt = function(elem, xmlID, parentID, tagname) {
  this.elem = elem;
  this.xmlID = xmlID;
  this.altitems = [];
  this.parentID = parentID;
  this.tagname = tagname;
}

MeiLib.Alt.prototype.getDefaultItem = function() {

  /* find the editors pick or the first alternative */
  var findDefault = function(altitems, editorspick_tagname, other_tagname) {
    var i;
    var first_sic;
    for (alt in altitems) {
      if (altitems[alt].tagname === editorspick_tagname) {
        return altitems[alt];
      } else if (!first_sic && (altitems[alt].tagname === other_tagname)) {
        first_sic = altitems[alt];
      }
    };
    return first_sic;
  }
  if (this.tagname === 'choice') {
    return findDefault(this.altitems, 'corr', 'sic');
  } else if (this.tagname === 'app') {
    return findDefault(this.altitems, 'lem');
  }
}
/**
 * @class MeiLib.Variant
 * Represents a <b>lem</b>, <b>rdg</b>, <b>sic</b> or <b>corr</b> element.
 *
 * @constructor
 * @param xmlID {String} the xml:id attribute value of the element.
 * @param tagname {String} 'lem' for <b>lem</b> and 'rdg for <b>rdg</b> elements.
 * @param source {String} space-separated list of the source IDs what the given
 *            item belongs to.
 * @param resp {String} xmlID of the editor responsible for the given reading or
 *            correction.
 * @param n {String} @n attribute value of the element.
 */
MeiLib.Variant = function(elem, xmlID, tagname, source, resp, n) {
  this.elem = elem;
  this.xmlID = xmlID;
  this.tagname = tagname;
  this.source = source;
  this.resp = resp;
  this.n = n;
}
/**
 * @class MeiLib.MeiDoc
 * A Rich MEI is an MEI that contain ambiguity represented by Critical Apparatus
 * (<b>app</b>, <b>rdg</b>, etc.), or Editorial Transformation (<b>choice</b>,
 * <b>corr</b>, etc.)
 * elements.
 *
 * @constructor
 * @param {XMLDocument} meiXmlDoc the MEI document.
 */
MeiLib.MeiDoc = function(meiXmlDoc) {
  if (meiXmlDoc)
    this.init(meiXmlDoc);
}
/**
 * @method init
 * Initializes a <code>MeiLib.MeiDoc</code> object.
 *
 * The constructor extracts information about alternative encodings and compiles
 * them into a JS object (this.ALTs). The obejcts are exposed as per the
 * following: 1. <code>sourceList</code> is the list of sources as defined in
 * the MEI header (meiHead). 2. <code>editorList</code> is the list of editors
 * listed in the MEI header. 3. <code>ALTs</code> is the object that contains
 * information about the alternative encodings. It contains one entry per for
 * each <b>app</b> or <b>choice</b> element. It is indexed by the xml:id
 * attribute value of the elements. 4. <code>altgroups</code> is the obejct that
 * contains how <b>app</b> and <b>choice</b> elements are grouped together to
 * form a logical unit of alternative encoding.
 *
 * @param {XMLDocument} meiXmlDoc an XML document containing the rich MEI
 */
MeiLib.MeiDoc.prototype.init = function(meiXmlDoc) {
  this.xmlDoc = meiXmlDoc;
  this.rich_head = meiXmlDoc.getElementsByTagNameNS(
  "http://www.music-encoding.org/ns/mei", 'meiHead')[0];
  this.rich_music = meiXmlDoc.getElementsByTagNameNS(
  "http://www.music-encoding.org/ns/mei", 'music')[0];
  this.rich_score = $(this.rich_music).find('score')[0];
  this.parseSourceList();
  this.parseEditorList();
  this.parseALTs();
  this.initAltgroups();
  this.initSectionView();
}
/**
 * @method getRichScore
 */
MeiLib.MeiDoc.prototype.getRichScore = function() {
  return this.rich_score;
}
/**
 * @method getPlainScore
 */
MeiLib.MeiDoc.prototype.getPlainScore = function() {
  return this.plain_score;
}
/**
 * @method getALTs
 */
MeiLib.MeiDoc.prototype.getALTs = function() {
  return this.ALTs;
}
/**
 * @method getSourceList
 */
MeiLib.MeiDoc.prototype.getSourceList = function() {
  return this.sourceList;
}
/**
 * @method getEditorList
 */
MeiLib.MeiDoc.prototype.getEditorList = function() {
  return this.editorList;
}
/**
 * @method parseSourceList
 * Extracts information about the sources as defined in the MEI header.
 *
 * @return {Object} is a container indexed by the xml:id attribute value of the
 *         <b>sourceDesc</b> element.
 */
MeiLib.MeiDoc.prototype.parseSourceList = function() {
  // var srcs = $(this.rich_head).find('sourceDesc').children();
  // this.sourceList = {};
  // var i
  // for(i=0;i<srcs.length;++i) {
  // var src = srcs[i];
  // var xml_id = $(src).attr('xml:id');
  // var serializer = new XMLSerializer();
  // this.sourceList[xml_id] = serializer.serializeToString(src);
  // }
  // return this.sourceList;
  this.sources = $(this.rich_head).find('sourceDesc').children();
  return this.sources;
}
/**
 * @method parseEditorList
 */
MeiLib.MeiDoc.prototype.parseEditorList = function() {
  // var edtrs = $(this.rich_head).find('titleStmt').children('editor');
  // this.editorList = {};
  // var i
  // for(i=0;i<edtrs.length;++i) {
  // var edtr = edtrs[i];
  // var xml_id = $(edtr).attr('xml:id');
  // this.editorList[xml_id] = edtr;
  // }
  this.editors = $(this.rich_head).find('titleStmt').children('editor');
  return this.editors;
}
/**
 * @method parseALTs
 * Extracts information about the elements encoding alternatives. The method
 * stores its result in the <code>ALTs</code> property.
 *
 * <code>ALTs</code> is a container of MeiLib.Alt obejcts indexed by the
 * xml:id attribute value of the <b>app</b> or <b>choice</b> elements.
 */
MeiLib.MeiDoc.prototype.parseALTs = function() {
  var i, j;
  this.ALTs = {};
  // console.log(this.rich_score);
  var apps = $(this.rich_score).find('app, choice');
  for ( i = 0; i < apps.length; i++) {
    var app = apps[i];
    var parent = app.parentNode;
    var altitems = $(app).find('rdg, lem, sic, corr');
    var AppsItem = new MeiLib.Alt(app, MeiLib.XMLID(app), MeiLib.XMLID(parent), app.localName);
    AppsItem.altitems = {};
    for ( j = 0; j < altitems.length; j++) {
      var altitem = altitems[j];
      var source = $(altitem).attr('source');
      var resp = $(altitem).attr('resp');
      var n = $(altitem).attr('n');
      var tagname = $(altitem).prop('localName');
      var varXMLID = MeiLib.XMLID(altitem);
      AppsItem.altitems[varXMLID] = new MeiLib.Variant(altitem, varXMLID, tagname, source, resp, n);
    }
    this.ALTs[MeiLib.XMLID(app)] = AppsItem;
  }
}
/**
 * @method initAltgroups
 */
MeiLib.MeiDoc.prototype.initAltgroups = function() {
  var i, j;
  var ALTs = this.ALTs;
  annots = $(this.rich_score).find('annot[type="appGrp"], annot[type="choiceGrp"]');
  this.altgroups = {};
  for ( i = 0; i < annots.length; i++) {
    altgroup = [];
    token_list = $(annots[i]).attr('plist').split(' ');
    for ( j = 0; j < token_list.length; j++) {
      altgroup.push(token_list[j].replace('#', ''));
    }
    for (j in altgroup) {
      this.altgroups[altgroup[j]] = altgroup;
    }
  };
}
/**
 * @method initSectionView
 * The MeiLib.MeiDoc.initSectionView transforms the rich MEI (this.rich_score)
 * into a plain MEI (this.sectionview_score)
 *
 * An MEI is called 'plain' MEI if it contains no <b>app</b> or <b>choice</b>
 * elements.
 * Such an MEI can also be referred after the analogy of 2D section views of a
 * 3D object: the rich MEI is a higher-dimensional object, of which we would
 * like to display a 'flat' section view. The term 'section plane' refers to a
 * combination of alternatives at different locations in the score. The section
 * plane defines the actual view of the higher-dimensional object. For instance,
 * consider a score that has two different variants at measure #5 (let's call
 * them (variant A and variant B), and it contains three different variants at
 * measure #10 (let's call those ones variants C, D and E). In this case the
 * section plane would contain two elements the first one is either A or B, the
 * second one is C, D or E.
 *
 * The extracted information about all the <b>app</b> and <b>choice</b> elements
 * are stored in an array. Using this array the application can access information
 * such as what alternative encodings are present in the score, what source a
 * variant comes from, etc. This array is exposed by te <code>ALTs</code>
 * property.
 *
 */

MeiLib.MeiDoc.prototype.selectDefaultAlternative = function(alt) {
  var result = {};
  if (alt.localName === 'choice') {
    // ...the default replacement is...
    var corr = $(alt).find('corr')[0];
    if (corr) {
      // ...the first corr...
      result.alt_item_xml_id = MeiLib.XMLID(corr);
      result.alt_item = corr;
      //...or
    } else {
      // ...the first sic.
      var sic = $(alt).find('sic')[0];
      if (sic) {
        result.alt_item_xml_id = MeiLib.XMLID(sic);
        result.alt_item = sic;
      } else {
        result = {};
      }
    }
  } else {
    var lem = $(alt).find('lem')[0];
    if (lem) {
      // ...the first lem...
      result.alt_item_xml_id = MeiLib.XMLID(lem);
      result.alt_item = lem;
      //...or nothing:
    } else {
      result = {};
    }
  }
  return result;
}

MeiLib.MeiDoc.prototype.initSectionView = function(altReplacements) {
  altReplacements = altReplacements || {};
  // Make a copy of the rich MEI. We don't want to remove nodes from the
  // original object.
  this.sectionview_score = this.rich_score.cloneNode(true);
  this.sectionplane = {};

  // Transform this.sectionview_score into a plain MEI:
  //
  // * itereate through all <app> and <choice> elements:
  // o chose the appropriate rdg or lem defined by sectionplane
  // (sectionplane[app.xmlID]).
  // If nothing is defined, leave it empty.
  // o chose the appropriate sic or corr defined by sectionplance
  // (sectionplane[choice.xmlID])
  // If nothing is defined, chose the first corr, if exists, otherwise chose
  // sic, if exists.
  // When replacing an item, mark the location of replacement with XML
  // processing instructions.

  var alts = $(this.sectionview_score).find('app, choice');

  var alt_item2insert;
  var alt_item_xml_id;
  var this_sectionview_score = this.sectionview_score;
  var this_sectionplane = this.sectionplane;
  var this_ALTs = this.ALTs;
  var xmlDoc = this.xmlDoc;
  var me = this;
  $(alts).each(function(i, alt) {
    var alt_xml_id = MeiLib.XMLID(alt);
    var replacement = altReplacements[alt_xml_id];
    if (replacement) {
      // apply replacement, or...
      alt_item_xml_id = replacement.xmlID;
      var alt_item2insert = $(this_sectionview_score).find(replacement.tagname + '[xml\\:id="' + alt_item_xml_id +'"]')[0];
      if (!alt_item2insert)
        throw new MeiLib.RuntimeError('MeiLib.MeiDoc.prototype.initSectionView():E01', "Cannot find <lem>, <rdg>, <sic>, or <corr> with @xml:id '" + alt_item_xml_id + "'.");
    } else {
      var defaultAlt = me.ALTs[alt_xml_id].getDefaultItem();
      if (defaultAlt) {
        alt_item_xml_id = defaultAlt.xmlID;
        alt_item2insert = defaultAlt.elem;
      }
    }
    var parent = alt.parentNode;
    var PIStart = xmlDoc.createProcessingInstruction('MEI2VF', 'rdgStart="' + alt_xml_id + '"');
    parent.insertBefore(PIStart, alt);
    if (alt_item2insert) {
      var childNodes = alt_item2insert.childNodes;
      var i;
      for ( i = 0; i < childNodes.length; ++i) {
        parent.insertBefore(childNodes.item(i).cloneNode(true), alt);
      };
    }
    var PIEnd = xmlDoc.createProcessingInstruction('MEI2VF', 'rdgEnd="' + alt_xml_id + '"');
    parent.insertBefore(PIEnd, alt);
    parent.removeChild(alt);

    this_sectionplane[alt_xml_id] = [];
    if (this_ALTs[alt_xml_id].altitems[alt_item_xml_id]) {
      this_sectionplane[alt_xml_id].push(this_ALTs[alt_xml_id].altitems[alt_item_xml_id]);
    }
  })

  return this.sectionview_score;

}
/**
 * @method updateSectionView
 * Updates the sectionview score (plain MEI) by replacing one or more
 * alternative instance with other alternatives.
 *
 * @param sectionplaneUpdate
 *            {object} the list of changes. It is an container of xml:id
 *            attribute values of <b>rdg</b>, <b>lem</b>, <b>sic</b> or
 * <b>corr</b> elements,
 *            indexed by the xml:id attribute values of the corresponding
 * <b>app</b>
 *            or <b>choice</b> elements. sectionplaneUpdate[altXmlID] =
 * altInstXmlID
 *            is the xml:id attribute value of the <b>rdg</b>, <b>lem</b>,
 * <b>sic</b> or <b>corr</b>
 *            element, which is to be inserted in place of the original <app
 *            xml:id=altXmlID> or <b>choice xml:id=altXmlID</b> When replacing an
 *            <b>app</b> or <b>choice</b> that is part of a group of such
 * elements
 *            (defined by this.altgroups), then those other elements needs to be
 *            replaced as well.
 */
MeiLib.MeiDoc.prototype.updateSectionView = function(sectionplaneUpdate) {

  var corresponding_alt_item = function(altitems, altitem) {
    var vars_match = function(v1, v2) {
      var res = 0;
      for (var field in v1) {
        if (v1[field] !== undefined && v1[field] === v2[field]) {
          res++;
        }
      }
      console.log('vars_match: ' + res);
      return res;
    }
    var max = 0;
    var corresponding_item;
    for (var alt_item_id in altitems) {
      M = vars_match(altitems[alt_item_id], altitem);
      if (max < M) {
        max = M;
        corresponding_item = altitems[alt_item_id];
      }
    }
    return corresponding_item;
  }
  for (altID in sectionplaneUpdate) {
    var this_ALTs = this.ALTs;
    var altitems2insert = [];
    // preserving backward compatibility:
    if ( typeof sectionplaneUpdate[altID] === 'string') {
      sectionplaneUpdate[altID] = [sectionplaneUpdate[altID]];
    }
    if (sectionplaneUpdate[altID].length > 0) {
      $(sectionplaneUpdate[altID]).each(function() {
        altitems2insert.push(this_ALTs[altID].altitems[this]);
      });
    } else {
      var defaultAltItem = this.ALTs[altID].getDefaultItem();
      if (defaultAltItem) {
        altitems2insert.push(defaultAltItem);
      }
    }
    altgroup = this.altgroups[altID];
    if (altgroup) {
      // if altID is present in altgroups, then replace all corresponding alts
      // with the
      // altitems that correspons to the any of the alt item that are being
      // inserted.
      var i;
      for ( i = 0; i < altgroup.length; i++) {
        altID__ = altgroup[i];
        var altitems2insert__ = [];
        $(altitems2insert).each(function() {
          altitems2insert__.push(corresponding_alt_item(this_ALTs[altID__].altitems, this))
        });
        this.replaceAltInstance({
          appXmlID : altID__,
          replaceWith : altitems2insert__
        });
      }
    } else {
      // otherwise just replace alt[xml:id=altID] with the list of items
      this.replaceAltInstance({
        appXmlID : altID,
        replaceWith : altitems2insert
      });
    }
  }
}
/**
 * @method replaceAltInstance
 * Replace an alternative instance in the sectionview score and in the
 * sectionplane
 *
 * @param {Object} alt_inst_update
 * @return the updated score
 */
MeiLib.MeiDoc.prototype.replaceAltInstance = function(alt_inst_update) {

  var extendWithNodeList = function(nodeArray, nodeList) {
    var res = nodeArray;
    var i;
    for ( i = 0; i < nodeList.length; ++i) {
      res.push(nodeList.item(i));
    }
    return res;
  }
  var app_xml_id = alt_inst_update.appXmlID;
  var parent = $(this.sectionview_score).find('[xml\\:id='
  + this.ALTs[app_xml_id].parentID +']')[0];
  if ( typeof parent === 'undefined') {
    return;
  }
  var children = parent.childNodes;

  var replaceWith = alt_inst_update.replaceWith;
  var nodes2insert = [];
  var this_rich_score = this.rich_score;
  if (replaceWith) {
    var i;
    for ( i = 0; i < replaceWith.length; ++i) {
      var replaceWith_item = replaceWith[i];
      var replaceWith_xmlID = replaceWith_item.xmlID;
      var var_inst_elem = $(this_rich_score).find(replaceWith_item.tagname
      + '[xml\\:id="' + replaceWith_xmlID +'"]')[0];
      nodes2insert = extendWithNodeList(nodes2insert, var_inst_elem.childNodes);
    };
  }
  console.log(nodes2insert)

  var match_pseudo_attrValues = function(data1, data2) {
    data1 = data1.replace("'", '"');
    data2 = data2.replace("'", '"');
    return data1 === data2;
  }
  var inside_inst = false;
  var found = false;
  var insert_before_this = null;
  $(children).each(function() {
    var child = this;
    if (child.nodeType === 7) {
      if (child.nodeName === 'MEI2VF' && match_pseudo_attrValues(child.nodeValue, 'rdgStart="' + app_xml_id + '"')) {
        inside_inst = true;
        found = true;
      } else if (child.nodeName === 'MEI2VF' && match_pseudo_attrValues(child.nodeValue, 'rdgEnd="' + app_xml_id + '"')) {
        inside_inst = false;
        insert_before_this = child;
      }
    } else if (inside_inst) {
      parent.removeChild(child);
    }
  });

  if (!found)
    throw "processing instruction not found";
  if (inside_inst)
    throw "Unmatched <?MEI2VF rdgStart?>";

  var insert_method;
  if (insert_before_this) {
    insert_method = function(elem) {
      parent.insertBefore(elem, insert_before_this)
    };
  } else {
    insert_method = function(elem) {
      parent.appendChild(elem)
    };
  }

  $.each(nodes2insert, function() {
    insert_method(this.cloneNode(true));
  });

  this.sectionplane[app_xml_id] = alt_inst_update.replaceWith;

  return this.sectionview_score;
}
/**
 * @method getSectionViewSlice
 * Get a slice of the sectionview_score.
 *
 * @param params
 *            {Obejct} contains the parameters for slicing. For more info see at
 *            documentation of MeiLib.SliceMEI
 * @return an XML DOM object containing the slice of the plain MEI
 */
MeiLib.MeiDoc.prototype.getSectionViewSlice = function(params) {
  return MeiLib.SliceMEI(this.sectionview_score, params);
}
/**
 * @method getRichSlice
 * Get a slice of the whole rich MEI document.
 *
 * @param params
 *            {Obejct} contains the parameters for slicing. For more info see at
 *            documentation of MeiLib.SliceMEI
 * @return a MeiDoc object
 */
MeiLib.MeiDoc.prototype.getRichSlice = function(params) {
  var slice = new MeiLib.MeiDoc();
  slice.xmlDoc = this.xmlDoc;
  slice.rich_head = this.rich_head.cloneNode(true);
  slice.rich_music = this.rich_music.cloneNode(true);
  slice.rich_score = MeiLib.SliceMEI(this.rich_score, params);
  slice.sourceList = this.sourceList;
  slice.editorList = this.editorList;
  slice.ALTs = this.ALTs;
  slice.altgroups = this.altgroups;
  return slice;
}
;/*
* MEItoVexFlow
*
* Author: Richard Lewis Contributors: Zoltan Komives, Raffaele Viglianti
*
* See README for details of this library
*
* Copyright © 2012, 2013 Richard Lewis, Raffaele Viglianti, Zoltan Komives,
* University of Maryland
*
* Licensed under the Apache License, Version 2.0 (the "License"); you may not
* use this file except in compliance with the License. You may obtain a copy of
* the License at
*
* http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
* WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
* License for the specific language governing permissions and limitations under
* the License.
*/

var MEI2VF = ( function(m2v, MeiLib, VF, $, undefined) {

    /**
     * Converts an MEI XML document / document fragment to VexFlow objects and
     * optionally renders it using Raphael or HTML5 Canvas.
     *
     * Usage:
     *
     * - Either pass a config object to the constructor function or (if no config
     * object has been passed) call {@link #initConfig} after construction.
     * - Call {@link #process} to process an MEI XML document
     * - Call {@link #draw} to draw the processed VexFlow objects to a canvas
     *
     * @class MEI2VF.Converter
     *
     * @constructor
     * @param {Object} [config]
     * @chainable
     * @return {MEI2VF.Converter} this
     */
    m2v.Converter = function(config) {
      if (config)
        this.initConfig(config);
      return this;
    };

    m2v.Converter.prototype = {

      BOTTOM : VF.Annotation.VerticalJustify.BOTTOM,

      defaults : {
        /**
         * @cfg {Number} page_width The width of the page
         */
        page_width : 800,
        /**
         * @cfg {Number} page_margin_top The top page margin
         */
        page_margin_top : 60,
        /**
         * @cfg {Number} page_margin_left The left page margin
         */
        page_margin_left : 20,
        /**
         * @cfg {Number} page_margin_right The right page margin
         */
        page_margin_right : 20,
        /**
         * @cfg {Number} systemSpacing The spacing between two staff
         * systems
         */
        systemSpacing : 90,
        /**
         * @cfg {Number} staveSpacing The default spacing between two staffs
         * within a system; overridden by the spacing attribute of a staffDef
         * element in the MEI code
         */
        staveSpacing : 60,
        /**
         * @cfg {Boolean} autoStaveConnectorLine Specifies if a stave connector
         * line is drawn on the left of systems by default; if set to true, the
         * auto line will not appear when staffDef/@symbol="none" is set for the
         * outermost staffDef element
         */
        autoStaveConnectorLine : true,
        /**
         * @cfg {"full"/"abbr"/null} labelMode Specifies the way voice labels are
         * added
         * to staves. Values:
         *
         * - 'full': renders full labels in the first system, abbreviated labels
         * in all following systems
         * - 'abbr': only render abbreviated labels
         * - null or undefined: renders no labels
         */
        labelMode : null, // 'full',
        /**
         * @cfg {Number} maxHyphenDistance The maximum distance (in pixels)
         * between two hyphens in the lyrics lines
         */
        maxHyphenDistance : 75,
        /**
         * @cfg {Object} lyricsFont The font used for rendering lyrics (and
         * hyphens)
         * @cfg {String} lyricsFont.family the font family
         * @cfg {Number} lyricsFont.size the font size
         *
         * NB the weight properties can be used to specify style, weight
         * or both (space separated); some of the objects are passed directly
         * to vexFlow (which requires the name 'weight'), so the name is
         * 'weight'
         */
        lyricsFont : {
          family : 'Times',
          size : 13,
          spacing: 1.3,
        },
        /**
         * @cfg {Object} annotFont the font used for annotations and directions
         * (for example, 'pizz.')
         * @cfg {String} annotFont.family the font family
         * @cfg {Number} annotFont.size the font size
         */
        annotFont : {
          family : 'Times',
          size : 15,
        },
        /**
         * @cfg {Object} exprFont the font used for expression marks (for example,
         * 'staccato')
         * @cfg {String} exprFont.family the font family
         * @cfg {Number} exprFont.size the font size
         * @cfg {String} exprFont.weight the font weight
         */
        exprFont : {
          family : 'Times',
          size : 15,
          weight : 'italic',
        },
        /**
         * @cfg {Object} dynamFont the font used for dynamics
         * @cfg {String} dynamFont.family the font family
         * @cfg {Number} dynamFont.size the font size
         * @cfg {String} dynamFont.weight the font weight
         */
        dynamFont : {
          family : 'Times',
          size : 18,
          weight : 'bold italic',
        },
        /**
         * @cfg {Object} tempoFont The tempo font
         * @cfg {String} tempoFont.family the font family
         * @cfg {Number} tempoFont.size the font size
         * @cfg {String} tempoFont.weight the font weight
         */
        tempoFont : {
          family : "Times",
          size : 17,
          weight : "bold",
        },
        /**
         * @cfg {Object} staff The staff config object passed to each
         * Vex.Flow.Staff
         */
        staff : {
          vertical_bar_width : 20, // 10 // Width around vertical bar end-marker
          top_text_position : 1.5, // 1 // in staff lines
          bottom_text_position : 7.5
        }
      },

      /**
       * initializes the Converter
       * @method initConfig
       * @param {Object} config A config object (optional)
       * @chainable
       * @return {MEI2VF.Converter} this
       */
      initConfig : function(config) {
        var me = this;
        me.cfg = $.extend(true, {}, me.defaults, config);
        /**
         * an instance of MEI2VF.SystemInfo dealing with the system and staff
         * info derived from the MEI data
         * @property {MEI2VF.SystemInfo} systemInfo
         */
        me.systemInfo = new m2v.SystemInfo();

        /**
         * The print space coordinates calculated from the page config.
         * @property {Object} printSpace
         * @property {Number} printSpace.top
         * @property {Number} printSpace.left
         * @property {Number} printSpace.right
         * @property {Number} printSpace.width
         */
        me.printSpace = {
          // substract four line distances (40px) from page_margin_top in order
          // to compensate VexFlow's default top spacing / allow specifying
          // absolute values
          top : me.cfg.page_margin_top - 40,
          left : me.cfg.page_margin_left,
          right : me.cfg.page_width - me.cfg.page_margin_right,
          width : Math.floor(me.cfg.page_width - me.cfg.page_margin_right - me.cfg.page_margin_left) - 1
        };
        return me;

      },

      /**
       * Resets all data. Called by {@link #process}.
       * @method reset
       * @chainable
       * @return {MEI2VF.Converter} this
       */
      reset : function() {
        var me = this;
        me.systemInfo.init(me.cfg, me.printSpace);
        /**
         * @property {MEI2VF.EventLink[][]} unresolvedTStamp2
         */
        me.unresolvedTStamp2 = [];
        /**
         * Contains all {@link MEI2VF.System} objects
         * @property {MEI2VF.System[]} systems
         */
        me.systems = [];
        /**
         * Contains all Vex.Flow.Stave objects. Addressing scheme:
         * [measure_n][staff_n]
         * @property {Vex.Flow.Stave[][]} allVexMeasureStaffs
         */
        me.allVexMeasureStaffs = [];
        /**
         * Contains all Vex.Flow.Beam objects. Data is just pushed in
         * and later processed as a whole, so the array index is
         * irrelevant.
         * @property {Vex.Flow.Beam[]} allBeams
         */
        me.allBeams = [];
        /**
         * Contains all Vex.Flow.Tuplet objects. Data is just pushed in
         * and later processed as a whole, so the array index is
         * irrelevant.
         * @property {Vex.Flow.Tuplet[]} allTuplets
         */
        me.allTuplets = [];
        /**
         * an instance of MEI2VF.Dynamics dealing with and storing all dynamics
         * found in the MEI document
         * @property {MEI2VF.Dynamics} dynamics
         */
        me.dynamics = new m2v.Dynamics(me.systemInfo, me.cfg.dynamFont);
        /**
         * an instance of MEI2VF.Directives dealing with and storing all
         * directives found in the MEI document
         * @property {MEI2VF.Directives} directives
         */
        me.directives = new m2v.Directives(me.systemInfo, me.cfg.annotFont);
        /**
         * an instance of MEI2VF.Fermatas dealing with and storing all
         * fermata elements found in the MEI document (fermata attributes are
         * attached directly to the containing note-like object)
         * @property {MEI2VF.Fermatas} fermatas
         */
        me.fermatas = new m2v.Fermatas(me.systemInfo);

        /**
         * an instance of MEI2VF.Ties dealing with and storing all ties found in
         * the MEI document
         * @property {MEI2VF.Ties} ties
         */
        me.ties = new m2v.Ties(me.systemInfo, me.unresolvedTStamp2);
        /**
         * an instance of MEI2VF.Ties dealing with and storing all slurs found in
         * the MEI document
         * @property {MEI2VF.Ties} slurs
         */
        me.slurs = new m2v.Ties(me.systemInfo, me.unresolvedTStamp2);
        /**
         * an instance of MEI2VF.Hairpins dealing with and storing all hairpins
         * found in the MEI document
         * @property {MEI2VF.Hairpins} hairpins
         */
        me.hairpins = new m2v.Hairpins(me.systemInfo, me.unresolvedTStamp2);
        /**
         * an instance of MEI2VF.Hyphenation dealing with and storing all lyrics
         * hyphens found in the MEI document
         * @property {MEI2VF.Hyphenation} hyphenation
         */
        me.hyphenation = new m2v.Hyphenation(me.cfg.lyricsFont, me.printSpace.right, me.cfg.maxHyphenDistance);
        me.verses = new m2v.Verses(me.cfg.lyricsFont, me.printSpace.right, me.cfg.maxHyphenDistance);
        /**
         * contains all note-like objects in the current MEI document, accessible
         * by their xml:id
         * @property {Object} notes_by_id
         * @property {XMLElement} notes_by_id.meiNote the XML Element of the note
         * @property {Vex.Flow.StaveNote} notes_by_id.vexNote the VexFlow note
         * object
         */
        me.notes_by_id = {};
        /**
         * the number of the current system
         * @property {Number} currentSystem_n
         */
        me.currentSystem_n = 0;
        /**
         * indicates if a system break is currently to be processed
         * @property {Boolean} pendingSystemBreak
         */
        me.pendingSystemBreak = false;
        /**
         * indicates if a system break is currently to be processed
         * @property {Boolean} pendingSectionBreak
         */
        me.pendingSectionBreak = true;
        /**
         * Contains information about the volta type of the current staff. Properties:
         *
         * -  `start` {String} indicates the number to render to the volta. When
         * falsy, it is assumed that the volta does not start in the current
         * measure
         * -  `end` {Boolean} indicates if there is a volta end in the current
         * measure
         *
         * If null, no volta is rendered
         * @property {Object} currentVoltaType
         */
        me.currentVoltaType = null;
        return me;
      },

      /**
       * Calls {@link #reset} and then processes the specified MEI document or
       * document fragment. The generated objects can
       * be processed further or drawn immediately to a canvas via {@link #draw}.
       * @method process
       * @chainable
       * @param {XMLDocument} xmlDoc the XML document
       * @return {MEI2VF.Converter} this
       */
      process : function(xmlDoc) {
        var me = this;
        me.reset();
        me.systemInfo.processScoreDef($(xmlDoc).find('scoreDef')[0]);
        me.processSections(xmlDoc);
        me.directives.createVexFromInfos(me.notes_by_id);
        me.dynamics.createVexFromInfos(me.notes_by_id);
        me.fermatas.createVexFromInfos(me.notes_by_id);
        me.ties.createVexFromInfos(me.notes_by_id);
        me.slurs.createVexFromInfos(me.notes_by_id);
        me.hairpins.createVexFromInfos(me.notes_by_id);
        return me;
      },

      /**
       * Draws the internal data objects to a canvas
       * @method draw
       * @chainable
       * @param ctx The canvas context
       * @return {MEI2VF.Converter} this
       */
      draw : function(ctx) {
        var me = this;
        me.drawSystems(ctx);
        me.drawVexBeams(me.allBeams, ctx);
        me.drawVexTuplets(me.allTuplets, ctx);
        me.ties.setContext(ctx).draw();
        me.slurs.setContext(ctx).draw();
        me.hairpins.setContext(ctx).draw();
        me.verses.drawHyphens(ctx);
        return me;
      },

      /**
       * Returns the width and the height of the area that contains all drawn
       * staves as per the last processing.
       *
       * @method getStaffArea
       * @return {Object} the width and height of the area that contains all
       * staves.
       * Properties: width, height
       */
      getStaffArea : function() {
        var height, i;
        height = this.systemInfo.getCurrentLowestY();
        var allVexMeasureStaffs = this.getAllVexMeasureStaffs();
        var i, k, max_start_x, area_width, staff;
        i = allVexMeasureStaffs.length;
        area_width = 0;
        while (i--) {
          if (allVexMeasureStaffs[i]) {
            max_start_x = 0;
            // get maximum start_x of all staffs in measure
            k = allVexMeasureStaffs[i].length;
            while (k--) {
              staff = allVexMeasureStaffs[i][k];
              if (staff)
                max_start_x = Math.max(max_start_x, staff.getNoteStartX());
            }
            k = allVexMeasureStaffs[i].length;
            while (k--) {
              // get maximum width of all staffs in measure
              staff = allVexMeasureStaffs[i][k];
              if (staff) {
                area_width = Math.max(area_width, max_start_x + staff.getWidth());
              }
            }
          }
        }
        return {
          width : area_width,
          height : height
        };
      },

      /**
       * returns a 2d array of all Vex.Flow.Stave objects, arranged by
       * [measure_n][staff_n]
       * @method getAllVexMeasureStaffs
       * @return {Vex.Flow.Stave[][]} see {@link #allVexMeasureStaffs}
       */
      getAllVexMeasureStaffs : function() {
        return this.allVexMeasureStaffs;
      },

      /**
       * returns all systems created when processing the MEI document
       * @method getSystems
       * @return {MEI2VF.System[]}
       */
      getSystems : function() {
        return this.systems;
      },

      /**
       * returns all note-like objects created when processing the MEI document
       * @method getNotes
       * @return {Object} for the object properties, see {@link #notes_by_id}
       */
      getNotes : function() {
        return this.notes_by_id;
      },

      /**
       * creates in initializes a new {@link MEI2VF.System} and updates the staff
       * modifier infos
       * @method createNewSystem
       */
      createNewSystem : function() {
        var me = this, system, coords;

        m2v.L('Converter.createNewSystem()', '{enter}');

        me.pendingSystemBreak = false;
        me.currentSystem_n += 1;

        coords = {
          x : me.printSpace.left,
          y : (me.currentSystem_n === 1) ? me.printSpace.top : me.systemInfo.getCurrentLowestY() + me.cfg.systemSpacing,
          w : me.printSpace.width
        };

        system = new m2v.System({
          leftMar : me.systemInfo.getLeftMar(),
          coords : coords,
          staffYs : me.systemInfo.getYs(coords.y),
          labels : me.getStaffLabels()
        });

        if (me.pendingSectionBreak) {
          me.pendingSectionBreak = false;
          me.systemInfo.forceSectionStartInfos();
        } else {
          me.systemInfo.forceStaveStartInfos();
        }

        me.hyphenation.addLineBreaks(me.systemInfo.getAllStaffInfos(), {
          system : system
        });

        me.verses.addLineBreaks(me.systemInfo.getAllStaffInfos(), {
          system : system
        });

        me.systems[me.currentSystem_n] = system;
        return system;
      },

      /**
       * @method processSections
       */
      processSections : function(xmlDoc) {
        var me = this;
        $(xmlDoc).find('section').each(function() {
            me.processSection(this);
        });
      },

      /**
       *@method processSection
       */
      processSection : function(element) {
        var me = this, i, j, sectionChildren = $(element).children();
        me.verses.initHyphenations( $(element).find('syl') );
        for ( i = 0, j = sectionChildren.length; i < j; i += 1) {
          me.processSectionChild(sectionChildren[i]);
        }
      },

      /**
       * @method processEnding
       */
      processEnding : function(element) {
        var me = this, i, j, sectionChildren = $(element).children();
        for ( i = 0, j = sectionChildren.length; i < j; i += 1) {
          me.currentVoltaType = {};
          if (i === 0)
            me.currentVoltaType.start = $(element).attr('n');
          if (i === j - 1)
            me.currentVoltaType.end = true;
          me.processSectionChild(sectionChildren[i]);
        }
        me.currentVoltaType = null;
      },

      /**
       * MEI element <b>section</b> may contain (MEI v2.1.0): MEI.cmn: measure
       * MEI.critapp: app MEI.edittrans: add choice corr damage del gap
       * handShift orig reg restore sic subst supplied unclear MEI.shared:
       * annot ending expansion pb sb scoreDef section staff staffDef
       * MEI.text: div MEI.usersymbols: anchoredText curve line symbol
       *
       * Supported elements: <b>measure</b> <b>scoreDef</b> <b>staffDef</b>
       * <b>sb</b>
       * @method processSectionChild
       */
      processSectionChild : function(element) {
        var me = this;
        switch (element.localName) {
          case 'measure' :
            me.processMeasure(element);
            break;
          case 'scoreDef' :
            me.systemInfo.processScoreDef(element);
            break;
          case 'staffDef' :
            me.systemInfo.processStaffDef(element);
            break;
          case 'sb' :
            me.setPendingSystemBreak(element);
            break;
          case 'ending' :
            me.processEnding(element);
            break;
          default :
            throw new m2v.RUNTIME_ERROR('MEI2VF.RERR.NotSupported', 'Element <' + element.localName + '> is not supported in <section>');
        }
      },

      /**
       * sets the property {@link #pendingSystemBreak} to `true`. When true, a
       * new system will be initialized when {@link #processMeasure} is called
       * the next time.
       * @method setPendingSystemBreak
       */
      setPendingSystemBreak : function() {
        this.pendingSystemBreak = true;
      },

      /**
       * Processes a MEI measure element and calls functions to process a
       * selection of ancestors: .//staff, ./slur, ./tie, ./hairpin, .//tempo
       * @method processMeasure
       * @param {XMLElement} element the MEI measure element
       */
      processMeasure : function(element) {
        var me = this, measure_n, atSystemStart, left_barline, right_barline, system, system_n;

        if (me.pendingSectionBreak || me.pendingSystemBreak) {
          system_n = me.systems.length;
          system = me.createNewSystem();
          atSystemStart = true;
        } else {
          system_n = me.systems.length - 1;
          system = me.systems[system_n];
          atSystemStart = false;
        }

        m2v.L('Converter.processMeasure()', '{enter}');

        measure_n = +element.getAttribute('n');
        left_barline = element.getAttribute('left');
        right_barline = element.getAttribute('right');

        var staffElements = [], dirElements = [], slurElements = [], tieElements = [], hairpinElements = [], tempoElements = [], dynamElements = [], fermataElements = [];

        $(element).find('*').each(function() {
          switch (this.localName) {
            case 'staff':
              staffElements.push(this);
              break;
            case 'dir':
              dirElements.push(this);
              break;
            case 'tie':
              tieElements.push(this);
              break;
            case 'slur':
              slurElements.push(this);
              break;
            case 'hairpin':
              hairpinElements.push(this);
              break;
            case 'tempo':
              tempoElements.push(this);
              break;
            case 'dynam':
              dynamElements.push(this);
              break;
            case 'fermata':
              fermataElements.push(this);
              break;
            default:
              break;
          }
        });

        // the staff objects will be stored in two places:
        // 1) in each MEI2VF.Measure
        // 2) in MEI2VF.Converter.allVexMeasureStaffs
        var staffs = me.initializeMeasureStaffs(system, staffElements, left_barline, right_barline);
        me.allVexMeasureStaffs[measure_n] = staffs;

        var currentStaveVoices = new m2v.StaveVoices();

        $.each(staffElements, function() {
          me.processStaffEvents(staffs, this, measure_n, currentStaveVoices);
        });

        me.directives.createInfos(dirElements, element);
        me.dynamics.createInfos(dynamElements, element);
        me.fermatas.createInfos(fermataElements, element);
        me.ties.createInfos(tieElements, element, me.systemInfo);
        me.slurs.createInfos(slurElements, element, me.systemInfo);
        me.hairpins.createInfos(hairpinElements, element, me.systemInfo);

        system.addMeasure(new m2v.Measure({
          element : element,
          n : measure_n,
          staffs : staffs,
          voices : currentStaveVoices,
          verses : me.verses,
          startConnectorCfg : (atSystemStart) ? {
            labelMode : me.cfg.labelMode,
            models : me.systemInfo.startConnectorInfos,
            staffs : staffs,
            system_n : me.currentSystem_n
          } : null,
          inlineConnectorCfg : {
            models : me.systemInfo.inlineConnectorInfos,
            staffs : staffs,
            barline_l : left_barline,
            barline_r : right_barline
          },
          tempoElements : tempoElements,
          tempoFont : me.cfg.tempoFont
        }));
      },

      /**
       * @method initializeMeasureStaffs
       * @param {MEI2VF.System} system the current system
       * @param {XMLElement[]} staffElements all staff elements in the current
       * measure
       * @param {String} left_barline the left barline
       * @param {String} right_barline the right barline
       */
      initializeMeasureStaffs : function(system, staffElements, left_barline, right_barline) {
        var me = this, staff, staff_n, staffs, isFirst = true, clefOffsets = {}, maxClefOffset = 0, keySigOffsets = {}, maxKeySigOffset = 0;

        staffs = [];

        // first run: create Vex.Flow.Staff objects, store them in the staffs
        // array. Set staff barlines and staff volta. Add clef. Get each staff's
        // clefOffset and calculate the maxClefOffset.
        $.each(staffElements, function() {
          staff_n = +$(this).attr('n');
          if (!staff_n) {
            throw new m2v.RUNTIME_ERROR('MEI2VF.RERR.BadArgument', 'Cannot render staff without attribute "n".');
          }
          staff = me.createVexStaff(system.getStaffYs()[staff_n]);
          staffs[staff_n] = staff;

          staff.setBegBarType( left_barline ? m2v.tables.barlines[left_barline] : VF.Barline.type.NONE);
          if (right_barline) {
            staff.setEndBarType(m2v.tables.barlines[right_barline]);
          }
          if (isFirst && me.currentVoltaType) {
            me.addStaffVolta(staff);
          }
          me.addStaffClef(staff, staff_n);
          clefOffsets[staff_n] = staff.getModifierXShift();
          maxClefOffset = Math.max(maxClefOffset, clefOffsets[staff_n]);
          isFirst = false;
        });

        // second run: add key signatures; if the clefOffset of a staff is lesser
        // maxClefOffset, add padding to the left of the key signature. Get each
        // staff's keySigOffset and calculate the maxKeySigOffset.
        $.each(staffs, function(i, staff) {
          if (staff) {
            if (clefOffsets[i] !== maxClefOffset) {
              me.addStaffKeySig(staff, i, maxClefOffset - clefOffsets[i] + 10);
            } else {
              me.addStaffKeySig(staff, i);
            }
            keySigOffsets[i] = staff.getModifierXShift();
            maxKeySigOffset = Math.max(maxKeySigOffset, keySigOffsets[i]);
          }
        });

        // third run: add time signatures; if the keySigOffset of a staff is
        // lesser maxKeySigOffset, add padding to the left of the time signature.
        $.each(staffs, function(i, staff) {
          if (staff) {
            if (keySigOffsets[i] !== maxKeySigOffset) {
              me.addStaffTimeSig(staff, i, maxKeySigOffset - keySigOffsets[i] + 15);
            } else {
              me.addStaffTimeSig(staff, i);
            }
          }
        });

        return staffs;
      },

      /**
       * Creates a new Vex.Flow.Stave object at the specified y coordinate. This
       * method sets fixed x coordinates, which will later be substituted in
       * {@link MEI2VF.System#format} - the Vex.Flow.Stave
       * objects must be initialized with some x measurements, but the real
       * values depend on values only available after modifiers, voices etc
       * have been added.
       *
       * @method createVexStaff
       * @param {Number} y the y coordinate of the staff
       * @return {Vex.Flow.Stave} The initialized stave object
       */
      createVexStaff : function(y) {
        var me = this, staff;
        staff = new VF.Stave();
        staff.init(0, y, 1000, me.cfg.staff);
        // temporary; (due to a bug?) in VexFlow, bottom_text_position does
        // not work when it's passed in the config object
        staff.options.bottom_text_position = me.cfg.staff.bottom_text_position;
        return staff;
      },

      /**
       * Adds clef to a Vex.Flow.Staff.
       *
       * @method addStaffClef
       * @param {Vex.Flow.Stave} staff The stave object
       * @param {Number} staff_n the staff number
       */
      addStaffClef : function(staff, staff_n) {
        var me = this, currentStaffInfo;
        currentStaffInfo = me.systemInfo.getStaffInfo(staff_n);
        if (currentStaffInfo.showClefCheck()) {
          staff.addClef(currentStaffInfo.getClef());
        }
      },

      /**
       * Adds a key signature to a Vex.Flow.Staff.
       *
       * @method addStaffKeySig
       * @param {Vex.Flow.Stave} staff The stave object
       * @param {Number} staff_n the staff number
       * @param {Number} padding the additional padding to the left of the
       * modifier
       */
      addStaffKeySig : function(staff, staff_n, padding) {
        var me = this, currentStaffInfo;
        currentStaffInfo = me.systemInfo.getStaffInfo(staff_n);
        if (currentStaffInfo.showKeysigCheck()) {
          // console.log('keysg pd:'+padding);
          staff.addModifier(new Vex.Flow.KeySignature(currentStaffInfo.getKeySpec(), padding));
        }
      },

      /**
       * Adds a time signature to a Vex.Flow.Staff.
       *
       * @method addStaffTimeSig
       * @param {Vex.Flow.Stave} staff The stave object
       * @param {Number} staff_n the staff number
       * @param {Number} padding the additional padding to the left of the
       * modifier
       */
      addStaffTimeSig : function(staff, staff_n, padding) {
        var me = this, currentStaffInfo;
        currentStaffInfo = me.systemInfo.getStaffInfo(staff_n);
        if (currentStaffInfo.showTimesigCheck()) {
          staff.hasTimeSig = true;
          staff.addTimeSignature(currentStaffInfo.getTimeSig(), padding);
        }
      },

      /**
       * Adds a volta to a staff. Currently not working due to the reworking of
       * the measure width calulation (27/4/2014)
       * @method addStaffVolta
       * @experimental
       */
      addStaffVolta : function(staff) {
        var volta = this.currentVoltaType;
        if (volta.start) {
          staff.setVoltaType(Vex.Flow.Volta.type.BEGIN, volta.start + '.', 30);
        } else if (volta.end) {
          //TODO: fix type.BEGIN and type.END interference in vexflow, then remove else!
          //[think through in which cases we actually need type.END]
          staff.setVoltaType(Vex.Flow.Volta.type.END, "", 30);
        } else if (!volta.start && !volta.end) {
          staff.setVoltaType(Vex.Flow.Volta.type.MID, "", 30);
        }
      },

      /**
       * @method getStaffLabels
       */
      getStaffLabels : function() {
        var me = this, labels, i, infos, labelType;
        labels = {};
        if (!me.cfg.labelMode) {
          return labels;
        }
        labelType = (me.cfg.labelMode === 'full' && me.currentSystem_n === 1) ? 'label' : 'labelAbbr';
        infos = me.systemInfo.getAllStaffInfos();
        i = infos.length;
        while (i--) {
          if (infos[i]) {
            labels[i] = infos[i][labelType];
          }
        }
        return labels;
      },

      /**
       * Processes a single stave in a measure
       *
       * @method processStaffEvents
       * @param {Vex.Flow.Stave[]} staffs the staff objects in the current
       * measure
       * @param {XMLElement} staff_element the MEI staff element
       * @param {Number} measure_n the measure number
       * @param {MEI2VF.StaveVoices} currentStaveVoices The current StaveVoices
       * object
       */
      processStaffEvents : function(staffs, staff_element, measure_n, currentStaveVoices) {
        var me = this, staff, staff_n, readEvents, layer_events;

        staff_n = +$(staff_element).attr('n');
        staff = staffs[staff_n];

        readEvents = function() {
          var event = me.processNoteLikeElement(this, staff, staff_n);
          // return event.vexNote;
          return event.vexNote || event;
        };

        $(staff_element).find('layer').each(function() {
          me.resolveUnresolvedTimestamps(this, staff_n, measure_n);
          layer_events = $(this).children().map(readEvents).get();
          currentStaveVoices.addVoice(me.createVexVoice(layer_events, staff_n), staff_n);
        });

      },

      /**
       * Creates a new Vex.Flow.Voice
       * @method createVexVoice
       * @param {Array} voice_contents The contents of the voice, an array of
       * tickables
       * @param {Number} staff_n The number of the enclosing staff element
       * return {Vex.Flow.Voice}
       */
      createVexVoice : function(voice_contents, staff_n) {
        var me = this, voice, meter;
        if (!$.isArray(voice_contents)) {
          throw new m2v.RUNTIME_ERROR('BadArguments', 'me.createVexVoice() voice_contents argument must be an array.');
        }
        meter = me.systemInfo.getStaffInfo(staff_n).meter;
        voice = new VF.Voice({
          num_beats : meter.count,
          beat_value : meter.unit,
          resolution : VF.RESOLUTION
        });
        voice.setStrict(false);
        voice.addTickables(voice_contents);
        return voice;
      },

      /**
       * @method resolveUnresolvedTimestamps
       */
      resolveUnresolvedTimestamps : function(layer, staff_n, measure_n) {
        var me = this, refLocationIndex;
        // check if there's an unresolved TStamp2 reference to this location
        // (measure, staff, layer):
        if (isNaN(measure_n))
          throw new m2v.RUNTIME_ERROR('MEI2VF.RERR.extract_events', '<measure> must have @n specified');
        staff_n = staff_n || 1;
        refLocationIndex = measure_n + ':' + staff_n + ':' + ($(layer).attr('n') || '1');
        if (me.unresolvedTStamp2[refLocationIndex]) {
          $(me.unresolvedTStamp2[refLocationIndex]).each(function(i) {
            this.setContext({
              layer : layer,
              meter : me.systemInfo.getStaffInfo(staff_n).meter
            });
            // TODO: remove eventLink from the list
            me.unresolvedTStamp2[refLocationIndex][i] = null;
          });
          // at this point all references should be supplied with context.
          me.unresolvedTStamp2[refLocationIndex] = null;
        }
      },

      /**
       * processes a note-like element by calling the adequate processing
       * function
       *
       * @method processNoteLikeElement
       * @param {XMLElement} element the element to process
       * @param {Vex.Flow.Stave} staff the VexFlow staff object
       * @param {Number} staff_n the number of the staff as given in the MEI
       * document
       */
      processNoteLikeElement : function(element, staff, staff_n) {
        var me = this;
        switch (element.localName) {
          case 'rest' :
            return me.processRest(element, staff);
          case 'mRest' :
            return me.processmRest(element, staff, staff_n);
          case 'space' :
            return me.processSpace(element, staff);
          case 'note' :
            return me.processNote(element, staff, staff_n);
          case 'beam' :
            return me.processBeam(element, staff, staff_n);
          case 'tuplet' :
            return me.processTuplet(element, staff, staff_n);
          case 'chord' :
            return me.processChord(element, staff, staff_n);
          case 'anchoredText' :
            return;
          default :
            throw new m2v.RUNTIME_ERROR('BadArguments', 'Rendering of element "' + element.localName + '" is not supported.');
        }
      },

      /**
       * @method processNote
       */
      processNote : function(element, staff, staff_n) {
        var me = this, dots, mei_accid, mei_ho, pname, oct, xml_id, mei_tie, mei_slur, mei_staff_n, i, atts, note_opts, note;

        atts = m2v.Util.attsToObj(element);

        dots = +atts.dots;
        mei_accid = atts.accid;
        mei_ho = atts.ho;
        pname = atts.pname;
        oct = atts.oct;
        mei_tie = atts.tie;
        mei_slur = atts.slur;
        mei_staff_n = +atts.staff || staff_n;

        xml_id = MeiLib.XMLID(element);

        try {

          note_opts = {
            keys : [me.processAttsPitch(element)],
            clef : me.systemInfo.getClef(staff_n),
            duration : me.processAttsDuration(element)
          };

          me.setStemDir(element, note_opts);
          note = new VF.StaveNote(note_opts);

          if (mei_staff_n === staff_n) {
            note.setStave(staff);
          } else {
            var otherStaff = me.allVexMeasureStaffs[me.allVexMeasureStaffs.length - 1][mei_staff_n];
            if (otherStaff) {
              note.setStave(otherStaff);
            } else {
              throw new m2v.RUNTIME_ERROR('Error', 'Note has staff attribute "' + mei_staff_n + '", but the staff does not exist.');
            }
          }

          me.processSyllables(note, element, staff_n);

          try {
            for ( i = 0; i < dots; i += 1) {
              note.addDotToAll();
            }
          } catch (e) {
            throw new m2v.RUNTIME_ERROR('BadArguments', 'A problem occurred processing the dots of <note>: ' + m2v.Util.attsToString(element));
          }

          if (mei_accid)
            me.processAttrAccid(mei_accid, note, 0);
          if (mei_ho)
            me.processAttrHo(mei_ho, note, staff);

          $.each($(element).find('artic'), function() {
            me.addArticulation(note, this);
          });
          if (atts.fermata) {
            me.fermatas.addFermataToNote(note, atts.fermata);
          }

          // FIXME For now, we'll remove any child nodes of <note>
          $.each($(element).children(), function() {
            $(this).remove();
          });

          // Build a note object that keeps the xml:id

          if (!pname)
            throw new m2v.RUNTIME_ERROR('MEI2VF.RERR.BadArguments', 'mei:note must have pname attribute');
          if (!oct)
            throw new m2v.RUNTIME_ERROR('MEI2VF.RERR.BadArguments', 'mei:note must have oct attribute');

          if (mei_tie)
            me.processAttrTie(mei_tie, xml_id, pname, oct, staff_n);
          if (mei_slur)
            me.processAttrSlur(mei_slur, xml_id);

          me.notes_by_id[xml_id] = {
            meiNote : element,
            vexNote : note,
            system : me.currentSystem_n
          };

          // return note object
          return {
            vexNote : note,
            id : xml_id
          };

        } catch (e1) {
          throw new m2v.RUNTIME_ERROR('BadArguments', 'A problem occurred processing the <note>: ' + m2v.Util.attsToString(element) + '\nORIGINAL ERROR MESSAGE: ' + e1.toString());
        }
      },

      /**
       * @method processChord
       */
      processChord : function(element, staff, staff_n) {
        var me = this, i, j, hasDots, children, keys = [], duration, durations = [], durAtt, xml_id, chord, chord_opts, atts;

        children = $(element).children();

        atts = m2v.Util.attsToObj(element);
        durAtt = atts.dur;

        xml_id = MeiLib.XMLID(element);

        hasDots = !!$(element).attr('dots');

        try {
          if (durAtt) {
            duration = me.translateDuration(+durAtt);
          } else {
            for ( i = 0, j = children.length; i < j; i += 1) {
              durations.push(+children[i].getAttribute('dur'));
            }
            duration = me.translateDuration(Math.max.apply(Math, durations));
          }

          for ( i = 0, j = children.length; i < j; i += 1) {
            keys.push(me.processAttsPitch(children[i]));
            // dots.push(+children[i].getAttribute('dots'));
            if (children[i].getAttribute('dots') === '1')
              hasDots = true;
          }

          if (hasDots)
            duration += 'd';

          chord_opts = {
            keys : keys,
            clef : me.systemInfo.getClef(staff_n),
            duration : duration
          };

          me.setStemDir(element, chord_opts);
          chord = new VF.StaveNote(chord_opts);
          chord.setStave(staff);

          var allNoteIndices = [];

          children.each(function(i) {
            me.processNoteInChord(i, this, element, chord, staff_n);
            allNoteIndices.push(i);
          });

          if (hasDots) {
            chord.addDotToAll();
          }
          if (atts.ho) {
            me.processAttrHo(atts.ho, chord, staff);
          }
          if (atts.fermata) {
            me.fermatas.addFermataToNote(chord, atts.fermata);
          }

          me.notes_by_id[xml_id] = {
            meiNote : element,
            vexNote : chord,
            index : allNoteIndices,
            system : me.currentSystem_n
          };

          return {
            vexNote : chord,
            id : xml_id
          };
        } catch (e) {
          throw new m2v.RUNTIME_ERROR('BadArguments', 'A problem occurred processing the <chord>:' + e.toString());
          // 'A problem occurred processing the <chord>: ' +
          // JSON.stringify($.each($(element).children(), function(i,
          // element) {
          // element.attrs();
          // }).get()) + '. \"' + x.toString() + '"');
        }
      },

      /**
       * @method processNoteInChord
       */
      processNoteInChord : function(i, element, chordElement, chord, staff_n) {
        var me = this, atts, xml_id;

        atts = m2v.Util.attsToObj(element);

        xml_id = MeiLib.XMLID(element);

        if (atts.tie)
          me.processAttrTie(atts.tie, xml_id, atts.pname, atts.oct, staff_n);
        if (atts.slur)
          me.processAttrSlur(atts.slur, xml_id);

        me.notes_by_id[xml_id] = {
          meiNote : chordElement,
          vexNote : chord,
          index : [i],
          system : me.currentSystem_n
        };

        if (atts.accid) {
          me.processAttrAccid(atts.accid, chord, i);
        }
        if (atts.fermata) {
          me.fermatas.addFermataToNote(chord, atts.fermata, i);
        }
      },

      /**
       * @method processRest
       */
      processRest : function(element, staff) {
        var me = this, dur, rest, xml_id, atts;
        try {
          atts = m2v.Util.attsToObj(element);

          dur = me.processAttsDuration(element, true);
          // assign whole rests to the fourth line, all others to the
          // middle line:
          rest = new VF.StaveNote({
            keys : [(dur === 'w') ? 'd/5' : 'b/4'],
            duration : dur + 'r'
          });

          xml_id = MeiLib.XMLID(element);

          if (atts.ho) {
            me.processAttrHo(atts.ho, rest, staff);
          }
          rest.setStave(staff);
          if (atts.dots === '1') {
            rest.addDotToAll();
          }
          if (atts.fermata) {
            me.fermatas.addFermataToNote(rest, atts.fermata);
          }
          me.notes_by_id[xml_id] = {
            meiNote : element,
            vexNote : rest,
            system : me.currentSystem_n
          };
          return {
            vexNote : rest,
            id : xml_id
          };
        } catch (e) {
          throw new m2v.RUNTIME_ERROR('BadArguments', 'A problem occurred processing the <rest>: ' + m2v.Util.attsToString(element));
        }
      },

      /**
       * @method processmRest
       */
      processmRest : function(element, staff, staff_n) {
        var me = this, mRest, atts, xml_id, meter, duration;

        meter = me.systemInfo.getStaffInfo(staff_n).meter;
        duration = new Vex.Flow.Fraction(meter.count, meter.unit);
        var dur, keys;
        if (duration.value() == 2) {
          dur = m2v.tables.durations['breve'];
          keys = ['b/4'];
        } else if (duration.value() == 4) {
          dur = m2v.tables.durations['long'];
          keys = ['b/4']
        } else {
          dur = 'w';
          keys = ['d/5'];
        }
        try {
          atts = m2v.Util.attsToObj(element);
          mRest = new VF.StaveNote({
            keys : keys,
            duration : dur + 'r',
            duration_override : duration,
            align_center : true
          });

          xml_id = MeiLib.XMLID(element);

          if (atts.ho) {
            me.processAttrHo(atts.ho, mRest, staff);
          }
          if (atts.fermata) {
            me.fermatas.addFermataToNote(mRest, atts.fermata);
          }
          mRest.setStave(staff);
          me.notes_by_id[xml_id] = {
            meiNote : element,
            vexNote : mRest,
            system : me.currentSystem_n
          };
          return {
            vexNote : mRest,
            id : xml_id
          };
        } catch (x) {
          throw new m2v.RUNTIME_ERROR('BadArguments', 'A problem occurred processing the <mRest>: ' + m2v.Util.attsToString(element));
        }
      },

      /**
       * @method processSpace
       */
      processSpace : function(element, staff) {
        var me = this, space, xml_id;
        try {
          space = new VF.GhostNote({
            duration : me.processAttsDuration(element, true) + 'r'
          });
          space.setStave(staff);
          return {
            vexNote : space
          };
        } catch (e) {
          throw new m2v.RUNTIME_ERROR('BadArguments', 'A problem occurred processing the <space>: ' + m2v.Util.attsToString(element));
        }
      },

      /**
       * @method processBeam
       * @param {XMLElement} element the MEI beam element
       * @param {Vex.Flow.Staff} staff the containing staff
       * @param {Number} the number of the containing staff
       */
      processBeam : function(element, staff, staff_n) {
        var me = this, elements;
        var process = function() {
          // make sure to get vexNote out of wrapped note objects
          var proc_element = me.processNoteLikeElement(this, staff, staff_n);
          return proc_element.vexNote || proc_element;
        };
        elements = $(element).children().map(process).get();
        me.allBeams.push(new VF.Beam(elements));
        return elements;
      },

      /**
       * Processes an MEI <b>tuplet</b>.
       * Supported attributes:
       *
       * - num (3 if not specified)
       * - numbase (2 if not specified)
       * - num.format ('count' if not specified)
       * - bracket.visible (auto if not specified)
       * - bracket.place (auto if not specified)
       *
       * @method processTuplet
       * @param {XMLElement} element the MEI tuplet element
       * @param {Vex.Flow.Staff} staff the containing staff
       * @param {Number} the number of the containing staff
       */
      processTuplet : function(element, staff, staff_n) {
        var me = this, elements, tuplet, bracketVisible, bracketPlace;
        var process = function() {
          // make sure to get vexNote out of wrapped note objects
          var proc_element = me.processNoteLikeElement(this, staff, staff_n);
          return proc_element.vexNote || proc_element;
        };
        elements = $(element).children().map(process).get();

        tuplet = new VF.Tuplet(elements, {
          num_notes : +element.getAttribute('num') || 3,
          beats_occupied : +element.getAttribute('numbase') || 2
        });

        if (element.getAttribute('num.format') === 'ratio') {
          tuplet.setRatioed(true);
        }

        bracketVisible = element.getAttribute('bracket.visible');
        if (bracketVisible) {
          tuplet.setBracketed((bracketVisible === 'true') ? true : false);
        }

        bracketPlace = element.getAttribute('bracket.place');
        if (bracketPlace) {
          tuplet.setTupletLocation((bracketPlace === 'above') ? 1 : -1);
        }

        me.allTuplets.push(tuplet);
        return elements;
      },

      /**
       * @method processAttrAccid
       */
      processAttrAccid : function(mei_accid, vexObject, i) {
        var val = m2v.tables.accidentals[mei_accid];
        if (!val) {
          throw new m2v.RUNTIME_ERROR('MEI2VF.RERR.BadAttributeValue', 'Invalid attribute value: ' + mei_accid);
        }
        vexObject.addAccidental(i, new VF.Accidental(val));
      },

      /**
       * @method processAttrHo
       */
      processAttrHo : function(mei_ho, vexObject, staff) {
        var me = this;
        vexObject.setExtraLeftPx(+mei_ho * staff.getSpacingBetweenLines() / 2);
      },

      /**
       * @method processAttrTie
       */
      processAttrTie : function(mei_tie, xml_id, pname, oct, staff_n) {
        var me = this, i, j;
        for ( i = 0, j = mei_tie.length; i < j; ++i) {
          if (mei_tie[i] === 'i') {
            me.ties.start_tieslur(xml_id, {
              pname : pname,
              oct : oct,
              staff_n: staff_n,
            });
          } else if (mei_tie[i] === 't') {
            me.ties.terminate_tie(xml_id, {
              pname : pname,
              oct : oct,
              staff_n: staff_n,
            });
          }
        }
      },

      /**
       * @method processAttrSlur
       */
      processAttrSlur : function(mei_slur, xml_id) {
        var me = this, tokens;
        if (mei_slur) {
          // create a list of { letter, num }
          tokens = me.parse_slur_attribute(mei_slur);
          $.each(tokens, function() {
            if (this.letter === 'i') {
              me.slurs.start_tieslur(xml_id, {
                nesting_level : this.nesting_level
              });
            } else if (this.letter === 't') {
              me.slurs.terminate_slur(xml_id, {
                nesting_level : this.nesting_level
              });
            }
          });
        }
      },

      /**
       * @method parse_slure_attribute
       */
      parse_slur_attribute : function(slur_str) {
        var result = [], numbered_tokens, numbered_token, i, j, num;
        numbered_tokens = slur_str.split(' ');
        for ( i = 0, j = numbered_tokens.length; i < j; i += 1) {
          numbered_token = numbered_tokens[i];
          if (numbered_token.length === 1) {
            result.push({
              letter : numbered_token,
              nesting_level : 0
            });
          } else if (numbered_token.length === 2) {
            num = +numbered_token[1];
            if (!num) {
              throw new m2v.RUNTIME_ERROR('MEI2VF.RERR.BadArguments:ParseSlur01', "badly formed slur attribute");
            }
            result.push({
              letter : numbered_token[0],
              nesting_level : num
            });
          } else {
            throw new m2v.RUNTIME_ERROR('MEI2VF.RERR.BadArguments:ParseSlur01', "badly formed slur attribute");
          }
        }
        return result;
      },

      /**
       * converts the pitch of an MEI <b>note</b> element to a VexFlow pitch
       *
       * @method processAttsPitch
       * @param {XMLElement} mei_note
       * @return {String} the VexFlow pitch
       */
      processAttsPitch : function(mei_note) {
        var pname, oct;
        pname = $(mei_note).attr('pname');
        oct = $(mei_note).attr('oct');
        if (!pname || !oct) {
          throw new m2v.RUNTIME_ERROR('MEI2VF.RERR.MissingAttribute', 'pname and oct attributes must be specified for <note>');
        }
        return pname + '/' + oct;
      },

      /**
       * adds an articulation to a note-like object
       * @method addArticulation
       * @param {Vex.Flow.StaveNote} note the note-like VexFlow object
       * @param {XMLElement} ar the articulation element
       */
      addArticulation : function(note, ar) {
        var vexArtic = new VF.Articulation(m2v.tables.articulations[ar.getAttribute('artic')]);
        var place = ar.getAttribute('place');
        if (place) {
          vexArtic.setPosition(m2v.tables.positions[place]);
        }
        note.addArticulation(0, vexArtic);
      },

      /**
       * @method processSyllables
       */
      processSyllables : function(note, element, staff_n) {
        var me = this, annot, syl, verse, text_line, verse_n, syls;
        // syl = me.processSyllable(element);
        syls = $(element).find('syl');
        $.each(syls, function(i) {
          syl = {
            text : $(this).text(),
            wordpos : $(this).attr('wordpos'),
            verse_n : $(this).parents('verse').attr('n'),
          };
          if (syl) {
            annot = me.createAnnot(syl.text, me.cfg.lyricsFont).
              setVerticalJustification(me.BOTTOM).
              setLineSpacing(me.cfg.lyricsFont.spacing);
            note.addAnnotation(0, annot);
            me.verses.addSyllable(annot, syl.wordpos, syl.verse_n, staff_n)
            if (syl.wordpos) {
              me.hyphenation.addSyllable(annot, syl.wordpos, staff_n);
            }
          }
        });
      },

      // processSyllable : function(mei_note) {
      // var me = this, syl, full_syl = '', dash;
      // syl = $(mei_note).find('syl');
      // $(syl).each(function(i, s) {
      // dash = ($(s).attr('wordpos') === 'i' || $(s).attr('wordpos') === 'm')
      // ?
      // '-' : '';
      // full_syl += (i > 0 ? '\n' : '') + $(s).text() + dash;
      // });
      // return full_syl;
      // },

      // temporarily only handle one syllable per note
      /**
       * @method processSyllable
       */
      processSyllable : function(mei_note) {
        var syl = $(mei_note).find('syl')[0];
        if (syl) {
          return {
            text : $(syl).text(),
            wordpos : $(syl).attr('wordpos'),
            verse_n : $(syl).parents('verse').attr('n'),
          };
        }
      },

      // Support for annotations
      /**
       * @method createAnnot
       */
      createAnnot : function(text, annotFont) {
        return (new VF.Annotation(text)).setFont(annotFont.family, annotFont.size, annotFont.weight);
      },

      /**
       * @method getMandatoryAttr
       */
      getMandatoryAttr : function(element, attribute) {
        var result = $(element).attr(attribute);
        if (!result) {
          throw new m2v.RUNTIME_ERROR('MEI2VF.RERR.MissingAttribute', 'Attribute ' + attribute + ' is mandatory.');
        }
        return result;
      },

      /**
       * @method translateDuration
       */
      translateDuration : function(mei_dur) {
        var result = m2v.tables.durations[mei_dur + ''];
        if (result)
          return result;
        throw new m2v.RUNTIME_ERROR('BadArguments', 'The MEI duration "' + mei_dur + '" is not supported.');
      },

      /**
       * @method processAttsDuration
       */
      processAttsDuration : function(mei_note, noDots) {
        var me = this, dur, dur_attr;

        dur_attr = $(mei_note).attr('dur');
        if (dur_attr === undefined) {
          alert('Could not get duration from:\n' + JSON.stringify(mei_note, null, '\t'));
        }
        dur = me.translateDuration(dur_attr);
        if (!noDots && $(mei_note).attr('dots') === '1')
          dur += 'd';
        return dur;
      },

      /**
       * @method setStemDir
       */
      setStemDir : function(element, optionsObj) {
        var specified_dir = {
        down : VF.StaveNote.STEM_DOWN,
        up : VF.StaveNote.STEM_UP
        }[$(element).attr('stem.dir')];
        if (specified_dir) {
          optionsObj.stem_direction = specified_dir;
        } else {
          optionsObj.auto_stem = true;
        }
      },

      /**
       * @method drawSystems
       */
      drawSystems : function(ctx) {
        var me = this, i = me.systems.length;
        while (i--) {
          if (me.systems[i]) {
            me.systems[i].format(ctx).draw(ctx);
          }
        }
      },

      /**
       * @method drawVexBeams
       */
      drawVexBeams : function(beams, ctx) {
        $.each(beams, function() {
          this.setContext(ctx).draw();
        });
      },
      /**
       * @method drawVexBeams
       */
      drawVexTuplets : function(tuplets, ctx) {
        $.each(tuplets, function() {
          this.setContext(ctx).draw();
        });
      }
    };

    return m2v;

  }(MEI2VF || {}, MeiLib, Vex.Flow, jQuery));
;/*
 * EventLink.js Author: Zoltan Komives (zolaemil@gmail.com) Created: 04.07.2013
 *
 * Copyright © 2012, 2013 Richard Lewis, Raffaele Viglianti, Zoltan Komives,
 * University of Maryland
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License. You may obtain a copy of
 * the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations under
 * the License.
 */

var MEI2VF = ( function(m2v, MeiLib, VF, $, undefined) {

    /**
     * @class MEI2VF.EventLink
     * @private
     * Represents a link between two MEI events. The link is represented by two
     * references:
     *  
     * 1. reference to start event, 
     * 2. reference to end event.     
     *
     * @constructor
     * @param {String} first_id
     * @param {String} last_id 
     */
    m2v.EventLink = function(first_id, last_id) {
      this.init(first_id, last_id);
    };

    m2v.EventLink.prototype = {
      init : function(first_id, last_id) {
        this.first_ref = new m2v.EventReference(first_id);
        this.last_ref = new m2v.EventReference(last_id);
        this.params = {};
      },

      /**
       * @param {Object} params
       *            is an object. for ties and slurs { linkCond } to indicate
       *            the linking condition when parsing from attributes (pitch
       *            name for ties, nesting level for slurs); for hairpins
       *            params it is an object { place, form }
       */
      setParams : function(params) {
        this.params = params;
      },

      setFirstRef : function(first_ref) {
        this.first_ref = first_ref;
      },

      setLastRef : function(last_ref) {
        this.last_ref = last_ref;
      },

      setFirstId : function(id) {
        this.first_ref.setId(id);
      },

      setLastId : function(id) {
        this.last_ref.setId(id);
      },

      setFirstTStamp : function(tstamp) {
        this.first_ref.setTStamp(tstamp);
      },

      setLastTStamp : function(tstamp2) {
        this.last_ref.setTStamp(tstamp2);
      },

      setContext : function(meicontext) {
        this.meicontext = meicontext;
      },

      getFirstId : function() {
        return this.first_ref.getId({
          meicontext : this.meicontext
        });
      },

      getLastId : function() {
        return this.last_ref.getId({
          meicontext : this.meicontext
        });
      }
    };

    return m2v;

  }(MEI2VF || {}, MeiLib, Vex.Flow, jQuery));
;/*
 * EventReference.js Author: Zoltan Komives (zolaemil@gmail.com) Created:
 * 04.07.2013
 *
 * Copyright © 2012, 2013 Richard Lewis, Raffaele Viglianti, Zoltan Komives,
 * University of Maryland
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License. You may obtain a copy of
 * the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations under
 * the License.
 */

var MEI2VF = ( function(m2v, MeiLib, VF, $, undefined) {

    /**
     * @class MEI2VF.EventReverence
     * Represents and event with its xmlid, but if the xmlid is not defined, it
     * can also hold the timestamp that can be resolved as soon as the context
     * that holds the event is established. When the tstamp reference is being
     * resolved, the xml:id is calculated using the generic function tstamp2id(),
     * then the xml:id stored, thus marking that the reference is resolved.
     * @private
     *
     * @constructor
     * @param {String} xmlid
     */
    m2v.EventReference = function(xmlid) {
      this.xmlid = xmlid;
    };

    m2v.EventReference.prototype = {

      setId : function(xmlid) {
        this.xmlid = xmlid;
      },

      setTStamp : function(tstamp) {
        this.tstamp = tstamp;
        if (this.xmlid)
          this.tryResolveReference(true);
      },

      tryResolveReference : function() {
        var tstamp, meicontext;
        tstamp = this.tstamp;
        meicontext = this.meicontext;
        if (!tstamp) {
          throw new m2v.RUNTIME_ERROR('MEI2VF:RERR:BADARG:EventRef001', 'EventReference: tstamp must be set in order to resolve reference.');
        }
        if (this.meicontext) {
          // look up event corresponding to the given tstamp (strictly or losely)
          this.xmlid = MeiLib.tstamp2id(this.tstamp, this.meicontext.layer, this.meicontext.meter);
        } else {
          this.xmlid = null;
        }
      },

      /**
       * @param params {
       *            meicontext, strict }; both parameters are optional;
       *            meicontext is an obejct { layer, meter }; strict is
       *            boolean, false if not defined.
       *
       */
      getId : function(params) {
        if (params && params.meicontext)
          this.setContext(params.meicontext);
        if (this.xmlid)
          return this.xmlid;
        if (this.tstamp && this.meicontext) {
          // look up the closest event to tstamp within
          // this.meicontext and return its ID
          this.tryResolveReference(params && params.strict);
          return this.xmlid;
        }
        return null;
      },

      setContext : function(meicontext) {
        this.meicontext = meicontext;
      }
    };

    return m2v;

  }(MEI2VF || {}, MeiLib, Vex.Flow, jQuery));
;var MEI2VF = ( function(m2v, MeiLib, VF, $, undefined) {

    /**
     * @class MEI2VF.Hyphenation
     * @private
     *
     * @constructor
     * @param {Object} cfg
     */
    m2v.Hyphenation = function(font, printSpaceRight, maxHyphenDistance) {
      var me = this;
      me.allSyllables = [];
      me.printSpaceRight = printSpaceRight;
      me.font = font;
      me.maxHyphenDistance = maxHyphenDistance;
    };

    m2v.Hyphenation.prototype = {

      WORDBOUND : null,

      addSyllable : function(annot, wordpos, staff_n) {
        var me = this;
        if (!me.allSyllables[staff_n])
          me.allSyllables[staff_n] = [];
        if (wordpos === 'i')
          me.allSyllables[staff_n].push(me.WORDBOUND);
        me.allSyllables[staff_n].push(annot);
        if (wordpos === 't')
          me.allSyllables[staff_n].push(me.WORDBOUND);
      },

      addLineBreaks : function(staffInfos, measureX) {
        var me = this, i, j;
        for ( i = 1, j = staffInfos.length; i < j; i += 1) {
          if (!me.allSyllables[i])
            me.allSyllables[i] = [];
          me.allSyllables[i].push(measureX);
        }
      },

      setContext : function(ctx) {
        this.ctx = ctx;
        return this;
      },

      draw : function() {
        var me = this, i, k, first, second, hyphenWidth;

        me.ctx.setFont(me.font.family, me.font.size, me.font.weight);

        hyphenWidth = me.ctx.measureText('-').width;

        i = me.allSyllables.length;
        while (i--) {
          if (me.allSyllables[i]) {
            k = me.allSyllables[i].length;
            while (k--) {
              first = me.allSyllables[i][k];
              second = me.allSyllables[i][k + 1];

              if (first !== me.WORDBOUND && second !== me.WORDBOUND) {
                var opts = {
                  hyphen_width : hyphenWidth,
                  max_hyphen_distance : me.maxHyphenDistance
                };
                if (first.system) {
                  opts.first_annot = {
                    x : first.system.getMeasures()[0].getX()
                  };
                } else {
                  opts.first_annot = first;
                }
                if (second === undefined || second.system) {
                  opts.last_annot = {
                    x : me.printSpaceRight
                  };
                } else {
                  opts.last_annot = second;
                }
                if (opts.first_annot.y || opts.last_annot.y) {
                  var h = new VF.Hyphen(opts);
                  h.setContext(me.ctx).renderHyphen();
                }
              }
            }
          }
        }
      }
    };

    return m2v;

  }(MEI2VF || {}, MeiLib, Vex.Flow, jQuery));
;var MEI2VF = ( function(m2v, MeiLib, VF, $, undefined) {

    /**
     * @class MEI2VF.Verses
     * @private
     *
     * @constructor
     * @param {Object} cfg
     */
    m2v.Verses = function(font, printSpaceRight, maxHyphenDistance) {
      var me = this;
      me.hyphenations = {};
      me.verses = {};
      me.printSpaceRight = printSpaceRight;
      me.font = font;
      me.maxHyphenDistance = maxHyphenDistance;
    };

    m2v.Verses.prototype = {

      newHyphenation : function() {
        return new m2v.Hyphenation(this.font, this.printSpaceRight, this.maxHyphenDistance);
      },

      addHyphenation : function(verse_n) {
        var me = this;
        if (!me.hyphenations[verse_n]) {
          me.hyphenations[verse_n] = me.newHyphenation();
        }
        return me;
      },

      getHyphenation : function(verse_n) {
        var me = this, hyphenation;
        hyphenation = me.hyphenations[verse_n];
        if (!hyphenation) {
          hyphenation = me.newHyphenation();
          me.hyphenations[verse_n] = hyphenation;
        }
        return hyphenation;
      },

      initHyphenations : function(elems) {
        var me = this, verse_n;
        $.each(elems, function(i) {
          verse_n = $(elems[i]).parents('verse').attr('n') || '1';
          me.addHyphenation(verse_n);
        });
      },

      drawHyphens : function(ctx) {
        var me = this, verse_n, i, hyph;
        for (verse_n in me.hyphenations) {
          me.getHyphenation(verse_n).setContext(ctx).draw();
        };
        return me;
      },

      format : function() {
        var me = this, verse_n, text_line, verse, i, j;
        text_line = 0;
        for (verse_n in me.verses) {
          verse = me.verses[verse_n];
          for (i = 0, j = verse.length; i < j; i++) {
            verse[i].setTextLine(text_line);
          }
          text_line += 1;
        };
        return me;
      },

      addLineBreaks : function(staffInfos, measureX) {
        var me = this;
        for (verse_n in me.hyphenations){
          me.hyphenations[verse_n].addLineBreaks(staffInfos, measureX);
        };
        return me;
      },

      addSyllable : function(annot, wordpos, verse_n, staff_n) {
        var me = this;
        verse_n = verse_n || '1';
        if (!me.verses[verse_n]) {
          me.verses[verse_n] = [];
        }
        me.verses[verse_n].push(annot);
        if (wordpos) {
          me.hyphenations[verse_n].addSyllable(annot, wordpos, staff_n);
        }
        return me;
      },

    };

    return m2v;

  }(MEI2VF || {}, MeiLib, Vex.Flow, jQuery));
;var MEI2VF = ( function(m2v, MeiLib, VF, $, undefined) {

    /**
     * @class MEI2VF.LinkCollection
     * @private
     *
     * @constructor
     */
    m2v.LinkCollection = function(systemInfo, unresolvedTStamp2) {
      this.init(systemInfo, unresolvedTStamp2);
    };

    m2v.LinkCollection.prototype = {

      /**
       * initializes the LinkCollection
       */
      init : function(systemInfo, unresolvedTStamp2) {
        /**
         * @property
         */
        this.allVexObjects = [];
        /**
         * @property
         */
        this.allModels = [];
        /**
         * @property
         */
        this.systemInfo = systemInfo;
        /**
         * @property
         */
        this.unresolvedTStamp2 = unresolvedTStamp2;
      },

      validateAtts : function() {
        throw new m2v.RUNTIME_ERROR('MEI2VF.DEVELOPMENT_ERROR.validateAtts', 'Developers have to provide a validateAtts method when inheriting MEI2VF.LinkCollection.');
      },

      createVexFromInfos : function() {
        throw new m2v.RUNTIME_ERROR('MEI2VF.DEVELOPMENT_ERROR.createVexFromInfos', 'Developers have to provide a createVexFromInfos method when inheriting MEI2VF.LinkCollection.');
      },

      /**
       * create EventLink objects from  <b>tie</b>, <b>slur</b> or <b>hairpin</b>
       * elements
       */
      createInfos : function(link_elements, measureElement, systemInfo) {
        var me = this;

        var link_staffInfo = function(lnkelem) {
          return {
            staff_n : $(lnkelem).attr('staff') || '1',
            layer_n : $(lnkelem).attr('layer') || '1'
          };
        };

        // convert tstamp into startid in current measure
        var local_tstamp2id = function(tstamp, lnkelem, measureElement) {
          var stffinf = link_staffInfo(lnkelem);
          var staff = $(measureElement).find('staff[n="' + stffinf.staff_n + '"]');
          var layer = $(staff).find('layer[n="' + stffinf.layer_n + '"]').get(0);
          if (!layer) {
            var layer_candid = $(staff).find('layer');
            if (layer_candid && !layer_candid.attr('n'))
              layer = layer_candid;
            if (!layer)
              throw new m2v.RUNTIME_ERROR('MEI2VF.RERR.createInfos:E01', 'Cannot find layer');
          }
          var staffdef = systemInfo.getStaffInfo(stffinf.staff_n);
          if (!staffdef)
            throw new m2v.RUNTIME_ERROR('MEI2VF.RERR.createInfos:E02', 'Cannot determine staff definition.');
          var meter = staffdef.meter;
          if (!meter.count || !meter.unit)
            throw new m2v.RUNTIME_ERROR('MEI2VF.RERR.createInfos:E03', "Cannot determine meter; missing or incorrect @meter.count or @meter.unit.");
          return MeiLib.tstamp2id(tstamp, layer, meter);
        };

        var measure_partOf = function(tstamp2) {
          return tstamp2.substring(0, tstamp2.indexOf('m'));
        };

        var beat_partOf = function(tstamp2) {
          return tstamp2.substring(tstamp2.indexOf('+') + 1);
        };

        $.each(link_elements, function() {
          var eventLink, atts, startid, tstamp, endid, tstamp2, measures_ahead;

          eventLink = new m2v.EventLink(null, null);

          atts = m2v.Util.attsToObj(this);

          me.validateAtts(atts);

          eventLink.setParams(atts);

          // find startid for eventLink. if tstamp is provided in the
          // element, tstamp will be calculated.
          startid = atts.startid;
          if (startid) {
            eventLink.setFirstId(startid);
          } else {
            tstamp = atts.tstamp;
            if (tstamp) {
              startid = local_tstamp2id(tstamp, this, measureElement);
              eventLink.setFirstId(startid);
            }
            // else {
            // // no @startid, no @tstamp ==> eventLink.first_ref
            // remains empty.
            // }
          }

          // find end reference value (id/tstamp) of eventLink:
          endid = atts.endid;
          if (endid) {
            eventLink.setLastId(endid);
          } else {
            tstamp2 = atts.tstamp2;
            if (tstamp2) {
              measures_ahead = +measure_partOf(tstamp2);
              if (measures_ahead > 0) {
                eventLink.setLastTStamp(beat_partOf(tstamp2));
                // register that eventLink needs context;
                // need to save: measure.n, link.staff_n,
                // link.layer_n
                var staffinfo = link_staffInfo(this);
                var target_measure_n = +$(measureElement).attr('n') + measures_ahead;
                var refLocationIndex = target_measure_n.toString() + ':' + staffinfo.staff_n + ':' + staffinfo.layer_n;
                if (!me.unresolvedTStamp2[refLocationIndex])
                  me.unresolvedTStamp2[refLocationIndex] = [];
                me.unresolvedTStamp2[refLocationIndex].push(eventLink);
              } else {
                endid = local_tstamp2id(beat_partOf(tstamp2), this, measureElement);
                eventLink.setLastId(endid);
              }
            }
            // else {
            // // TODO no @endid, no @tstamp2 ==> eventLink.last_ref remains empty.
            // }
          }
          me.addModel(eventLink);
        });
      },

      /**
       * adds a new model to {@link #allModels}
       * @param {Object} obj the object to add
       */
      addModel : function(obj) {
        this.allModels.push(obj);
      },

      /**
       * gets all models
       * @return {Object[]} all models in {@link #allModels}
       */
      getModels : function() {
        return this.allModels;
      },

      /**
       * sets the context for the link collection
       * @param {Object} ctx the canvas context
       */
      setContext : function(ctx) {
        this.ctx = ctx;
        return this;
      },

      /**
       * draws the link collection to the canvas set by {@link #setContext}
       */
      draw : function() {
        var ctx = this.ctx;
        $.each(this.allVexObjects, function() {
          this.setContext(ctx).draw();
        });
      }
    };

    /**
     * @class MEI2VF.Hairpins
     * @extend MEI2VF.LinkCollection
     * @private
     *
     * @constructor
     */
    m2v.Hairpins = function(systemInfo, unresolvedTStamp2) {
      this.init(systemInfo, unresolvedTStamp2);
    };

    Vex.Inherit(m2v.Hairpins, m2v.LinkCollection, {

      init : function(systemInfo, unresolvedTStamp2) {
        m2v.Ties.superclass.init.call(this, systemInfo, unresolvedTStamp2);
      },

      validateAtts : function(atts) {
        if (!atts.form) {
          throw new m2v.RUNTIME_ERROR('MEI2VF.RERR.BadArguments:createInfos', '@form is mandatory in <hairpin> - make sure the xml is valid.');
        }
      },

      createVexFromInfos : function(notes_by_id) {
        var me = this, f_note, l_note, vex_options;
        vex_options = {
          height : 10,
          y_shift : 0,
          left_shift_px : 0,
          r_shift_px : 0
        };
        $.each(me.allModels, function() {
          f_note = notes_by_id[this.getFirstId()] || {};
          l_note = notes_by_id[this.getLastId()] || {};

          if (f_note.system !== undefined && l_note.system !== undefined && f_note.system !== l_note.system) {
          } else {
            me.createSingleHairpin(f_note, l_note, this.params, vex_options);
          }

        });
        return this;
      },

      createSingleHairpin : function(f_note, l_note, params, vex_options) {
        var me = this, place, type, hairpin;
        place = m2v.tables.positions[params.place];
        type = m2v.tables.hairpins[params.form];

        if (f_note.vexNote && l_note.vexNote) {
          hairpin = new VF.StaveHairpin({
            first_note : f_note.vexNote,
            last_note : l_note.vexNote
          }, type);

          hairpin.setRenderOptions(vex_options);
          hairpin.setPosition(place);

          me.allVexObjects.push(hairpin);
        } else {
          m2v.L('Hairpins', 'Hairpin cannot be rendered:');
          console.log(arguments);
        }

      }
    });

    /**
     * @class MEI2VF.Ties
     * @extend MEI2VF.LinkCollection
     * @private
     *
     * @constructor
     */

    m2v.Ties = function(systemInfo, unresolvedTStamp2) {
      this.init(systemInfo, unresolvedTStamp2);
    };

    Vex.Inherit(m2v.Ties, m2v.LinkCollection, {

      init : function(systemInfo, unresolvedTStamp2) {
        m2v.Ties.superclass.init.call(this, systemInfo, unresolvedTStamp2);
      },

      validateAtts : function() {
        return;
      },

      // NB called from tie/slur attributes elements
      start_tieslur : function(startid, linkCond) {
        var eventLink = new m2v.EventLink(startid, null);
        eventLink.setParams({
          linkCond : linkCond
        });
        this.allModels.push(eventLink);
      },

      terminate_tie : function(endid, linkCond) {
        var cmpLinkCond, found, i, tie, allTies;

        allTies = this.getModels();

        cmpLinkCond = function(lc1, lc2) {
          return (lc1 && lc2 && lc1.pname === lc2.pname && lc1.oct === lc2.oct 
            && lc1.staff_n === lc2.staff_n);
        };

        if (!linkCond.pname || !linkCond.oct)
          throw new m2v.RUNTIME_ERROR('MEI2VF.RERR.BadArguments:TermTie01', 'no pitch or octave specified for the tie');
        found = false;
        for ( i = 0; !found && i < allTies.length; ++i) {
          tie = allTies[i];
          if (!tie.getLastId()) {
            if (cmpLinkCond(tie.params.linkCond, linkCond)) {
              found = true;
              tie.setLastId(endid);
            }
            // else {
            // // TODO in case there's no link condition set for the
            // link,
            // // we have to retreive the pitch of the referenced note.
            // // var note_id = tie.getFirstId();
            // // if (note_id) {
            // // var note = me.notes_by_id[note_id];
            // // if (note && cmpLinkCond(tie.params.linkCond,
            // // linkCond)) {
            // // found=true;
            // // tie.setLastId(endid);
            // // }
            // // }
            // }
          }
        }
        // if no tie object found that is uncomplete and with the same
        // pitch, then create a tie that has only endid set.
        if (!found)
          this.addModel(new m2v.EventLink(null, endid));
      },

      terminate_slur : function(endid, linkCond) {
        var me = this, cmpLinkCond, found, i, slur;

        var allModels = this.getModels();

        cmpLinkCond = function(lc1, lc2) {
          return lc1.nesting_level === lc2.nesting_level;
        };

        found = false;
        for ( i = 0; i < allModels.length; ++i) {
          slur = allModels[i];
          if (slur && !slur.getLastId() && cmpLinkCond(slur.params.linkCond, linkCond)) {
            slur.setLastId(endid);
            found = true;
            break;
          }
        }
        if (!found)
          me.addModel(new m2v.EventLink(null, endid));
      },

      createVexFromInfos : function(notes_by_id) {
        var me = this, f_note, l_note;
        $.each(me.allModels, function() {
          f_note = notes_by_id[this.getFirstId()] || {};
          l_note = notes_by_id[this.getLastId()] || {};
          if (f_note.system !== undefined && l_note.system !== undefined && f_note.system !== l_note.system) {
            me.createSingleStaveTie(f_note, {}, this.params);

            // temporary: set the same curve direction for the second note by
            // evaluating the stem direction of the first note; change this when
            // the curve dir of the first note is calculated differently in
            // VexFlow
            this.params.curvedir = (f_note.vexNote.getStemDirection() === -1) ? 'above' : 'below';
            me.createSingleStaveTie({}, l_note, this.params);
          } else {
            me.createSingleStaveTie(f_note, l_note, this.params);
          }
        });
        return this;
      },

      createSingleStaveTie : function(f_note, l_note, params) {
        var me = this, vexTie, bezier, cps;
        bezier = params.bezier;
        if (bezier) {
          cps = me.bezierStringToCps(bezier);
          vexTie = new VF.Curve(f_note.vexNote, l_note.vexNote, {
            cps : cps,
            y_shift_start : +params.startvo,
            y_shift_end : +params.endvo
          });
        } else {
          vexTie = new VF.StaveTie({
            first_note : f_note.vexNote,
            last_note : l_note.vexNote,
            first_indices : f_note.index,
            last_indices : l_note.index
          });
          vexTie.setDir(params.curvedir);
        }
        me.allVexObjects.push(vexTie);
      },

      bezierStringToCps : function(str) {
        var cps = [], xy, bezierArray = str.split(' ');
        while (bezierArray[0]) {
          xy = bezierArray.splice(0, 2);
          cps.push({
            x : +xy[0],
            y : +xy[1]
          });
        }
        return cps;
      }
    });

    return m2v;

  }(MEI2VF || {}, MeiLib, Vex.Flow, jQuery));
;var MEI2VF = ( function(m2v, MeiLib, VF, $, undefined) {

    /**
     * @class MEI2VF.PointerCollection
     * @private
     *
     * @constructor
     */
    m2v.PointerCollection = function(systemInfo, font) {
      this.init(systemInfo, font);
    };

    m2v.PointerCollection.prototype = {

      BOTTOM : VF.Annotation.VerticalJustify.BOTTOM,

      /**
       * initializes the PointerCollection
       */
      init : function(systemInfo, font) {
        /**
         * @property
         */
        this.allVexObjects = [];
        /**
         * @property
         */
        this.allModels = [];
        /**
         * @property
         */
        this.systemInfo = systemInfo;
        /**
         * @property
         */
        this.font = font;
      },

      createVexFromInfos : function() {
        throw new m2v.RUNTIME_ERROR('MEI2VF.DEVELOPMENT_ERROR.createVexFromInfos', 'You have to prodide a createVexFromInfos method when inheriting MEI2VF.PointerCollection.');
      },

      createInfos : function(elements, measureElement) {
        var me = this;

        var link_staffInfo = function(lnkelem) {
          return {
            staff_n : $(lnkelem).attr('staff') || '1',
            layer_n : $(lnkelem).attr('layer') || '1'
          };
        };

        // convert tstamp into startid in current measure
        var local_tstamp2id = function(tstamp, lnkelem, measureElement) {
          var stffinf = link_staffInfo(lnkelem);
          var staff = $(measureElement).find('staff[n="' + stffinf.staff_n + '"]');
          var layer = $(staff).find('layer[n="' + stffinf.layer_n + '"]').get(0);
          if (!layer) {
            var layer_candid = $(staff).find('layer');
            if (layer_candid && !layer_candid.attr('n'))
              layer = layer_candid;
            if (!layer)
              throw new m2v.RUNTIME_ERROR('MEI2VF.RERR.createInfos:E01', 'Cannot find layer');
          }
          var staffdef = me.systemInfo.getStaffInfo(stffinf.staff_n);
          if (!staffdef)
            throw new m2v.RUNTIME_ERROR('MEI2VF.RERR.createInfos:E02', 'Cannot determine staff definition.');
          var meter = staffdef.meter;
          if (!meter.count || !meter.unit)
            throw new m2v.RUNTIME_ERROR('MEI2VF.RERR.createInfos:E03', "Cannot determine meter; missing or incorrect @meter.count or @meter.unit.");
          return MeiLib.tstamp2id(tstamp, layer, meter);
        };

        $.each(elements, function() {
          var atts, startid, tstamp;

          atts = m2v.Util.attsToObj(this);

          startid = atts.startid;
          if (!startid) {
            tstamp = atts.tstamp;
            if (tstamp) {
              startid = local_tstamp2id(tstamp, this, measureElement);
            } else {
              throw new m2v.RUNTIME_ERROR('MEI2VF.RERR.createInfos', "Neither @startid nor @tstamp are specified");
            }
          }
          me.allModels.push({
            element : this,
            atts : atts,
            startid : startid
          });
        });
      },

      /**
       * adds a new model to {@link #allModels}
       * @param {Object} obj the object to add
       */
      addModel : function(obj) {
        this.allModels.push(obj);
      },

      /**
       * gets all models
       * @return {Object[]} all models in {@link #allModels}
       */
      getModels : function() {
        return this.allModels;
      }
    };

    /**
     * @class MEI2VF.Directives
     * @extend MEI2VF.PointerCollection
     * @private
     *
     * @constructor
     */
    m2v.Directives = function(systemInfo, font) {
      this.init(systemInfo, font);
    };

    Vex.Inherit(m2v.Directives, m2v.PointerCollection, {

      init : function(systemInfo, font) {
        m2v.Directives.superclass.init.call(this, systemInfo, font);
      },

      createVexFromInfos : function(notes_by_id) {
        var me = this, i, model, note, annot;
        i = me.allModels.length;
        while (i--) {
          model = me.allModels[i];
          note = notes_by_id[model.startid];
          if (note) {
            annot = (new VF.Annotation($(model.element).text().trim())).setFont(me.font.family, me.font.size, me.font.weight);

            // TEMPORARY: set width of modifier to zero so voices with modifiers
            // don't get too much width; remove when the width calculation in
            // VexFlow does distinguish between different y values when
            // calculating the width of tickables
            annot.setWidth(0);
            if (model.atts.place === 'below') {
              note.vexNote.addAnnotation(0, annot.setVerticalJustification(me.BOTTOM));
            } else {
              note.vexNote.addAnnotation(0, annot);
            }
          } else {
            throw new m2v.RUNTIME_ERROR('MEI2VF.RERR.createVexFromInfos', "The reference in the directive could not be resolved.");
          }
        }
      }
    });

    /**
     * @class MEI2VF.Dynamics
     * @extend MEI2VF.PointerCollection
     * @private
     *
     * @constructor
     */
    m2v.Dynamics = function(systemInfo, font) {
      this.init(systemInfo, font);
    };

    Vex.Inherit(m2v.Dynamics, m2v.PointerCollection, {

      init : function(systemInfo, font) {
        m2v.Dynamics.superclass.init.call(this, systemInfo, font);
      },

      // TODO use Vex.Flow.Textnote instead of VF.Annotation!?
      createVexFromInfos : function(notes_by_id) {
        var me = this, i, model, note, annot;
        i = me.allModels.length;
        while (i--) {
          model = me.allModels[i];
          note = notes_by_id[model.startid];
          if (note) {
            annot = (new VF.Annotation($(model.element).text().trim())).setFont(me.font.family, me.font.size, me.font.weight);
            if (model.atts.place === 'above') {
              note.vexNote.addAnnotation(0, annot);
            } else {
              note.vexNote.addAnnotation(0, annot.setVerticalJustification(me.BOTTOM));
            }
          } else {
            throw new m2v.RUNTIME_ERROR('MEI2VF.RERR.createVexFromInfos', "The reference in the directive could not be resolved.");
          }
        }

      }
    });

    /**
     * @class MEI2VF.Fermatas
     * @extend MEI2VF.PointerCollection
     * @private
     *
     * @constructor
     */
    m2v.Fermatas = function(systemInfo, font) {
      this.init(systemInfo, font);
    };

    Vex.Inherit(m2v.Fermatas, m2v.PointerCollection, {

      init : function(systemInfo, font) {
        m2v.Fermatas.superclass.init.call(this, systemInfo, font);
      },

      createVexFromInfos : function(notes_by_id) {
        var me = this, i, model, note, annot;
        i = me.allModels.length;
        while (i--) {
          model = me.allModels[i];
          note = notes_by_id[model.startid];
          if (note) {
            me.addFermataToNote(note.vexNote, model.atts.place);
          } else {
            throw new m2v.RUNTIME_ERROR('MEI2VF.RERR.createVexFromInfos', "The reference in the directive could not be resolved.");
          }
        }

      },

      /**
       * adds a fermata to a note-like object
       * @method addFermataToNote
       * @param {Vex.Flow.StaveNote} note the note-like VexFlow object
       * @param {'above'/'below'} place The place of the fermata
       * @param {Number} index The index of the note in a chord (optional)
       */
      addFermataToNote : function(note, place, index) {
        var vexArtic = new VF.Articulation(m2v.tables.fermata[place]);
        vexArtic.setPosition(m2v.tables.positions[place]);
        note.addArticulation(index || 0, vexArtic);
      }
    });

    return m2v;

  }(MEI2VF || {}, MeiLib, Vex.Flow, jQuery));
;var MEI2VF = ( function(m2v, MeiLib, VF, $, undefined) {

    /**
     * @class MEI2VF.Measure
     * @private
     *
     * @constructor
     * @param {Object} config The configuration object
     */
    m2v.Measure = function(config) {
      this.init(config);
    };

    m2v.Measure.prototype = {

      /**
       * initializes the current MEI2VF.Measure object
       * @param {Object} config The configuration object
       */
      init : function(config) {
        var me = this;
        /**
         * @cfg {XMLElement} element the MEI element of the current measure
         */
        me.element = config.element;
        /**
         * @cfg {Number} n The number of the current measure as specified in
         * the MEI document
         */
        me.n = config.n;
        /**
         * @cfg {Array} staffs an array of the staffs in the current
         * measure. Contains
         */
        me.staffs = config.staffs;
        /**
         * @cfg {MEI2VF.StaveVoices} voices The voices of all staffs in the
         * current measure
         */
        me.voices = config.voices;
        /**
         * @cfg {MEI2VF.Verses} verses All verses in the entire score
         */
         me.verses = config.verses;
        /**
         * @cfg {MEI2VF.Connectors} startConnectors an instance of
         * MEI2VF.Connectors handling all left connectors (only the first measure
         * in a system has data)
         */
        me.startConnectors = new m2v.Connectors(config.startConnectorCfg);
        /**
         * @cfg {MEI2VF.Connectors} inlineConnectors an instance of
         * MEI2VF.Connectors handling all right connectors
         */
        me.inlineConnectors = new m2v.Connectors(config.inlineConnectorCfg);

        me.tieElements = config.tieElements;
        me.slurElements = config.slurElements;
        me.hairpinElements = config.hairpinElements;
        /**
         * @cfg {XMLElement[]} tempoElements the MEI tempo elements in the
         * current measure
         */
        me.tempoElements = config.tempoElements;
        /**
         * @cfg {Object} tempoFont the font used for rendering tempo
         * specifications
         */
        me.tempoFont = config.tempoFont;
        /**
         * @property {Number} maxNoteStartX the maximum note_start_x value of all
         * Vex.Flow.Stave objects in the current measure
         */
        me.maxNoteStartX = 0;
        /**
         * @property {Number} meiW the width attribute of the measure element or
         * null if NaN
         */
        me.meiW = me.readMEIW(me.element);
      },

      /**
       *  reads the width attribute of the specified element and converts it to a
       * number
       * @param {XMLElement} element the element to process
       * @return {Number} the number of the attribute or null if NaN
       */
      readMEIW : function(element) {
        return +element.getAttribute('width') || null;
      },

      /**
       * gets the staffs array of the current measure
       * @return {Array}
       */
      getStaffs : function() {
        return this.staffs;
      },

      /**
       * gets the voices object of the current measure
       * @return {MEI2VF.StaveVoices}
       */
      getVoices : function() {
        return this.voices;
      },

      /**
       * gets the x coordinate of the staff
       * @return {Number}
       */
      getX : function() {
        return this.getFirstDefinedStaff().x;
      },

      /**
       * gets the number of the current staff as specified in the MEI code
       * @return {Number}
       */
      getN : function() {
        return this.n;
      },

      /**
       * gets the first defined staff in the current measure
       * @return {Vex.Flow.Stave}
       */
      getFirstDefinedStaff : function() {
        var me = this, i, j;
        for ( i = 0, j = me.staffs.length; i < j; i += 1) {
          if (me.staffs[i]) {
            return me.staffs[i];
          }
        }
        throw new m2v.RUNTIME_ERROR('ERROR', 'getFirstDefinedStaff(): no staff found in the current measure.');
      },

      /**
       * Writes the data of the tempo elements in the current measure to the
       * corresponding Vex.Flow.Stave object
       */
      addTempoToStaves : function() {
        var me = this, offsetX, vexStaff, vexTempo, atts, halfLineDistance;
        $.each(me.tempoElements, function() {
          atts = m2v.Util.attsToObj(this);
          vexStaff = me.staffs[atts.staff];
          halfLineDistance = vexStaff.getSpacingBetweenLines() / 2; 
          vexTempo = new Vex.Flow.StaveTempo({
            name : $(this).text(),
            duration : atts['mm.unit'],
            dots : +atts['mm.dots'],
            bpm : +atts.mm
          }, vexStaff.x, 5);
          if (atts.vo) {
            vexTempo.setShiftY(+atts.vo * halfLineDistance);
          }
          offsetX = (vexStaff.getModifierXShift() > 0) ? -14 : 14;

          // if a staff has a time signature, set the tempo on top of the time
          // signature instead of the first note
          if (vexStaff.hasTimeSig) {
            offsetX -= 24;
          }
          if (atts.ho) {
            offsetX += +atts.ho * halfLineDistance;
          }
          vexTempo.setShiftX(offsetX);
          vexTempo.font = me.tempoFont;
          vexStaff.modifiers.push(vexTempo);
        });
      },

      /**
       * calculates the minimum width of the current measure
       */
      calculateMinWidth : function() {
        var me = this;
        me.calculateMaxNoteStartX();
        me.calculateRepeatPadding();
        /**
         * @property {Number} minVoicesW the minimum width of the voices in the
         * measure
         */
        me.minVoicesW = me.voices.preFormat();
        /**
         * @property {Number} minWidth the minimum width of the measure
         */
        me.minWidth = me.maxNoteStartX + me.minVoicesW + me.repeatPadding;
      },

      /**
       * gets the minimum width of the current measure;
       */
      getMinWidth : function() {
        return this.minWidth;
      },

      /**
       * calculates the maximum note_start_x of all Vex.Flow.Stave objects in the
       * current measure
       */
      calculateMaxNoteStartX : function() {
        var me = this, i, staffs, staff;
        staffs = me.staffs;
        i = staffs.length;
        while (i--) {
          staff = staffs[i];
          if (staff) {
            me.maxNoteStartX = Math.max(me.maxNoteStartX, staff.getNoteStartX());
          }
        }
      },

      /**
       * calculates additional start padding when there are repetition start bars
       * in the current measure
       */
      calculateRepeatPadding : function() {
        var me = this;
        var staff = me.getFirstDefinedStaff();
        /**
         * @property {0|20} repeatPadding additional padding (20px) if the staff
         * does have a left REPEAT_BEGIN barline located to the right of other
         * staff modifiers; 0px in all other cases.
         */
        me.repeatPadding = (staff.modifiers[0].barline == Vex.Flow.Barline.type.REPEAT_BEGIN && staff.modifiers.length > 2) ? 20 : 0;
      },

      /**
       * Formats the staffs in the current measure: sets x coordinates and adds
       * staff labels
       * @param {Number} x The x coordinate of the the measure
       * @param {String[]} labels The labels of all staves
       */
      format : function(x, labels) {
        var me = this, width = me.w, i = me.staffs.length, staff, k;
        while (i--) {
          if (me.staffs[i]) {
            staff = me.staffs[i];
            if (labels && typeof labels[i] === 'string') {
              staff.setText(labels[i], VF.Modifier.Position.LEFT, {
                shift_y : -3
              });
            }

            if (typeof staff.setX == "function") {
              staff.setX(x);
            } else {
              /* Fallback if VexFlow doesn't have setter */
              //TODO: remove when setX() is merged to standard VexFlow
              staff.x = x;
              staff.glyph_start_x = x + 5;
              staff.bounds.x = x;
              for (k = 0; k < staff.modifiers.length; k++) {
                staff.modifiers[k].x = x;
              }
            }

            staff.start_x = staff.x + me.maxNoteStartX;
            staff.setWidth(width);
            staff.modifiers[0].x += x;
          }
        }
        me.voices.format(me.getFirstDefinedStaff());
        me.verses.format();
      },

      /**
       * Draws the staffs, voices and connectors in the current measure to a
       * canvas
       * @param {Object} ctx the canvas context
       */
      draw : function(ctx) {
        var me = this, i, staffs, staff;
        staffs = me.staffs;
        i = staffs.length;
        while (i--) {
          staff = staffs[i];
          if (staff) {
            staff.setContext(ctx).draw();
          }
        }
        me.voices.draw(ctx, staffs);
        me.startConnectors.setContext(ctx).draw();
        me.inlineConnectors.setContext(ctx).draw();
      }
    };

    return m2v;

  }(MEI2VF || {}, MeiLib, Vex.Flow, jQuery));
;/**
 * @class MEI2VF
 */
var MEI2VF = ( function(m2v, MeiLib, VF, $, undefined) {

    /**
     * @property {Boolean} DO_LOG specifies if logging is enabled or disabled.
     * Defaults to false. Use {@link MEI2VF#setLogging setLogging()} to change
     * the value.
     * @private
     */
    m2v.DO_LOG = false;

    /**
     * @method setLogging enables or disables MEI2VF logging
     * @param {Boolean} value
     */
    m2v.setLogging = function(value) {
      m2v.DO_LOG = value;
    };

    /**
     * @method L the internal MEI2VF logging function. Passes the function
     * arguments to VexFlow's Vex.L function if {@link #DO_LOG} is `true`
     * @private
     */
    m2v.L = function() {
      if (m2v.DO_LOG)
        Vex.L("MEI2VF", arguments);
    };

    /**
     * @class MEI2VF.RUNTIME_ERROR
     * @private
     *
     * @constructor
     * @param {String} error_code
     * @param {String} message
     */
    m2v.RUNTIME_ERROR = function(error_code, message) {
      this.error_code = error_code;
      this.message = message;
    };

    /**
     * @method
     * @return {String} the string representation of the error
     */
    m2v.RUNTIME_ERROR.prototype.toString = function() {
      return "MEI2VF.RUNTIME_ERROR: " + this.error_code + ': ' + this.message;
    };

    return m2v;

  }(MEI2VF || {}, MeiLib, Vex.Flow, jQuery));
;/*
* Component of MEItoVexFlow Author: Raffaele Viglianti, 2012
*
* Copyright © 2012, 2013 Richard Lewis, Raffaele Viglianti, Zoltan Komives,
* University of Maryland
*
* Licensed under the Apache License, Version 2.0 (the "License"); you may
* not
* use this file except in compliance with the License. You may obtain a copy
* of the License at
*
* http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
* WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
* License for the specific language governing permissions and limitations
* under the License.
*/

/**
 * @class MEI2VF
 * @singleton
 * Tables for MEI <-> VexFlow values
 */
var MEI2VF = ( function(m2v, MeiLib, VF, $, undefined) {

    /**
     * @private
     * @property tables
     */
    m2v.tables = {

      accidentals : {
        'n' : 'n',
        'f' : 'b',
        's' : '#',
        'bb' : 'ff',
        'ss' : '##'
      },

      durations : {
        'long' : 'l',
        'breve' : 'd',
        '1' : 'w',
        '2' : 'h',
        '4' : 'q',
        '8' : '8',
        '16' : '16',
        '32' : '32',
        '64' : '64'
        // '128': '',
        // '256': '',
        // '512': '',
        // '1024': '',
        // '2048': '',
        // 'maxima': '',
        // 'longa': '',
        // 'brevis': '',
        // 'semibrevis': '',
        // 'minima': '',
        // 'semiminima': '',
        // 'fusa': '',
        // 'semifusa': ''
      },

      positions : {
        'above' : VF.Modifier.Position.ABOVE,
        'below' : VF.Modifier.Position.BELOW
      },

      hairpins : {
        'cres' : VF.StaveHairpin.type.CRESC,
        'dim' : VF.StaveHairpin.type.DECRESC
      },

      articulations : {
        'acc' : 'a>',
        'stacc' : 'a.',
        'ten' : 'a-',
        'stacciss' : 'av',
        'marc' : 'a^',
        // 'marc-stacc':
        // 'spicc':
        // 'doit':
        // 'rip':
        // 'plop':
        // 'fall':
        // 'bend':
        // 'flip':
        // 'smear':
        'dnbow' : 'am',
        'upbow' : 'a|',
        // 'harm':
        'snap' : 'ao',
        // 'fingernail':
        // 'ten-stacc':
        // 'damp':
        // 'dampall':
        // 'open':
        // 'stop':
        // 'dbltongue':
        // 'trpltongue':
        // 'heel':
        // 'toe':
        // 'tap':
        'lhpizz' : 'a+',
        'dot' : 'a.',
        'stroke' : 'a|'
      },
      
      fermata: {
        'above': 'a@a',
        'below': 'a@u'
      },

      barlines : {
        'single' : VF.Barline.type.SINGLE,
        'dbl' : VF.Barline.type.DOUBLE,
        'end' : VF.Barline.type.END,
        'rptstart' : VF.Barline.type.REPEAT_BEGIN,
        'rptend' : VF.Barline.type.REPEAT_END,
        'rptboth' : VF.Barline.type.REPEAT_BOTH,
        'invis' : VF.Barline.type.NONE
      }
    };

    return m2v;

  }(MEI2VF || {}, MeiLib, Vex.Flow, jQuery));
;/*
 * StaffInfo.js Author: Zoltan Komives (zolaemil@gmail.com) Created: 03.07.2013
 *
 * Copyright © 2012, 2013 Richard Lewis, Raffaele Viglianti, Zoltan Komives,
 * University of Maryland
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License. You may obtain a copy of
 * the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations under
 * the License.
 */

var MEI2VF = ( function(m2v, MeiLib, VF, $, undefined) {

    /**
     * @class MEI2VF.StaffInfo
     * Contains the definition and the rendering information (i.e. what
     * clef modifiers are to be rendered) of a single staff
     * @private
     *
     * @constructor
     * @param staffdef
     * @param scoredef
     * @param w_clef
     * @param w_keysig
     * @param w_timesig
     */
    m2v.StaffInfo = function(staffdef, scoredef, w_clef, w_keysig, w_timesig) {
      var me = this;
      me.scoreDefObj = scoredef ? m2v.Util.attsToObj(scoredef) : {};
      me.renderWith = {
        clef : w_clef,
        keysig : w_keysig,
        timesig : w_timesig
      };
      me.spacing = null;
      me.staffDefObj = m2v.Util.attsToObj(staffdef);
      me.updateMeter();
      me.updateStaveLabels();
      me.updateSpacing();
      me.currentClef = me.convertClef();
    };

    m2v.StaffInfo.prototype = {

      updateMeter : function() {
        var me = this;
        if (me.staffDefObj.hasOwnProperty('meter.count') && me.staffDefObj.hasOwnProperty('meter.unit')) {
          me.meter = {
            count : +me.staffDefObj['meter.count'],
            unit : +me.staffDefObj['meter.unit']
          };
        } else if (me.scoreDefObj.hasOwnProperty('meter.count') && me.scoreDefObj.hasOwnProperty('meter.unit')) {
          me.meter = {
            count : +me.scoreDefObj['meter.count'],
            unit : +me.scoreDefObj['meter.unit']
          };
        }
      },

      updateStaveLabels : function() {
        var me = this, label, labelAbbr;
        label = me.staffDefObj.label;
        if ( typeof label === 'string')
          me.label = label;
        labelAbbr = me.staffDefObj['label.abbr'];
        if ( typeof labelAbbr === 'string')
          me.labelAbbr = labelAbbr;
      },

      updateSpacing : function() {
        var me = this, spacing;
        spacing = +me.staffDefObj.spacing;
        if (!isNaN(spacing))
          me.spacing = spacing;
        return me.spacing;
      },

      forceSectionStartInfo : function() {
        var me = this;
        me.renderWith.clef = true;
        me.renderWith.keysig = true;
        me.renderWith.timesig = true;
      },

      forceStaveStartInfo : function() {
        var me = this;
        me.renderWith.clef = true;
        me.renderWith.keysig = true;
      },

      showClefCheck : function() {
        var me = this;
        if (me.renderWith.clef && me.staffDefObj['clef.visible'] !== 'false') {
          me.renderWith.clef = false;
          return true;
        }
      },

      showKeysigCheck : function() {
        var me = this;
        if (me.renderWith.keysig) {
          me.renderWith.keysig = false;
          if (me.staffDefObj['key.sig.show'] !== 'false')
            return true;
        }
      },

      showTimesigCheck : function() {
        var me = this;
        if (me.renderWith.timesig) {
          me.renderWith.timesig = false;
          if (me.staffDefObj['meter.rend'] === 'norm' || me.staffDefObj['meter.rend'] === undefined) {
            return true;
          }
        }
      },

      convertClef : function() {
        var me = this, clef_shape, clef_line, clef_dis, clef_dis_place;
        clef_shape = me.staffDefObj['clef.shape'];
        if (!clef_shape) {
          throw new m2v.RUNTIME_ERROR('MEI2VF.RERR.MissingAttribute', 'Attribute clef.shape is mandatory.');
        }
        clef_line = me.staffDefObj['clef.line'];
        clef_dis = me.staffDefObj['clef.dis'];
        clef_dis_place = me.staffDefObj['clef.dis.place'];
        if (clef_shape === 'G' && (!clef_line || clef_line === '2')) {
          if (clef_dis === '8' && clef_dis_place === 'below' && VF.clefProperties.values.octave != undefined) {
            return 'octave';
          }
          return 'treble';
        }
        if (clef_shape === 'F' && (!clef_line || clef_line === '4'))
          return 'bass';
        if (clef_shape === 'C' && clef_line === '3')
          return 'alto';
        if (clef_shape === 'C' && clef_line === '4')
          return 'tenor';
        throw new m2v.RUNTIME_ERROR('MEI2VF.RERR.NotSupported', 'Clef definition is not supported: [ clef.shape="' + clef_shape + '" ' + ( clef_line ? ('clef.line="' + clef_line + '"') : '') + ' ]');
      },

      getClef : function() {
        return this.currentClef;
      },

      getKeySpec : function() {
        var me = this, keyname, key_accid, key_mode;
        var keys = {
          '0': 'C',
          '1f': 'F',
          '2f': 'Bb',
          '3f': 'Eb',
          '4f': 'Ab',
          '5f': 'Db',
          '6f': 'Gb',
          '7f': 'Cb',
          '1s': 'G',
          '2s': 'D',
          '3s': 'A',
          '4s': 'E',
          '5s': 'B',
          '6s': 'F#',
          '7s': 'C#',
        }
        if (me.staffDefObj['key.sig'] !== undefined) {
          keysig = me.staffDefObj['key.sig'].toLowerCase();
          return keys[keysig];
        }
        else if (me.staffDefObj['key.pname'] !== undefined) {
          keyname = me.staffDefObj['key.pname'].toUpperCase();
          key_accid = me.staffDefObj['key.accid'];
          if (key_accid !== undefined) {
            switch (key_accid) {
              case 's' :
                keyname += '#';
                break;
              case 'f' :
                keyname += 'b';
                break;
              default :
                throw new m2v.RUNTIME_ERROR('MEI2VF.RERR.UnexpectedAttributeValue', "Value of key.accid must be 's' or 'f'");
            }
          }
          key_mode = me.staffDefObj['key.mode'];
          if (key_mode !== undefined)
            keyname += (key_mode === 'major') ? '' : 'm';
          return keyname;
        }
        // Fallback key
        return 'C';
      },

      /**
       * gets the vexFlow time signature from an MEI staffDef element
       *
       * @return {String} the vexFlow time signature or undefined
       */
      getTimeSig : function() {
        var me = this, symbol, count, unit;
        symbol = me.staffDefObj['meter.sym'];
        if (symbol) {
          return (symbol === 'cut') ? 'C|' : 'C';
        }
        count = me.meter.count;
        unit = me.meter.unit;
        return (count && unit) ? count + '/' + unit : undefined;
      },

      updateRenderWith : function(newStaffDef) {
        var me = this, result, hasEqualAtt;

        result = {
          clef : false,
          keysig : false,
          timesig : false
        };

        // if (Object.keys(newStaffDef).length === 0) {
        // return result;
        // }

        hasEqualAtt = function(attr_name) {
          return me.staffDefObj[attr_name] === newStaffDef[attr_name];
        };

        if (!hasEqualAtt('clef.shape') || !hasEqualAtt('clef.line')) {
          result.clef = true;
        }
        if ((!hasEqualAtt('key.pname') || !hasEqualAtt('key.accid') || !hasEqualAtt('key.mode'))) {
          result.keysig = true;
        }
        if (!hasEqualAtt('meter.count') || !hasEqualAtt('meter.unit')) {
          result.timesig = true;
        }

        me.renderWith = result;
      },

      updateDef : function(staffDef, scoreDef) {
        var me = this, newStaffDef;
        newStaffDef = m2v.Util.attsToObj(staffDef);
        me.updateRenderWith(newStaffDef);
        me.staffDefObj = newStaffDef;
        me.scoreDefObj = scoreDef ? m2v.Util.attsToObj(scoreDef) : {};
        me.updateMeter();
        me.updateStaveLabels();
        me.updateSpacing();
        me.currentClef = me.convertClef();
      }
    };

    return m2v;

  }(MEI2VF || {}, MeiLib, Vex.Flow, jQuery));
;/*
 * StaveConnector.js Author: Zoltan Komives (zolaemil@gmail.com) Created:
 * 24.07.2013
 *
 * Copyright © 2012, 2013 Richard Lewis, Raffaele Viglianti, Zoltan Komives,
 * University of Maryland
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License. You may obtain a copy of
 * the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations under
 * the License.
 */

var MEI2VF = ( function(m2v, MeiLib, VF, $, undefined) {

    /**
     * @class MEI2VF.Connectors
     * Handles stave connectors
     * @private
     *
     * @constructor
     * @param {Object} config the config object
     */
    m2v.Connectors = function(config) {
      var me = this;
      me.allVexConnectors = [];
      if (config) {
        me.init(config);
      }
    };

    m2v.Connectors.prototype = {

      vexTypes : {
        'line' : VF.StaveConnector.type.SINGLE_LEFT,
        'brace' : VF.StaveConnector.type.BRACE,
        'bracket' : VF.StaveConnector.type.BRACKET,
        'none' : null,
        'singleright' : VF.StaveConnector.type.SINGLE_RIGHT
      },

      vexTypesBarlineRight : {
        'single' : VF.StaveConnector.type.SINGLE_RIGHT,
        'dbl' : VF.StaveConnector.type.THIN_DOUBLE,
        'end' : VF.StaveConnector.type.BOLD_DOUBLE_RIGHT,
        'rptend' : VF.StaveConnector.type.BOLD_DOUBLE_RIGHT,
        'invis' : null
      },

      vexTypesBarlineLeft : {
        'single' : VF.StaveConnector.type.SINGLE_LEFT,
        'dbl' : VF.StaveConnector.type.THIN_DOUBLE,
        'end' : VF.StaveConnector.type.BOLD_DOUBLE_LEFT,
        'rptstart' : VF.StaveConnector.type.BOLD_DOUBLE_LEFT,
        'invis' : null
      },

      init : function(config) {
        var me = this, vexType, top_staff, bottom_staff, vexConnector, label, labelMode;
        var models = config.models;
        var staffs = config.staffs;
        var barline_l = config.barline_l;
        var barline_r = config.barline_r;
        var system_n = config.system_n;
        labelMode = config.labelMode;

        $.each(models, function() {

          vexType = (barline_r) ? me.vexTypesBarlineRight[barline_r] : me.vexTypes[this.symbol];
          top_staff = staffs[this.top_staff_n];
          bottom_staff = staffs[this.bottom_staff_n];

          if ( typeof vexType === 'number' && top_staff && bottom_staff) {
            vexConnector = new VF.StaveConnector(top_staff, bottom_staff);
            vexConnector.setType(vexType);
            me.allVexConnectors.push(vexConnector);
            if (labelMode === 'full') {
              label = (system_n === 1) ? this.label : this.labelAbbr;
            } else if (labelMode === 'abbr') {
              label = this.labelAbbr;
            }
            if (label)
              vexConnector.setText(label);
          }

          if (barline_l) {
            vexType = me.vexTypesBarlineLeft[barline_l];
            if ( typeof vexType === 'number' && top_staff && bottom_staff) {
              vexConnector = new VF.StaveConnector(top_staff, bottom_staff);
              vexConnector.setType(vexType);
              if (vexType === VF.StaveConnector.type.BOLD_DOUBLE_LEFT) {
                vexConnector.checkShift = true;
              }
              me.allVexConnectors.push(vexConnector);
            }
          }

        });
      },

      getAll : function() {
        return this.allVexConnectors;
      },

      setContext : function(ctx) {
        this.ctx = ctx;
        return this;
      },

      draw : function() {
        var me = this, i, j, conn, shift;
        for ( i = 0, j = me.allVexConnectors.length; i < j; i += 1) {
          conn = me.allVexConnectors[i];
          if (conn.checkShift) {
            shift = conn.top_stave.getModifierXShift();
            if (shift > 0) {
              conn.setXShift(shift);
            }
          }
          conn.setContext(me.ctx).draw();
        }
      }
    };

    return m2v;

  }(MEI2VF || {}, MeiLib, Vex.Flow, jQuery));
;/*
 * StaveVoices.js Author: Zoltan Komives (zolaemil@gmail.com) Created:
 * 25.07.2013
 *
 * Copyright © 2012, 2013 Richard Lewis, Raffaele Viglianti, Zoltan Komives,
 * University of Maryland
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License. You may obtain a copy of
 * the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations under
 * the License.
 */

var MEI2VF = ( function(m2v, MeiLib, VF, $, undefined) {

    /**
     * @class MEI2VF.StaffVoice
     * @private
     *
     * @constructor
     * @param {Object} voice
     * @param {Object} staff_n
     */
    m2v.StaffVoice = function(voice, staff_n) {
      this.voice = voice;
      this.staff_n = staff_n;
    };

    /**
     * @class MEI2VF.StaveVoices
     * Stores all voices in a given measure along with the respective staff id.
     * Passes all voices to Vex.Flow.Formatter and calls joinVoices, then draws
     * all voices.
     * @private
     *
     * @constructor
     */
    m2v.StaveVoices = function() {
      this.all_voices = [];
      this.formatter = new VF.Formatter();
    };

    m2v.StaveVoices.prototype = {
      addStaffVoice : function(staffVoice) {
        this.all_voices.push(staffVoice);
      },

      addVoice : function(voice, staff_n) {
        this.addStaffVoice(new m2v.StaffVoice(voice, staff_n));
      },

      reset : function() {
        this.all_voices = [];
      },

      preFormat : function() {
        var me = this, all, staff_n, i;
        all = me.all_voices;
        me.vexVoices = [];
        me.vexVoicesStaffWise = {};
        i = all.length;
        while (i--) {
          me.vexVoices.push(all[i].voice);
          staff_n = all[i].staff_n;
          if (me.vexVoicesStaffWise[staff_n]) {
            me.vexVoicesStaffWise[staff_n].push(all[i].voice);
          } else {
            me.vexVoicesStaffWise[staff_n] = [all[i].voice];
          }
        }
        me.formatter.preCalculateMinTotalWidth(me.vexVoices);
        return me.formatter.getMinTotalWidth();
      },

      /**
       *
       * @param {Object} staff a staff in the current measure used to set
       * the x dimensions of the voice
       */
      format : function(staff) {
        var me = this, i, f;
        f = me.formatter;
        for (i in me.vexVoicesStaffWise) {
          f.joinVoices(me.vexVoicesStaffWise[i], {align_rests: true});
        }
        f.formatToStave(me.vexVoices, staff);
      },

      draw : function(context, staves) {
        var i, staffVoice, all_voices = this.all_voices;
        for ( i = 0; i < all_voices.length; ++i) {
          staffVoice = all_voices[i];
          staffVoice.voice.draw(context, staves[staffVoice.staff_n]);
        }
      }
    };

    return m2v;

  }(MEI2VF || {}, MeiLib, Vex.Flow, jQuery));
;var MEI2VF = ( function(m2v, MeiLib, VF, $, undefined) {

    /**
     * A single instance of a staff system, containing and processing information
     * about the measures contained
     * @class MEI2VF.System
     * @private
     *
     * @constructor
     * @param {Object} config The configuration object
     */
    m2v.System = function(config) {
      this.init(config);
    };

    m2v.System.prototype = {

      /**
       * @property {Number} LABEL_PADDING the padding (in pixels) between the voice
       * labels and the staves
       */
      LABEL_PADDING : 20,

      /**
       * @param {Object} config The configuration object
       */
      init : function(config) {
        var me = this;

        /**
         * @cfg {Number|null} leftMar the left system margin as specified in the
         * MEI file or null if there is no margin specified. In the latter case,
         * the margin will be calculated on basis of the text width of the labels
         */
        me.leftMar = config.leftMar;
        /**
         * @cfg {Object} coords the coords of the current system
         * @cfg {Number} coords.x the x coordinate of the system
         * @cfg {Number} coords.y the y coordinate of the system
         * @cfg {Number} coords.w the system width
         */
        me.coords = config.coords;
        /**
         * @cfg {Number[]} staffYs the y coordinates of all staffs in the current
         * system
         */
        me.staffYs = config.staffYs;
        /**
         * @cfg {String[]} labels the labels of all staffs in the current system
         */
        me.labels = config.labels;
        /**
         * @property {MEI2VF.Measure[]} measures the measures in the current
         * system
         */
        me.measures = [];
      },

      /**
       * @return {Number[]} the value of {@link #staffYs}
       */
      getStaffYs : function() {
        return this.staffYs;
      },

      /**
       * adds a measure to the end of the measure array
       * @param {MEI2VF.Measure} measure the measure to add
       */
      addMeasure : function(measure) {
        this.measures.push(measure);
      },

      /**
       * gets a measure in the current system at the specified index
       * @param {Number} i the measure index (the first measure in the current
       * system has the index 0)
       * @return {MEI2VF.Measure}
       */
      getMeasure : function(i) {
        return this.measures[i];
      },

      /**
       * gets all measures in the current system
       * @return {MEI2VF.Measure[]}
       */
      getMeasures : function() {
        return this.measures;
      },

      /**
       * Calculates the system indent based on the width of the stave and
       * stave-connector labels
       * @param {Object} ctx the canvas context
       */
      calculateInitialIndent : function(ctx) {
        var me = this, label, max = 0, w, connectors, i, text;
        ctx.setFont('Times', 16);
        for (label in me.labels) {
          text = me.labels[label];
          if ( typeof text === 'string') {
            w = ctx.measureText(me.labels[label]).width;
            if (max < w) {
              max = w;
            }
          }
        }
        connectors = me.getMeasures()[0].startConnectors.getAll();
        i = connectors.length;
        while (i--) {
          text = connectors[i].text;
          if ( typeof text === 'string') {
            w = ctx.measureText(me.labels[label]).width;
            if (max < w) {
              max = w;
            }
          }
        }
        me.leftMar = (max === 0) ? 0 : max + me.LABEL_PADDING;
      },

      /**
       * Calculates the minimum width of each measure in the current system
       */
      calculateMeasureMinWidths : function() {
        var measures = this.measures, i = measures.length;
        while (i--) {
          measures[i].calculateMinWidth();
        }
      },

      /**
       * calculates the width of all measures in a stave which don't have a
       * specified width in the MEI code and writes them to their enclosing
       * measure object
       */
      calculateMissingMeasureWidths : function() {
        var me = this, i, j, totalSpecifiedMeasureWidth = 0, avaliableSingleWidth, nonSpecified_n = 0;
        for ( i = 0, j = me.measures.length; i < j; i += 1) {
          if (me.measures[i].meiW === null) {
            nonSpecified_n += 1;
            totalSpecifiedMeasureWidth += me.measures[i].getMinWidth();
          } else {
            totalSpecifiedMeasureWidth += me.measures[i].meiW;
          }
        }
        avaliableSingleWidth = Math.floor((me.coords.w - me.leftMar - totalSpecifiedMeasureWidth) / nonSpecified_n);
        for ( i = 0, j = me.measures.length; i < j; i += 1) {
          if (me.measures[i].meiW === null) {
            me.measures[i].w = avaliableSingleWidth + me.measures[i].getMinWidth();
          } else {
            me.measures[i].w = me.measures[i].meiW;
          }
        }
      },

      /**
       * formats the measures in the current system
       * @param {Object} ctx the canvas context
       * @return {MEI2VF.System} this
       */
      format : function(ctx) {
        var me = this, i, j, measures, offsetX, labels;
        if ( typeof me.leftMar !== 'number') {
          me.calculateInitialIndent(ctx);
        }
        me.calculateMeasureMinWidths();
        me.calculateMissingMeasureWidths();
        offsetX = me.coords.x + me.leftMar;
        measures = me.getMeasures();
        for ( i = 0, j = measures.length; i < j; i += 1) {
          if (measures[i]) {
            labels = (i === 0) ? me.labels : null;
            measures[i].format(offsetX, labels);
            offsetX += measures[i].w;
          }
          measures[i].addTempoToStaves();
        }
        return me;
      },

      /**
       * draws the current system to a canvas
       * @param {Object} ctx the canvas context
       */
      draw : function(ctx) {
        var me = this, i = me.measures.length;
        while (i--) {
          if (me.measures[i]) {
            me.measures[i].draw(ctx);
          }
        }
      }
    };

    return m2v;

  }(MEI2VF || {}, MeiLib, Vex.Flow, jQuery));
;var MEI2VF = ( function(m2v, MeiLib, VF, $, undefined) {

    /**
     * @class MEI2VF.SystemInfo
     * Deals with MEI data provided by scoreDef, staffDef and staffGrp elements and its children
     * @private
     *
     * @constructor

     */
    m2v.SystemInfo = function() {
      return;
    };

    m2v.SystemInfo.prototype = {

      STAVE_HEIGHT : 40,

      init : function(cfg, printSpace) {
        var me = this;
        me.cfg = cfg;
        me.printSpace = printSpace;

        /**
         * contains the current {@link MEI2VF.StaffInfo} objects
         */
        me.currentStaffInfos = [];
        /**
         * @property {Number} systemLeftMar the left margin of the
         * current system (additional to the left print space margin)
         */
        me.systemLeftMar = undefined;
        /**
         * @property {Number} currentLowestY the lowest Y coordinate of the
         * previously processed staffs
         */
        me.currentLowestY = 0;
        
        me.startConnectorInfos = {};
        me.inlineConnectorInfos = {}; 
        
      },

      setLeftMar : function(width) {
        this.systemLeftMar = width;
      },

      getLeftMar : function() {
        return this.systemLeftMar;
      },

      setModelForStaveRange : function(target, obj, add) {
        add = add || '';
        target[obj.top_staff_n + ':' + obj.bottom_staff_n + add] = obj;
      },

      /**
       * @method
       */
      setConnectorModels : function(staffGrp, range, isChild) {
        var me = this, symbol, barthru, first_n, last_n;

        first_n = range.first_n;
        last_n = range.last_n;
        symbol = $(staffGrp).attr('symbol');
        barthru = $(staffGrp).attr('barthru');

        m2v.L('Converter.setConnectorModels() {2}', 'symbol: ' + symbol, ' range.first_n: ' + first_n, ' range.last_n: ' + last_n);

        // 1. left connectors specified in the MEI file:
        me.setModelForStaveRange(me.startConnectorInfos, {
          top_staff_n : first_n,
          bottom_staff_n : last_n,
          symbol : symbol || 'line',
          label : $(staffGrp).attr('label'),
          labelAbbr : $(staffGrp).attr('label.abbr')
        });

        // 2. left auto line, only (if at all) attached to
        // //staffGrp[not(ancestor::staffGrp)]
        if (!isChild && me.cfg.autoStaveConnectorLine) {
          me.setModelForStaveRange(me.startConnectorInfos, {
            top_staff_n : first_n,
            bottom_staff_n : last_n,
            symbol : (symbol === 'none') ? 'none' : 'line'
          }, 'autoline');
        }

        // 3. inline connectors
        if (barthru === 'true') {
          me.setModelForStaveRange(me.inlineConnectorInfos, {
            top_staff_n : first_n,
            bottom_staff_n : last_n,
            symbol : 'singleright' // default
          });
        }
      },

      getStaffInfo : function(staff_n) {
        return this.currentStaffInfos[staff_n];
      },

      getAllStaffInfos : function() {
        return this.currentStaffInfos;
      },

      /**
       * @method
       */
      getClef : function(staff_n) {
        var me = this, staff_info;
        staff_info = me.currentStaffInfos[staff_n];
        if (!staff_info) {
          throw new m2v.RUNTIME_ERROR('MEI2VF.getClefForStaffNr():E01', 'No staff definition for staff n=' + staff_n);
        }
        return staff_info.getClef();
      },

      getCurrentLowestY : function() {
        return this.currentLowestY;
      },

      setCurrentLowestY : function(y) {
        this.currentLowestY = y;
      },

      getYs : function(currentSystemY) {
        var me = this, currentStaffY, i, j, isFirstStaff = true, infoSpacing, lowestYCandidate, ys = [];
        currentStaffY = 0;
        for ( i = 1, j = me.currentStaffInfos.length; i < j; i += 1) {
          if (me.currentStaffInfos[i]) {
            infoSpacing = me.currentStaffInfos[i].spacing;
            currentStaffY += (isFirstStaff) ? 0 : (infoSpacing !== null) ? me.STAVE_HEIGHT + me.currentStaffInfos[i].spacing : me.STAVE_HEIGHT + me.cfg.staveSpacing;
            ys[i] = currentSystemY + currentStaffY;
            isFirstStaff = false;
          }
        }
        lowestYCandidate = currentSystemY + currentStaffY + me.STAVE_HEIGHT;
        if (lowestYCandidate > me.currentLowestY)
          me.currentLowestY = lowestYCandidate;
        return ys;
      },

      forceSectionStartInfos : function() {
        var me = this, i = me.currentStaffInfos.length;
        while (i--) {
          if (me.currentStaffInfos[i])
            me.currentStaffInfos[i].forceSectionStartInfo();
        }
      },

      forceStaveStartInfos : function() {
        var me = this, i = me.currentStaffInfos.length;
        while (i--) {
          if (me.currentStaffInfos[i])
            me.currentStaffInfos[i].forceStaveStartInfo();
        }
      },

      /**
       *
       */
      processScoreDef : function(scoredef) {
        var me = this, i, j, children, systemLeftmar;
        me.scoreDefElement = scoredef;
        me.scoreDef = $(scoredef);
        systemLeftmar = me.scoreDef.attr('system.leftmar');
        if ( typeof systemLeftmar === 'string') {
          me.setLeftMar(+systemLeftmar);
        }
        children = me.scoreDef.children();
        for ( i = 0, j = children.length; i < j; i += 1) {
          me.processScoreDef_child(children[i]);
        }
      },

      /**
       * MEI element <b>scoreDef</b> may contain (MEI v2.1.0):
       * MEI.cmn: <b>meterSig</b> <b>meterSigGrp</b>
       * MEI.harmony: <b>chordTable</b> MEI.linkalign:
       * <b>timeline</b> MEI.midi: <b>instrGrp</b> MEI.shared:
       * <b>keySig</b> <b>pgFoot</b> <b>pgFoot2</b> <b>pgHead</b>
       * <b>pgHead2</b> <b>staffGrp</b> MEI.usersymbols:
       * <b>symbolTable</b>
       *
       * Supported elements: <b>staffGrp</b>
       *
       * @param {XMLElement} element the scoreDef element to process
       */
      processScoreDef_child : function(element) {
        var me = this;
        switch (element.localName) {
          case 'staffGrp' :
            me.processStaffGrp(element);
            break;
          case 'pgHead' :
            break;
          default :
            throw new m2v.RUNTIME_ERROR('MEI2VF.RERR.NotSupported', 'Element <' + element.localName + '> is not supported in <scoreDef>');
        }
      },


      /**
       *
       * @param {XMLElement} staffGrp
       * @param {Boolean} isChild specifies if the staffGrp is a child of another
       *            staffGrp (auto staff connectors only get attached
       *            to the outermost staffGrp elements)
       * @return {Object} the range of the current staff group. Properties:
       *         first_n, last_n
       */
      processStaffGrp : function(staffGrp, isChild) {
        var me = this, range = {};
        $(staffGrp).children().each(function(i, childElement) {
          var childRange = me.processStaffGrp_child(childElement);
          m2v.L('Converter.processStaffGrp() {1}.{a}', 'childRange.first_n: ' + childRange.first_n, ' childRange.last_n: ' + childRange.last_n);
          if (i === 0)
            range.first_n = childRange.first_n;
          range.last_n = childRange.last_n;
        });
        me.setConnectorModels(staffGrp, range, isChild);
        return range;
      },

      /**
       * MEI element <b>staffGrp</b> may contain (MEI v2.1.0): MEI.cmn: meterSig
       * meterSigGrp MEI.mensural: mensur proport MEI.midi: instrDef
       * MEI.shared: clef clefGrp keySig label layerDef
       *
       * Supported elements: <b>staffGrp</b> <b>staffDef</b>
       *
       * @param {XMLElement} element
       * @return {Object} the range of staffs. Properties: first_n, last_n
       */
      processStaffGrp_child : function(element) {
        var me = this, staff_n;
        switch (element.localName) {
          case 'staffDef' :
            staff_n = me.processStaffDef(element);
            return {
              first_n : staff_n,
              last_n : staff_n
            };
          case 'staffGrp' :
            return me.processStaffGrp(element, true);
          default :
            throw new m2v.RUNTIME_ERROR('MEI2VF.RERR.NotSupported', 'Element <' + element.localName + '> is not supported in <staffGrp>');
        }
      },

      /**
       * reads a staffDef, writes it to currentStaffInfos
       *
       * @param {XMLElement} staffDef
       * @return {Number} the staff number of the staffDef
       */
      processStaffDef : function(staffDef) {
        var me = this, staff_n, staff_info;
        staff_n = +$(staffDef).attr('n');
        staff_info = me.currentStaffInfos[staff_n];
        if (staff_info) {
          staff_info.updateDef(staffDef, me.scoreDefElement);
        } else {
          me.currentStaffInfos[staff_n] = new m2v.StaffInfo(staffDef, me.scoreDefElement, true, true, true);
        }
        return staff_n;
      }
    };

    return m2v;

  }(MEI2VF || {}, MeiLib, Vex.Flow, jQuery));
;
// Vex Flow Notation
// Implements key signatures
//
// Requires vex.js.

/**
 * @constructor
 */
Vex.Flow.KeySignature = ( function() {
  // ########### MODIFIED ############
    function KeySignature(keySpec, customPadding) {
      if (arguments.length > 0)
        this.init(keySpec, customPadding);
    }


    Vex.Inherit(KeySignature, Vex.Flow.StaveModifier, {
      // ########### MODIFIED ############
      init : function(key_spec, customPadding) {
        KeySignature.superclass.init();
        var padding = customPadding || 10;
        this.setPadding(padding);

        this.glyphFontScale = 38;
        // TODO(0xFE): Should this match StaveNote?
        this.accList = Vex.Flow.keySignature(key_spec);
      },

      addAccToStave : function(stave, acc) {
        var glyph = new Vex.Flow.Glyph(acc.glyphCode, this.glyphFontScale);
        this.placeGlyphOnLine(glyph, stave, acc.line);
        stave.addGlyph(glyph);
      },

      addModifier : function(stave) {
        this.convertAccLines(stave.clef, this.accList[0].glyphCode);
        for (var i = 0; i < this.accList.length; ++i) {
          this.addAccToStave(stave, this.accList[i]);
        }
      },

      addToStave : function(stave, firstGlyph) {
        if (this.accList.length === 0)
          return this;

        if (!firstGlyph) {
          stave.addGlyph(this.makeSpacer(this.padding));
        }

        this.addModifier(stave);
        return this;
      },

      convertAccLines : function(clef, code) {
        var offset = 0.0;
        // if clef === "treble"
        var tenorSharps;
        var isTenorSharps = ((clef === "tenor") && (code === "v18")) ? true : false;

        switch (clef) {
          case "bass":
            offset = 1;
            break;
          case "alto":
            offset = 0.5;
            break;
          case "tenor":
            if (!isTenorSharps) {
              offset = -0.5;
            }
            break;
        }

        // Special-case for TenorSharps
        var i;
        if (isTenorSharps) {
          tenorSharps = [3, 1, 2.5, 0.5, 2, 0, 1.5];
          for ( i = 0; i < this.accList.length; ++i) {
            this.accList[i].line = tenorSharps[i];
          }
        } else {
          if (clef != "treble") {
            for ( i = 0; i < this.accList.length; ++i) {
              this.accList[i].line += offset;
            }
          }
        }
      }
    });

    return KeySignature;
  }());

/**
 * Create hyphens between the specified annotations.
 *
 * @constructor
 */
Vex.Flow.Hyphen = ( function() {
    function Hyphen(config) {
      if (arguments.length > 0)
        this.init(config);
    };

    Hyphen.prototype = {
      init : function(config) {
        /**
         * config is a struct that has:
         *
         *  {
         *    first_annot: Annotation or any other object with an x (and optional
         * y) property,
         *    last_annot: Annotation or any other object with an x (and optional
         * y) property,
         *    NOTE: either first_annot or last_annot must have an y property
         *    (optional) max_hyphen_distance: the maximum distance between two
         * hyphens
         *    (optional) hyphen_width: the width of the hyphen character to draw
         *  }
         *
         **/

        this.max_hyphen_distance = config.max_hyphen_distance || 75;
        this.font = {
          family : "Arial",
          size : 10,
          style : ""
        };

        this.config = config;
        this.context = null;

      },

      setContext : function(context) {
        this.context = context;
        return this;
      },

      setFont : function(font) {
        this.font = font;
        return this;
      },

      renderHyphen : function() {
        var cfg = this.config;
        var ctx = this.context;
        var hyphen_width = cfg.hyphen_width || ctx.measureText('-').width;

        var first = cfg.first_annot;
        var last = cfg.last_annot;

        var start_x = (first.text) ? first.x + first.text_width : first.x;
        var end_x = last.x;

        var distance = end_x - start_x;

        if (distance > hyphen_width) {
          var y = (first.y && last.y) ? (first.y + last.y) / 2 : first.y || last.y;
          var hyphen_count = Math.ceil(distance / this.max_hyphen_distance);
          var single_width = distance / (hyphen_count + 1);
          while (hyphen_count--) {
            start_x += single_width;
            ctx.fillText('-', start_x - hyphen_width / 2, y);
          }
        };
      },

      draw : function() {
        if (!this.context)
          throw new Vex.RERR("NoContext", "No context to render hyphens.");
        var ctx = this.context;
        ctx.save();
        ctx.setFont(this.font.family, this.font.size, this.font.style);
        this.renderHyphen();
        ctx.restore();
        return true;
      }
    };

    return Hyphen;
  }());

//fallback: remove when the CMN breve (double whole) is implemented in VexFlow
if (!Vex.Flow.durationToTicks.durations['d']) {
  Vex.Flow.durationToTicks.durations['d'] = Vex.Flow.RESOLUTION / 0.5;
}
// fallback: remove when the CMN breve (double whole) is implemented in VexFlow
if (!Vex.Flow.durationToGlyph.duration_codes['d']) {
  Vex.Flow.durationToGlyph.duration_codes['d'] = {
    common : {
      head_width : 20,
      stem : false,
      stem_offset : 0,
      flag : false,
      dot_shiftY : 0,
      line_above : 0,
      line_below : 0
    },
    type : {
      "n" : {// Breve note
        code_head : "noteheadDoubleWholeSquare"
      },
      "h" : {// Whole note harmonic
        code_head : "v46"
      },
      "m" : {// Whole note muted
        code_head : "v92",
        stem_offset : -3
      },
      "r" : {// Breve rest
        code_head : "restDoubleWhole",
        head_width : 12,
        rest : true,
        position : "D/5",
        dot_shiftY : 0.5
      },
      "s" : {// Whole note slash
        // Drawn with canvas primitives
        head_width : 15,
        position : "B/4"
      }
    }
  };
}

//fallback: remove when the CMN long is implemented in VexFlow
if (!Vex.Flow.durationToTicks.durations['l']) {
  Vex.Flow.durationToTicks.durations['l'] = Vex.Flow.RESOLUTION / 0.25;
}

// fallback: remove when the CMN long is implemented in VexFlow
if (!Vex.Flow.durationToGlyph.duration_codes['l']) {
  Vex.Flow.durationToGlyph.duration_codes['l'] = {
    common : {
      head_width : 20,
      stem : false,
      stem_offset : 0,
      flag : false,
      dot_shiftY : 0,
      line_above : 0,
      line_below : 0
    },
    type : {
      "n" : {// Breve note
        code_head : "noteheadQuadWholeSquare"
      },
      "h" : {// Whole note harmonic
        code_head : "v46"
      },
      "m" : {// Whole note muted
        code_head : "v92",
        stem_offset : -3
      },
      "r" : {// Breve rest
        code_head : "restDoubleWhole",
        head_width : 12,
        rest : true,
        position : "D/5",
        dot_shiftY : 0.5
      },
      "s" : {// Whole note slash
        // Drawn with canvas primitives
        head_width : 15,
        position : "B/4"
      }
    }
  };
}

// Bravura glyphs
Vex.Flow.Font.glyphs["gClef"] = {
  "x_min" : 0,
  "x_max" : 948,
  "ha" : 944,
  "o" : "0 0 117 0 1 1 560 560 1 -1 0 -1120 m 948 35 l 948 15 b 693 -328 948 -141 850 -269 b 728 -536 711 -454 728 -536 b 736 -633 734 -571 736 -603 b 489 -920 736 -853 588 -914 b 456 -921 477 -920 466 -921 b 190 -700 225 -921 190 -777 b 196 -650 190 -671 195 -650 b 323 -532 204 -587 259 -536 l 333 -532 b 476 -665 409 -532 469 -592 l 476 -675 b 378 -806 476 -738 435 -788 b 343 -815 365 -812 356 -812 b 330 -826 336 -818 330 -820 b 343 -841 330 -830 335 -836 b 459 -869 372 -862 412 -869 l 486 -869 b 673 -638 503 -869 673 -867 b 665 -543 673 -610 671 -578 l 633 -347 l 626 -347 b 531 -353 595 -351 563 -353 b 10 94 301 -353 36 -245 b 8 136 8 108 8 122 b 445 788 8 406 239 612 l 428 876 b 419 1019 421 925 419 973 b 645 1543 419 1273 511 1484 b 750 1410 645 1543 696 1534 b 811 1141 790 1319 811 1229 b 528 594 811 951 715 767 b 573 354 542 518 557 445 b 591 357 578 357 585 357 l 606 357 b 948 35 785 357 937 216 m 655 1320 b 477 948 545 1315 477 1092 b 480 897 477 930 477 913 b 491 829 480 889 486 862 b 745 1177 641 942 728 1061 b 748 1208 746 1189 748 1198 b 655 1320 748 1284 701 1320 m 120 22 l 120 11 b 531 -302 129 -234 378 -302 b 623 -291 570 -302 602 -298 l 547 157 b 382 -3 455 141 382 95 l 382 -17 b 476 -155 385 -74 448 -143 b 497 -181 487 -161 497 -172 b 480 -192 497 -186 491 -192 b 451 -186 473 -192 463 -190 b 300 0 385 -165 322 -95 b 291 62 294 20 291 41 b 517 344 291 188 391 307 l 482 563 b 120 22 298 427 120 256 m 683 -276 b 833 -64 781 -234 833 -162 l 833 -49 b 609 162 827 69 727 162 l 603 162 b 683 -276 633 4 661 -148 "
};

Vex.Flow.Font.glyphs["gClef8vb"] = {
  "x_min" : 0,
  "x_max" : 937,
  "ha" : 930,
  "o" : "0 0 117 0 1 1 560 560 1 -1 0 -1120 m 937 46 l 937 24 b 685 -316 937 -130 839 -256 b 717 -521 704 -441 717 -521 b 727 -622 724 -557 727 -591 b 533 -896 727 -799 624 -872 b 588 -963 563 -906 588 -928 b 546 -1030 588 -1008 559 -1016 b 535 -1049 538 -1036 535 -1042 b 540 -1070 535 -1054 538 -1061 b 553 -1116 549 -1085 553 -1100 b 493 -1203 553 -1154 531 -1189 b 435 -1211 473 -1211 455 -1211 b 315 -1133 391 -1211 328 -1183 b 314 -1120 314 -1128 314 -1124 b 382 -1030 314 -1082 349 -1040 b 391 -1023 388 -1029 391 -1026 b 388 -1016 391 -1021 389 -1018 b 365 -963 372 -1000 365 -981 b 396 -903 365 -941 377 -918 b 185 -680 213 -879 185 -750 b 190 -634 185 -652 189 -634 b 319 -518 200 -570 252 -521 l 329 -518 b 468 -650 402 -518 462 -578 l 468 -657 b 371 -790 468 -720 428 -770 b 337 -799 360 -797 350 -797 b 326 -809 330 -801 326 -805 b 337 -825 326 -813 329 -818 b 454 -853 367 -846 407 -853 l 476 -853 b 665 -620 493 -853 665 -850 b 657 -526 665 -592 662 -561 l 626 -336 l 617 -336 b 531 -342 589 -339 560 -342 b 7 102 301 -342 35 -237 b 6 144 6 116 6 130 b 435 792 6 414 234 617 l 423 881 b 413 1025 416 930 413 979 b 637 1541 413 1275 501 1483 b 741 1411 637 1541 689 1532 b 801 1142 780 1320 801 1231 b 522 599 801 953 707 773 b 566 363 533 524 550 452 b 585 365 571 365 577 365 l 601 365 b 937 46 777 365 927 225 m 435 -1196 b 484 -1148 462 -1196 484 -1170 b 482 -1130 484 -1142 484 -1135 b 447 -1082 473 -1110 462 -1095 b 426 -1064 440 -1075 430 -1070 b 406 -1053 420 -1061 413 -1053 b 385 -1064 396 -1053 391 -1061 b 379 -1075 382 -1067 379 -1070 b 364 -1117 370 -1085 364 -1102 b 365 -1127 364 -1120 365 -1124 b 435 -1196 374 -1170 409 -1196 m 540 -966 l 540 -956 b 528 -925 540 -944 535 -930 b 473 -903 514 -911 493 -903 b 430 -937 452 -906 433 -914 b 455 -983 430 -956 442 -970 b 490 -1014 465 -993 476 -1005 b 508 -1021 497 -1018 503 -1021 b 540 -966 531 -1021 538 -986 m 648 1322 b 468 946 538 1315 468 1089 b 470 902 468 930 469 916 b 484 833 470 893 476 867 b 736 1179 634 946 717 1063 b 738 1208 738 1189 738 1198 b 648 1322 738 1284 694 1322 m 116 35 l 116 21 b 522 -290 123 -223 370 -290 b 615 -279 561 -290 594 -286 l 540 165 b 375 8 447 150 375 104 l 375 -6 b 468 -143 379 -62 440 -132 b 489 -168 480 -148 489 -160 b 470 -179 489 -175 483 -179 b 442 -175 463 -179 454 -178 b 293 11 379 -153 315 -83 b 286 70 288 31 286 50 b 508 351 286 195 382 315 l 473 568 b 116 35 293 437 116 266 m 675 -262 b 822 -52 770 -221 822 -150 l 822 -36 b 602 171 816 80 717 171 l 596 171 b 675 -262 626 14 652 -137 "
};
Vex.Flow.Font.glyphs["noteheadDoubleWholeSquare"] = {
  "x_min" : 0,
  "x_max" : 746,
  "ha" : 746,
  "o" : "0 0 117 0 1 1 560 560 1 -1 0 -1120 m 724 350 b 746 328 736 350 746 340 l 746 -328 b 724 -350 746 -339 736 -350 b 701 -328 711 -350 701 -339 l 701 -270 b 659 -234 701 -253 683 -234 l 83 -234 b 45 -276 67 -234 45 -256 l 45 -328 b 22 -350 45 -339 35 -350 b 0 -328 10 -350 0 -339 l 0 328 b 22 350 0 340 10 350 b 45 328 35 350 45 340 l 45 260 b 77 218 45 260 64 218 l 659 218 b 701 265 679 218 701 232 l 701 328 b 724 350 701 340 711 350 m 45 18 l 45 -36 b 146 -94 45 -70 83 -94 l 606 -94 b 701 -36 664 -94 701 -77 l 701 28 b 606 78 701 57 664 78 l 139 78 b 45 18 71 78 45 59 "
};
// NOT PART OF BRAVURA:
Vex.Flow.Font.glyphs["noteheadQuadWholeSquare"] = {
  "x_min" : 0,
  "x_max" : 746,
  "ha" : 746,
  // based on the Bravura breve glyph; CHANGES: all values < -1400
  "o" : "0 0 117 0 1 1 560 560 1 -1 0 -1120 " + "m 724 350 " + "b 746 328 736 350 746 340 " + "l 746 -1428 " + "b 724 -1450 746 -1439 736 -1450 " + "b 701 -1428 711 -1450 701 -1439 " + "l 701 -270 " + "b 659 -234 701 -253 683 -234 " + "l 83 -234 " + "b 45 -276 67 -234 45 -256 " + "l 45 -328 " + "b 22 -350 45 -339 35 -350 " + "b 0 -328 10 -350 0 -339 " + "l 0 328 " + "b 22 350 0 340 10 350 " + "b 45 328 35 350 45 340 " + "l 45 260 " + "b 77 218 45 260 64 218 " + "l 659 218 " + "b 701 265 679 218 701 232 " + "l 701 328 " + "b 724 350 701 340 711 350 " + "m 45 18 " + "l 45 -36 " + "b 146 -94 45 -70 83 -94 " + "l 606 -94 " + "b 701 -36 664 -94 701 -77 " + "l 701 28 " + "b 606 78 701 57 664 78 " + "l 139 78 " + "b 45 18 71 78 45 59 "
};
Vex.Flow.Font.glyphs["restDoubleWhole"] = {
  "x_min" : 0,
  "x_max" : 640,
  "ha" : 202,
  "o" : "0 0 133 0 1 1 640 640 2 -2 0 -1280 m 200 24 b 173 0 200 11 189 0 l 26 0 b 0 24 11 0 0 11 l 0 376 b 26 400 0 389 11 400 l 173 400 b 200 376 189 400 200 389 l 200 24 "
};

// fallback: remove when the octave g clef is implemented in VexFlow
Vex.Flow.clefProperties.values.octave = {
  line_shift : 3.5 // 0 for G clef pitches; 3.5 for transposed G clef pitches
};
// fallback: remove when the octave g clef is implemented in VexFlow
Vex.Flow.Clef.types.octave = {
  code : "gClef8vb", // v83: regular g clef
  point : 40, // 38
  line : 3
};
Vex.Flow.Clef.types.treble = {
  code : "gClef",
  point : 40,
  line : 3
};

Vex.Flow.Curve.prototype.renderCurve = function(params) {
  var ctx = this.context;
  var cps = this.render_options.cps;

  var x_shift = this.render_options.x_shift;
  var y_shift = this.render_options.y_shift * params.direction;

  // TODO name variables according to staveTie
  // ################# MODIFICATION (allows to specify y_shift for start & end
  // note separately):
  var y_shift_start = this.render_options.y_shift_start || 0;
  var y_shift_end = this.render_options.y_shift_end || 0;
  var first_x = params.first_x + x_shift;
  var first_y = params.first_y + y_shift + y_shift_start;
  var last_x = params.last_x - x_shift;
  var last_y = params.last_y + y_shift + y_shift_end;
  var thickness = this.render_options.thickness;

  var cp_spacing = (last_x - first_x) / (cps.length + 2);

  ctx.beginPath();
  ctx.moveTo(first_x, first_y);
  ctx.bezierCurveTo(first_x + cp_spacing + cps[0].x, first_y + (cps[0].y * params.direction), last_x - cp_spacing + cps[1].x, last_y + (cps[1].y * params.direction), last_x, last_y);
  ctx.bezierCurveTo(last_x - cp_spacing + cps[1].x, last_y + ((cps[1].y + thickness) * params.direction), first_x + cp_spacing + cps[0].x, first_y + ((cps[0].y + thickness) * params.direction), first_x, first_y);
  ctx.stroke();
  ctx.closePath();
  ctx.fill();
};

// [VexFlow](http://vexflow.com) - Copyright (c) Mohit Muthanna 2010.
//
// ## Description
//
// This file implements text annotations as modifiers that can be attached to
// notes.
//
// See `tests/annotation_tests.js` for usage examples.

Vex.Flow.Annotation = ( function() {
    function Annotation(text) {
      if (arguments.length > 0)
        this.init(text);
    }

    // To enable logging for this class. Set `Vex.Flow.Annotation.DEBUG` to
    // `true`.
    function L() {
      if (Annotation.DEBUG)
        Vex.L("Vex.Flow.Annotation", arguments);
    }

    // Text annotations can be positioned and justified relative to the note.
    Annotation.Justify = {
      LEFT : 1,
      CENTER : 2,
      RIGHT : 3,
      CENTER_STEM : 4
    };

    Annotation.VerticalJustify = {
      TOP : 1,
      CENTER : 2,
      BOTTOM : 3,
      CENTER_STEM : 4
    };

    Annotation.DEFAULT_FONT_SIZE = 10;

    // ## Prototype Methods
    //
    // Annotations inherit from `Modifier` and is positioned correctly when
    // in a `ModifierContext`.
    var Modifier = Vex.Flow.Modifier;
    Vex.Inherit(Annotation, Modifier, {
      // Create a new `Annotation` with the string `text`.
      init : function(text) {
        Annotation.superclass.init.call(this);

        this.note = null;
        this.index = null;
        this.text_line = 0;
        this.text = text;
        this.justification = Annotation.Justify.CENTER;
        this.vert_justification = Annotation.VerticalJustify.TOP;
        this.font = {
          family : "Arial",
          size : Annotation.DEFAULT_FONT_SIZE,
          weight : ""
        };

        // Line spacing, relative to font size
        this.line_spacing = 1.1; 

        // The default width is calculated from the text.
        this.setWidth(Vex.Flow.textWidth(text));
      },

      setLineSpacing : function(spacing) {
        this.line_spacing = spacing;
        return this;
      },

      // Return the modifier type. Used by the `ModifierContext` to calculate
      // layout.
      getCategory : function() {
        return "annotations";
      },

      // Set the vertical position of the text relative to the stave.
      setTextLine : function(line) {
        this.text_line = line;
        return this;
      },

      // Set font family, size, and weight. E.g., `Arial`, `10pt`, `Bold`.
      setFont : function(family, size, weight) {
        this.font = {
          family : family,
          size : size,
          weight : weight
        };
        return this;
      },

      // Set vertical position of text (above or below stave). `just` must be
      // a value in `Annotation.VerticalJustify`.
      setVerticalJustification : function(just) {
        this.vert_justification = just;
        return this;
      },

      // Get and set horizontal justification. `justification` is a value in
      // `Annotation.Justify`.
      getJustification : function() {
        return this.justification;
      },
      setJustification : function(justification) {
        this.justification = justification;
        return this;
      },

      // Render text beside the note.
      draw : function() {
        if (!this.context)
          throw new Vex.RERR("NoContext", "Can't draw text annotation without a context.");
        if (!this.note)
          throw new Vex.RERR("NoNoteForAnnotation", "Can't draw text annotation without an attached note.");

        var start = this.note.getModifierStartXY(Modifier.Position.ABOVE, this.index);

        // We're changing context parameters. Save current state.
        this.context.save();
        this.context.setFont(this.font.family, this.font.size, this.font.weight);
        var text_width = this.context.measureText(this.text).width;

        // Estimate text height to be the same as the width of an 'm'.
        //
        // This is a hack to work around the inability to measure text height
        // in HTML5 Canvas (and SVG).
        var text_height = this.context.measureText("M").width;
        var x, y;

        if (this.justification == Annotation.Justify.LEFT) {
          x = start.x;
        } else if (this.justification == Annotation.Justify.RIGHT) {
          x = start.x - text_width;
        } else if (this.justification == Annotation.Justify.CENTER) {
          x = start.x - text_width / 2;
        } else/* CENTER_STEM */
        {
          x = this.note.getStemX() - text_width / 2;
        }

        var stem_ext, spacing, font_scale;
        var has_stem = this.note.hasStem();
        var stave = this.note.getStave();

        // The position of the text varies based on whether or not the note
        // has a stem.
        if (has_stem) {
          stem_ext = this.note.getStemExtents();
          spacing = stave.getSpacingBetweenLines();
        }

        font_scale = this.font.size / Annotation.DEFAULT_FONT_SIZE * this.line_spacing;
        if (this.vert_justification == Annotation.VerticalJustify.BOTTOM) {
          y = stave.getYForBottomText(this.text_line, font_scale);
          if (has_stem) {
            var stem_base = (this.note.getStemDirection() === 1 ? stem_ext.baseY : stem_ext.topY);
            y = Math.max(y, stem_base + ( spacing * (this.text_line + 1) * font_scale + ( spacing * (this.text_line) ) ) );
          }
        } else if (this.vert_justification == Annotation.VerticalJustify.CENTER) {
          var yt = this.note.getYForTopText(this.text_line) - 1;
          var yb = stave.getYForBottomText(this.text_line);
          y = yt + (yb - yt ) / 2 + text_height / 2;
        } else if (this.vert_justification == Annotation.VerticalJustify.TOP) {
          y = Math.min(stave.getYForTopText(this.text_line), this.note.getYs()[0] - 10);
          if (has_stem) {
            y = Math.min(y, (stem_ext.topY - 5) - (spacing * this.text_line));
          }
        } else/* CENTER_STEM */
        {
          var extents = this.note.getStemExtents();
          y = extents.topY + (extents.baseY - extents.topY) / 2 + text_height / 2;
        }

        // ############# ADDITON #############
        this.x = x;
        this.y = y;
        this.text_height = text_height;
        this.text_width = text_width;

        L("Rendering annotation: ", this.text, x, y);
        this.context.fillText(this.text, x, y);
        this.context.restore();
      }
    });

    return Annotation;
  }());

// VexFlow - Music Engraving for HTML5
// Copyright Mohit Muthanna 2010
//
// This class implements varies types of ties between contiguous notes. The
// ties include: regular ties, hammer ons, pull offs, and slides.

/**
 * Create a new tie from the specified notes. The notes must
 * be part of the same line, and have the same duration (in ticks).
 *
 * @constructor
 * @param {!Object} context The canvas context.
 * @param {!Object} notes The notes to tie up.
 * @param {!Object} Options
 */
Vex.Flow.StaveTie = ( function() {
    function StaveTie(notes, text) {
      if (arguments.length > 0)
        this.init(notes, text);
    }


    StaveTie.prototype = {
      init : function(notes, text) {
        /**
         * Notes is a struct that has:
         *
         *  {
         *    first_note: Note,
         *    last_note: Note,
         *    first_indices: [n1, n2, n3],
         *    last_indices: [n1, n2, n3]
         *  }
         *
         **/
        this.notes = notes;
        this.context = null;
        this.text = text;

        this.render_options = {
          cp1 : 8, // Curve control point 1
          cp2 : 12, // Curve control point 2
          text_shift_x : 0,
          first_x_shift : 0,
          last_x_shift : 0,
          y_shift : 7,
          tie_spacing : 0,
          font : {
            family : "Arial",
            size : 10,
            style : ""
          }
        };

        this.font = this.render_options.font;
        this.setNotes(notes);
      },

      setContext : function(context) {
        this.context = context;
        return this;
      },
      setFont : function(font) {
        this.font = font;
        return this;
      },

      /**
       * Set the notes to attach this tie to.
       *
       * @param {!Object} notes The notes to tie up.
       */
      setNotes : function(notes) {
        if (!notes.first_note && !notes.last_note)
          throw new Vex.RuntimeError("BadArguments", "Tie needs to have either first_note or last_note set.");

        if (!notes.first_indices)
          notes.first_indices = [0];
        if (!notes.last_indices)
          notes.last_indices = [0];

        if (notes.first_indices.length != notes.last_indices.length)
          throw new Vex.RuntimeError("BadArguments", "Tied notes must have similar" + " index sizes");

        // Success. Lets grab 'em notes.
        this.first_note = notes.first_note;
        this.first_indices = notes.first_indices;
        this.last_note = notes.last_note;
        this.last_indices = notes.last_indices;
        return this;
      },

      /**
       * @return {boolean} Returns true if this is a partial bar.
       */
      isPartial : function() {
        return (!this.first_note || !this.last_note);
      },

      // ADDITION:
      setDir : function(dir) {
        this.curvedir = dir;
      },

      getDir : function() {
        return this.curvedir;
      },

      renderTie : function(params) {
        if (params.first_ys.length === 0 || params.last_ys.length === 0)
          throw new Vex.RERR("BadArguments", "No Y-values to render");

        // ADDITION:
        if (this.curvedir) {
          params.direction = (this.curvedir === 'above') ? -1 : 1;
        } else {
          this.curvedir = params.direction;
        }

        var ctx = this.context;
        var cp1 = this.render_options.cp1;
        var cp2 = this.render_options.cp2;

        if (Math.abs(params.last_x_px - params.first_x_px) < 10) {
          cp1 = 2;
          cp2 = 8;
        }

        var first_x_shift = this.render_options.first_x_shift;
        var last_x_shift = this.render_options.last_x_shift;
        var y_shift = this.render_options.y_shift * params.direction;

        for (var i = 0; i < this.first_indices.length; ++i) {
          var cp_x = ((params.last_x_px + last_x_shift) + (params.first_x_px + first_x_shift)) / 2;
          var first_y_px = params.first_ys[this.first_indices[i]] + y_shift;
          var last_y_px = params.last_ys[this.last_indices[i]] + y_shift;

          if (isNaN(first_y_px) || isNaN(last_y_px))
            throw new Vex.RERR("BadArguments", "Bad indices for tie rendering.");

          var top_cp_y = ((first_y_px + last_y_px) / 2) + (cp1 * params.direction);
          var bottom_cp_y = ((first_y_px + last_y_px) / 2) + (cp2 * params.direction);

          ctx.beginPath();
          ctx.moveTo(params.first_x_px + first_x_shift, first_y_px);
          ctx.quadraticCurveTo(cp_x, top_cp_y, params.last_x_px + last_x_shift, last_y_px);
          ctx.quadraticCurveTo(cp_x, bottom_cp_y, params.first_x_px + first_x_shift, first_y_px);

          ctx.closePath();
          ctx.fill();
        }
      },

      renderText : function(first_x_px, last_x_px) {
        if (!this.text)
          return;
        var center_x = (first_x_px + last_x_px) / 2;
        center_x -= this.context.measureText(this.text).width / 2;

        this.context.save();
        this.context.setFont(this.font.family, this.font.size, this.font.style);
        this.context.fillText(this.text, center_x + this.render_options.text_shift_x, (this.first_note || this.last_note).getStave().getYForTopText() - 1);
        this.context.restore();
      },

      draw : function() {
        if (!this.context)
          throw new Vex.RERR("NoContext", "No context to render tie.");
        var first_note = this.first_note;
        var last_note = this.last_note;
        var first_x_px, last_x_px, first_ys, last_ys, stem_direction;

        if (first_note) {
          first_x_px = first_note.getTieRightX() + this.render_options.tie_spacing;
          stem_direction = first_note.getStemDirection();
          first_ys = first_note.getYs();
        } else {
          first_x_px = last_note.getStave().getTieStartX();
          first_ys = last_note.getYs();
          this.first_indices = this.last_indices;
        }

        if (last_note) {
          last_x_px = last_note.getTieLeftX() + this.render_options.tie_spacing;
          stem_direction = last_note.getStemDirection();
          last_ys = last_note.getYs();
        } else {
          last_x_px = first_note.getStave().getTieEndX();
          last_ys = first_note.getYs();
          this.last_indices = this.first_indices;
        }

        this.renderTie({
          first_x_px : first_x_px,
          last_x_px : last_x_px,
          first_ys : first_ys,
          last_ys : last_ys,
          direction : stem_direction
        });

        this.renderText(first_x_px, last_x_px);
        return true;
      }
    };

    return StaveTie;
  }());

// Vex Flow
// Mohit Muthanna <mohit@muthanna.com>
//
// Copyright Mohit Cheppudira 2010

/** @constructor */
Vex.Flow.Stave = (function() {
  function Stave(x, y, width, options) {
    if (arguments.length > 0) this.init(x, y, width, options);
  }

  var THICKNESS = (Vex.Flow.STAVE_LINE_THICKNESS > 1 ?
        Vex.Flow.STAVE_LINE_THICKNESS : 0);
  Stave.prototype = {
    init: function(x, y, width, options) {
      this.x = x;
      this.y = y;
      this.width = width;
      this.start_x = this.getGlyphStartX();
      this.end_x = this.getGlyphEndX();
      this.context = null;
      this.glyphs = [];
      this.end_glyphs = [];
      this.modifiers = [];  // non-glyph stave items (barlines, coda, segno, etc.)
      this.measure = 0;
      this.clef = "treble";
      this.font = {
        family: "sans-serif",
        size: 8,
        weight: ""
      };
      this.options = {
        vertical_bar_width: 10,       // Width around vertical bar end-marker
        glyph_spacing_px: 10,
        num_lines: 5,
        fill_style: "#999999",
        spacing_between_lines_px: 10, // in pixels
        space_above_staff_ln: 4,      // in staff lines
        space_below_staff_ln: 4,      // in staff lines
        top_text_position: 1          // in staff lines
      };
      this.bounds = {x: this.x, y: this.y, w: this.width, h: 0};
      Vex.Merge(this.options, options);

      this.resetLines();

      this.modifiers.push(
          new Vex.Flow.Barline(Vex.Flow.Barline.type.SINGLE, this.x)); // beg bar
      this.modifiers.push(
          new Vex.Flow.Barline(Vex.Flow.Barline.type.SINGLE,
          this.x + this.width)); // end bar
    },

    getGlyphStartX: function() {
      return this.x + 5;
    },

    getGlyphEndX: function() {
      return this.x + this.width;
    },

    resetLines: function() {
      this.options.line_config = [];
      for (var i = 0; i < this.options.num_lines; i++) {
        this.options.line_config.push({visible: true});
      }
      this.height = (this.options.num_lines + this.options.space_above_staff_ln) *
         this.options.spacing_between_lines_px;
      this.options.bottom_text_position = this.options.num_lines + 1;
    },

    setNoteStartX: function(x) { this.start_x = x; return this; },
    getNoteStartX: function() {
      var start_x = this.start_x;

      // Add additional space if left barline is REPEAT_BEGIN and there are other
      // start modifiers than barlines
      if (this.modifiers[0].barline == Vex.Flow.Barline.type.REPEAT_BEGIN &&
          this.modifiers.length > 2)
        start_x += 20;
      return start_x;
    },

    getNoteEndX: function() { return this.end_x; },
    getTieStartX: function() { return this.start_x; },
    getTieEndX: function() { return this.x + this.width; },
    setContext: function(context) { this.context = context; return this; },
    getContext: function() { return this.context; },

    setX: function(x) {
      var i;
      var dx = (typeof this.x == "number") ? x - this.x : 0;
      console.log('dx: ' + dx.toString());
      this.x = x;
      this.bounds.x = x;
      this.start_x += dx;
      for (i = 0; i < this.modifiers.length; i++) {
        this.modifiers[i].x = x;
      }
      return this;
    },

    getX: function() { return this.x; },
    getNumLines: function() { return this.options.num_lines; },
    setNumLines: function(lines) {
      this.options.num_lines = parseInt(lines, 10);
      this.resetLines();
      return this;
    },
    setY: function(y) { this.y = y; return this; },

    setWidth: function(width) {
      this.width = width;
      this.end_x = this.getGlyphEndX();

      // reset the x position of the end barline
      this.modifiers[1].setX(this.end_x);
      return this;
    },

    getWidth: function() {
      return this.width;
    },

    setMeasure: function(measure) { this.measure = measure; return this; },

      // Bar Line functions
    setBegBarType: function(type) {
      // Only valid bar types at beginning of stave is none, single or begin repeat
      if (type == Vex.Flow.Barline.type.SINGLE ||
          type == Vex.Flow.Barline.type.REPEAT_BEGIN ||
          type == Vex.Flow.Barline.type.NONE) {
          this.modifiers[0] = new Vex.Flow.Barline(type, this.x);
      }
      return this;
    },

    setEndBarType: function(type) {
      // Repeat end not valid at end of stave
      if (type != Vex.Flow.Barline.type.REPEAT_BEGIN)
        this.modifiers[1] = new Vex.Flow.Barline(type, this.x + this.width);
      return this;
    },

    /**
     * Gets the pixels to shift from the beginning of the stave
     * following the modifier at the provided index
     * @param  {Number} index The index from which to determine the shift
     * @return {Number}       The amount of pixels shifted
     */
    getModifierXShift: function(index) {
      if (typeof index === 'undefined') index = this.glyphs.length -1;
      if (typeof index !== 'number') new Vex.RERR("InvalidIndex",
        "Must be of number type");

      var x = this.getGlyphStartX();
      var bar_x_shift = 0;

      for (var i = 0; i < index + 1; ++i) {
        var glyph = this.glyphs[i];
        x += glyph.getMetrics().width;
        bar_x_shift += glyph.getMetrics().width;
      }

      // Add padding after clef, time sig, key sig
      if (bar_x_shift > 0) bar_x_shift += this.options.vertical_bar_width + 10;

      return bar_x_shift;
    },

    // Coda & Segno Symbol functions
    setRepetitionTypeLeft: function(type, y) {
      this.modifiers.push(new Vex.Flow.Repetition(type, this.x, y));
      return this;
    },

    setRepetitionTypeRight: function(type, y) {
      this.modifiers.push(new Vex.Flow.Repetition(type, this.x, y) );
      return this;
    },

    // Volta functions
    setVoltaType: function(type, number_t, y) {
      this.modifiers.push(new Vex.Flow.Volta(type, number_t, this.x, y));
      return this;
    },

    // Section functions
    setSection: function(section, y) {
      this.modifiers.push(new Vex.Flow.StaveSection(section, this.x, y));
      return this;
    },

    // Tempo functions
    setTempo: function(tempo, y) {
      this.modifiers.push(new Vex.Flow.StaveTempo(tempo, this.x, y));
      return this;
    },

    // Text functions
    setText: function(text, position, options) {
      this.modifiers.push(new Vex.Flow.StaveText(text, position, options));
      return this;
    },

    getHeight: function() {
      return this.height;
    },

    getSpacingBetweenLines: function() {
      return this.options.spacing_between_lines_px;
    },

    getBoundingBox: function() {
      return new Vex.Flow.BoundingBox(this.x, this.y, this.width, this.getBottomY() - this.y);
      // body...
    },

    getBottomY: function() {
      var options = this.options;
      var spacing = options.spacing_between_lines_px;
      var score_bottom = this.getYForLine(options.num_lines) +
         (options.space_below_staff_ln * spacing);

      return score_bottom;
    },

    getBottomLineY: function() {
      return this.getYForLine(this.options.num_lines);
    },

    getYForLine: function(line) {
      var options = this.options;
      var spacing = options.spacing_between_lines_px;
      var headroom = options.space_above_staff_ln;

      var y = this.y + ((line * spacing) + (headroom * spacing)) -
        (THICKNESS / 2);

      return y;
    },

    getYForTopText: function(line, font_scale) {
      var l = line || 0;
      var scale = font_scale || 1;
      return this.getYForLine(-(l * scale) - this.options.top_text_position);
    },

    getYForBottomText: function(line, font_scale) {
      var l = line || 0;
      var scale = font_scale || 1;
      return this.getYForLine(this.options.bottom_text_position + (l * scale));
    },

    getYForNote: function(line) {
      var options = this.options;
      var spacing = options.spacing_between_lines_px;
      var headroom = options.space_above_staff_ln;
      var y = this.y + (headroom * spacing) + (5 * spacing) - (line * spacing);

      return y;
    },

    getYForGlyphs: function() {
      return this.getYForLine(3);
    },

    addGlyph: function(glyph) {
      glyph.setStave(this);
      this.glyphs.push(glyph);
      this.start_x += glyph.getMetrics().width;
      return this;
    },

    addEndGlyph: function(glyph) {
      glyph.setStave(this);
      this.end_glyphs.push(glyph);
      this.end_x -= glyph.getMetrics().width;
      return this;
    },

    addModifier: function(modifier) {
      this.modifiers.push(modifier);
      modifier.addToStave(this, (this.glyphs.length === 0));
      return this;
    },

    addEndModifier: function(modifier) {
      this.modifiers.push(modifier);
      modifier.addToStaveEnd(this, (this.end_glyphs.length === 0));
      return this;
    },

    addKeySignature: function(keySpec) {
      this.addModifier(new Vex.Flow.KeySignature(keySpec));
      return this;
    },

    addClef: function(clef) {
      this.clef = clef;
      this.addModifier(new Vex.Flow.Clef(clef));
      return this;
    },

    addEndClef: function(clef) {
      this.addEndModifier(new Vex.Flow.Clef(clef));
      return this;
    },

    addTimeSignature: function(timeSpec, customPadding) {
      this.addModifier(new Vex.Flow.TimeSignature(timeSpec, customPadding));
      return this;
    },

    addEndTimeSignature: function(timeSpec, customPadding) {
      this.addEndModifier(new Vex.Flow.TimeSignature(timeSpec, customPadding));
    },

    addTrebleGlyph: function() {
      this.clef = "treble";
      this.addGlyph(new Vex.Flow.Glyph("v83", 40));
      return this;
    },

    /**
     * All drawing functions below need the context to be set.
     */
    draw: function() {
      if (!this.context) throw new Vex.RERR("NoCanvasContext",
          "Can't draw stave without canvas context.");

      var num_lines = this.options.num_lines;
      var width = this.width;
      var x = this.x;
      var y;
      var glyph;

      // Render lines
      for (var line=0; line < num_lines; line++) {
        y = this.getYForLine(line);

        this.context.save();
        this.context.setFillStyle(this.options.fill_style);
        this.context.setStrokeStyle(this.options.fill_style);
        if (this.options.line_config[line].visible) {
          this.context.fillRect(x, y, width, Vex.Flow.STAVE_LINE_THICKNESS);
        }
        this.context.restore();
      }

      // Render glyphs
      x = this.getGlyphStartX();
      for (var i = 0; i < this.glyphs.length; ++i) {
        glyph = this.glyphs[i];
        if (!glyph.getContext()) {
          glyph.setContext(this.context);
        }
        glyph.renderToStave(x);
        x += glyph.getMetrics().width;
      }

      // Render end glyphs
      x = this.getGlyphEndX();
      for (i = 0; i < this.end_glyphs.length; ++i) {
        glyph = this.end_glyphs[i];
        if (!glyph.getContext()) {
          glyph.setContext(this.context);
        }
        x -= glyph.getMetrics().width;
        glyph.renderToStave(x);
      }

      // Draw the modifiers (bar lines, coda, segno, repeat brackets, etc.)
      for (i = 0; i < this.modifiers.length; i++) {
        // Only draw modifier if it has a draw function
        if (typeof this.modifiers[i].draw == "function")
          this.modifiers[i].draw(this, this.getModifierXShift());
      }

      // Render measure numbers
      if (this.measure > 0) {
        this.context.save();
        this.context.setFont(this.font.family, this.font.size, this.font.weight);
        var text_width = this.context.measureText("" + this.measure).width;
        y = this.getYForTopText(0) + 3;
        this.context.fillText("" + this.measure, this.x - text_width / 2, y);
        this.context.restore();
      }

      return this;
    },

    // Draw Simple barlines for backward compatability
    // Do not delete - draws the beginning bar of the stave
    drawVertical: function(x, isDouble) {
      this.drawVerticalFixed(this.x + x, isDouble);
    },

    drawVerticalFixed: function(x, isDouble) {
      if (!this.context) throw new Vex.RERR("NoCanvasContext",
          "Can't draw stave without canvas context.");

      var top_line = this.getYForLine(0);
      var bottom_line = this.getYForLine(this.options.num_lines - 1);
      if (isDouble)
        this.context.fillRect(x - 3, top_line, 1, bottom_line - top_line + 1);
      this.context.fillRect(x, top_line, 1, bottom_line - top_line + 1);
    },

    drawVerticalBar: function(x) {
      this.drawVerticalBarFixed(this.x + x, false);
    },

    drawVerticalBarFixed: function(x) {
      if (!this.context) throw new Vex.RERR("NoCanvasContext",
          "Can't draw stave without canvas context.");

      var top_line = this.getYForLine(0);
      var bottom_line = this.getYForLine(this.options.num_lines - 1);
      this.context.fillRect(x, top_line, 1, bottom_line - top_line + 1);
    },

    /**
     * Get the current configuration for the Stave.
     * @return {Array} An array of configuration objects.
     */
    getConfigForLines: function() {
      return this.options.line_config;
    },

    /**
     * Configure properties of the lines in the Stave
     * @param line_number The index of the line to configure.
     * @param line_config An configuration object for the specified line.
     * @throws Vex.RERR "StaveConfigError" When the specified line number is out of
     *   range of the number of lines specified in the constructor.
     */
    setConfigForLine: function(line_number, line_config) {
      if (line_number >= this.options.num_lines || line_number < 0) {
        throw new Vex.RERR("StaveConfigError",
          "The line number must be within the range of the number of lines in the Stave.");
      }
      if (!line_config.hasOwnProperty('visible')) {
        throw new Vex.RERR("StaveConfigError",
          "The line configuration object is missing the 'visible' property.");
      }
      if (typeof(line_config.visible) !== 'boolean') {
        throw new Vex.RERR("StaveConfigError",
          "The line configuration objects 'visible' property must be true or false.");
      }

      this.options.line_config[line_number] = line_config;

      return this;
    },

    /**
     * Set the staff line configuration array for all of the lines at once.
     * @param lines_configuration An array of line configuration objects.  These objects
     *   are of the same format as the single one passed in to setLineConfiguration().
     *   The caller can set null for any line config entry if it is desired that the default be used
     * @throws Vex.RERR "StaveConfigError" When the lines_configuration array does not have
     *   exactly the same number of elements as the num_lines configuration object set in
     *   the constructor.
     */
    setConfigForLines: function(lines_configuration) {
      if (lines_configuration.length !== this.options.num_lines) {
        throw new Vex.RERR("StaveConfigError",
          "The length of the lines configuration array must match the number of lines in the Stave");
      }

      // Make sure the defaults are present in case an incomplete set of
      //  configuration options were supplied.
      for (var line_config in lines_configuration) {
        // Allow 'null' to be used if the caller just wants the default for a particular node.
        if (!lines_configuration[line_config]) {
          lines_configuration[line_config] = this.options.line_config[line_config];
        }
        Vex.Merge(this.options.line_config[line_config], lines_configuration[line_config]);
      }

      this.options.line_config = lines_configuration;

      return this;
    }
  };

  return Stave;
}());

;var MEI2VF = ( function(m2v, MeiLib, VF, $, undefined) {

    /**
     * @class MEI2VF.Util
     * @singleton
     * @private
     */
    m2v.Util = {

      /**
       *
       */
      attsToObj : function(element) {
        var i, obj;
        if (element.attributes) {
          obj = {};
          i = element.attributes.length;
          while (i--) {
            obj[element.attributes[i].nodeName] = element.attributes[i].nodeValue;
          }
        }
        return obj;
      },

      /**
       *
       */
      attsToString : function(element) {
        var result = '', i, j, atts, att;
        atts = element.attributes;
        for ( i = 0, j = atts.length; i < j; i += 1) {
          att = atts.item(i);
          result += ' ' + att.nodeName + '="' + att.nodeValue + '"';
        }
        return result;
      },

      /**
       *
       */
      drawBoundingBoxes : function(ctx, options) {
        var me = this, i, j, k, l, measure, m, coords;
        options = options || {};
        ctx.save();
        if (options.staffs && options.staffs.data) {
          for ( i = 0, j = options.staffs.data.length; i < j; i += 1) {
            measure = options.staffs.data[i];
            if (measure) {
              for ( k = 0, l = measure.length; k < l; k += 1) {
                if (measure[k]) {
                  m = measure[k];
                  measure[k].getBoundingBox().draw(ctx);
                  // ############### NOTEAREA ##############
                  coords = {
                    x : m.getNoteStartX(),
                    y : m.getYForLine(0) - 30,
                    w : m.getNoteEndX() - m.getNoteStartX(),
                    h : m.getYForLine(4) - m.getYForLine(0) + 60
                  };
                  me.drawRectangle(coords, '120, 80, 200', ctx, options.frame);
                  // ############### MODIFIERS ##############
                  coords = {
                    x : m.x,
                    y : m.getYForLine(0) - 30,
                    w : m.getModifierXShift(),
                    h : m.getYForLine(4) - m.getYForLine(0) + 60
                  };
                  me.drawRectangle(coords, '100, 100, 0', ctx, options.frame);
                }
              }
            }
          }
        }
        if (options.voices && options.voices.data) {
          $.each(options.voices.data, function() {
            if (this && this.all_voices) {
              $.each(this.all_voices, function() {
                if (this && this.voice) {
                  if (this.voice.boundingBox && options.voices.drawFrame) {
                    this.voice.getBoundingBox().draw(ctx);
                  }
                  if (options.voices.drawTickables) {
                    $.each(this.voice.tickables, function() {
                      this.getBoundingBox().draw(ctx);
                    });
                  }
                }
              });
            }
          });
        }
        ctx.restore();
      },

      /**
       *
       */
      drawRectangle : function(coords, color, ctx, frame) {
        if (frame) {
          ctx.strokeStyle = 'rgba(' + color + ', 0.5)';
          ctx.rect(coords.x, coords.y, coords.w, coords.h);
        }
        ctx.fillStyle = 'rgba(' + color + ', 0.1)';
        ctx.fillRect(coords.x, coords.y, coords.w, coords.h);
        ctx.stroke();
      }
    };

    return m2v;

  }(MEI2VF || {}, MeiLib, Vex.Flow, jQuery));
;/**
 * @class MEI2VF
 * @singleton
 */
var MEI2VF = (function(m2v, MeiLib, VF, $, undefined) {
    return {
      /**
       * enables or disables MEI2VF logging
       * @method setLogging
       * @param {Boolean} value True if logging should be enabled, false if not. Defaults to false.
       */
      setLogging : m2v.setLogging,
      /**
       * The methods in Converter can be used to manually address distinct
       * processing steps and retrieve the created data. Can be used in
       * addition or as a supplement to {@link render_notation} and
       * {@link rendered_measures}
       */
      Converter : {
        /**
         * initializes the converter
         * @method initConfig
         * @param {Object} config The options passed to the converter. For a list, see
         * {@link MEI2VF.Converter#defaults}
         */
        initConfig : function(config) {
          m2v.Converter.prototype.initConfig(config);
        },
        /**
         * Processes the specified MEI document or document fragment. The generated
         * objects can be processed further or drawn immediately to a canvas via
         * {@link #draw}.
         * @method process
         * @param {XMLDocument} xmlDoc the XML document
         */
        process : function(xmlDoc) {
          m2v.Converter.prototype.process(xmlDoc);
        },
        /**
         * Draws the processed data to a canvas
         * @method draw
         * @param ctx The canvas context
         */
        draw : function(ctx) {
          m2v.Converter.prototype.draw(ctx);
        },
        /**
         * returns a 2d array of all Vex.Flow.Stave objects, arranged by
         * [measure_n][staff_n]
         * @method getAllVexMeasureStaffs
         * @return {Vex.Flow.Stave[][]} see {@link MEI2VF.Converter#allVexMeasureStaffs}
         */
        getAllVexMeasureStaffs : function() {
          return m2v.Converter.prototype.getAllVexMeasureStaffs();
        },
        /**
         * Returns the width and the height of the area that contains all drawn
         * staves as per the last processing.
         *
         * @method getStaffArea
         * @return {Object} the width and height of the area that contains all staves.
         * Properties: width, height
         */
        getStaffArea : function() {
          return m2v.Converter.prototype.getStaffArea();
        }
      },
      /**
       * Contains all Vex.Flow.Stave objects created when calling {@link #render_notation}.
       * Addressing scheme: [measure_n][staff_n]
       * @property {Vex.Flow.Stave[][]} rendered_measures
       */
      rendered_measures: null,
      /**
       * Main rendering function.
       * @param {XMLDocument} xmlDoc The MEI XML Document
       * @param {Element} target An svg or canvas element
       * @param {Number} width The width of the print space in pixels. Defaults to 800 (optional)
       * @param {Number} height The height of the print space in pixels. Defaults to 350 (optional)
       * @param {Number} backend Set to Vex.Flow.Renderer.Backends.RAPHAEL to
       * render to a Raphael context; if falsy, Vex.Flow.Renderer.Backends.CANVAS
       * is set (optional)
       * @param {Object} options The options passed to the converter. For a list, see
       * {@link MEI2VF.Converter#defaults} (optional)
       */
      render_notation: function (xmlDoc, target, width, height, backend, options) {
        var ctx;
        var cfg = options || {};

        ctx = new VF.Renderer(target, backend || VF.Renderer.Backends.CANVAS).getContext();

        width = width || 800;
        height = height || 350;

        if (+backend === VF.Renderer.Backends.RAPHAEL) {
          ctx.paper.setSize(width, height);
        }

        cfg.page_width = width;

        this.Converter.initConfig(cfg);
        this.Converter.process(xmlDoc[0] || xmlDoc);
        this.Converter.draw(ctx);
        this.rendered_measures = this.Converter.getAllVexMeasureStaffs();

      }
    };

  }(MEI2VF || {}, MeiLib, Vex.Flow, jQuery));
