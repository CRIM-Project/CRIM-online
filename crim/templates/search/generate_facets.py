# Tool for generating organized facet HTML for the musical types.

FILE_OUT = 'facets_auto.html'

ACCORDIONS = [
    ('model', 'Model musical type'),
    ('derivative', 'Derivative musical type'),
]

MUSICAL_TYPES = [
    (
        ('Cantus firmus', 'mt_cf_b', 'mt-cf'),
        [
            # ('Voices (one per line)', 'mt_cf_voices_ss', 'mt-cf-voices'),
            ('Rhythmic durations', 'mt_cf_dur_b', 'mt-cf-dur'),
            ('Melodic intervals', 'mt_cf_mel_b', 'mt-cf-mel'),
        ]
    ),
    (
        ('Soggetto', 'mt_sog_b', 'mt-sog'),
        [
            # ('Voices (one per line)', 'mt_sog_voices_ss', 'mt-sog-voices'),
            ('Rhythmic durations', 'mt_sog_dur_b', 'mt-sog-dur'),
            ('Melodic intervals', 'mt_sog_mel_b', 'mt-sog-mel'),
            ('Ostinato', 'mt_sog_ostinato_b', 'mt-sog-ostinato'),
            ('Periodic', 'mt_sog_periodic_b', 'mt-sog-periodic'),
        ]
    ),
    (
        ('Counter-soggetto', 'mt_csog_b', 'mt-csog'),
        [
            # ('Voices (one per line)', 'mt_csog_voices_ss', 'mt-csog-voices'),
            ('Rhythmic durations', 'mt_csog_dur_b', 'mt-csog-dur'),
            ('Melodic intervals', 'mt_csog_mel_b', 'mt-csog-mel'),
        ]
    ),
    (
        ('Contrapuntal duo', 'mt_cd_b', 'mt-cd'),
        [
            # ('Voices (one per line)', 'mt_cd_voices_ss', 'mt-cd-voices'),
        ]
    ),
    (
        ('Fuga', 'mt_fg_b', 'mt-fg'),
        [
            # ('Voices (one per line)', 'mt_fg_voices_ss', 'mt-fg-voices'),
            ('Melodic interval of entry', 'mt_fg_int_b', 'mt-fg-int'),
            ('Time interval of entry', 'mt_fg_tint_b', 'mt-fg-tint'),
            ('Periodic', 'mt_fg_periodic_b', 'mt-fg-periodic'),
            ('Strict', 'mt_fg_strict_b', 'mt-fg-strict'),
            ('Flexed', 'mt_fg_flexed_b', 'mt-fg-flexed'),
            ('Sequential', 'mt_fg_sequential_b', 'mt-fg-sequential'),
            ('Inverted', 'mt_fg_inverted_b', 'mt-fg-inverted'),
            ('Retrograde', 'mt_fg_retrograde_b', 'mt-fg-retrograde'),
        ]
    ),
    (
        ('Periodic entry', 'mt_pe_b', 'mt-pe'),
        [
            # ('Voices (one per line)', 'mt_pe_voices_ss', 'mt-pe-voices'),
            ('Melodic interval of entry', 'mt_pe_int_b', 'mt-pe-int'),
            ('Time interval of entry', 'mt_pe_tint_b', 'mt-pe-tint'),
            ('Strict', 'mt_pe_strict_b', 'mt-pe-strict'),
            ('Flexed', 'mt_pe_flexed_b', 'mt-pe-flexed'),
            ('Flexed, tonal', 'mt_pe_flt_b', 'mt-pe-flt'),
            ('Sequential', 'mt_pe_sequential_b', 'mt-pe-sequential'),
            ('Added', 'mt_pe_added_b', 'mt-pe-added'),
            ('Invertible', 'mt_pe_invertible_b', 'mt-pe-invertible'),
        ]
    ),
    (
        ('Imitative duo', 'mt_id_b', 'mt-id'),
        [
            # ('Voices (one per line)', 'mt_id_voices_ss', 'mt-id-voices'),
            ('Melodic interval of entry', 'mt_id_int_b', 'mt-id-int'),
            ('Time interval of entry', 'mt_id_tint_b', 'mt-id-tint'),
            ('Strict', 'mt_id_strict_b', 'mt-id-strict'),
            ('Flexed', 'mt_id_flexed_b', 'mt-id-flexed'),
            ('Flexed, tonal', 'mt_id_flt_b', 'mt-id-flt'),
            ('Invertible', 'mt_id_invertible_b', 'mt-id-invertible'),
        ]
    ),
    (
        ('Non-imitative duo', 'mt_nid_b', 'mt-nid'),
        [
            # ('Voices (one per line)', 'mt_nid_voices_ss', 'mt-nid-voices'),
            ('Melodic interval of entry', 'mt_nid_int_b', 'mt-nid-int'),
            ('Time interval of entry', 'mt_nid_tint_b', 'mt-nid-tint'),
            ('Strict', 'mt_nid_strict_b', 'mt-nid-strict'),
            ('Flexed', 'mt_nid_flexed_b', 'mt-nid-flexed'),
            ('Flexed, tonal', 'mt_nid_flt_b', 'mt-nid-flt'),
            ('Sequential', 'mt_nid_sequential_b', 'mt-nid-sequential'),
            ('Invertible', 'mt_nid_invertible_b', 'mt-nid-invertible'),
        ]
    ),
    (
        ('Homorhythm', 'mt_hr_b', 'mt-hr'),
        [
            # ('Voices (one per line)', 'mt_hr_voices_ss', 'mt-hr-voices'),
            ('Simple', 'mt_hr_simple_b', 'mt-hr-simple'),
            ('Staggered', 'mt_hr_staggered_b', 'mt-hr-staggered'),
            ('Sequential', 'mt_hr_sequential_b', 'mt-hr-sequential'),
            ('Fauxbourdon', 'mt_hr_fauxbourdon_b', 'mt-hr-fauxbourdon'),
        ]
    ),
    (
        ('Cadence', 'mt_cad_b', 'mt-cad'),
        [
            # ('Cantizans', 'mt_cad_cantizans_s', 'mt-cad-cantizans'),
            # ('Tenorizans', 'mt_cad_tenorizans_s', 'mt-cad-tenorizans'),
            # ('Type', 'mt_cad_type_s', 'mt-cad-type'),
            # ('Tone', 'mt_cad_tone_s', 'mt-cad-tone'),
            # ('Dovetail voice', 'mt_cad_dtv_s', 'mt-cad-dtv'),
            # ('Dovetail interval', 'mt_cad_dti_s', 'mt-cad-dti'),
        ]
    ),
    (
        ('Interval pattern', 'mt_int_b', 'mt-int'),
        [
            # ('Voices (one per line)', 'mt_int_voices_ss', 'mt-int-voices'),
            ('Parallel 6', 'mt_int_p6_b', 'mt-int-p6'),
            ('Parallel 3 (or 10)', 'mt_int_p3_b', 'mt-int-p3'),
            ('Chained 3 and 5', 'mt_int_c35_b', 'mt-int-c35'),
            ('Chained 8 and 3', 'mt_int_c83_b', 'mt-int-c83'),
            ('Chained 6 and 5', 'mt_int_c65_b', 'mt-int-c65'),
        ]
    ),
    (
        ('Form and process', 'mt_fp_b', 'mt-fp'),
        [
            ('Internal repetition', 'mt_fp_ir_b', 'mt-fp-ir'),
            ('Range', 'mt_fp_range_s', 'mt-fp-range'),
            # ('Comment', 'mt_fp_comment_t', 'mt-fp-comment'),
        ]
    ),
]


def top_level_keys(a, mt_list):
    mt_names = ["request.GET|dictkey:'{0}'".format(a[0] + '-' + mt[0][2]) for mt in mt_list]
    return ' or '.join(mt_names)


def top_level_tuples(mt_list):
    return [mt[0] for mt in mt_list]


def second_level_keys(a, mt):
    mst_names = ["not request.GET|dictkey:'{0}'".format(a[0] + '-' + mst[2]) for mst in mt[1]]
    return ' and '.join(mst_names) if mst_names else '1'  # i.e. True


def accordion_header(a):
    return """\
<div class="accordion-heading">
  <a class="accordion-toggle" data-toggle="collapse" data-parent="#facet-{0}-mt-accordion" href="#collapse-{0}-mt">{1}</a>
</div>
""".format(a[0], a[1])


def accordion_subtype_blocks(a, mt):
    mst_blocks = []
    for mst in mt[1]:
        mst_blocks.append("""\
          {{% if type_facets.{1}.true %}}
            <li>
              <label class="checkbox">
                <input class="facet-refine" type="checkbox" name="{2}" value="true" />{0} ({{% if type_facets.{1}.true %}}{{{{ type_facets.{1}.true }}}}{{% else %}}0{{% endif %}})
              </label>
            </li>
          {{% endif %}}
""".format(
            mst[0],
            a[0] + '_' + mst[1],
            a[0] + '-' + mst[2],
        ))
    return ''.join(mst_blocks)


def accordion_musical_types(a):
    mt_blocks = []
    for mt in MUSICAL_TYPES:
        mt_blocks.append(
            """\
      {{% if type_facets.{1}.true %}}
        {{% if {3} %}}
          <li>
            <label class="checkbox">
              <input class="facet-refine" type="checkbox" name="{2}" value="true" />{{% if request.GET|dictkey:'{2}' %}}Any{{% else %}}{0}{{% endif %}} ({{{{ type_facets.{1}.true }}}})
            </label>
          </li>
        {{% endif %}}
        {{% if request.GET|dictkey:'{2}' %}}
""".format(
                mt[0][0],
                a[0] + '_' + mt[0][1],
                a[0] + '-' + mt[0][2],
                second_level_keys(a, mt)
            ) +
            accordion_subtype_blocks(a, mt) +
            """\
        {% endif %}
      {% endif %}
""")
    return ''.join(mt_blocks)


def accordion_ul(a):
    return (
        '    <ul class="unstyled">\n' +
        accordion_musical_types(a) +
        '    </ul>\n'
    )


def accordion_inner(a):
    return (
        '  <div class="accordion-inner">\n' +
        accordion_inner_header(a) +
        accordion_ul(a) +
        '  </div>\n'
    )


def accordion_inner_header(a):
    cases = []
    for mt_tl in top_level_tuples(MUSICAL_TYPES):
        cases.append("""\
    {{% {3} type_facets.{1}.true and request.GET|dictkey:'{2}' %}}
      <h4>{0}</h4>""".format(
            mt_tl[0],
            a[0] + '_' + mt_tl[1],
            a[0] + '-' + mt_tl[2],
            'if' if not cases else 'elif')
        )

    cases.append("""\
    {% else %}
      <h4></h4>
    {% endif %}
""")
    return '\n'.join(cases)


def accordion_body(a):
    return accordion_outer_head(a) + accordion_inner(a) + '</div>\n'


def accordion_outer_head(a):
    return """\
<div id="collapse-{0}-mt" class="accordion-body collapse {{% if {1} %}}in{{% endif %}}">
""".format(a[0], top_level_keys(a, MUSICAL_TYPES))


def accordion_facets(a):
    return accordion_header(a) + accordion_body(a)


if __name__ == '__main__':
    with open(FILE_OUT, 'w') as f:
        for a in ACCORDIONS:
            f.write(accordion_facets(a))
