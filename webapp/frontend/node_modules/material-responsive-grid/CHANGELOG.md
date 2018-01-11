HEAD

## [1.0.1] - 2017-03-17
### Fixed
- Preserve margin for fixed width, left aligned grids.  It was being set to 0, which pulled content to the left.
- Width of fixed width grids: Set width to auto and specify a max-width instead.  Widths close to cutoff were overflowing.

### Added
- Examples app

## [1.1.0] - 2017-03-24
### Added
- .marginless grid class - Eliminates the outer padding that prevents a row's content from spanning edge to edge.
- .fixed-left grid class - Modifier class for .grid, will replace .grid-fixed-left in next major release
- .fixed-center class - Modifier class for .grid, will replace .grid-fixed-center in next major release
- Marginless grid example to examples app.

### Deprecated
- .grid-fixed-left - Deprecated in favor of the .fixed-left modifier class for .grid
- .grid-fixed-center - Deprecated in favor of the .fixed-center modifier class for .grid
