# Tool for generating organized facet HTML for the musical types.

FILE_OUT = 'facets_auto.html'

ACCORDIONS = [
    ('model-mt', 'model_mt', 'Model musical type'),
    ('derivative-mt', 'derivative_mt', 'Derivative musical type'),
]

MUSICAL_TYPES = [
    (
        ('Cantus firmus', 'mt_cf_b', 'mt-cf'),
        [
            # ('Voices (one per line)', 'mt_cf_voices_ss', 'mt-cf-voices'),
            ('Durations only', 'mt_cf_dur_b', 'mt-cf-dur'),
            ('Intervals only', 'mt_cf_mel_b', 'mt-cf-mel'),
        ]
    ),
    (
        ('Soggetto', 'mt_sog_b', 'mt-sog'),
        [
            # ('Voices (one per line)', 'mt_sog_voices_ss', 'mt-sog-voices'),
            ('Durations only', 'mt_sog_dur_b', 'mt-sog-dur'),
            ('Intervals only', 'mt_sog_mel_b', 'mt-sog-mel'),
            ('Ostinato', 'mt_sog_ostinato_b', 'mt-sog-ostinato'),
            ('Periodic', 'mt_sog_periodic_b', 'mt-sog-periodic'),
        ]
    ),
    (
        ('Counter-soggetto', 'mt_csog_b', 'mt-csog'),
        [
            # ('Voices (one per line)', 'mt_csog_voices_ss', 'mt-csog-voices'),
            ('Durations only', 'mt_csog_dur_b', 'mt-csog-dur'),
            ('Intervals only', 'mt_csog_mel_b', 'mt-csog-mel'),
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
            ('Periodic', 'mt_fg_periodic_b', 'mt-fg-periodic'),
            ('Strict', 'mt_fg_strict_b', 'mt-fg-strict'),
            ('Flexed', 'mt_fg_flexed_b', 'mt-fg-flexed'),
            ('Sequential', 'mt_fg_sequential_b', 'mt-fg-sequential'),
            ('Inverted', 'mt_fg_inverted_b', 'mt-fg-inverted'),
            ('Retrograde', 'mt_fg_retrograde_b', 'mt-fg-retrograde'),
            ('Melodic interval of entry', 'mt_fg_int_b', 'mt-fg-int'),
            ('Time interval of entry', 'mt_fg_tint_b', 'mt-fg-tint'),
        ]
    ),
    (
        ('Periodic entry', 'mt_pe_b', 'mt-pe'),
        [
            # ('Voices (one per line)', 'mt_pe_voices_ss', 'mt-pe-voices'),
            ('Strict', 'mt_pe_strict_b', 'mt-pe-strict'),
            ('Flexed', 'mt_pe_flexed_b', 'mt-pe-flexed'),
            ('Flexed, tonal', 'mt_pe_flt_b', 'mt-pe-flt'),
            ('Sequential', 'mt_pe_sequential_b', 'mt-pe-sequential'),
            ('Added', 'mt_pe_added_b', 'mt-pe-added'),
            ('Invertible', 'mt_pe_invertible_b', 'mt-pe-invertible'),
            ('Melodic interval of entry', 'mt_pe_int_b', 'mt-pe-int'),
            ('Time interval of entry', 'mt_pe_tint_b', 'mt-pe-tint'),
        ]
    ),
    (
        ('Imitative duo', 'mt_id_b', 'mt-id'),
        [
            # ('Voices (one per line)', 'mt_id_voices_ss', 'mt-id-voices'),
            ('Strict', 'mt_id_strict_b', 'mt-id-strict'),
            ('Flexed', 'mt_id_flexed_b', 'mt-id-flexed'),
            ('Flexed, tonal', 'mt_id_flt_b', 'mt-id-flt'),
            ('Invertible', 'mt_id_invertible_b', 'mt-id-invertible'),
            ('Melodic interval of entry', 'mt_id_int_b', 'mt-id-int'),
            ('Time interval of entry', 'mt_id_tint_b', 'mt-id-tint'),
        ]
    ),
    (
        ('Non-imitative duo', 'mt_nid_b', 'mt-nid'),
        [
            # ('Voices (one per line)', 'mt_nid_voices_ss', 'mt-nid-voices'),
            ('Strict', 'mt_nid_strict_b', 'mt-nid-strict'),
            ('Flexed', 'mt_nid_flexed_b', 'mt-nid-flexed'),
            ('Flexed, tonal', 'mt_nid_flt_b', 'mt-nid-flt'),
            ('Sequential', 'mt_nid_sequential_b', 'mt-nid-sequential'),
            ('Invertible', 'mt_nid_invertible_b', 'mt-nid-invertible'),
            ('Melodic interval of entry', 'mt_nid_int_b', 'mt-nid-int'),
            ('Time interval of entry', 'mt_nid_tint_b', 'mt-nid-tint'),
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
            # ('Comment', 'mt_fp_comment_t', 'mt-fp-comment'),
            ('Internal repetition', 'mt_fp_ir_b', 'mt-fp-ir'),
            ('Range', 'mt_fp_range_s', 'mt-fp-range'),
        ]
    ),
]


def top_level_keys(mt_list=MUSICAL_TYPES):
    mt_names = ["request.GET|dictkey:'{0}'".format(mt[0][2]) for mt in mt_list]
    return ' or '.join(mt_names)


def top_level_tuples(mt_list=MUSICAL_TYPES):
    return [mt[0] for mt in mt_list]


def accordion_header(a):
    return """\
<div class="accordion-heading">
  <a class="accordion-toggle" data-toggle="collapse" data-parent="#facet-{0}-accordion" href="#collapse-{0}">{1}</a>
</div>
""".format(a[0], a[2])


def accordion_ul(a):
    return '\n'  # TODO


def accordion_inner(a):
    return (
        '  <div class="accordion-inner">\n' +
        accordion_inner_header(a) +
        accordion_ul(a) +
        '  </div>\n'
    )


def accordion_inner_header(a):
    cases = []
    for mt_tl in top_level_tuples():
        cases.append("""\
    {{% {3} type_facets.{1}.true and request.GET|dictkey:'{2}' %}}
      <h4>{0}</h4>""".format(mt_tl[0], mt_tl[1], mt_tl[2], 'if' if not cases else 'elif'))

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
<div id="collapse-{0}" class="accordion-body collapse in {{# if {1} #}}">
""".format(a[0], top_level_keys())


def accordion_facets(a):
    return accordion_header(a) + accordion_body(a)


if __name__ == '__main__':
    with open(FILE_OUT, 'w') as f:
        for a in ACCORDIONS:
            f.write(accordion_facets(a))
