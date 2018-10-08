[![Build Status](https://travis-ci.org/umd-mith/continuo.svg?branch=master)](https://travis-ci.org/umd-mith/continuo)

# Continuo

Continuo is a JS library to select notes on a rendered MEI music score and create permalinks using the Music Addressability URL scheme.

## Dependencies
* [Verovio](http://www.verovio.org/) must be available globally.

The built version will include
* jQuery
* Backbone

Import `continuo` directly into your JS app too avoid duplication. Or file an [issue](https://github.com/umd-mith/continuo/issues) if your project needs a build without dependencies and we'll work on it. You'll need [Gulp](http://gulpjs.com/) for building.

## How to use
```
$ npm install continuo
$ gulp
```

```
(new Continuo({el: "#html_id", mei: '/URL/to/MEI'})).render();
// or
(new Continuo({el: "#html_id", meiString: '<mei><!-- MEI data --></mei>'})).render();
```

## Based on
* [Music Encoding Initiative](http://music-encoding.org)
* [Verovio](http://www.verovio.org/)
* [Music Addressability API](https://github.com/umd-mith/ema/blob/master/docs/api.md)

## License
Apache 2.0
