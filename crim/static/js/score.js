var setScore = function (container_id, score_id, nav_id, mei, ema, reloadDataOnPageChange=false) {
    function _renderPage(p) {
        if (reloadDataOnPageChange) {
            window.vrv.loadData( mei + "\n", "" )
        }
        const svg = window.vrv.renderToSVG(p)
        document.getElementById(score_id).innerHTML = svg
    }

    if (!window.vrv) {
        window.vrv = new window.verovio.toolkit()
    }
    let page = 1
    let selectedEvents = []
    const container = document.getElementById(container_id)
    const verovioOpts = {
        pageWidth: container.offsetWidth * 100 / 35,
        ignoreLayout: 1,
        adjustPageHeight: 1,
        border: 10,
        scale: 35
    }
    window.vrv.setOptions(verovioOpts)
    window.vrv.loadData( mei + "\n", "" )
    _renderPage(page)

    const prev_button = document.querySelector(`#${nav_id} .score_prev`)
    prev_button.addEventListener('click', function(e) {
      e.preventDefault()
      page = page > 1 ? page -1 : page
      if (page === 1) {
        prev_button.classList.add('disabled')
      } else {
        prev_button.classList.remove('disabled')
      }
      _handleDisabledBtns()
      _renderPage(page)
      if (ema) {
          _highlightSelectedEvents()
      }
    }, false)

    const start_button = document.querySelector(`#${nav_id} .score_start`)
    if (ema) {
      start_button.addEventListener('click', function(e) {
          e.preventDefault()
          const start_page = window.vrv.getPageWithElement(selectedEvents[0].replace('#', ''))
          console.log(start_page)
          if (page != start_page + 1) {
              console.log('h')
              page = start_page
              _handleDisabledBtns()
              _renderPage(page)
          }
          _highlightSelectedEvents()
        }, false)
    } else {
        start_button.addEventListener('click', function(e) {
          e.preventDefault()
          page = 1
          _handleDisabledBtns()
          _renderPage(page)
          if (ema) {
              _highlightSelectedEvents()
          }
        }, false)
    }

    const next_button = document.querySelector(`#${nav_id} .score_next`)
    next_button.addEventListener('click', function(e) {
      e.preventDefault()
      page = page < window.vrv.getPageCount() ? page  + 1 : page
      if (page === window.vrv.getPageCount()) {
        next_button.classList.add('disabled')
      } else {
        next_button.classList.remove('disabled')
      }
      _handleDisabledBtns()
      _renderPage(page)
      if (ema) {
          _highlightSelectedEvents()
      }
    }, false)

    function _handleDisabledBtns() {
      if (page === 1) {
        prev_button.classList.add('disabled')
        next_button.classList.remove('disabled')
      } else if (page === window.vrv.getPageCount()) {
        next_button.classList.add('disabled')
      } else {
        prev_button.classList.remove('disabled')
        next_button.classList.remove('disabled')
      }
    }

      // EMA processing

      if (ema) {
        const emamei = EmaMei.withDocumentString(mei.trim(), ema+'/highlight')
        const selection = emamei.getSelection().querySelector('*|annot')
        if (selection) {
            selectedEvents = selection.getAttribute("plist").split(' ')
            const start_page = window.vrv.getPageWithElement(selectedEvents[0].replace('#', ''))
            console.log(start_page)
            if (page != start_page + 1) {
                console.log('h')
                page = start_page
                _handleDisabledBtns()
                _renderPage(page)
            }
            _highlightSelectedEvents()
        }

        function _highlightSelectedEvents() {
        for (const id of selectedEvents) {
            const event = document.querySelector(`#${score_id} ${id}`)
            if (event) {
            event.classList.add('ema-highlight') 
            }
        }
        }
      }

      
};
