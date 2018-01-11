'use strict';

Object.defineProperty(exports, "__esModule", {
	value: true
});

var _extends2 = require('babel-runtime/helpers/extends');

var _extends3 = _interopRequireDefault(_extends2);

var _objectWithoutProperties2 = require('babel-runtime/helpers/objectWithoutProperties');

var _objectWithoutProperties3 = _interopRequireDefault(_objectWithoutProperties2);

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _propTypes = require('prop-types');

var _propTypes2 = _interopRequireDefault(_propTypes);

var _utils = require('../shared/utils');

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var Grid = function Grid(_ref) {
	var className = _ref.className,
	    fixed = _ref.fixed,
	    marginless = _ref.marginless,
	    tagName = _ref.tagName,
	    other = (0, _objectWithoutProperties3.default)(_ref, ['className', 'fixed', 'marginless', 'tagName']);

	var classNames = [(0, _utils.getClass)('grid')];

	if (fixed === 'left') {
		classNames.push((0, _utils.getClass)('fixed-left'));
	} else if (fixed === 'center') {
		classNames.push((0, _utils.getClass)('fixed-center'));
	}

	if (marginless) {
		classNames.push((0, _utils.getClass)('marginless'));
	}

	// specified class is added last
	if (className) {
		classNames.push(className);
	}

	return _react2.default.createElement(tagName, (0, _extends3.default)({
		className: classNames.filter(function (cssName) {
			return cssName;
		}).join(' ')
	}, other));
};

Grid.propTypes = {
	className: _propTypes2.default.string,
	fixed: _propTypes2.default.oneOf(['left', 'center']),
	marginless: _propTypes2.default.bool,
	tagName: _propTypes2.default.string
};

Grid.defaultProps = {
	className: null,
	fixed: null,
	marginless: false,
	tagName: 'div'
};

exports.default = Grid;