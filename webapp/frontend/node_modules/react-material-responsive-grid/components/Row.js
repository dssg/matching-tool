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

var Row = function Row(_ref) {
	var className = _ref.className,
	    reverse = _ref.reverse,
	    start = _ref.start,
	    center = _ref.center,
	    end = _ref.end,
	    top = _ref.top,
	    middle = _ref.middle,
	    bottom = _ref.bottom,
	    around = _ref.around,
	    between = _ref.between,
	    tagName = _ref.tagName,
	    other = (0, _objectWithoutProperties3.default)(_ref, ['className', 'reverse', 'start', 'center', 'end', 'top', 'middle', 'bottom', 'around', 'between', 'tagName']);

	var classNames = [(0, _utils.getClass)('row')];

	if (reverse) {
		classNames.push((0, _utils.getClass)('reverse'));
	}

	// properties implemented as an array of sizes
	(0, _utils.pushSizeClassNames)(classNames, start, 'start-');
	(0, _utils.pushSizeClassNames)(classNames, center, 'center-');
	(0, _utils.pushSizeClassNames)(classNames, end, 'end-');
	(0, _utils.pushSizeClassNames)(classNames, top, 'top-');
	(0, _utils.pushSizeClassNames)(classNames, middle, 'middle-');
	(0, _utils.pushSizeClassNames)(classNames, bottom, 'bottom-');
	(0, _utils.pushSizeClassNames)(classNames, around, 'around-');
	(0, _utils.pushSizeClassNames)(classNames, between, 'between-');

	// specified class is added last
	if (className) {
		classNames.push(className);
	}

	return _react2.default.createElement(tagName || 'div', (0, _extends3.default)({
		className: classNames.filter(function (cssName) {
			return cssName;
		}).join(' ')
	}, other));
};

Row.propTypes = {
	className: _propTypes2.default.string,
	reverse: _propTypes2.default.bool,
	start: _propTypes2.default.arrayOf(_propTypes2.default.string),
	center: _propTypes2.default.arrayOf(_propTypes2.default.string),
	end: _propTypes2.default.arrayOf(_propTypes2.default.string),
	top: _propTypes2.default.arrayOf(_propTypes2.default.string),
	middle: _propTypes2.default.arrayOf(_propTypes2.default.string),
	bottom: _propTypes2.default.arrayOf(_propTypes2.default.string),
	around: _propTypes2.default.arrayOf(_propTypes2.default.string),
	between: _propTypes2.default.arrayOf(_propTypes2.default.string),
	tagName: _propTypes2.default.string
};

Row.defaultProps = {
	className: null,
	reverse: false,
	start: [],
	center: [],
	end: [],
	top: [],
	middle: [],
	bottom: [],
	around: [],
	between: [],
	tagName: null
};

exports.default = Row;